from pathlib import Path
from polars import LazyFrame, DataFrame
from dataclasses import dataclass, fields
from typing import (
    Any
    , Union
    , Optional
)
from .type_alias import (
    PolarsFrame
    , ActionType
    , ClassifModel
    , RegressionModel
)
# from datetime import datetime
import pickle # Use pickle for now. Think about other ways to preserve.
import polars as pl
import logging
import copy
import dsds

logger = logging.getLogger(__name__)

# P = ParamSpec("P")


# action + the only non-None field name is a unique identifier for this Step (fully classifies all steps)
@dataclass
class Step:
    action:ActionType
    with_columns: Optional[list[pl.Expr]] = None
    map_dict: Optional[list[pl.Expr]] = None
    filter: Optional[pl.Expr] = None
    select: Optional[list[Union[str, pl.Expr]]] = None
    drop: Optional[list[str]] = None
    model_step: Optional[dict[str, Any]] = None

    def __str__(self) -> str:
        output = ""
        if self.action == "with_columns":
            output += "Details: \n"
            for i,expr in enumerate(self.with_columns):
                output += f"({i+1}) {expr}\n"
        elif self.action == "filter":
            output += f"By condition: {self.filter}\n"
        elif self.action in ("classif", "regression"):
            output += f"Model: {self.model_step['model'].__class__}\n"
            features = self.model_step.get('features', None)
            if features is None:
                output += "Using all non-target columns as features.\n"
            else:
                output += f"Using the features {features}\n"
            output += f"Appends {self.model_step['score_col']} to dataframe."
        elif self.action == "map_dict":
            output += "Encoder/Mapper for columns. This is unprintable for now.\n"
        elif self.action == "select":
            pure_strs = []
            exprs = []
            for c in self.select:
                if isinstance(c, str):
                    pure_strs.append(c)
                else:
                    exprs.append(c)
            if len(pure_strs) > 0:
                output += str(pure_strs)
            if len(exprs) > 0:
                for e in exprs:
                    output += f"{e}\n"
                output += "\n"
        else:
            output += str(self.content())

        return output

    def validate(self) -> bool:
        not_nones:list[str] = []
        for field in fields(self):
            if field.name in ("with_columns", "map_dict", "select", "drop", "filter", "model_step"):
                if getattr(self, field.name) is not None:
                    not_nones.append(field.name)
            elif field.name == "action":
                continue
            else:
                logger.warning(f"Found unknown action: {field.name}")
                return False

        if len(not_nones) == 1:
            return True
        elif len(not_nones) == 0:
            logger.warning(f"The Step {self.action} does not have any action value associated with it.")
            return False
        else:
            logger.warning(f"The step {self.action} has two action values associated with it: {not_nones}")
            return False
        
    def content(self) -> Any:
        for field in fields(self):
            value = getattr(self, field.name)
            if field.name != "action" and value is not None:
                return value
            
    def get_expressions(self) -> list[pl.Expr]:
        if self.action in ("model_step"):
            return []
        else:
            return copy.deepcopy(self.content())
            
    def show_content(self):
        content = self.content()
        if isinstance(content, list):
            for s in content:
                print(s)
        else:
            print(s) 

@pl.api.register_lazyframe_namespace("blueprint")
class Blueprint:
    def __init__(self, ldf: LazyFrame):
        self._ldf = ldf
        self.steps:list[Step] = []

    def get_step(self, n:int) -> Step:
        return self.steps[n]
    
    def get_steps(self, indices:list[int]) -> list[Step]:
        return [self.steps[i] for i in indices]
    
    def show_content_at_step(self, idx:int):
        self.get_step(idx).show_content()

    def get_content_at_step(self, idx:int) -> Any:
        content = self.get_step(idx).content()
        if isinstance(content, list):
            out = [] 
            for s in content:
                out.append(copy.deepcopy(s))
            return out
        else:
            return copy.deepcopy(content)
    
    def get_by_action_type(self, action_type:ActionType) -> list[Step]:
        indices = (i for i,s in enumerate(self.steps) if s.action == action_type)
        return [copy.deepcopy(self.steps[i]) for i in indices]
    
    def get_by_mention(self, keyword:str) -> list[Step]:
        '''
        You will get a shallow copy of the expressions mentioning the keyword. Be very careful 
        not to mutate them!
        '''
        output = []
        for s in self.steps:
            if s.action == "with_columns":
                exprs = s.with_columns
                for e in exprs:
                    if keyword in e.meta.root_names():
                        output.append(copy.copy(s))
                        break
            elif s.action == "map_dict":
                exprs = s.map_dict
                for e in exprs:
                    if keyword in e.meta.root_names():
                        output.append(copy.copy(s))
                        break
            elif s.action == "select":
                exprs = s.select
                for e in exprs:
                    if isinstance(e, str):
                        if e == keyword:
                            output.append(copy.copy(s))
                    else: # e is expression
                        for n in e.meta.root_names():
                            if n == keyword:
                                output.append(copy.copy(s))
                                break
            elif s.action == "drop":
                exprs = s.drop
                for c in exprs:
                    if c == keyword:
                        output.append(copy.copy(s))
            elif s.action == "filter":
                for n in s.filter.meta.root_names():
                    if n == keyword:
                        output.append(copy.copy(s))
                        break
        
        return output


    def as_str(self, n:int) -> str:
        output = ""
        start = max(len(self.steps) + n, 0) if n < 0 else 0
        till = len(self.steps) if n < 0 else min(n, len(self.steps))
        for k,s in enumerate(self.steps):
            if k < start:
                continue
            output += f"Step {k} | Action: {s.action}\n"
            output += str(s) + "\n\n"
            if k > till:
                break
        return output
    
    def show(self, n:int) -> None:
        print(self.as_str(n))

    def __str__(self) -> str:
        return self.as_str(len(self.steps))
    
    def __len__(self) -> int:
        return len(self.steps)
    
    def _ipython_display_(self):
        print(self)
        
    @staticmethod
    def _process_classif(
        df: PolarsFrame
        , model:ClassifModel
        , features: list[str]
        , target: Optional[str] = None
        , score_idx:int = -1 
        , score_col:str = "model_score"
    ) -> PolarsFrame:
        
        if target is not None:
            if target in features:
                features.remove(target)

        data = df.lazy().collect()
        score = pl.DataFrame({
            score_col: model.predict_proba(data.select(features))[:, score_idx]
        })
        output = pl.concat([data, score], how="horizontal")
        if isinstance(df, pl.LazyFrame):
            return output.lazy()
        return output
    
    @staticmethod
    def _process_regression(
        df: PolarsFrame
        , model:RegressionModel
        , features: list[str]
        , target: Optional[str] = None
        , score_col:str = "model_score"
    ) -> DataFrame:
        
        if target is not None:
            if target in features:
                features.remove(target)

        data = df.lazy().collect()
        score = pl.DataFrame({
            score_col: model.predict(data.select(features)).ravel()
        })
        output = pl.concat([data, score], how="horizontal")
        if isinstance(df, pl.LazyFrame):
            return output.lazy()
        return output

    # Shallow copy should work
    # Just make sure exprs are not lazy structures like generators
    
    # Transformations that can be done with with_columns(exprs)
    def with_columns(self, exprs:list[pl.Expr]) -> LazyFrame:
        output = self._ldf.with_columns(exprs)
        output.blueprint.steps = self.steps.copy() # Shallow copy should work
        output.blueprint.steps.append(
            Step(action = "with_columns", with_columns = exprs)
        )
        return output
    
    # Map dict is just the same as with_columns, but I want to differentiate them in name..
    def map_dict(self, exprs:list[pl.Expr]) -> LazyFrame:
        output = self._ldf.with_columns(exprs)
        output.blueprint.steps = self.steps.copy() # Shallow copy should work
        output.blueprint.steps.append(
            Step(action = "map_dict", map_dict = exprs)
        )
        return output
    
    def filter(self, expr:pl.Expr) -> LazyFrame:
        output = self._ldf.filter(expr)
        output.blueprint.steps = self.steps.copy() # Shallow copy should work
        output.blueprint.steps.append(
            Step(action = "filter", filter = expr)
        )
        return output
    
    # Transformations are just select, used mostly in selector functions
    def select(self, select_cols:list[str]) -> LazyFrame:
        output = self._ldf.select(select_cols)
        output.blueprint.steps = self.steps.copy() 
        output.blueprint.steps.append(
            Step(action = "select", select = select_cols)
        )
        return output
    
    # Transformations that drops, used mostly in removal functions
    # I am not sure if Polars internally optimizes for this.
    # Say I have 2 consecutive drops, then I should be able to merge them into one drop
    # which may be more efficient. 
    def drop(self, drop_cols:list[str]) -> LazyFrame:
        output = self._ldf.drop(drop_cols)
        output.blueprint.steps = self.steps.copy() 
        output.blueprint.steps.append(
            Step(action = "drop", drop = drop_cols)
        )
        return output

    def add_classif(self
        , model:ClassifModel
        , features: list[str]
        , target: Optional[str] = None
        , score_idx:int = -1 
        , score_col:str = "model_score"
    ) -> LazyFrame:
        '''
        Appends a classification model at given index. This step will collect the lazy frame. All non-target
        column will be used as features.

        Parameters
        ----------
        at
            Index at which to insert the model step
        model
            The trained classification model
        target
            The target of the model, which will not be used in making the prediction. It is only used so that we can 
            remove it from feature list.
        features
            The features the model takes. If none, will use all non-target features.
        score_idx
            The index of the score column in predict_proba you want to append to the dataframe. E.g. -1 will take the 
            score of the positive class in a binary classification
        score_col
            The name of the score column
        '''
        output = Blueprint._process_classif(self._ldf, model, features, target, score_idx, score_col)
        output.blueprint.steps = self.steps.copy()
        output.blueprint.steps.append(
            Step(action = "classif", model_step = {"model":model,
                                                    "target": target,
                                                    "features": features,
                                                    "score_idx": score_idx,
                                                    "score_col":score_col})
        )
        return output
    
    def add_regression(self
        , model:RegressionModel
        , features: list[str]
        , target: Optional[str] = None
        , score_col:str = "model_score"
    ) -> LazyFrame:
        '''
        Appends a classification model at given index. This step will collect the lazy frame. All non-target
        column will be used as features.

        Parameters
        ----------
        at
            Index at which to insert the model step
        model
            The trained classification model
        target
            The target of the model, which will not be used in making the prediction. It is only used so that we can 
            remove it from feature list.
        features
            The features the model takes. If none, will use all non-target features.
        score_idx
            The index of the score column in predict_proba you want to append to the dataframe. E.g. -1 will take the 
            score of the positive class in a binary classification
        score_col
            The name of the score column
        '''        
        output = Blueprint._process_regression(self._ldf, model, features, target, score_col)
        output.blueprint.steps = self.steps.copy()
        output.blueprint.steps.append(
            Step(action = "regression", model_step = {"model":model,
                                                        "target": target,
                                                        "features": features,
                                                        "score_col":score_col})
        )
        return output
    
    def preserve(self, path:Union[str,Path]) -> None:
        '''
        Writes the blueprint to disk as a Python pickle file at the given path.

        Parameters
        ----------
        path
            A valid path to write to
        '''
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def apply(self, df:PolarsFrame, up_to:int=-1, collect:bool=False) -> PolarsFrame:
        '''
        Apply all the steps to the given df. The result will be lazy if df is lazy, and eager if df is eager.

        Parameters
        ----------
        df
            Either an eager or lazy Polars Dataframe
        up_to
            If > 0, will perform the steps up to this number
        collect
            If input is lazy and collect = True, then this will collect the result at the end. If streaming
            collect is desired, please set this to False and collect manually.
        '''
        _up_to = len(self.steps) if up_to <=0 else min(up_to, len(self.steps))
        for i,s in enumerate(self.steps):
            if i < _up_to:
                if s.action == "drop":
                    df = df.drop(s.drop)
                elif s.action == "with_columns":
                    df = df.with_columns(s.with_columns)
                elif s.action == "map_dict":
                    df = df.with_columns(s.map_dict)
                elif s.action == "select":
                    df = df.select(s.select)
                elif s.action == "filter":
                    df = df.filter(s.filter)
                elif s.action == "classif":
                    df = df.pipe(Blueprint._process_classif, **s.model_step)
                elif s.action == "regression":
                    df = df.pipe(Blueprint._process_regression, **s.model_step)
            else:
                break

        if isinstance(df, pl.LazyFrame) & collect:
            return df.collect()
        return df
    
    def fit(self, X:pl.DataFrame, y=None) -> None:
        return None 
    
    def transform(self) -> pl.DataFrame:
        return self.apply(collect=True)
    
    def deep_copy(self) -> "Blueprint":
        return copy.deepcopy(self)
    
    # Move with_columns expressions into one context if possible, to ensure maximal parallelization
    # at all times
    def compactify(self):
        pass

# -------------------------------------------------------------------------------------------------------------

# Right now, use Pickle. Definitely move away from Pickle in the future.
def from_pkl(path: Union[str,Path]) -> Blueprint:
    with open(path, "rb") as f:
        obj = pickle.loads(f.read())
        if isinstance(obj, Blueprint):
            return obj
        else:
            raise ValueError("The object in the pickled file is not a Blueprint object.")

def _dsds_with_columns(df:PolarsFrame, exprs:list[pl.Expr]) -> PolarsFrame:
    if len(exprs) == 0:
        return df
    if isinstance(df, pl.LazyFrame) & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.with_columns(exprs)
    return df.with_columns(exprs)
    
def _dsds_map_dict(df:PolarsFrame, exprs:list[pl.Expr]) -> PolarsFrame:
    if len(exprs) == 0:
        return df
    if isinstance(df, pl.LazyFrame) & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.map_dict(exprs)
    return df.with_columns(exprs)
    
def _dsds_with_columns_and_drop(df:PolarsFrame, exprs:list[pl.Expr], to_drop: list[str]) -> PolarsFrame:
    if len(to_drop) == 0:
        return _dsds_with_columns(df, exprs)
    if len(exprs) == 0:
        return df
    if isinstance(df, pl.LazyFrame) & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.with_columns(exprs).blueprint.drop(to_drop)
    return df.with_columns(exprs).drop(to_drop)
    
def _dsds_select(
    df:PolarsFrame
    , selector: Union[list[str], list[pl.Expr]]
    , persist: bool = True
) -> PolarsFrame:
    '''
    A select wrapper that makes it pipeline compatible.

    Set persist = True so that this will be remembered by the blueprint.
    '''
    if len(selector) == 0:
        return df
    if isinstance(df, pl.LazyFrame) & persist & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.select(selector)
    return df.select(selector)

def _dsds_drop(df:PolarsFrame, to_drop:list[str], persist:bool=True) -> PolarsFrame:
    '''
    A pipeline compatible way to drop the given columns, which will be remembered by the blueprint
    by default.
    '''
    if len(to_drop) == 0:
        return df
    if isinstance(df, pl.LazyFrame) & persist & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.drop(to_drop)
    return df.drop(to_drop)

def _dsds_filter(
    df:PolarsFrame
    , condition: pl.Expr
    , persist: bool = False
) -> PolarsFrame:
    ''' 
    A wrapper function for Polars' filter so that it can be used in pipeline.

    Set persist = True so that this will be remembered by the blueprint.
    '''
    if isinstance(df, pl.LazyFrame) & persist & dsds.PERSIST_IN_BLUEPRINT:
        return df.blueprint.filter(condition)
    return df.filter(condition)
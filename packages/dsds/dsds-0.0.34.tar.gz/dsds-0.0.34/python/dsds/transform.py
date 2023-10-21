from __future__ import annotations
from .type_alias import (
    PolarsFrame
    , SimpleImputeStrategy
    , HotDeckImputeStrategy
    , ScalingStrategy
    , ScaleByStrategy
    , PowerTransformStrategy
    , DateExtract
    , ListExtract
    , StrExtract
    , HorizontalExtract
    , ZeroOneCombineStrategy
    , POLARS_NUMERICAL_TYPES
)
from .prescreen import (
    type_checker, 
    infer_nums_from_str,
    infer_infreq_categories,
)
from .blueprint import(
    _dsds_with_columns
)
from typing import Optional, Union, Any
from scipy.stats import (
    yeojohnson_normmax
    , boxcox_normmax
)
from functools import partial
import dsds
import logging
import math
import polars as pl

# A lot of companies are still using Python < 3.10
# So I am not using match statements

logger = logging.getLogger(__name__)

def impute(
    df:PolarsFrame
    , cols:list[str]
    , *
    , strategy:SimpleImputeStrategy = 'median'
    , const:float = 1.
) -> PolarsFrame:
    '''
    Impute the given columns with the given strategy.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        The columns to impute. Please make sure the columns are either numeric or string columns. If a 
        column is string, then only mode makes sense.
    strategy
        One of 'median', 'mean', 'const', 'mode' or 'coalease'. If 'const', the const argument 
        must be provided. Note that if strategy is mode and if two values occur the same number 
        of times, a random one will be picked. If strategy is coalease, it is not guaranteed that
        all nulls will be filled, and the first non-null values in cols will be used to construct a new
        column with the same name as cols[0]'s name.
    const
        The constant value to impute by if strategy = 'const'
    '''
    if strategy == "median":
        all_medians = df.lazy().select(pl.col(cols).median()).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [pl.col(c).fill_null(all_medians[i]) for i,c in enumerate(cols)]
    elif strategy in ("mean", "avg"):
        all_means = df.lazy().select(pl.col(cols).mean()).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [pl.col(c).fill_null(all_means[i]) for i,c in enumerate(cols)]
    elif strategy in ("const", "constant"):
        exprs = [pl.col(cols).fill_null(const)]
    elif strategy in ("mode", "most_frequent"):
        all_modes = df.lazy().select(pl.col(cols).mode().first()).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [pl.col(c).fill_null(all_modes[i]) for i,c in enumerate(cols)]
    elif strategy == "coalease":
        exprs = [pl.coalesce(cols).alias(cols[0])]
    else:
        raise TypeError(f"Unknown imputation strategy: {strategy}")

    return _dsds_with_columns(df, exprs)

def impute_nan(
    df: PolarsFrame
    , cols: list[str]
    , *
    , by: Optional[float] = None
) -> PolarsFrame:
    '''
    Maps all NaN or infinite values to the given value. If `by` is not provided, this will map
    NaN or infinite values to null.
    
    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        If none, this will infer all columns that contains NaN or infinity
    by
        If this is None, this will map all NaNs/infinity value to null. If this is a valid float,
        this will impute NaN/infinity by this value.
    '''
    _ = type_checker(df, cols, "numeric", "impute_nan")
    exprs = [pl.when((pl.col(c).is_infinite()) | pl.col(c).is_nan()).then(by).otherwise(pl.col(c)).alias(c) 
             for c in cols]
    return _dsds_with_columns(df, exprs)

def _get_agg_impute_expr(c:str, strategy:SimpleImputeStrategy) -> pl.Expr:
    if strategy in ("mean", "avg"):
        agg = pl.col(c).mean().alias(strategy)
    elif strategy == "median":
        agg = pl.col(c).median().alias(strategy)
    elif strategy == "max":
        agg = pl.col(c).max().alias(strategy)
    elif strategy == "min":
        agg = pl.col(c).min().alias(strategy)
    elif strategy == ("mode", "most_frequent"):
        agg = pl.col(c).mode().first().alias(strategy)
    else:
        raise TypeError(f"Unknown hot deck imputation strategy: {strategy}")
    return agg

def hot_deck_impute(
    df: PolarsFrame
    , cols: list[str]
    , group_by: list[str]
    , *
    , strategy:HotDeckImputeStrategy = 'mean'
) -> PolarsFrame:
    '''
    Imputes column c according to the segment it is in. Performance will hurt if columns in group_by has 
    too many segments (combinations). Note that cols shouldn't have any column in common with columns in 
    group_by. In the case that a new combination which was not in training data appears, the null will 
    be mapped to the default value.

    In the example below, let's say a new combination (cat, 1) appears, which was not in training, 
    and col(a) is null, then the missing value will remain missing. If you want to handle that case,
    you can chain an imputation step after this.
    
    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        Columns to be imputed. Please make sure these are either numeric or string columns. If column is
        string, then only mode makes sense.
    group_by
        Computes value to impute with according to the segments in these columns.
    strategy
        One of ['mean', 'avg', 'median', 'mode', 'most_frequent', 'min', 'max'], which can be
        computed as aggregated stats.

    Example
    -------
    >>> df = pl.DataFrame({
    ...     "a": [None, 1,2,3,4, None,],
    ...     "b": ["cat", "cat", "cat", "dog", "dog", "dog"],
    ...     "c": [0,0,0,0,1,1]
    ... })
    >>> print(t.hot_deck_impute(df, ["a"], group_by=["b", "c"], strategy="mean"))
    shape: (6, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    │ --- ┆ --- ┆ --- │
    │ f64 ┆ str ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 1.5 ┆ cat ┆ 0   │
    │ 1.0 ┆ cat ┆ 0   │
    │ 2.0 ┆ cat ┆ 0   │
    │ 3.0 ┆ dog ┆ 0   │
    │ 4.0 ┆ dog ┆ 1   │
    │ 4.0 ┆ dog ┆ 1   │
    └─────┴─────┴─────┘
    '''
    for c in cols:
        if c in group_by:
            raise ValueError(f"Columns in cols should not appear in group_by. Found {c} in both.")

    # Probably not the most performant.
    references = (
        df.lazy().group_by(group_by).agg(
            _get_agg_impute_expr(c, strategy)
        )
        for c in cols
    )
    dfs = pl.collect_all(references, streaming=dsds.STREAM_TRANSFORM)
    exprs = []
    for c, ref in zip(cols, dfs):
        expr = pl.col(c)
        for row_dict in ref.iter_rows(named=True):
            impute = row_dict.pop(strategy)
            expr = pl.when(
                pl.all_horizontal(
                    pl.col(c).is_null()
                    , *(pl.col(k) == pl.lit(v) for k,v in row_dict.items())
                )
            ).then(impute).otherwise(expr)
        expr = expr.alias(c)
        exprs.append(expr)

    return _dsds_with_columns(df, exprs)

def coalesce(
    df: PolarsFrame
    , exprs: list[pl.Expr]
    , new_col_name: str
) -> PolarsFrame:
    '''
    Coaleases using the given expressions in exprs.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    exprs
        The expressions which we will use to perform the coalease
    new_col_name
        Name of the new coaleased column
    '''
    return _dsds_with_columns(df, [pl.coalesce(exprs).alias(new_col_name)])

def scale(
    df:PolarsFrame
    , cols:list[str]
    , *
    , strategy:ScalingStrategy="standard"
    , const:float = 1.0
    , qcuts:tuple[float, float, float] = (0.25, 0.5, 0.75)
) -> PolarsFrame:
    '''
    Scale the given columns with the given strategy.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        The columns to scale
    strategy
        One of `standard`, `min_max`, `const`, `abs_max` or `robust`. If 'const', 
        the const argument should be provided
    const
        The constant value to scale by if strategy = 'const'
    qcuts
        The quantiles used in robust scaling. Must be three increasing numbers between 0 and 1. The formula is 
        (X - qcuts[1]) / (qcuts[2] - qcuts[0]) for each column X.
    '''
    _ = type_checker(df, cols, "numeric", "scale")
    if strategy == "standard":
        mean_std = df.lazy().select(
            pl.col(cols).mean().prefix("mean:"),
            pl.col(cols).std(ddof=0).prefix("std:")
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [(pl.col(c) - mean_std[i])/(mean_std[i + len(cols)]) for i,c in enumerate(cols)]
    elif strategy == "min_max":
        min_max = df.lazy().select(
            pl.col(cols).min().prefix("min:"),
            pl.col(cols).max().prefix("max:")
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0) # All mins come first, then maxs
        exprs = [(pl.col(c) - min_max[i])/((min_max[i + len(cols)] - min_max[i])) for i,c in enumerate(cols)]
    elif strategy == "robust":        
        quantiles = df.lazy().select(
            pl.col(cols).quantile(qcuts[0]).suffix("_1"),
            pl.col(cols).quantile(qcuts[1]).suffix("_2"),
            pl.col(cols).quantile(qcuts[2]).suffix("_3")
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [(pl.col(c) - quantiles[len(cols) + i])/((quantiles[2*len(cols) + i] - quantiles[i])) 
                 for i,c in enumerate(cols)]
    elif strategy == "max_abs":
        max_abs = df.lazy().select(
            pl.max_horizontal(pl.col(c).min().abs(), pl.col(c).max().abs()).suffix("_absmax")
            for c in cols
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs = [pl.col(c)/max_abs[i] for i,c in enumerate(cols)]
    elif strategy in ("const", "constant"):
        exprs = [pl.col(cols) / const]
    else:
        raise TypeError(f"Unknown scaling strategy: {strategy}")

    return _dsds_with_columns(df, exprs)

def scale_by(
    df: PolarsFrame
    , c: str
    , by: str
    , *
    , strategy:ScaleByStrategy="standard"
    , qcuts:tuple[float, float, float] = (0.25, 0.5, 0.75)
) -> PolarsFrame:
    '''
    Scaling by segment. If segment-level constant (one constant per segment) scaling is needed, 
    please consider using a when-then expression in a custom transform.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    c
        The column to scale
    by 
        The segment to scale by
    strategy
        ScaleByStrategy, one of "standard", "min_max", "robust", "max_abs", "mean", "median", or "max"
    qcuts
        If strategy = "robust", the three quantile cuts to be used.

    Example
    -------
    >>> df = pl.DataFrame({
    ...     "segment": ["a", "a", "a", "b", "b", "b"],
    ...     "value": [-3,1,2,200,300,250]
    ... })
    >>> print(df)
    shape: (6, 2)
    ┌─────────┬───────┐
    │ segment ┆ value │
    │ ---     ┆ ---   │
    │ str     ┆ i64   │
    ╞═════════╪═══════╡
    │ a       ┆ -3    │
    │ a       ┆ 1     │
    │ a       ┆ 2     │
    │ b       ┆ 200   │
    │ b       ┆ 300   │
    │ b       ┆ 250   │
    └─────────┴───────┘
    >>> print(t.scale_by(df, "value", "segment", strategy="max_abs"))
    shape: (6, 2)
    ┌─────────┬──────────┐
    │ segment ┆ value    │
    │ ---     ┆ ---      │
    │ str     ┆ f64      │
    ╞═════════╪══════════╡
    │ a       ┆ -1.0     │
    │ a       ┆ 0.333333 │
    │ a       ┆ 0.666667 │
    │ b       ┆ 0.666667 │
    │ b       ┆ 1.0      │
    │ b       ┆ 0.833333 │
    └─────────┴──────────┘
    >>> print(t.scale_by(df, "value", "segment", strategy="min_max"))
    shape: (6, 2)
    ┌─────────┬───────┐
    │ segment ┆ value │
    │ ---     ┆ ---   │
    │ str     ┆ f64   │
    ╞═════════╪═══════╡
    │ a       ┆ 0.0   │
    │ a       ┆ 0.8   │
    │ a       ┆ 1.0   │
    │ b       ┆ 0.0   │
    │ b       ┆ 1.0   │
    │ b       ┆ 0.5   │
    └─────────┴───────┘
    '''
    
    _ = type_checker(df, [c], "numeric", "scale_by")    
    if strategy in ("const", "constant"):
        raise ValueError("Constant strategy is only available scale, not in scale_by.")
    
    if strategy == "standard":
        agg_exprs = [pl.col(c).mean().prefix("mean:"), pl.col(c).std().prefix("std:")]
    elif strategy == "max_abs":
        agg_exprs = [pl.max_horizontal(pl.col(c).min().abs(), pl.col(c).max().abs()).suffix("_maxabs")]
    elif strategy == "min_max":
        agg_exprs = [pl.col(c).min().prefix("min:"), pl.col(c).max().prefix("max:")]
    elif strategy == "mean":
        agg_exprs = [pl.col(c).mean().prefix("mean:")]
    elif strategy == "median":
        agg_exprs = [pl.col(c).median().prefix("median:")]
    elif strategy == "max":
        agg_exprs = [pl.col(c).max().prefix("max:")]
    elif strategy == "robust":
        agg_exprs = [
            pl.col(c).quantile(qcuts[0]).suffix("_1"),
            pl.col(c).quantile(qcuts[1]).suffix("_2"),
            pl.col(c).quantile(qcuts[2]).suffix("_3")
        ]
    else:
        raise TypeError(f"Unknown scaling strategy: {strategy}. "
                        "Note: ScaleByStrategies are not the same as ScalingStrategies.")

    stats = df.lazy().group_by(by).agg(
        *agg_exprs
    ).collect(streaming=dsds.STREAM_TRANSFORM)
    expr = pl.lit(None)
    if strategy == "standard":
        for b, mean, std in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then((pl.col(c)-pl.lit(mean))/pl.lit(std)).otherwise(expr)
    elif strategy == "min_max":
        for b, min_, max_ in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then((pl.col(c)-pl.lit(min_))/pl.lit(max_-min_)).otherwise(expr)
    elif strategy == "robust":
        for b, q1, q2, q3 in zip(*stats.get_columns()): 
            expr = pl.when(pl.col(by) == b).then((pl.col(c)-pl.lit(q2))/pl.lit(q3-q1)).otherwise(expr)
    elif strategy == "max_abs":
        for b, abs_max in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then(pl.col(c)/pl.lit(abs_max)).otherwise(expr)
    elif strategy == "mean":
        for b, mean in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then(pl.col(c)/pl.lit(mean)).otherwise(expr)
    elif strategy == "median":
        for b, median in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then(pl.col(c)/pl.lit(median)).otherwise(expr)
    elif strategy == "max":
        for b, max_ in zip(*stats.get_columns()):
            expr = pl.when(pl.col(by) == b).then(pl.col(c)/pl.lit(max_)).otherwise(expr)

    return _dsds_with_columns(df, [expr])

def custom_transform(
    df: PolarsFrame
    , exprs: list[pl.Expr]
) -> PolarsFrame:
    '''
    A passthrough that performs all expressions given. For example, a typical use case is that you might want 
    to use pl.col("a")/pl.col("b") as a feature. Unlike Scikit-learn pipeline, you do not need any transformer
    for this task. Just pass in your Polars expressions.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    exprs
        List of Polars expressions
    '''
    return _dsds_with_columns(df, exprs)

def add_dummy(
    df: PolarsFrame
    , id_col: str
    , dummy_col_name: str = "_dummy"
    , period: int = 7
) -> PolarsFrame:
    '''
    Creates a 'random' column that should have no predictive value whatsoever. This is useful in feature 
    selection. Everything with importance less than this feature should not be selected. Internally, it
    will hash the given id_col, mod by period, and then randomly shuffle. It is recommended to use a 
    column that is like an id_col to avoid hashing conflicts.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    id_col
        Name of the column you want to hash
    dummy_col_name
        Name of the new dummy column
    period
        The period of the dummy column. It is used to mod the hashed value.
    '''
    expr = pl.col(id_col).hash().mod(period).shuffle().alias(dummy_col_name)
    return _dsds_with_columns(df, [expr])

def cast_dtype(
    df: PolarsFrame
    , cols: list[str]
    , dtype: pl.DataType
) -> PolarsFrame:
    '''
    Casts the given columns to the given type. This type is for general use. For things like casting boolean
    columns to 0s and 1s, please use more specialized functions like dsds.encoders.force_binary.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        List of columns to cast
    dtype
        The dtype to cast to
    '''
    return _dsds_with_columns(df, [pl.col(cols).cast(dtype)])

def binarize(
    df: PolarsFrame
    , rules: dict[str, pl.Expr]
) -> PolarsFrame:
    '''
    Binarize the columns according to the rules given. E.g. if rules = {"c": pl.col(c) > 25}, then
    values in column c which are > 25 will be mapped to 1 and 0 otherwise. The resulting 0-1 column
    will replace the original column c.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    rules
        Dict with keys representing column names, and value representing some boolean condition 
        given as polars expression
    '''
    exprs = [cond.cast(pl.UInt8).alias(c) for c, cond in rules.items()]
    return _dsds_with_columns(df, exprs)

def merge_infreq_categories(
    df: PolarsFrame
    , cols: list[str]
    , *
    , min_count: Optional[int] = 10
    , min_frac: Optional[float] = None
    , separator: str = '|'
) -> PolarsFrame:
    '''
    Combines infrequent categories in string columns together. Note this does not guarantee similar
    categories to be combined. If there is only 1 infrequent category, nothing will be done.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        List of string columns to perform this operation
    min_count
        Define a category to be infrequent if it occurs less than min_count. This defaults to 10 if both min_count and 
        min_frac are None.
    min_frac
        Define category to be infrequent if it occurs less than this percentage of times. If both min_count and min_frac
        are set, min_frac takes priority
    separator
        The separator for the new value representing the combined categories

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a":["a", "b", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"],
    ...     "b":["a", "b", "c", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d", "d"]
    ... })
    >>> df
    shape: (14, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ str ┆ str │
    ╞═════╪═════╡
    │ a   ┆ a   │
    │ b   ┆ b   │
    │ c   ┆ c   │
    │ c   ┆ d   │
    │ …   ┆ …   │
    │ c   ┆ d   │
    │ c   ┆ d   │
    │ c   ┆ d   │
    │ c   ┆ d   │
    └─────┴─────┘
    >>> t.merge_infreq_values(df, ["a", "b"], min_count=3)
    shape: (14, 2)
    ┌─────┬───────┐
    │ a   ┆ b     │
    │ --- ┆ ---   │
    │ str ┆ str   │
    ╞═════╪═══════╡
    │ a|b ┆ a|c|b │
    │ a|b ┆ a|c|b │
    │ c   ┆ a|c|b │
    │ c   ┆ d     │
    │ …   ┆ …     │
    │ c   ┆ d     │
    │ c   ┆ d     │
    │ c   ┆ d     │
    │ c   ┆ d     │
    └─────┴───────┘
    '''
    _ = type_checker(df, cols, "string", "merge_infreq_categories")
    result = infer_infreq_categories(df, cols, min_count=min_count, min_frac=min_frac)

    exprs = []
    for c, infreq in zip(*result.get_columns()):
        if len(infreq) > 1:
            value = separator.join(infreq)
            exprs.append(
                pl.when(pl.col(c).is_in(infreq)).then(value).otherwise(pl.col(c)).alias(c)
            )
    
    return _dsds_with_columns(df, exprs)

def feature_mapping(
    df:PolarsFrame
    , mapping: Union[dict[str, dict[Any, Any]], list[pl.Expr] , pl.Expr]
) -> PolarsFrame:
    '''
    Maps specific values of a feature into values provided. This is a common task when the feature columns 
    come with error codes. This allows features to be mapped to other types, but the user has to make sure 
    that the output column has one clear type. This method can be slow when there are lots of values to map.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    mapping
        Either a dict like {"a": {999: None, 998: None, 997: None}, ...}, meaning that 999, 998 and 997 in column "a" 
        should be replaced by null, or a list/a single Polars (when-then) expression(s) like the following,  
        pl.when(pl.col("a") >= 997).then(None).otherwise(pl.col("a")).alias("a"), which will perform the same mapping 
        as the dict example. Note that using Polars expression can tackle more complex replacement. If the key 
        is not a valid column in df, it will be ignored.

    Example
    -------
    >>> df = pl.DataFrame({
    ...     "a": [1,2,3,998,999],
    ...     "b": [999, 1,2,3,4]
    ... })
    >>> print(df)
    shape: (5, 2)
    ┌─────┬─────┐
    │ a   ┆ b   │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 1   ┆ 999 │
    │ 2   ┆ 1   │
    │ 3   ┆ 2   │
    │ 998 ┆ 3   │
    │ 999 ┆ 4   │
    └─────┴─────┘
    >>> feature_mapping(df, mapping = {"a":{998:None,999:None}, "b":{999:None}})
    shape: (5, 2)
    ┌──────┬──────┐
    │ a    ┆ b    │
    │ ---  ┆ ---  │
    │ i64  ┆ i64  │
    ╞══════╪══════╡
    │ 1    ┆ null │
    │ 2    ┆ 1    │
    │ 3    ┆ 2    │
    │ null ┆ 3    │
    │ null ┆ 4    │
    └──────┴──────┘
    >>> mapping = [pl.when(pl.col("a")>=998).then(None).otherwise(pl.col("a")).alias("a")
    ...          , pl.when(pl.col("b")==999).then(None).otherwise(pl.col("b")).alias("b")]
    >>> feature_mapping(df, mapping)
    shape: (5, 2)
    ┌──────┬──────┐
    │ a    ┆ b    │
    │ ---  ┆ ---  │
    │ i64  ┆ i64  │
    ╞══════╪══════╡
    │ 1    ┆ null │
    │ 2    ┆ 1    │
    │ 3    ┆ 2    │
    │ null ┆ 3    │
    │ null ┆ 4    │
    └──────┴──────┘
    '''
    if isinstance(mapping, dict):
        exprs = [
            pl.col(c).map_dict(repl_map, default=pl.first())
            for c, repl_map in mapping.items()
        ]
    elif isinstance(mapping, list):
        exprs = []
        for f in mapping:
            if isinstance(f, pl.Expr):
                exprs.append(f)
            else:
                logger.warn(f"Found {f} is not a Polars expression. Ignored.")
    elif isinstance(mapping, pl.Expr):
        exprs = [mapping]
    else:
        raise TypeError("The argument `mapping` must be one of the following types: "
                        "dict[str, dict[Any, Any]] | list[pl.Expr] | pl.Expr")
    
    return _dsds_with_columns(df, exprs)

def replace_by_pattern(
    df: PolarsFrame
    , c: str
    , pattern: str
    , by: str
) -> PolarsFrame:
    '''
    Use a regex pattern to capture patterns in a string column and replace the patterns by
    another string. This works like feature_mapping but only works for strings.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    c 
        Name of the string column to work on
    pattern
        The pattern to replace
    by
        Replace the pattern by this string
    '''
    _ = type_checker(df, [c], "string", "replace_by_pattern")
    return _dsds_with_columns(df, [pl.col(c).str.replace(pattern=pattern, value=by)])

def merge_categories(
    df: PolarsFrame
    , merge_what: dict[str, list[str]]
    , *
    , separator: str = "|"
) -> PolarsFrame:
    '''
    Merge the categories for the columns.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    merge_what
        Dict where keys represents columns, and values are list of categories to merge.
    separator
        The separator that will be used to construct combined categories
    '''
    exprs = [
        pl.when(pl.col(c).is_in(cats)).then(separator.join(cats)).otherwise(pl.col(c)).alias(c)
        for c, cats in merge_what.items()
    ]
    return _dsds_with_columns(df, exprs)

def combine_zero_ones(
    df: PolarsFrame
    , cols: list[str]
    , new_name: str
    , *
    , rule: ZeroOneCombineStrategy = "union"
) -> PolarsFrame:
    '''
    Take columns that are all binary 0, 1 columns, combine them horizontally according to the rule. 
    Please make sure the columns only contain binary 0s and 1s. Depending on the rule, this can be 
    used, for example, to quickly combine many one hot encoded columns into one, or reducing the 
    same binary columns into one.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars DataFrame
    cols
        List of binary 0, 1 columns to combine
    new_name
        Name for the combined column
    rule
        One of 'union', 'intersection', 'same'.

    Examples
    --------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a": [1, 1, 0],
    ...     "b":[1, 0, 1],
    ...     "c":[1, 1, 1]
    ... })
    >>> t.combine_zero_ones(df, cols=["a", "b", "c"], new_name="abc", rule="same")
    shape: (3, 1)
    ┌─────┐
    │ abc │
    │ --- │
    │ u8  │
    ╞═════╡
    │ 1   │
    │ 0   │
    │ 0   │
    └─────┘
    >>> t.combine_zero_ones(df, cols=["a", "b", "c"], new_name="abc", rule="union")
    shape: (3, 1)
    ┌─────┐
    │ abc │
    │ --- │
    │ u8  │
    ╞═════╡
    │ 1   │
    │ 1   │
    │ 1   │
    └─────┘
    '''
    if rule == "union":
        expr = pl.max_horizontal([pl.col(cols)]).cast(pl.UInt8).alias(new_name)
    elif rule == "intersection":
        expr = pl.min_horizontal([pl.col(cols)]).cast(pl.UInt8).alias(new_name)
    elif rule == "same":
        expr = pl.sum_horizontal([pl.col(cols)]).is_in((0, len(cols))).cast(pl.UInt8).alias(new_name)
    else:
        raise TypeError(f"The input `{rule}` is not a valid ZeroOneCombineStrategy.")

    return _dsds_with_columns(df, [expr])

def power_transform(
    df: PolarsFrame
    , cols: list[str]
    , *
    , strategy: PowerTransformStrategy = "yeo_johnson"
) -> PolarsFrame:
    '''
    Performs power transform on the numerical columns. This will skip null values in the columns. If strategy is
    box_cox, all values in cols must be positive.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and must all be numerical
    strategy
        Either 'yeo_johnson' or 'box_cox'
    '''
    _ = type_checker(df, cols, "numeric", "power_transform")
    exprs:list[pl.Expr] = []
    if strategy in ("yeo_johnson", "yeojohnson"):
        lmaxs = df.lazy().select(
            pl.col(c)
            .map(yeojohnson_normmax, return_dtype=pl.Float64).alias(c)
            for c in cols
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        for c, lmax in zip(cols, lmaxs):
            if lmax == 0: # log(x + 1)
                x_ge_0_sub_expr = (pl.col(c).add(1)).log()
            else: # ((x + 1)**lmbda - 1) / lmbda
                x_ge_0_sub_expr = ((pl.col(c).add(1)).pow(lmax) - 1) / lmax

            if lmax == 2: # -log(-x + 1)
                x_lt_0_sub_expr = pl.lit(-1) * (1 - pl.col(c)).log()
            else: #  -((-x + 1)**(2 - lmbda) - 1) / (2 - lmbda)
                t = 2 - lmax
                x_lt_0_sub_expr = pl.lit(-1/t) * ((1 - pl.col(c)).pow(t) - 1)

            exprs.append(
                pl.when(pl.col(c).ge(0)).then(x_ge_0_sub_expr).otherwise(x_lt_0_sub_expr).alias(c)
            )
    elif strategy in ("box_cox", "boxcox"):
        bc_normmax = partial(boxcox_normmax, method="mle")
        lmaxs = df.lazy().select(
            pl.col(c)
            .map(bc_normmax, return_dtype=pl.Float64).alias(c)
            for c in cols
        ).collect(streaming=dsds.STREAM_TRANSFORM).row(0)
        exprs.extend(
            pl.col(c).log() if lmax == 0 else (pl.col(c).pow(lmax) - 1) / lmax 
            for c, lmax in zip(cols, lmaxs)
        )
    else:
        raise TypeError(f"The input strategy {strategy} is not a valid strategy. Valid strategies are: yeo_johnson "
                        "or box_cox")
    
    return _dsds_with_columns(df, exprs)

def normalize(
    df: PolarsFrame
    , cols:list[str]
) -> PolarsFrame:
    '''
    Normalize the given columns by dividing them with the respective column sum.

    !!! Note this is pipeline-compatible but will NOT be remembered by the blueprint !!!

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    '''
    _ = type_checker(df, cols, "numeric", "normalize")
    return df.with_columns(pl.col(c)/pl.col(c).sum() for c in cols)

def clip(
    df: PolarsFrame
    , cols: list[str]
    , *
    , min_clip: Optional[float] = None
    , max_clip: Optional[float] = 999999.0
) -> PolarsFrame:
    '''
    Clips the columns within the min and max_clip bounds. This can be used to control outliers. If both min_clip and
    max_clip are provided, perform two-sided clipping. If only one bound is provided, only one side will be clipped.
    It will throw an error if both min and max_clips are not provided.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    min_clip
        Every value smaller than min_clip will be replaced by min_cap
    max_clip
        Every value bigger than max_clip will be replaced by max_cap
    '''
    _ = type_checker(df, cols, "numeric", "clip")
    a:bool = min_clip is None
    b:bool = max_clip is None
    if a & (not b):
        exprs = [pl.col(cols).clip_max(max_clip)]
    elif (not a) & b:
        exprs = [pl.col(cols).clip_min(min_clip)]
    elif not (a | b):
        exprs = [pl.col(cols).clip(min_clip, max_clip)]
    else:
        raise ValueError("At least one of min_cap and max_cap should be provided.")
    
    return _dsds_with_columns(df, exprs)

def log_transform(
    df: PolarsFrame
    , cols:list[str]
    , *
    , base:float = math.e
    , plus_one:bool = False
    , suffix:str = "_log"
) -> PolarsFrame:
    '''
    Performs classical log transform on the given columns, e.g. log(x), or if plus_one = True, ln(1 + x).
    
    Important: If input to log is <= 0, (in the case plus_one = True, if 1 + x <= 0), then result will be NaN. 
    Some algorithms may break if there exists NaN in the columns. Users should perform their due diligence before 
    calling the log transform.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    base
        Base of log. Default is math.e
    plus_one
        If plus_one is true, this will perform ln(1+x) and ignore the `base` input.
    suffix
        Choice of a suffix to the transformed columns. If you wish to drop the original ones, set suffix = "".
    '''
    _ = type_checker(df, cols, "numeric", "log_transform")
    if plus_one:
        exprs = [pl.col(cols).log1p().suffix(suffix)]
    else:
        exprs = [pl.col(cols).log(base).suffix(suffix)]
    return _dsds_with_columns(df, exprs)

def sqrt_transform(
    df: PolarsFrame
    , cols: list[str]
    , *
    , suffix: str = "_sqrt"
) -> PolarsFrame:
    '''
    Performs classical square root transform for the given columns. Negative numbers will be mapped to
    NaN. Set suffix = "" to replace the original columns.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    suffix
        The suffix to add to the transformed columns.
    '''
    _ = type_checker(df, cols, "numeric", "sqrt_transform")
    return _dsds_with_columns(df, [pl.col(cols).sqrt().suffix(suffix)])

def cbrt_transform(
    df: PolarsFrame
    , cols: list[str]
    , *
    , suffix: str = "_cbrt"
) -> PolarsFrame:
    '''
    Performs cube root transform for the given columns. This has the advantage of preserving the sign of 
    numbers.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    suffix
        The suffix to add to the transformed columns.
    '''
    _ = type_checker(df, cols, "numeric", "cbrt_transform")
    return _dsds_with_columns(df, [pl.col(cols).cbrt().suffix(suffix)])

def linear_transform(
    df: PolarsFrame
    , cols: list[str]
    , *
    , coeffs: Union[float, list[float]] = 1.0
    , consts: Union[float, list[float]] = 0.
    , suffix: str = ""
) -> PolarsFrame:
    '''
    Performs a classical linear transform on the given columns. The formula is coeff*x + const.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be numeric columns
    coeffs
        The coefficient terms. Either one number, which will be used to all columns, or a list of numbers of 
        the same size as cols, which will be applied to the corresponding column in cols
    consts
        The constant terms. Either one number, which will be used to all columns, or a list of numbers of 
        the same size as cols, which will be applied to the corresponding column in cols
    suffix
        The suffix to add to the transformed columns. If you wish to drop the original ones, set suffix = "".
    '''
    _ = type_checker(df, cols, "numeric", "linear_transform")
    if isinstance(coeffs, (float, int)):
        coeff_list = [coeffs]*len(cols)
    else:
        coeff_list = coeffs

    if isinstance(consts, (float, int)):
        const_list = [consts]*len(cols)
    else:
        const_list = consts

    if (len(cols) != len(coeff_list)) | (len(cols) != len(const_list)) | (len(const_list) != len(coeff_list)):
        raise ValueError("The inputs `cols`, `coeffs` or `consts` must have the same length, or coeffs and consts must "
                         "be one fixed value.")
    
    exprs = [
        (pl.col(c) * pl.lit(a) + pl.lit(b)).suffix(suffix) 
        for c, a, b in zip(cols, coeff_list, const_list)
    ]
    
    return _dsds_with_columns(df, exprs)

def sine_cosine_transform(
    df: PolarsFrame
    , sin_cols: Optional[list[str]] = None
    , cos_cols: Optional[list[str]] = None
    , sin_amplitude: float = 1.
    , cos_amplitude: float = 1.
    , sin_period: float = 1.
    , cos_period: float = 1.
) -> PolarsFrame:
    '''
    Applies sin and cos transformations to the corresponding columns. This might be useful 
    for date/time features.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    sin_cols
        Columns to apply sine transform. Either sin_cols or cos_cols must be provided.
    cos_cols
        Columns to apply cosine transform. Either sin_cols or cos_cols must be provided.
    sin_amplitude
        Amplitude for the sine columns
    cos_amplitude
        Amplitude for the cosine columns
    sin_period
        Period for the sine columns
    cos_period
        Period for the cos columns
    '''
    if (sin_cols is None) & (cos_cols is None):
        raise ValueError("Either sin_cols or cos_cols must be not none.")
    if len(sin_cols) + len(cos_cols) == 0:
        raise ValueError("Either sin_cols or cos_cols must be non-empty.")
    
    exprs = []
    _ = type_checker(df, sin_cols + cos_cols, "numeric", "sine_cosine_transform")
    if sin_cols:
        exprs.append(
            (pl.col(sin_cols) * pl.lit(2.*math.pi/sin_period)).sin() * pl.lit(sin_amplitude)
        )
    if cos_cols:
        exprs.append(
            (pl.col(cos_cols) * pl.lit(2.*math.pi/cos_period)).cos() * pl.lit(cos_amplitude)
        )

    return _dsds_with_columns(df, exprs)

def extract_dt_features(
    df: PolarsFrame
    , cols: list[str]
    , *
    , extract: Union[DateExtract, list[DateExtract]] = ["year", "quarter", "month"]
    , sunday_first: bool = False
) -> PolarsFrame:
    '''
    Extracts additional date related features from existing date/datetime columns.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be date/datetime columns
    extract
        One of "year", "quarter", "month", "week", "day_of_week", "day_of_year", or a list of these values 
        such as ["year", "quarter"], which means extract year and quarter from all the columns provided 
    sunday_first
        For day_of_week, by default, Monday maps to 1, and so on. If sunday_first = True, then Sunday will be
        mapped to 1 and so on

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "date1":["2021-01-01", "2022-02-03", "2023-11-23"]
    ...     , "date2":["2021-01-01", "2022-02-03", "2023-11-23"]
    ... }).with_columns(
    ...     pl.col(c).str.to_date() for c in ["date1", "date2"]
    ... )
    >>> print(df)
    shape: (3, 2)
    ┌────────────┬────────────┐
    │ date1      ┆ date2      │
    │ ---        ┆ ---        │
    │ date       ┆ date       │
    ╞════════════╪════════════╡
    │ 2021-01-01 ┆ 2021-01-01 │
    │ 2022-02-03 ┆ 2022-02-03 │
    │ 2023-11-23 ┆ 2023-11-23 │
    └────────────┴────────────┘
    >>> cols = ["date1", "date2"]
    >>> print(t.extract_dt_features(df, cols=cols))
    shape: (3, 8)
    ┌────────────┬────────────┬────────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
    │ date1      ┆ date2      ┆ date1_year ┆ date2_yea ┆ date1_qua ┆ date2_qua ┆ date1_mon ┆ date2_mon │
    │ ---        ┆ ---        ┆ ---        ┆ r         ┆ rter      ┆ rter      ┆ th        ┆ th        │
    │ date       ┆ date       ┆ u32        ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
    │            ┆            ┆            ┆ u32       ┆ u32       ┆ u32       ┆ u32       ┆ u32       │
    ╞════════════╪════════════╪════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
    │ 2021-01-01 ┆ 2021-01-01 ┆ 2021       ┆ 2021      ┆ 1         ┆ 1         ┆ 1         ┆ 1         │
    │ 2022-02-03 ┆ 2022-02-03 ┆ 2022       ┆ 2022      ┆ 1         ┆ 1         ┆ 2         ┆ 2         │
    │ 2023-11-23 ┆ 2023-11-23 ┆ 2023       ┆ 2023      ┆ 4         ┆ 4         ┆ 11        ┆ 11        │
    └────────────┴────────────┴────────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
    '''
    _ = type_checker(df, cols, "datetime", "extract_dt_features")
    exprs = []
    if isinstance(extract, list):
        to_extract = extract
    else:
        to_extract = [extract]
    
    for e in to_extract:
        if e == "month":
            exprs.append(pl.col(cols).dt.month().suffix("_month"))
        elif e == "year":
            exprs.append(pl.col(cols).dt.year().suffix("_year"))
        elif e == "quarter":
            exprs.append(pl.col(cols).dt.quarter().suffix("_quarter"))
        elif e == "week":
            exprs.append(pl.col(cols).dt.week().suffix("_week"))
        elif e == "day_of_week":
            if sunday_first:
                exprs.extend(
                    pl.when(pl.col(c).dt.weekday() == 7).then(1).otherwise(pl.col(c).dt.weekday()+1)
                    .suffix("_day_of_week") 
                    for c in cols
                )
            else:
                exprs.append(pl.col(cols).dt.weekday().suffix("_day_of_week"))
        elif e == "day_of_year":
            exprs.append(pl.col(cols).dt.ordinal_day().suffix("_day_of_year"))
        else:
            logger.info(f"Found {e} in extract, but it is not a valid DateExtract value. Ignored.")

    return _dsds_with_columns(df, exprs)

def extract_horizontally(
    df:PolarsFrame
    , cols: list[str]
    , *
    , extract: Union[HorizontalExtract, list[HorizontalExtract]] = ["min", "max"]
) -> PolarsFrame:
    '''
    Extract features horizontally across a few columns.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        List of columns to extract feature from
    extract
        One of "min", "max", "sum", "any", "all". Note that "any" and "all" only make practical sense when 
        all of cols are boolean columns, but they work even when cols are numbers.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a":[1, 2, 3],
    ...     "b":[1, 2, 3],
    ...     "c":[1, 2, 3]
    ... })
    >>> t.extract_horizontally(df, cols=["a", "b", "c"], extract=["min", "max", "sum"])
    shape: (3, 3)
    ┌────────────┬────────────┬────────────┐
    │ min(a,b,c) ┆ max(a,b,c) ┆ sum(a,b,c) │
    │ ---        ┆ ---        ┆ ---        │
    │ i64        ┆ i64        ┆ i64        │
    ╞════════════╪════════════╪════════════╡
    │ 1          ┆ 1          ┆ 3          │
    │ 2          ┆ 2          ┆ 6          │
    │ 3          ┆ 3          ┆ 9          │
    └────────────┴────────────┴────────────┘
    '''
    if isinstance(extract, list):
        to_extract = extract
    else:
        to_extract = [extract]
    
    exprs = []
    for e in to_extract:
        alias = f"{e}({','.join(cols)})"
        if e == "min":
            exprs.append(pl.min_horizontal(pl.col(cols)).alias(alias))
        elif e == "max":
            exprs.append(pl.max_horizontal(pl.col(cols)).alias(alias))
        elif e == "sum":
            exprs.append(pl.sum_horizontal(pl.col(cols)).alias(alias))
        elif e == "any":
            exprs.append(pl.any_horizontal(pl.col(cols)).alias(alias))
        elif e == "all":
            exprs.append(pl.all_horizontal(pl.col(cols)).alias(alias))
        else:
            logger.info(f"Found {e} in extract, but it is not a valid HorizontalExtract value. Ignored.")

    return _dsds_with_columns(df, exprs)

def extract_word_count(
    df: PolarsFrame
    , cols: Union[str, list[str]]
    , words: list[str]
    , *
    , lower: bool = True
) -> PolarsFrame:
    '''
    Extract word counts from the cols.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Either a string representing a name of a column, or a list of column names.
    words
        Words/Patterns to count
    lower
        Whether a lowercase() step should be done before the count match

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "test_str": ["hello world hello", "hello Tom", "test", "world hello"],
    ...     "test_str2": ["hello world hello", "hello Tom", "test", "world hello"]
    ... })
    >>> t.extract_word_count(df, cols=["test_str", "test_str2"], words=["hello", "world"])
    shape: (4, 4)
    ┌──────────────────────┬──────────────────────┬───────────────────────┬───────────────────────┐
    │ test_str_count_hello ┆ test_str_count_world ┆ test_str2_count_hello ┆ test_str2_count_world │
    │ ---                  ┆ ---                  ┆ ---                   ┆ ---                   │
    │ u32                  ┆ u32                  ┆ u32                   ┆ u32                   │
    ╞══════════════════════╪══════════════════════╪═══════════════════════╪═══════════════════════╡
    │ 2                    ┆ 1                    ┆ 2                     ┆ 1                     │
    │ 1                    ┆ 0                    ┆ 1                     ┆ 0                     │
    │ 0                    ┆ 0                    ┆ 0                     ┆ 0                     │
    │ 1                    ┆ 1                    ┆ 1                     ┆ 1                     │
    └──────────────────────┴──────────────────────┴───────────────────────┴───────────────────────┘
    '''
    if isinstance(cols, str):
        str_cols = [cols]
    else:
        str_cols = cols

    _ = type_checker(df, str_cols, "string", "extract_word_count")
    exprs = []

    base = pl.col(str_cols)
    if lower:
        base = base.str.to_lowercase()
    
    exprs.extend(base.str.count_matches(w).suffix(f"_count_{w}") for w in words)
    return _dsds_with_columns(df, exprs)

def str_col_to_list(
    df: PolarsFrame
    , cols: list[str]
    , *
    , inner: Optional[pl.DataType] = None
) -> PolarsFrame:
    '''
    Converts string columns like ['[1,2,3]', '[2,3,4]', ...] into columns of list type.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be string columns
    inner
        If you know the inner dtype and don't want Polars to infer the inner dtype, you can provide it. You 
        typically want to do this to conserve memory, e.g. Polars may choose f64 over f32 but you may know f32 
        is enough. But note that if inner is provided, then all columns will be casted to the same inner dtype.
    '''
    _ = type_checker(df, cols, "string", "str_col_to_list")
    return _dsds_with_columns(df, [pl.col(cols).str.json_extract(dtype = inner)])

def extract_from_str(
    df: PolarsFrame
    , cols: list[str]
    , *
    , extract: Union[StrExtract, list[StrExtract]]
    , pattern: Optional[str] = None
) -> PolarsFrame:
    '''
    Extract data from string columns. For multiple word counts on the same column, see extract_word_count.
    Note that for 'starts_with' and 'ends_with', pattern will be used as a substring instead of a regex pattern.
    If you want to extract numbers from str, see `dsds.transform.extract_numbers`

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be string columns
    extract
        One of "count", "len", "contains", "starts_with", "ends_with" or a list of these values such as 
        ["len", "starts_with"]. If non-"len" extract type is provided, pattern must not be None.
    pattern
        The pattern for every non-"len" extract.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "test_str": ["a_1", "x_2", "c_3", "x_22"]
    ... })
    >>> t.extract_from_str(df, cols=["test_str"], extract=["len", "contains"], pattern="(a_|x_)")
    shape: (4, 2)
    ┌──────────────┬───────────────────────────┐
    │ test_str_len ┆ test_str_contains_(a_|x_) │
    │ ---          ┆ ---                       │
    │ u32          ┆ u8                        │
    ╞══════════════╪═══════════════════════════╡
    │ 3            ┆ 1                         │
    │ 3            ┆ 1                         │
    │ 3            ┆ 0                         │
    │ 4            ┆ 1                         │
    └──────────────┴───────────────────────────┘
    '''    
    _ = type_checker(df, cols, "string", "extract_from_str")
    if isinstance(extract, list):
        to_extract = extract
    else:
        to_extract = [extract]
    
    if ((len(to_extract) > 1) | (len(to_extract) == 1 and to_extract[0] != 'len')) & (pattern is None):
        raise ValueError("The argument `pattern` has to be supplied when extract contains non-'len' types.")
    
    exprs = []
    for e in to_extract:
        if e == "len":
            exprs.append(pl.col(cols).str.len_bytes().suffix("_len"))
        elif e == "starts_with":
            exprs.append(pl.col(cols).str.starts_with(pattern).cast(pl.UInt8).suffix(f"_starts_with_{pattern}"))
        elif e == "ends_with":
            exprs.append(pl.col(cols).str.ends_with(pattern).cast(pl.UInt8).suffix(f"_ends_with_{pattern}"))
        elif e == "count":
            exprs.append(pl.col(cols).str.count_matches(pattern).suffix(f"_{pattern}_count"))
        elif e == "contains":
            exprs.append(pl.col(cols).str.contains(pattern).cast(pl.UInt8).suffix(f"_contains_{pattern}"))
        else:
            logger.info(f"Found {e} in extract, but it is not a valid StrExtract value. Ignored.")

    return _dsds_with_columns(df, exprs)

def extract_numbers(
    df: PolarsFrame
    , cols: Optional[list[str]] = None
    , *
    , ignore_comma: bool = False
    , join_by: str = ""
    , dtype: pl.DataType = pl.Utf8
) -> PolarsFrame:
    '''
    Extracts all numbers from the string column. This will always replace the original string column.
    This is useful for survey data where strings like "10% to 20%" are common.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        If not given, will infer possible numerical columns from string columns. If given, must be all 
        string columns.
    ignore_comma
        If true, remove the "," in the string before matching for numbers. If you know there won't be 
        comma, turn this to False can improve performance.
    join_by
        If this is not the empty string, then the numbers will be joined by the given string and a new
        string column will be returned instead of a column of lists of strings.
    dtype
        If a Polars numerical data type is given, the list's inner dtype will be cast to this. This takes
        priority over join_by.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "survey":["0% of my time", "1% to 25% of my time", "75% to 99% of my time", 
    ...             "50% to 74% of my time", "75% to 99% of my time", 
    ...             "50% to 74% of my time"]
    ... })
    >>> t.extract_numbers(df, ["survey"], join_by="-")
    shape: (6, 1)
    ┌────────┐
    │ survey │
    │ ---    │
    │ str    │
    ╞════════╡
    │ 0      │
    │ 1-25   │
    │ 75-99  │
    │ 50-74  │
    │ 75-99  │
    │ 50-74  │
    └────────┘
    >>> t.extract_numbers(df, ["survey"], dtype=pl.UInt16)
    shape: (6, 1)
    ┌───────────┐
    │ survey    │
    │ ---       │
    │ list[u16] │
    ╞═══════════╡
    │ [0]       │
    │ [1, 25]   │
    │ [75, 99]  │
    │ [50, 74]  │
    │ [75, 99]  │
    │ [50, 74]  │
    └───────────┘
    '''
    if isinstance(cols, list):
        _ = type_checker(df, cols, "string", "extract_numbers")
        strs = cols
    else:
        strs = infer_nums_from_str(df, ignore_comma)

    expr = pl.col(strs)
    if ignore_comma:
        expr = expr.str.replace_all(",", "")
    
    expr = expr.str.extract_all("(\d*\.?\d+)")
    if dtype in POLARS_NUMERICAL_TYPES: # as list of numbers
        expr = expr.list.eval(pl.element().cast(dtype))
    else: # as list of strings
        if join_by != "":
            expr = expr.list.join(join_by)

    return _dsds_with_columns(df, [expr])

def extract_first_number(
    df: PolarsFrame
    , cols: Optional[list[str]] = None
    , *
    , ignore_comma: bool = True
    , dtype: pl.DataType = pl.Float64
    , default: Optional[float] = None
) -> PolarsFrame:
    '''
    Extracts the first number from the given columns. This will always replace the original string column.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        If not given, will infer possible numerical columns from string columns. If given, must be all 
        string columns.
    ignore_comma
        If true, remove the "," in the string before matching for numbers. If you know there won't be 
        comma, turn this to False can improve performance. Note this replaces "," by the empty string,
        which may cause problems for comma-separated formats.
    dtype
        A valid Polars numeric type, like pl.Float64, that you want to cast the numbers to.
    default
        If not none, then will add a fill null step with this default value. Note that default will have numerical
        dtype as provided by dtype.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a": ["$1,123.23", "$2,221", "$31.23"],
    ...     "b": ["(1,123.23)", "(2,221)", "(31.23)"], 
    ...     "c": ["1212@1212", "12312DGAD231", "123!!!"] 
    ... })
    >>> t.extract_first_number(df)
    shape: (3, 3)
    ┌─────────┬─────────┬─────────┐
    │ a       ┆ b       ┆ c       │
    │ ---     ┆ ---     ┆ ---     │
    │ f64     ┆ f64     ┆ f64     │
    ╞═════════╪═════════╪═════════╡
    │ 1123.23 ┆ 1123.23 ┆ 1212.0  │
    │ 2221.0  ┆ 2221.0  ┆ 12312.0 │
    │ 31.23   ┆ 31.23   ┆ 123.0   │
    └─────────┴─────────┴─────────┘
    '''
    if isinstance(cols, list):
        _ = type_checker(df, cols, "string", "extract_first_number")
        strs = cols
    else:
        strs = infer_nums_from_str(df, ignore_comma)

    expr = pl.col(strs)
    if ignore_comma:
        expr = expr.str.replace_all(",", "")
    
    expr = expr.str.extract("(\d*\.?\d+)").cast(dtype)
    if default is not None:
        expr = expr.fill_null(pl.lit(default, dtype))
    return _dsds_with_columns(df, [expr])

def extract_patterns(
    df: PolarsFrame
    , pattern: str
    , cols: list[str]
    , *
    , lowercase: bool = False
    , join_by: str = ""
) -> PolarsFrame:
    '''
    Extracts all matching patterns from the string column. This will always replace the original string column.
    If you are trying to extract numbers, it is recommended that you use `dsds.transform.extract_numbers` instead.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    pattern
        Regex pattern
    cols
        A list of string columns
    lowercase
        If true, lowercase the columns before matching.
    join_by
        If this is not the empty string, then the matched patterns will be joined by the given string and a new
        string column will be returned instead of a column of lists of strings.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "survey":["0% of my time", "1% to 25% of my time", "75% to 99% of my time", 
    ...             "50% to 74% of my time", "75% to 99% of my time", 
    ...             "50% to 74% of my time"]
    ... })
    >>> print(t.extract_patterns(df, "(\d*\.?\d+)%", ["survey"], join_by=" to "))
    shape: (6, 1)
    ┌────────────┐
    │ survey     │
    │ ---        │
    │ str        │
    ╞════════════╡
    │ 0%         │
    │ 1% to 25%  │
    │ 75% to 99% │
    │ 50% to 74% │
    │ 75% to 99% │
    │ 50% to 74% │
    └────────────┘
    '''
    _ = type_checker(df, cols, "string", "extract_patterns")
    strs = cols
    expr = pl.col(strs)
    if lowercase:
        expr = expr.str.to_lowercase()

    expr = expr.str.extract_all(pattern)
    if join_by != "":
        expr = expr.list.join(join_by)

    return _dsds_with_columns(df, [expr])

def extract_from_json(
    df: PolarsFrame
    , json_col: str
    , *
    , paths: list[str]
    , dtypes: list[pl.DataType]
) -> PolarsFrame:
    '''
    Extract JSON fields from a JSON string column according to the json path.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    json_col
        The json column to extract from
    paths
        The values at the json paths will be extracted
    dtypes
        The corresponding dtypes for the values. Must be of the same length as paths
    
    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a": ['{ "id": 1, "name": "a", "course": {"0":"abc"}}', '{ "id": 2, "name": "b", "course": {"0":"efg"}}']
    ... })
    >>> print(t.extract_from_json(df, json_col="a", paths=["id", "course.0"] ,dtypes=[pl.UInt16, pl.Utf8]))
    shape: (2, 2)
    ┌──────┬────────────┐
    │ a.id ┆ a.course.0 │
    │ ---  ┆ ---        │
    │ u16  ┆ str        │
    ╞══════╪════════════╡
    │ 1    ┆ abc        │
    │ 2    ┆ efg        │
    └──────┴────────────┘
    '''
    _ = type_checker(df, [json_col], "string", "extract_from_json")
    if len(paths) != len(dtypes):
        raise ValueError("Length of paths must be the same as length of dtypes.")
    
    exprs = [
        pl.col(json_col).str.json_path_match(f"$.{p}").cast(t).suffix(f".{p}")
        for p, t in zip(paths, dtypes)
    ]
    return _dsds_with_columns(df, exprs)

def extract_list_features(
    df: PolarsFrame
    , cols: list[str]
    , *
    , extract: Union[ListExtract, list[ListExtract]] = ["min", "max"]
) -> PolarsFrame:
    '''
    Extract data from columns that contains lists.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Must be explicitly provided and should all be date/datetime columns
    extract
        One of "min", "max", "mean", "len", "first", "last", "sum" or a list of these values such as 
        ["min", "max"], which means extract min and max from all the columns provided. Notice if you 
        want to extract mean, then the column must be list of numbers.

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "a":[["a"],["b"], ["c"]],
    ...     "b":[[1,2], [3,3], [4,5,6]]
    ... })
    >>> t.extract_list_features(df, ["a","b"], extract=["min", "max", "len"])
    shape: (3, 6)
    ┌───────┬───────┬───────┬───────┬───────┬───────┐
    │ a_min ┆ b_min ┆ a_max ┆ b_max ┆ a_len ┆ b_len │
    │ ---   ┆ ---   ┆ ---   ┆ ---   ┆ ---   ┆ ---   │
    │ str   ┆ i64   ┆ str   ┆ i64   ┆ u32   ┆ u32   │
    ╞═══════╪═══════╪═══════╪═══════╪═══════╪═══════╡
    │ a     ┆ 1     ┆ a     ┆ 2     ┆ 1     ┆ 2     │
    │ b     ┆ 3     ┆ b     ┆ 3     ┆ 1     ┆ 2     │
    │ c     ┆ 4     ┆ c     ┆ 6     ┆ 1     ┆ 3     │
    └───────┴───────┴───────┴───────┴───────┴───────┘
    '''
    _ = type_checker(df, cols, "list", "extract_list_features")
    exprs = []
    to_extract = extract if isinstance(extract, list) else [extract]
    
    for e in to_extract:
        if e == "min":
            exprs.append(pl.col(cols).list.min().suffix("_min"))
        elif e == "max":
            exprs.append(pl.col(cols).list.max().suffix("_max"))
        elif e in ("mean", "avg"):
            exprs.append(pl.col(cols).list.mean().suffix("_mean"))
        elif e == "len":
            exprs.append(pl.col(cols).list.len().suffix("_len"))
        elif e == "first":
            exprs.append(pl.col(cols).list.first().suffix("_first"))
        elif e == "last":
            exprs.append(pl.col(cols).list.last().suffix("_last"))
        elif e == "sum":
            exprs.append(pl.col(cols).list.sum().suffix("_sum"))
        else:
            logger.info(f"Found {e} in extract, but it is not a valid ListExtract value. Ignored.")

    return _dsds_with_columns(df, exprs)

def combine_str_cols(
    df: PolarsFrame
    , cols: list[Union[str, pl.Expr]]
    , new_name: str
    , *
    , to_null: Optional[list[str]] = None
    , ignore_null: bool = True
    , empty_as_null: bool = True
    , separator: str = ""
) -> PolarsFrame:
    '''
    Combines multiple string columns/expressions into one column as a column of lists of strings. 
    You can optionally turn the new combined column into a string column separated 
    by a separator.

    This will be remembered by blueprint by default.

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        A list of either strings representing column names or Polars expressions
    new_name
        The name of the combined column
    to_null
        A list of other string values that should be considered to be null. This is useful
        because sometimes in some columns `N/A` is equivalent to null.
    ignore_null
        Whether to ignore nulls in the final concatenated list. If false, nulls will be elements
        in the list.
    empty_as_null
        Whether to treat empty list as null
    separator
        If it is not the empty string, then the output column will be a string column
        separated by this separator

    Example
    -------
    >>> import dsds.transform as t
    ... df = pl.DataFrame({
    ...     "category1": ["Fruit", "N/A", "Meat", "Kitchen"],
    ...     "category2": ["edible", None, "", "tool"]
    ... })
    >>> t.combine_str_cols(df, [pl.col("category1").str.to_lowercase(), "category2"], new_name="category", to_null=["n/a", ""])
    shape: (4, 3)
    ┌───────────┬───────────┬─────────────────────┐
    │ category1 ┆ category2 ┆ category            │
    │ ---       ┆ ---       ┆ ---                 │
    │ str       ┆ str       ┆ list[str]           │
    ╞═══════════╪═══════════╪═════════════════════╡
    │ Fruit     ┆ edible    ┆ ["fruit", "edible"] │
    │ N/A       ┆ null      ┆ []                  │
    │ Meat      ┆           ┆ ["meat"]            │
    │ Kitchen   ┆ tool      ┆ ["kitchen", "tool"] │
    └───────────┴───────────┴─────────────────────┘
    >>> t.combine_str_cols(df, [pl.col("category1").str.to_lowercase(), "category2"], new_name="category", to_null=["n/a", ""], separator="|")
    shape: (4, 3)
    ┌───────────┬───────────┬──────────────┐
    │ category1 ┆ category2 ┆ category     │
    │ ---       ┆ ---       ┆ ---          │
    │ str       ┆ str       ┆ str          │
    ╞═══════════╪═══════════╪══════════════╡
    │ Fruit     ┆ edible    ┆ fruit|edible │
    │ N/A       ┆ null      ┆ null         │
    │ Meat      ┆           ┆ meat         │
    │ Kitchen   ┆ tool      ┆ kitchen|tool │
    └───────────┴───────────┴──────────────┘
    '''
    _ = type_checker(df, cols, "string", "combine_str_cols") 
    if to_null is None:
        new_cols = cols
    else: # Expressions and str cases are different
        new_cols = [
            pl.when(pl.col(c).is_in(to_null)).then(None).otherwise(pl.col(c))
            if isinstance(c, str) else 
            pl.when(c.is_in(to_null)).then(None).otherwise(c) 
            for c in cols
        ]

    expr = pl.concat_list(new_cols)
    if ignore_null:
        expr = expr.list.set_difference(pl.Series("", [None]))

    if empty_as_null and separator == "":
        expr = pl.when(expr.list.len() == 0).then(None).otherwise(expr)
    elif separator != "":
        expr = pl.when(expr.list.len() == 0).then(None).otherwise(expr.list.join(separator))

    return _dsds_with_columns(df, [expr.alias(new_name)])

def moving_avgs(
    df:PolarsFrame
    , cols: list[str]
    , *
    , window_sizes:list[int]
    , min_periods: Optional[int] = None,
) -> PolarsFrame:
    '''
    Computes moving averages for column c with given window_sizes. Please make sure the dataframe is sorted
    before this. For a pipeline compatible sort, see `dsds.prescreen.order_by`.

    This will be remembered by blueprint by default.
    
    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Columns for which you want to compute moving averages
    window_sizes
        A list of positive integers > 1, representing the different moving average periods for the column c.
        Everything <= 1 will be ignored
    min_periods
        The number of values in the window that should be non-null before computing a result. If None, 
        it will be set equal to window size.
    '''
    _ = type_checker(df, cols, "numeric", "moving_avgs")
    exprs = [pl.col(cols).rolling_mean(i, min_periods=min_periods).suffix(f"_ma_{i}") 
             for i in window_sizes if i > 1]
    return _dsds_with_columns(df, exprs)

def as_percentages(
    df: PolarsFrame,
    cols: list[str],
) -> PolarsFrame:
    '''
    Transform the columns in cols into percentage changes. This will NOT make sense unless df is sorted
    beforehand according to some time column. It computes percentage change between current element and 
    the most-recent non-null element before the current element.

    !!! Note this is pipeline-compatible but will NOT be remembered by the blueprint !!!

    Parameters
    ----------
    df
        Either a lazy or eager Polars dataframe
    cols
        Numeric columns that you want to compute percentage changes.
    '''
    _ = type_checker(df, cols, "numeric", "as_percentages")
    return df.with_columns(pl.col(cols).pct_change())

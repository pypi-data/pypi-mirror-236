use crate::snowball::{SnowballEnv, algorithms};
use crate::text::consts::EN_STOPWORDS;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use rayon::prelude::*;
use std::str;


// use polars_lazy::dsl::GetOutput;
// use polars_core::prelude::*;
// use polars_lazy::prelude::*;
// use std::iter::zip;
// use std::borrow::Cow;

// pub enum STEMMER {
//     SNOWBALL
//     , NONE 
// }

// impl STEMMER {
//     pub fn from_str(s:&str) -> Self {
//         match s {
//             "snowball" => STEMMER::SNOWBALL,
//             _ => STEMMER::NONE
//         }
//     }
// }

#[inline]
pub fn hamming_dist(s1:&str, s2:&str) -> Option<u32> {
    if s1.len() != s2.len() {
        return None
    }
    let x = s1.as_bytes();
    let y = s2.as_bytes();
    Some(
        x.iter()
        .zip(y)
        .fold(0, |a, (b, c)| a + (*b ^ *c).count_ones() as u32)
    )
}

#[inline]
pub fn snowball_stem(word:Option<&str>, no_stopwords:bool) -> Option<String> {
    
    match word {
        Some(w) => {
            if (no_stopwords) & (EN_STOPWORDS.binary_search(&w).is_ok()) {
                None
            } else if w.parse::<f64>().is_ok() {
                None
            } else {
                let mut env: SnowballEnv<'_> = SnowballEnv::create(w);
                algorithms::english_stemmer::stem(&mut env);
                Some(env.get_current().to_string())
            }
        },
        _ => None
    }
}

#[inline]
pub fn levenshtein_dist(s1:&str, s2:&str) -> u32 {
    // It is possible to go faster by not using a matrix to represent the 
    // data structure it seems.

    // https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm

    let (len1, len2) = (s1.len(), s2.len());
    let mut dp: Vec<Vec<u32>> = vec![vec![0; len2 + 1]; len1 + 1];

    // Initialize the first row and first column
    for i in 0..=len1 {
        dp[i][0] = i as u32;
    }

    for j in 0..=len2 {
        dp[0][j] = j as u32;
    }

    // Fill the dp matrix using dynamic programming
    for (i, char1) in s1.chars().enumerate() {
        for (j, char2) in s2.chars().enumerate() {
            if char1 == char2 {
                dp[i + 1][j + 1] = dp[i][j];
            } else {
                dp[i + 1][j + 1] = 1 + dp[i][j].min(dp[i][j + 1].min(dp[i + 1][j]));
            }
        }
    }
    dp[len1][len2]
}

// ---------------------------------- Plugins below --------------------------------

#[polars_expr(output_type=UInt32)]
fn pl_levenshtein_dist(inputs: &[Series]) -> PolarsResult<Series> {
    let ca1 = inputs[0].utf8()?;
    let ca2 = inputs[1].utf8()?;

    if ca2.len() == 1 {
        let r = ca2.get(0).unwrap();
        let out: UInt32Chunked = ca1.par_iter().map(|op_s| {
            if let Some(s) = op_s {
                Some(levenshtein_dist(s, r))
            } else {
                None
            }
        }).collect();
        Ok(out.into_series())
    } else if ca1.len() == ca2.len() {
        let out: UInt32Chunked = ca1.par_iter_indexed()
            .zip(ca2.par_iter_indexed())
            .map(|(op_w1, op_w2)| {
                if let (Some(w1), Some(w2)) = (op_w1, op_w2) {
                    Some(levenshtein_dist(w1, w2))
                } else {
                    None
                }
            }).collect();
        Ok(out.into_series())
    } else {
        Err(PolarsError::ComputeError("Inputs must have the same length.".into()))
    }
}

#[polars_expr(output_type=Float64)]
fn pl_str_jaccard(inputs: &[Series]) -> PolarsResult<Series> {
    let ca1 = inputs[0].utf8()?;
    let ca2 = inputs[1].utf8()?;
    let ca3 = inputs[2].u32()?;
    let n = ca3.get(0).unwrap() as usize;

    if ca2.len() == 1 {

        let r = ca2.get(0).unwrap();
        let s2 = if r.len() > n {
            PlHashSet::from_iter(
                r.as_bytes().windows(n).map(|sl| str::from_utf8(sl).unwrap()
            )
        )} else {
            PlHashSet::from_iter([r])
        };
        let out: Float64Chunked = ca1.par_iter().map(|op_s| {
            if let Some(s) = op_s {
                let s1 = if s.len() > n {
                    PlHashSet::from_iter(
                        s.as_bytes().windows(n).map(|sl| str::from_utf8(sl).unwrap())
                    )
                } else {
                    PlHashSet::from_iter([s])
                };
                let intersection = s1.intersection(&s2).count();
                Some(
                    (intersection as f64) / ((s1.len() + s2.len() - intersection) as f64)
                )
            } else {
                None
            }
        }).collect();
        Ok(out.into_series())
    } else if ca1.len() == ca2.len() {

        let out: Float64Chunked = ca1.par_iter_indexed()
            .zip(ca2.par_iter_indexed())
            .map(|(op_w1, op_w2)| {
                if let (Some(w1), Some(w2)) = (op_w1, op_w2) {
                    if (w1.len() >= n) & (w2.len() >= n) {
                        let s1 = PlHashSet::from_iter(
                            w1.as_bytes().windows(n).map(|sl| str::from_utf8(sl).unwrap())
                        );
                        let s2 = PlHashSet::from_iter(
                            w2.as_bytes().windows(n).map(|sl| str::from_utf8(sl).unwrap())
                        );
                        let intersection = s1.intersection(&s2).count();
                        Some(
                            (intersection as f64) / ((s1.len() + s2.len() - intersection) as f64)
                        )
                    } else if (w1.len() < n) & (w2.len() < n) {
                        Some(((w1 == w2) as u8) as f64)
                    } else {
                        Some(0.)
                    }
                } else {
                    None
                }
            }).collect();
        Ok(out.into_series())
    } else {
        Err(PolarsError::ComputeError("Inputs must have the same length.".into()))
    }
}

#[polars_expr(output_type=UInt32)]
fn pl_hamming_dist(inputs: &[Series]) -> PolarsResult<Series> {
    let ca1 = inputs[0].utf8()?;
    let ca2 = inputs[1].utf8()?;

    if ca2.len() == 1 {
        let r = ca2.get(0).unwrap();
        let out: UInt32Chunked = ca1.par_iter().map(|op_s| {
            if let Some(w) = op_s {
                hamming_dist(w, r)
            } else {
                None
            }            
        }).collect();
        Ok(out.into_series())
    } else if ca1.len() == ca2.len() {
        let out: UInt32Chunked = ca1.par_iter_indexed()
            .zip(ca2.par_iter_indexed())
            .map(|(op_w1, op_w2)| {
                if let (Some(w1), Some(w2)) = (op_w1, op_w2) {
                    hamming_dist(w1, w2)
                } else {
                    None
                }
            }).collect();
        Ok(out.into_series())
    } else {
        Err(PolarsError::ComputeError("Inputs must have the same length.".into()))
    }
}

#[polars_expr(output_type=Utf8)]
fn pl_snowball_stem(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].utf8()?;
    let out: Utf8Chunked = ca.par_iter()
        .map(|op_s| snowball_stem(op_s, true)).collect();
    Ok(out.into_series())
}

// #[inline]
// pub fn get_ref_table(
//     df: DataFrame
//     , c: &str
//     , stemmer: STEMMER
//     , min_dfreq:f32
//     , max_dfreq:f32
//     , max_word_per_doc: u32
//     , max_feautures: u32
// ) -> PolarsResult<DataFrame> {

//     // this function assumes all documents in df[c] are lowercased.
//     let stemmer_expr:Expr = match stemmer {
//         STEMMER::SNOWBALL => col(c).map(snowball_on_series, GetOutput::from_type(DataType::Utf8)).alias(&"ref"),
//         _ => col(c).alias(&"ref")
//     };

//     let height: f32 = df.height() as f32;
//     let min_count: u32 = (height * min_dfreq).floor() as u32;
//     let max_count: u32 = (height * max_dfreq).ceil() as u32;
//     let output: DataFrame = df.select([c])?
//     .lazy()
//     .with_row_count(&"i", None)
//     .select([
//         col(&"i")
//         , col(c).str().extract_all(lit(r"(?u)\b\w\w+\b")).list().head(lit(max_word_per_doc))
//     ]).explode([col(c)])
//     .filter(col(c).str().lengths().gt(lit(2)).and(col(c).is_not_null()))
//     .select([
//         col(&"i")
//         , col(c)
//         , stemmer_expr // stemmed words, column name is ref
//     ]).group_by([col(&"ref")])
//     .agg([
//         col(c).unique()
//         , col(&"i").n_unique().alias(&"doc_cnt")
//         , count().alias(&"corpus_cnt")
//     ])
//     .filter(
//         (col(&"doc_cnt").gt(min_count)).and(col(&"doc_cnt").lt(max_count))
//     ).top_k(max_feautures, [col(&"doc_cnt")], [true], true, false)
//     .select([
//         col(&"ref")
//         , (lit("(") + col(c).list().join(&"|") + lit(")")).alias(&"captures")
//         , (col(&"doc_cnt").cast(DataType::Float32)/lit(height)).alias(&"doc_freq")
//         , (lit(height + 1.)/(col(&"doc_cnt") + lit(1)).cast(DataType::Float64))
//             .log(std::f64::consts::E).alias(&"smooth_idf")
//         , col(&"corpus_cnt")
//     ]).collect()?;
//     // .sort(&"doc_cnt", SortOptions::default())
//     // .with_column(col(&"doc_cnt").set_sorted_flag(IsSorted::Ascending))
//     Ok(output)

// }

// pub fn count_vectorizer(
//     df: DataFrame
//     , c: &str
//     , stemmer: STEMMER
//     , min_dfreq:f32
//     , max_dfreq:f32
//     , max_word_per_doc: u32
//     , max_feautures: u32
//     , lowercase: bool
// ) -> PolarsResult<DataFrame> {

//     // lowercase is expensive, do it only once.

//     // This, in fact, is still doing some duplicate work.
//     // The get_ref_table call technically has computed all count/tfidf vectorizer information
//     // at least once.
//     // The with_columns(exprs) call technically can be skipped. But the problem is for better 
//     // user-experience, we want to use dataframe as output.
//     // Scikit-learn uses sparse matrix as output, so technically get_ref_table is all Scikit-learn needs.
//     // With that said, this is still faster than Scikit-learn, and does stemming, does more 
//     // filtering, and technically computes some stuff twice,

//     let mut df_local: DataFrame = df.clone();
//     if lowercase {
//         df_local = df.lazy().with_column(col(c).str().to_lowercase().alias(c)).collect()?;
//     }

//     let stemmed_vocab: DataFrame = get_ref_table(
//                                             df_local.clone(),
//                                             c,
//                                             stemmer,
//                                             min_dfreq, 
//                                             max_dfreq, 
//                                             max_word_per_doc, 
//                                             max_feautures
//                                     )?.sort(["ref"], false, false)?;

//     // let mut exprs: Vec<Expr> = Vec::with_capacity(stemmed_vocab.height());
    
//     let temp: &Series = stemmed_vocab.column("ref")?;
//     let stems: &ChunkedArray<Utf8Type> = temp.utf8()?;
//     let temp: &Series = stemmed_vocab.column(&"captures")?;
//     let vocabs: &ChunkedArray<Utf8Type> = temp.utf8()?;

//     let mut exprs:Vec<Expr> = Vec::with_capacity(stems.len());
//     for (stem, pat) in zip(stems.into_iter(), vocabs.into_iter()) {
//         if let (Some(s), Some(p)) = (stem, pat) {
//             exprs.push(col(c).str().count_matches(p).suffix(format!("::cnt_{}", s).as_ref()))
//         }
//     }

//     let out: DataFrame = df_local.lazy().with_columns(exprs).drop_columns([c]).collect()?;
//     Ok(out)

// }

// pub fn tfidf_vectorizer(
//     df: DataFrame
//     , c: &str
//     , stemmer: STEMMER
//     , min_dfreq:f32
//     , max_dfreq:f32
//     , max_word_per_doc: u32
//     , max_feautures: u32
//     , lowercase: bool
// ) -> PolarsResult<DataFrame> {

//     let mut df_local: DataFrame = df.clone();
//     if lowercase {
//         df_local = df.lazy().with_column(col(c).str().to_lowercase().alias(c)).collect()?;
//     }

//     let stemmed_vocab: DataFrame = get_ref_table(
//                                             df_local.clone(),
//                                             c,
//                                             stemmer,
//                                             min_dfreq, 
//                                             max_dfreq, 
//                                             max_word_per_doc, 
//                                             max_feautures
//                                     )?.sort(["ref"], false, false)?;

//     let temp: &Series = stemmed_vocab.column(&"ref")?;
//     let stems: &ChunkedArray<Utf8Type> = temp.utf8()?;
//     let temp: &Series = stemmed_vocab.column(&"captures")?;
//     let vocabs: &ChunkedArray<Utf8Type> = temp.utf8()?;
//     let temp: &Series = stemmed_vocab.column(&"smooth_idf")?;
//     let smooth_idf: &ChunkedArray<Float64Type> = temp.f64()?;
                                        
//     let mut exprs: Vec<Expr> = Vec::with_capacity(stems.len());
//     for ((stem, pat), idf) in 
//         stems.into_iter().zip(vocabs.into_iter()).zip(smooth_idf.into_iter()) 
//     {
//         if let (Some(w), Some(p), Some(f)) = (stem, pat, idf) {
//             exprs.push(
//                 (   lit(f).cast(DataType::Float64)
//                     * col(c).str().count_matches(p).cast(DataType::Float64)
//                     / col(&"__doc_len__")
//                 ).suffix(format!("::tfidf_{}", w).as_ref())
//             )
//         }
//     }
//     let out: DataFrame = df_local.lazy().with_column(
//         col(c).str().extract_all(lit(r"(?u)\b\w\w+\b"))
//         .list().head(lit(max_word_per_doc))
//         .list().lengths()
//         .cast(DataType::Float64).alias(&"__doc_len__")
//     ).with_columns(exprs)
//     .drop_columns([c, &"__doc_len__"]).collect()?;
    
//     Ok(out)
// }
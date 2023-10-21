use ndarray::{Axis, ArrayView1, Array2};
use ndarray::parallel::prelude::*;
//use faer_core::Scale;
//use faer::{prelude::*, IntoNdarray};
//use faer_core::mul::matmul;
use polars_core::utils::accumulate_dataframes_vertical;
use polars::prelude::*;
use pyo3::pyfunction;
use pyo3_polars::derive::polars_expr;
use std::collections::HashSet;
use super::utils::split_offsets;

// Don't use these functions in Rust.. They shouldn't be in place operations
// from a user experience point of view. But they are copied from Python input
// and only serve this purpose. So I decided on these in place operations.


// Distance/Error Metrics

#[inline]
pub fn mae(
    y_a:ArrayView1<f64>,
    y_p:ArrayView1<f64>,
    weights:Option<ArrayView1<f64>>
)-> f64 {

    let mut diff = &y_a - &y_p;
    diff.mapv_inplace(f64::abs);
    if let Some(w) = weights {
        return diff.dot(&w) / w.sum()
    }
    diff.mean().unwrap_or(0.)
}

#[inline]
pub fn mse(
    y_a:ArrayView1<f64>,
    y_p:ArrayView1<f64>,
    weights:Option<ArrayView1<f64>>
) -> f64 {

    let diff = &y_a - &y_p;
    if let Some(w) = weights {
        return (&diff * &w).dot(&diff) / w.sum()
    } 
    diff.dot(&diff) / y_a.len() as f64
}

#[inline]
pub fn mape(
    y_a:ArrayView1<f64>,
    y_p:ArrayView1<f64>,
    weighted: bool 
) -> f64 {
    if (y_a.len() == 0) | (y_p.len() == 0) {
        return 0.
    }
    if weighted {
        let diff = &y_a - &y_p;
        let denominator = y_a.fold(0., |acc, x| acc + x.abs());
        if denominator == 0. {
            return f64::INFINITY
        }
        diff.fold(0., |acc, x| acc + x.abs()) / denominator

    } else {
        let summand = 1.0 - (&y_p / &y_a);
        let sum = summand.fold(0., |acc, x| acc + x.abs());
        sum / (y_a.len() as f64)
    }
}

#[inline]
pub fn smape(
    y_a:ArrayView1<f64>,
    y_p:ArrayView1<f64>,
    double_sum: bool
) -> f64 {
    if (y_a.len() == 0) | (y_p.len() == 0) {
        return 0.
    }
    if double_sum {
        let (nom, denom) = y_a.into_iter().zip(y_p.into_iter())
            .fold((0.,0.), |acc,(a,f)| (acc.0 + (a-f).abs(), acc.1 + a + f));
        if denom == 0. {
            return f64::INFINITY
        }
        nom / denom
    } else {
        let sum: f64 = y_a.into_iter().zip(y_p.into_iter()).fold(0., |acc, (a, f)| {
            let denom: f64 = a.abs() + f.abs();
            if denom > 0. {
                acc + (a-f).abs() / denom 
            } else {
                acc 
            }
        });
        (100.0 / y_a.len() as f64) * sum
    }
}

#[inline]
pub fn huber_loss(
    y_a:ArrayView1<f64>,
    y_p:ArrayView1<f64>,
    delta: f64,
    weights:Option<ArrayView1<f64>>
) -> f64 {

    let mut diff = &y_a - &y_p;
    let half_delta: f64 = 0.5 * delta;
    diff.mapv_inplace(|x| {
        let abs_x: f64 = x.abs();
        if abs_x < delta {
            0.5 * abs_x.powi(2)
        } else {
            delta * (abs_x - half_delta)
        }
    });

    if let Some(w) = weights {
        return (diff.dot(&w)) / w.sum()
    }
    diff.mean().unwrap_or(0.)
}

// Cosine Similarity

#[inline]
pub fn cosine_similarity(
    mut mat1:Array2<f64>,
    mut mat2:Array2<f64>,
    normalize:bool
) -> Array2<f64> {
    if normalize {
        normalize_in_place(&mut mat1, Axis(0));
        normalize_in_place(&mut mat2, Axis(0));
        mat1.dot(&mat2.t())
    } else {
        mat1.dot(&mat2.t())
    }
}


#[inline]
pub fn self_cosine_similarity(
    mut mat1:Array2<f64>,
    normalize:bool
) -> Array2<f64> {
    if normalize {
        normalize_in_place(&mut mat1, Axis(0));
        mat1.dot(&mat1.t())
    } else {
        mat1.dot(&mat1.t())
    }
}

#[inline]
fn normalize_in_place(mat:&mut Array2<f64>, axis:Axis) {
    mat.axis_iter_mut(axis).into_par_iter().for_each(|mut rc| {
        // let norm: f64 = rc.fold(0., |acc, x| acc + x.powi(2)).sqrt();
        let norm = rc.dot(&rc).sqrt();
        rc /= norm;
    });
}

// Jaccard Similarity

pub enum HashableType {
    STRING,
    INTEGER
}

impl HashableType {

    pub fn from_str(s:&str) -> Option<HashableType> {
        match s {
            "string"|"str" => Some(HashableType::STRING),
            "int" => Some(HashableType::INTEGER),
            _ => None
        }
    }
}

fn compute_jaccard_similarity(
    sa: &Series, 
    sb: &Series, 
    st: &HashableType, 
    include_null:bool
) -> PolarsResult<Series> {
    let sa: &ChunkedArray<ListType> = sa.list()?;
    let sb: &ChunkedArray<ListType> = sb.list()?;

    let ca: ChunkedArray<Float64Type> = sa.into_iter().zip(sb.into_iter()).map(|(a, b)| {
        match (a, b) {
            (Some(a), Some(b)) => {
                let (mut s3_len, s1_len, s2_len) = match st {
                    HashableType::INTEGER => {
                        let (a, b) = (a.i64()?, b.i64()?);
                        let s1 = a.into_iter().collect::<PlHashSet<_>>();
                        let s2 = b.into_iter().collect::<PlHashSet<_>>();
                        (s1.intersection(&s2).count(), s1.len(), s2.len())
                    },
                    HashableType::STRING => {
                        let (a, b) = (a.utf8()?, b.utf8()?);
                        let s1 = a.into_iter().collect::<PlHashSet<_>>();
                        let s2 = b.into_iter().collect::<PlHashSet<_>>();
                        (s1.intersection(&s2).count(), s1.len(), s2.len())
                    }
                };
                // return similarity
                if (!include_null) & (a.null_count() > 0) & (b.null_count() > 0) {
                    s3_len -= 1;
                }
                Ok(Some(s3_len as f64 / (s1_len + s2_len - s3_len) as f64))
            },
            _ => Ok(None)
        }
    }).collect::<PolarsResult<Float64Chunked>>()?;
    Ok(ca.into_series())
}

pub fn list_jaccard_similarity(
    df:DataFrame, 
    col_a: &str, 
    col_b: &str, 
    st: HashableType, 
    include_null:bool
) -> PolarsResult<DataFrame> {

    let offsets: Vec<(usize, usize)> = split_offsets(df.height(), rayon::current_num_threads());

    let dfs: Vec<DataFrame>= offsets.par_iter().map(|(offset, len)| {
        let sub_df = df.slice(*offset as i64, *len);
        let a: &Series = sub_df.column(col_a)?;
        let b: &Series = sub_df.column(col_b)?;
        let name = format!("{}_{}_jaccard", col_a, col_b);
        let out: Series = compute_jaccard_similarity(a, b, &st, include_null)?;
        df!(name.as_str() => out)
    }).collect::<PolarsResult<Vec<_>>>()?;
    accumulate_dataframes_vertical(dfs)
}

#[inline]
pub fn series_jaccard_similarity(
    a: Series,
    b: Series,
    st: HashableType, 
    include_null:bool,
    parallel: bool
) -> PolarsResult<f64> {

    // Jaccard similarity of two series.
    let na: usize = a.null_count();
    let nb: usize = b.null_count();
    let (mut s3_len, s1_len, s2_len) = match st {
        HashableType::INTEGER => {
            let (a, b) = (a.i64()?, b.i64()?);
            let s1 = a.into_iter().collect::<PlHashSet<_>>();
            let s2 = b.into_iter().collect::<PlHashSet<_>>();
            (s1.intersection(&s2).count(), s1.len(), s2.len())
        },
        HashableType::STRING => {
            let (a, b) = (a.utf8()?, b.utf8()?);
            if parallel {
                let cas: [&ChunkedArray<Utf8Type>; 2] = [a, b];
                let mut sets: Vec<PlHashSet<Option<&str>>> = Vec::with_capacity(2);
                cas.into_par_iter().map(|s| s.into_iter().collect::<PlHashSet<_>>())
                .collect_into_vec(&mut sets);
                let (s1, s2) = unsafe {
                    (sets.get_unchecked(0), sets.get_unchecked(1))
                };
                (s1.intersection(&s2).count(), s1.len(), s2.len())
            } else {
                let s1 = a.into_iter().collect::<PlHashSet<_>>();
                let s2 = b.into_iter().collect::<PlHashSet<_>>();
                (s1.intersection(&s2).count(), s1.len(), s2.len())
            }
        }
    };
    if (!include_null) & (na > 0) & (nb > 0) {
        s3_len -= 1;
    }
    Ok(s3_len as f64 / (s1_len + s2_len - s3_len) as f64)
}

// Complexity Metrics

#[pyfunction]
pub fn rs_lempel_ziv_complexity(
    s: &[u8]
) -> usize {

    let mut ind:usize = 0;
    let mut inc:usize = 1;

    let mut sub_strings: HashSet<&[u8]> = HashSet::new();
    while ind + inc <= s.len() {
        let subseq: &[u8] = &s[ind..ind+inc];
        if sub_strings.contains(subseq) {
            inc += 1;
        } else {
            sub_strings.insert(subseq);
            ind += inc;
            inc = 1;
        }
    }
    sub_strings.len()
}

#[polars_expr(output_type=UInt32)]
fn pl_lempel_ziv_complexity(inputs: &[Series]) -> PolarsResult<Series>  {
    
    let input: &Series = &inputs[0];
    let bytes: Vec<u8> = match input.dtype() {
        DataType::Boolean => {
            let ca = input.bool()?;
            ca.into_iter().map(
                |x| {
                    if let Some(b) = x {
                        b as u8
                    } else {
                        0
                    }
                }
            ).collect()
        }
        , _ => {
            return Err(
                PolarsError::ComputeError("Input series must be bool.".into())
            )
        }
    };

    let c: usize = rs_lempel_ziv_complexity(&bytes);
    Ok(Series::from_iter([c as u64]))

}
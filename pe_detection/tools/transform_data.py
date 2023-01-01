from typing import Optional, List, Dict, Union, Tuple
from more_itertools import windowed
import pandas as pd


# ====================
def paras_df_to_xy_df(paras_df: pd.DataFrame,
                      cols_to_classes: Dict[str, str],
                      cols_to_keep: Optional[Union[List[str], Dict[str, str]]] = None) -> pd.DataFrame:
    """Take data from a pandas DataFrame with columns for different
    text types and a row for each paragraph and return a DataFrame
    with paragraphs in the 'x' column and class labels in the 'y' column

    Args:
      paras_df (pd.DataFrame):
        The DataFrame containing columns for different text types and a
        row for each paragraph 
      cols_to_classes (Dict[str, str]):
        The mapping of column labels to class labels.
        E.g.:
            {
                'ted.en-de.ht.de.norm': 'ht',
                'ted.en-de.penmt1.de.norm': 'pe'
            }
      cols_to_keep (Optional[Union[List[str], Dict[str, str]]], optional):
        Other columns to keep in the output DataFrame. May be a list of
        column labels or a dictionary mapping existing column labels to 
        new column labels. Defaults to None.

    Returns:
      pd.DataFrame:
        A DataFrame with columns 'x' (for paragraphs) and 'y' (for class
        labels), as well as any other columns that were kept.
    """

    if cols_to_keep is None:
        cols_to_keep = dict()
    elif isinstance(cols_to_keep, list):
        cols_to_keep = {x: x for x in cols_to_keep}
    col_dfs = {
        col: ((paras_df[list(cols_to_keep.keys()) + [col]])
            .rename(columns={col: 'x'})
            .rename(columns=cols_to_keep)
            .assign(y=class_)
        )
        for col, class_ in cols_to_classes.items()
    }
    return pd.concat(col_dfs, ignore_index=True)
    

# ====================
def train_test_df_to_xy_dfs(train_test_df: pd.DataFrame,
                            cols_to_classes: Dict[str, str],
                            cols_to_keep: Optional[Union[List[str], Dict[str, str]]] = None
                            ) -> pd.DataFrame:

    train = train_test_df[train_test_df['role'] == 'train']
    test = train_test_df[train_test_df['role'] == 'test']
    train_ = paras_df_to_xy_df(train, cols_to_classes, cols_to_keep)
    test_ = paras_df_to_xy_df(test, cols_to_classes, cols_to_keep)
    return train_, test_


# ====================
def ngram_overlaps_df(df: pd.DataFrame,
                      x1_label: str,
                      x2_label: str,
                      ngrams: Tuple[int, int]) -> pd.DataFrame:

    overlaps_df_rows = {}
    col_label_root = f"{x1_label}_{x2_label}_overlap"
    ngram_range = range(ngrams[0], ngrams[1]+1)
    for _, row in df.iterrows():
        this_row = {
            f"{col_label_root}_{n}gram": ngram_overlap(row[x1_label], row[x2_label], n)
            for n in ngram_range
        }
        overlaps_df_rows.append(this_row)
    overlaps_df = pd.DataFrame(overlaps_df_rows)
    other_cols = [c for c in df.columns if c not in [x1_label, x2_label]]
    for c in other_cols:
        overlaps_df[c] = df[c]
    return overlaps_df


# ====================
def ngram_overlap(text1, text2, n) -> float:

    ngrams1 = set(windowed(text1.split(), n=n, step=n))
    ngrams2 = set(windowed(text2.split(), n=n, step=n))
    ngram_overlap = len(ngrams1.intersection(ngrams2) / len(ngrams1))
    return ngram_overlap




# def split_by_column(df: pd.DataFrame, column: str) -> dict:

#     vals = df[column].to_list()
#     dfs = {val: df[df[column] == val].drop(columns=[column]).reset_index(drop=True) for val in vals}
#     return dfs

# # ====================
# def append_diffs(df: pd.DataFrame, X_columns: list, ref_column: str, ngrams: Tuple[int, int]) -> pd.DataFrame:

#     new_df = df.copy()
#     ref_texts = df[ref_column].to_list()
#     ngram_range = list(range(ngrams[0], ngrams[1]+1))
#     ref_ngrams = {}
#     for n in ngram_range:
#         ref_ngrams[n] = [set(windowed(x.split(), n=n, step=n)) for x in ref_texts]
#     for col in X_columns:
#         texts = df[col].to_list()
#         for n in ngram_range:
#             ngrams = [set(windowed(x.split(), n=n, step=n)) for x in texts]
#             ngram_diffs = [len(this.difference(ref)) / len(this) for this, ref in zip(ngrams, ref_ngrams[n])]
#             new_df[f"{col}_diff_{ref_column}_{n}gram"] = pd.Series(ngram_diffs)
#     return new_df

# # ====================
# def split_and_label(df: pd.DataFrame, categories: list, main_col: str, label_col: str) -> pd.DataFrame:

#     dfs = []
#     for cat in categories:
#         cols_as_is = [col for col in df.columns if col.startswith(cat)]
#         cols_to_be = [main_col if col == cat else col.replace(f"{cat}_", "") for col in cols_as_is]
#         df_ = df[cols_as_is]
#         df_.columns = cols_to_be
#         df_.insert(len(df_.columns), label_col, cat)
#         dfs.append(df_)
#     return pd.concat(dfs)
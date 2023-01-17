from typing import Optional, List, Dict, Union, Tuple
from more_itertools import windowed
import pandas as pd

from pe_detection.tools.column_name_helper import get_column_name


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
                            cols_to_keep: Optional[Union[List[str], Dict[str, str]]] = None,
                            train_docs: Optional[List[int]] = None,
                            test_docs: Optional[List[int]] = None,
                            ) -> pd.DataFrame:

    if train_docs is not None and test_docs is not None:
        train = train_test_df[train_test_df['doc_idx'].isin(train_docs)]
        test = train_test_df[train_test_df['doc_idx'].isin(test_docs)]
    else:
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

    overlaps_df_rows = []
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
    ngram_overlap = len(ngrams1.intersection(ngrams2)) / len(ngrams1)
    return ngram_overlap


# ====================
def get_cols_to_classes(dataset: str,
                        language_pair: str,
                        preprocessing_steps: str,
                        systems: List[str],
                        labels: List[str],
                        prefix: str = '') -> Dict[str, str]:

    if len(systems) != len(labels):
        raise ValueError(
            "Lists of systems and labels should have the same length. " +\
            f"len(systems) = {len(systems)} but len(labels) = {len(labels)}."
        )
    return {
        prefix + get_column_name(language_pair, system, preprocessing_steps, dataset): label
        for system, label in zip(systems, labels)
    }

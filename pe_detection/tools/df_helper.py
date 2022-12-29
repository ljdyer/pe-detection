import pandas as pd
from pe_detection.tools.text_helper import num_tokens
from typing import Optional


# ====================
def display_row(df: pd.DataFrame, row_idx: int):
    """Print the content of each column in a row of a pandas DataFrame

    Args:
      df (pd.DataFrame):
        The pandas DataFrame
      row_idx (int):
        The index of the row to print
    """

    for c in df.columns:
        print(str(c) + '\t' + str(df.iloc[row_idx][c]))


# ====================
def sents_df_to_paras_df(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a pandas DataFrame where each row contains a sentence
    to one where each row contains a (pseudo-)paragraph based on
    information in doc_idx and para_idx columns

    Args:
      df (pd.DataFrame):
        The pandas DataFrame to convert. Must have 'doc_idx' and
        'para_idx' columns.

    Returns:
      pd.DataFrame: A pandas DataFrame where each row contains a
      (pseudo-)paragraph.
    """

    doc_idxs = set(df['doc_idx'].to_list())
    paras_df = pd.DataFrame()
    for doc_idx in doc_idxs:
        doc_df = df[df['doc_idx'] == doc_idx]
        para_idxs = set(doc_df['para_idx'].to_list())
        for para_idx in para_idxs:
            next_idx = len(paras_df)
            for col in [c for c in doc_df.columns
             if c not in ['para_idx', 'doc_idx']]:
                paras_df.at[next_idx, col] = ' '.join(
                    doc_df[doc_df['para_idx'] == para_idx][col].to_list())
            paras_df.at[next_idx, 'doc_idx'] = doc_idx
    return paras_df


# ====================
def token_counts_df(df: pd.DataFrame,
                    ignore_cols: Optional[list] = None) -> pd.DataFrame:
    """Replace each element of a pandas DataFrame (except those in columns
    specified in ignore_cols) with the number of tokens in that element.

    Args:
      df (pd.DataFrame):
        A pandas DataFrame in which all elements other than those in
        ignore_cols are string objects.
      ignore_cols (Optional[list], optional): 
        A list of columns to ignore. Defaults to None.

    Returns:
      pd.DataFrame:
        The DataFrame of token counts
    """

    if ignore_cols is None:
        ignore_cols = []
    columns_to_count = [c for c in df.columns if c not in ignore_cols]
    counts_df = df.copy()
    for c in columns_to_count:
        counts_df[c] = counts_df[c].apply(lambda x: num_tokens(x))
    return counts_df

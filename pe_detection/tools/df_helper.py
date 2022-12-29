import pandas as pd


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
def sents_df_to_paras_df(df: pd.DataFrame):
    """Convert a pandas DataFrame where each row contains a sentence
    to one where each row contains a (pseudo-)paragraph based on
    information in doc_idx and para_idx columns

    Args:
      df (pd.DataFrame):
        The pandas DataFrame to convert. Must have 'doc_idx' and
        'para_idx' columns.
    """    

    doc_idxs = set(df['doc_idx'].to_list())
    paras_df = pd.DataFrame()
    for doc_idx in doc_idxs:
        doc_df = df[df['doc_idx'] == doc_idx]
        para_idxs = set(doc_df['para_idx'].to_list())
        for para_idx in para_idxs:
            next_idx = len(paras_df)
            for col in doc_df.columns:
                if col not in ['para_idx', 'doc_idx']:
                    paras_df.at[next_idx, col] = ' '.join(doc_df[doc_df['para_idx'] == para_idx][col].to_list())
                paras_df.at[next_idx, 'doc_idx'] = doc_idx
                paras_df.at[next_idx, 'para_idx'] = para_idx
    return paras_df

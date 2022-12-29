import pandas as pd


# ====================
def train_test_split(df: pd.DataFrame, doc_idxs_train: list):

    train_df = df[df['doc_idx'].isin(doc_idxs_train)]
    test_df = df[~df['doc_idx'].isin(doc_idxs_train)]
    return train_df, test_df

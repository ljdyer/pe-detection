import pandas as pd
from typing import Dict
from pe_detection.tools.text_helper import num_tokens


# ====================
def get_doc_token_counts(df: pd.DataFrame, col_label: str) -> Dict[int, int]:

    doc_idxs = df['doc_idx'].to_list()
    token_counts = {}
    for doc_idx in doc_idxs:
        token_counts[int(doc_idx)] \
            = num_tokens(''.join(df[df['doc_idx'] == doc_idx][col_label].to_list()))
    return token_counts
    



# ====================
def train_test_split(df: pd.DataFrame, doc_idxs_train: list):

    train_df = df[df['doc_idx'].isin(doc_idxs_train)]
    test_df = df[~df['doc_idx'].isin(doc_idxs_train)]
    return train_df, test_df

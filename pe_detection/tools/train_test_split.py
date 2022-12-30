import pandas as pd
from typing import Dict, Tuple, List
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
def best_split(doc_token_counts: Dict[int, int],
               desired_test_ratio: float) -> Tuple[List[int], List[int], float]:
    """Work out train/test split that gets ratio of tokens as close as possible to 0.2"""

    num_docs = len(doc_token_counts.keys())
    total_toks = sum(doc_token_counts.values())
    splits = []
    # Iterate over binary numbers from 0*num_docs to 1*num_docs
    for i in range(int('1' * num_docs, 2)):
        # Remove '0b' from start of binary string
        bin_ = bin(i)[2:].zfill(num_docs)
        train = [doc_idx for doc_idx in range(num_docs) if bin_[doc_idx] == '0']
        test = [doc_idx for doc_idx in range(num_docs) if bin_[doc_idx] == '1']
        test_toks = sum([doc_token_counts[x] for x in test])
        actual_ratio = test_toks / total_toks
        splits.append((test, train, actual_ratio))
    return min(splits, key=lambda x: abs(x[2] - desired_test_ratio))


# ====================
def train_test_split(df: pd.DataFrame, doc_idxs_train: list):

    train_df = df[df['doc_idx'].isin(doc_idxs_train)]
    test_df = df[~df['doc_idx'].isin(doc_idxs_train)]
    return train_df, test_df

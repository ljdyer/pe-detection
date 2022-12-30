import pandas as pd
from typing import Dict, Tuple, List, Optional
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
               desired_test_ratio: float,
               must_be_train: Optional[List[int]] = None
               ) -> Tuple[List[int], List[int], float]:
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
        if any([doc_idx in must_be_train for doc_idx in test]):
            continue
        test_toks = sum([doc_token_counts[x] for x in test])
        actual_ratio = test_toks / total_toks
        splits.append((test, train, actual_ratio))
    return min(splits, key=lambda x: abs(x[2] - desired_test_ratio))


# ====================
def n_best_splits(doc_token_counts: Dict[int, int],
                  desired_test_ratio: float,
                  n: int) -> List[Tuple[List[int], List[int], float]]:

    best_splits = []
    must_be_train = []
    for _ in n:
        next_best = best_split(doc_token_counts, desired_test_ratio, must_be_train)
        best_splits.append(next_best)
        must_be_train.extend(next_best[0])
    return best_splits


# ====================
def train_test_split(df: pd.DataFrame, doc_idxs_train: list):

    train_df = df[df['doc_idx'].isin(doc_idxs_train)]
    test_df = df[~df['doc_idx'].isin(doc_idxs_train)]
    return train_df, test_df

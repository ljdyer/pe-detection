from typing import Dict, List, Optional, Tuple

import pandas as pd

from pe_detection.tools.text_helper import num_tokens


# ====================
def get_doc_token_counts(df: pd.DataFrame, col_label: str) -> Dict[int, int]:
    """Return a dictonary containing the number of tokens in each document
    in the DataFrame based on the 'doc_idx' column.

    Args:
      df (pd.DataFrame):
        A pandas DataFrame in which each row contains a sentence or (pseudo-)
        paragraph and which has a 'doc_idx' column.
      col_label (str):
        The label of a text column to get token counts for.
        (e.g. 'ted.en-fr.src.en.norm')

    Returns:
      Dict[int, int]:
        A dictionary whose keys are document indices and values are the number
        of tokens in the specified column for the corresponding document.
    """    

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
    """Return the train/test split for which the ratio of document tokens
    in test/train sets is the closest to desired_test_ratio

    Args:
      doc_token_counts (Dict[int, int]):
        A dictionary of document token counts (can be obtained using
        get_doc_token_counts).
      desired_test_ratio (float):
        The desired ratio of test to train tokens (e.g. 0.2).
      must_be_train (Optional[List[int]], optional):
        A list of document indices that must not be included in the
        test set. Defaults to None.

    Returns:
      Tuple[List[int], List[int], float]:
        A tuple of a list of document indices in the train set, a list
        of document indices in the test set, and the ratio of tokens
        between the test and train sets.
    """    

    if must_be_train is None:
        must_be_train = []
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
        splits.append((train, test, actual_ratio))
    return min(splits, key=lambda x: abs(x[2] - desired_test_ratio))


# ====================
def n_best_splits(doc_token_counts: Dict[int, int],
                  desired_test_ratio: float,
                  n: int) -> List[Tuple[List[int], List[int], float]]:
    """Return the n distinct train/test splits (with no document included
    in the test set in more than one split) for which the ratio of document
    tokens in test/train sets is the closest to desired_test_ratio

    Args:
      doc_token_counts (Dict[int, int]):
        A dictionary of document token counts (can be obtained using
        get_doc_token_counts).
      desired_test_ratio (float):
        The desired ratio of test to train tokens (e.g. 0.2).
      n (int):
        The number of splits to return.

    Returns:
      List[Tuple[List[int], List[int], float]]: _description_
        A list of tuples each containing a list of document indices in
        the train set, a list of document indices in the test set,
        and the ratio of tokens between the test and train sets.
        The splits are ordered from best to worst.
    """                  

    best_splits = []
    must_be_train = []
    for i in range(n):
        if set(must_be_train) == set(doc_token_counts.keys()):
            print(
                'No more documents that can be included in test set. ' + \
                f'Returning {i} best splits.'
            )
            break
        next_best = best_split(doc_token_counts, desired_test_ratio, must_be_train)
        best_splits.append(next_best)
        must_be_train.extend(next_best[1])
    return best_splits


# ====================
def train_test_split(df: pd.DataFrame,
                     doc_idxs_train: List[int]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split a DataFrame into train and test DataFrames based on the document
    indices in the doc_idx column

    Args:
      df (pd.DataFrame):
        The original DataFrame. Must include a column named 'doc_idx.
      doc_idxs_train (List[int]):
        The indices of the documents to include in the train set.

    Returns:
      Tuple[pd.DataFrame, pd.DataFrame]:
        A tuple containing the train DataFrame and the test DataFrame
    """    

    train_df = df[df['doc_idx'].isin(doc_idxs_train)]
    test_df = df[~df['doc_idx'].isin(doc_idxs_train)]
    return train_df, test_df

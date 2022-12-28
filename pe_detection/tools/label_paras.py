from itertools import chain
from typing import List, Optional, Tuple, Generator
import pandas as pd
from pe_detection.tools.text_helper import num_tokens


# ====================
def flatten(lis_: List[list]) -> list:
    """Flatten a list of lists.
    E.g. [[0,1], [2,3]] -> [0, 1, 2, 3]

    Args:
      lis_ (List[list]):
        A list of lists (e.g. [[0,1], [2,3]])

    Returns:
      list:
        A list of only the elements in the original lists.
        E.g. [0, 1, 2, 3].
    """

    return list(chain(*lis_))


# ====================
def get_smallest_partition(lis_: List[int],
                           min_: int,
                           max_diff: int = 100) -> Tuple[List[List[int]], int]:
    """Find the partition of a list of integers such that the sum of
    the integers in each sub-list is no less than min_, but the maximum
    sum of a integers in any sub-list is as close as possible to min_.

    Args:
      lis_ (List[int]):
        A list of integers (e.g. [12, 5, 7, 13, 6, 5])
      min_ (int): 
        The minimum value for the sum of the integers in any of the
        sub-lists in the partition.
      max_diff (int, optional):
        The maximum difference from min_ permitted for the total of each
        sub-list. For example, if min_=12 and max=12, sub-lists in the
        partition may sum up to 24 but no higher.
        Defaults to 100.

    Raises:
      ValueError:
        If there are no partitions that satisfy the requirements.

    Returns:
      Tuple[List[List[int]], int]: _description_
        A tuple containing the optimal partition of the original list based
        on the parameters specified, and the maximum sub-list total for the
        partition.
        E.g. ([[12], [5, 7], [13, 6, 5]], 24)
        If two or more partitions are found that satisfy the requirements,
        the one containing the highest number of sub-lists is returned (or
        only the first of these is returned if there are multiple partitions
        with equal numbers of sub-lists).
    """
    for max_ in range(min_, min_+max_diff+1):
        poss_parts = list(get_possible_partitions(lis_, min_, max_))
        if poss_parts:
            result = max(poss_parts, key=lambda x: len(x))
            assert flatten(result) == lis_
            return result, max(map(sum, result))
    else:
        raise ValueError(
            f"No possible partitions found for the list {lis_} with sub-list " + \
            f"sums between {min_} and {max_diff}. Try increasing max_diff."
        )


# ====================
def get_possible_partitions(remaining: list,
                            min_: int,
                            max_: int,
                            so_far: Optional[list] = None) -> Generator[List[list]]:
    """A recursive generator function to yield partitions of a list such
    that the sum of the integers in each sub-list is no less than min_,
    but the maximum sum of a integers in any sub-list is no greater than max_.

    Args:
      remaining (list):
        The list to partition. For recursive calls of the function, the list
        of elements that have yet to be placed in a sub list.
      min_ (int): 
        The minimum value for the sum of the integers in any of the
        sub-lists in a partition.
      max_ (int):
        The minimum value for the sum of the integers in any of the
        sub-lists in a partition.
      so_far (Optional[list], optional): The partition generated so far in
        this iteration. Defaults to None (for initial calls to the function).

    Yields:
      Generator[List[list]]:
        Partitions of the original list satisfying the requirements.
    """

    if so_far is None:
        so_far = []
    if sum(remaining) >= min_ and sum(remaining) <= max_:
        result = so_far + [remaining]
        yield result
    for i in range(len(remaining)):
        candidate = remaining[:i]
        if sum(candidate) < min_:
            continue
        elif sum(candidate) > max_:
            break
        else:
            remaining_ = remaining[i:]
            yield from get_possible_partitions(
                remaining_, min_, max_, so_far + [candidate]
            )


# ====================
def add_para_labels(df: pd.DataFrame,
                    col_label: str,
                    min_len: int,
                    max_diff: int = 100) -> pd.DataFrame:
    """Add paragraph labels to sentences in a pandas DataFrame such that
    each pseudo-paragraph contains at least min_len tokens but no more than
    max_diff+min_len tokens.

    Args:
      df (pd.DataFrame):
        A pandas DataFrame. Must contain a column named 'doc_idx' specifying
        to which document each sentence belongs.
      col_label (str):
        The name of the column on which to base token counts.
      min_len (int):
        The minimum token length of any pseudo-paragraph.
      max_diff (int, optional): 
        The maximum number of tokens by which a pseudo-paragraph may differ
        from min_len. Defaults to 100.

    Returns:
      pd.DataFrame:
        The original DataFrame with a new column named 'para_idx' appended.
    """    
    
    doc_idxs = set(df['doc_idx'].to_list())
    for doc_idx in doc_idxs:
        doc_df = df[df['doc_idx'] == doc_idx]
        sent_idxs = doc_df.index.to_list()
        token_counts = [num_tokens(df.iloc[sent_idx][col_label]) for sent_idx in sent_idxs]
        partition, _ = get_smallest_partition(token_counts, min_=min_len, max_diff=max_diff)
        for para_idx, sent_lengths in enumerate(partition):
            for _ in range(len(sent_lengths)):
                df.at[sent_idxs.pop(0), 'para_idx'] = para_idx
    return df


# ====================

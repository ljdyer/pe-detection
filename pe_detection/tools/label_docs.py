from typing import List, Tuple
import pandas as pd

# ====================
def get_sentence_numbers(path: str) -> List[Tuple[int, int]]:
    """Get document sentence numbers from a text file.

    Args:
      path (str):
        The path to the text file. Each line in the text file should begin
        with a pair of integers separated by a hyphen indicating the range of
        sentence numbers, followed by a colon.
        E.g. '514-599: https://shukepianblog.wordpress.com/'

    Returns:
      List[Tuple[int, int]]:
        A list of tuples of the form (first_sentence_index, last_sentence_index)
    """

    with open(path, 'r', encoding='utf-8') as f:
        file_lines = f.read().splitlines()
    line_numbers = [
        tuple([int(x) for x in line.split(':').split()])
        for line in file_lines
    ]


# ====================
def add_doc_labels(sents_df: pd.DataFrame, sent_numbers_path: str) -> pd.DataFrame:
    """Add document labels to a DataFrame based on information from a text file"""

    sentence_numbers = get_sentence_numbers(sent_numbers_path)
    labelled = sents_df.copy()
    for doc_idx, doc_lines in enumerate(sentence_numbers):
        first_line, last_line = doc_lines
        for i in range(first_line, last_line+1):
            labelled.at[i, 'doc_idx'] = int(doc_idx)
    return labelled
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
        tuple([int(x) for x in line.split(':')[0].split('-')])
        for line in file_lines
    ]
    return line_numbers


# ====================
def add_doc_labels(sents_df: pd.DataFrame, sent_numbers_path: str) -> pd.DataFrame:
    """Add document labels to a DataFrame based on information from a text file

    Args:
      sents_df (pd.DataFrame):
        A DataFrame in which each row contains a single sentence.
      sent_numbers_path (str):
        The path to the text file. Each line in the text file should begin
        with a pair of integers separated by a hyphen indicating the range of
        sentence numbers, followed by a colon.
        E.g. '514-599: https://shukepianblog.wordpress.com/'

    Returns:
      pd.DataFrame:
        The original DataFrame with an extra column, doc_idx containing an index
        uniquely identifying the document to which each sentence belongs.
    """

    sentence_numbers = get_sentence_numbers(sent_numbers_path)
    labelled = sents_df.copy()
    for doc_idx, doc_lines in enumerate(sentence_numbers):
        first_line, last_line = doc_lines
        for i in range(first_line, last_line+1):
            labelled.at[i, 'doc_idx'] = int(doc_idx)
    return labelled


# ====================
def show_doc_start_end(df: pd.DataFrame, col_label: str):
    """Show the entries of the col_label in the first and last rows
    with each doc_idx in a pandas DataFrame.

    Args:
      df (pd.DataFrame):
        The DataFrame. Must contain a column called 'doc_idx' containing
        document indices.
      src_col_label (str):
        The label of a column containing the source text
        (e.g. 'ted.en-fr.src.en.norm.tok')
    """

    doc_idxs = set(df['doc_idx'].to_list())
    row_dicts = []
    for doc_idx in doc_idxs:
        doc_df = df[df['doc_idx'] == doc_idx]
        row_dicts.append({
            'start': doc_df.iloc[0][col_label],
            'end': doc_df.iloc[-1][col_label]
        })
    display(pd.DataFrame(row_dicts))


# ====================
def add_role_labels(df: pd.DataFrame,
                    train_docs: List[int],
                    test_docs: List[int]) -> pd.DataFrame:

    doc_idxs = set(df['doc_idx'].to_list())
    assert doc_idxs == set(train_docs + test_docs)
    df['role'] = df['doc_idx'].apply(lambda x: 'train' if x in train_docs else 'test')
    return df
    
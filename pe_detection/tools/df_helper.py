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



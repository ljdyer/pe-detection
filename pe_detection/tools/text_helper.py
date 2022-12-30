import pandas as pd


# ====================
def num_tokens(doc: str) -> int:
    """Get the number of tokens in a document.
    Tokens are defined as sequences of non-space characters separated by spaces

    Args:
      doc (str):
        The document

    Returns:
      int:
        The number of tokens
    """    

    return len(doc.split())


# ====================
def alpha_part(str_: str) -> str:

    return ''.join([c for c in str_ if c.isalpha()])

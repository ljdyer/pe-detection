# ====================
def get_digits(string: str) -> str:
    """Get only the digits from a string

    Args:
      string (str):
        The input string (e.g. "Hello123xxx")

    Returns:
      str:
        Only the digits part of the string (e.g. "123")
    """    

    return ''.join([c for c in string if c.isdigit()])
import pandas as pd
from contextlib import contextmanager
from typing import List, Tuple


# ====================
@contextmanager
def pandas_options(options: List[Tuple]):

    before = [pd.get_option(option_name) for option_name, _ in options]
    for option in options:
        pd.set_option(*option)
    yield
    for option_idx, option in enumerate(options):
        pd.set_option(option[0], before[option_idx])


# ====================
@contextmanager
def show_all_rows():

    with pandas_options([('display.max_rows', None)]):
        yield

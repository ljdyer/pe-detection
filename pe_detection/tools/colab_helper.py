import os
import sys
from contextlib import contextmanager


# ====================
@contextmanager
def surpress_output():
    
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    yield
    sys.stdout.close()
    sys.stdout = original_stdout

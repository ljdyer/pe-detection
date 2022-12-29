import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import matplotlib.patches as mpatches
from math import floor, ceil
from numpy import linspace
from typing import Optional


# ====================
def token_counts_histogram(token_counts_df: pd.DataFrame,
                           ignore_cols: Optional[list] = None):
    """Display a histogram showing distribution of token counts for all
    columns in token counts DataFrame.

    Args:
      token_counts_df (pd.DataFrame):
        A DataFrame containing token counts.
      ignore_cols (Optional[list], optional):
        A list of columns to ignore. Defaults to None.
    """

    if ignore_cols is None:
        ignore_cols = []
    cividis = get_cmap('cividis')  
    token_counts_df = token_counts_df.drop(columns=ignore_cols)
    min_tokens = token_counts_df.min().min()
    max_tokens = token_counts_df.max().max()
    norm_cols = [col for col in token_counts_df.columns if 'norm.tok' not in col]
    norm_tok_cols = [col for col in token_counts_df.columns if 'norm.tok' in col]
    assert len(norm_tok_cols) + len(norm_cols) == len(token_counts_df.columns)
    norm_col_colors = [cividis(x) for x in linspace(0, 0.5, num=len(norm_cols), endpoint=False)]
    norm_tok_col_colors = [cividis(x) for x in linspace(0.5, 1, num=len(norm_tok_cols), endpoint=False)]
    col_colors = {col: color for col, color in list(zip(norm_cols, norm_col_colors)) + list(zip(norm_tok_cols, norm_tok_col_colors))}    
    bins = list(range(floor(min_tokens/10)*10, ceil(max_tokens/10)*10, 10))
    _, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 20))
    legend_patches = []
    for col in token_counts_df.columns:
        token_counts_df[col].hist(ax=axes[0], color=col_colors[col], bins=bins)
        legend_patches.append(mpatches.Patch(color=col_colors[col], label=col))
    axes[1].axis('off')
    axes[1].legend(handles=legend_patches, ncol=5)

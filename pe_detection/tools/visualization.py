from math import ceil, floor
from typing import Optional

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import get_cmap
from numpy import linspace


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


# ====================
def visualize_diffs(diffs_df: pd.DataFrame,
                    dim1: str,
                    dim2: str = None,
                    title: str = None):

    if dim2 is None:
        diffs_boxplot(diffs_df, dim1, title)
    else:
        diffs_scatter(diffs_df, dim1, dim2, title)


# ====================
def diffs_boxplot(diffs_df: pd.DataFrame,
                  dim1: str,
                  title: str = None):

    categories = set(diffs_df['y'].to_list())
    values = {}
    for c in categories:
        values[c] = diffs_df[diffs_df['y'] == 'ht'][dim1].to_list()
    _, ax = plt.subplots()
    if title is not None:
        ax.set_title(title)
    ax.set_xlabel(dim1)
    ax.set_ylabel('Mode')
    ax.set_xlim([0, 1])
    boxplot = ax.boxplot(
        list(categories.values()), labels=list(categories.keys()), vert=False
    )


# ====================
def diffs_scatter(diffs_df: pd.DataFrame,
                  dim1: str,
                  dim2: str,
                  title: str = None):

    pass

from urllib.parse import urljoin

import bs4
import pandas as pd
import requests
import html


# ====================
def get_github_dirlist(dir_url: str) -> dict:
    """Get a Python dictionary containing information about files and sub-directories
    in a directory of a GitHub repository.

    Args:
      dir_url (str): 
        The URL the GitHub repository directory
        (e.g. https://github.com/antot/posteditese_mtsummit19/tree/master/datasets/wit3)

    Returns:
      dict:    
        A dictionary whose keys are file/directory names, and values are either
        'DIR' for directories or the URL to the raw content for files.
        e.g.
            {
                'IWSLT15-HE-RELEASE/data/IWSLT15.TED.tst2015.MT_ende': 'DIR',
                'IWSLT16-HE-RELEASE': 'DIR',
                'ted.en-de.ht.de.norm': 
                    'https://raw.githubusercontent.com/.../wit3/ted.en-de.ht.de.norm',
                'ted.en-de.ht.de.norm.tok':
                    'https://raw.githubusercontent.com/.../ted.en-de.ht.de.norm.tok',
                'ted.en-de.nmt1.de.norm':
                    'https://raw.githubusercontent.com/.../ted.en-de.nmt1.de.norm',
                etc...
            }
    """
    
    page = requests.get(dir_url).text
    soup = bs4.BeautifulSoup(page, features='lxml')
    names = [a.text for a in soup.find_all("a", {"class": "js-navigation-open Link--primary"})]
    icons = soup.find_all("svg", attrs={"aria-label": ['File', 'Directory']})
    dir_or_file = [icon['aria-label'] for icon in icons]
    raw_file_root = (dir_url
        .replace('github.com', 'raw.githubusercontent.com')
        .replace('/tree', '')
    ) + '/'
    dirlist = {
        name: 'DIR' if dir_or_file == 'Directory' else urljoin(raw_file_root, name)
        for name, dir_or_file in zip(names, dir_or_file)}
    return dirlist


# ====================
def get_posteditese_mtsummit19_data(dataset: str) -> pd.DataFrame:
    """Get a pandas DataFrame combining all available data from files
    containing the specified tags for data in the datasets at
    https://github.com/antot/posteditese_mtsummit19/tree/master/datasets/

    Args:
      dataset (str):
        The dataset to access. One of 'MS', 'taraxu', or 'wit3'
      tags (list):
        A list of tags that should appear in file names (e.g. ['en-de', 'tok'] for all
        tokenized data for EN->DE

    Returns:
      pd.DataFrame:
        A pandas DataFrame with a row for each sentence and a column for each of the
        files in the dataset directory
    """

    if dataset.lower() not in ['MS', 'taraxu', 'wit3']:
        raise ValueError(
            "dataset should be one of 'MS', 'taraxu', or 'wit3', " + \
            f"not {dataset}."
        )
    dirlist = get_github_dirlist(urljoin(
        "https://github.com/antot/posteditese_mtsummit19/tree/master/datasets/",
        dataset
    ))
    files = {f: url for f, url in dirlist.items()}
    df = pd.DataFrame()
    len_ = -1
    for file, url in files:
        with open(url, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        if len_ == -1:
            len_ = len(lines)
        else:
            if len(lines) != len_:
                raise RuntimeError(
                    'Number of lines appears to differ between files. ' + \
                    f'The first file had {len_} lines, but {file} has ' + \
                    f'{len(lines)} lines.'
                )
        df[file] = pd.Series(lines)
    df.applymap(lambda x: html.unescape(x))
    return df

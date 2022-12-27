from urllib.parse import urljoin

import bs4
import pandas as pd
import requests


# ====================
def get_github_dir(dir_url: str) -> dict:
    """Get a Python dictionary containing information about files and sub-directories
    in a directory of a GitHub repo.

    Args:
      dir_url (str): 
        The URL the GitHub repository directory
        (e.g. https://github.com/antot/posteditese_mtsummit19/tree/master/datasets/wit3)

    Returns:
      dict:    
        A dictionary whose keys are file/directory names, and values are either
        'DIR' for directories or the URL to the raw content for files.
    """
    
    page = requests.get(dir_url).text
    soup = bs4.BeautifulSoup(page)
    names = [a.text for a in soup.find_all("a", {"class": "js-navigation-open Link--primary"})]
    icons = soup.find_all("svg", attrs={"aria-label": ['File', 'Directory']})
    dir_or_file = [icon['aria-label'] for icon in icons]
    raw_file_root = (dir_url
        .replace('github.com', 'raw.githubusercontent.com')
        .replace('/tree', '')
    )
    dirlist = {
        name: 'DIR' if dir_or_file == 'Directory' else urljoin(raw_file_root, name)
        for name, dir_or_file in zip(names, dir_or_file)}
    return dirlist


# def get_df_by_tags(required_tags: list, dirlist: dict) -> pd.DataFrame:
#     """Get a DataFrame combining available files for a given directory.

#     Required tags can be e.g. ['en-de', 'tok'] for the tokenized data for EN->DE
#     """

#     files = {f: url for f, url in iwslt_dir.items() if all([x in f for x in required_tags])}
#     # The third section of the filename differentiates the data ('ht', 'nmt1', etc.)
#     dfs = {f.split('.')[2]: pd.read_csv(url, sep='XXXXX', header=None) for f, url in files.items()}
#     df = pd.DataFrame()
#     for f, df_ in dfs.items():
#         df[f] = df_[0]
#     return df
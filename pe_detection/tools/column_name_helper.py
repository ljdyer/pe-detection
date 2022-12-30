import pandas as pd
from typing import Optional
from pe_detection.tools.text_helper import alpha_part


# ====================
def parse_columns(df: pd.DataFrame) -> dict:

    columns = [c for c in df.columns if c!= 'doc_idx']
    data = {}
    data['datasets'] = set([c.split('.')[0] for c in columns])
    data['language_pairs'] = set([c.split('.')[1] for c in columns])
    data['preprocessing_steps'] = set(['.'.join(c.split('.')[4:])
                                       for c in columns])
    data['translation_modes'] = {}
    for lp in data['language_pairs']:
        this_lp = [c for c in columns if lp in c]
        translation_modes = set([c.split('.')[2] for c in this_lp])
        types = set([alpha_part(c) for c in translation_modes])
        translation_modes_dict = {}
        for type_ in types:
            modes = [c for c in translation_modes if alpha_part(c) == type_]
            if len(modes) == 1:
                translation_modes_dict[type_] = modes[0]
            else:
                translation_modes_dict[type_] = sorted(modes)
        data['translation_modes'][lp] = translation_modes_dict
    return data


# ====================
def get_column_name(language_pair: str,
                    translation_mode: str,
                    preprocessing_steps: str,
                    dataset: str) -> pd.Series:

    source, target = language_pair.split('-')
    language = source if translation_mode == 'src' else target
    return f"{dataset}.{language_pair}.{translation_mode}.{language}.{preprocessing_steps}"

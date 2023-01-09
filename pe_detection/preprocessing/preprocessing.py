from typing import Optional, Union, List
import pandas as pd
import spacy


NLP = {}


# ====================
def text_col_to_pos(df: pd.DataFrame, pipeline: str, col_label_or_labels: Optional[Union[str, List[str]]] = 'x') -> str:

    if pipeline not in NLP:
        NLP[pipeline] = spacy.load(pipeline)
    if isinstance(col_label_or_labels, str):
        col_label_or_labels = [col_label_or_labels]
    for c in col_label_or_labels:
        df[c] = df[c].apply(lambda x: pos_tags(x, pipeline))
    return df


# ====================
def apply_pos_to_series(series: pd.Series, pipeline: str) -> pd.Series:

    if pipeline not in NLP:
        NLP[pipeline] = spacy.load(pipeline)
    texts = series.to_list()
    pos = [pos_tags(x, pipeline) for x in texts]
    return pd.Series(pos)


# ====================
def pos_tags(doc: str, pipeline: str) -> str:

    if pipeline not in NLP:
        NLP[pipeline] = spacy.load(pipeline)
    nlp = NLP[pipeline]
    doc_ = nlp(doc)
    if len([t.pos_ for t in doc_]) != len(doc.split()):
        print(doc)
        quit()
    return ' '.join([t.pos_ for t in doc_])

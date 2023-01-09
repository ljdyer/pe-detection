from typing import Optional, Union, List, Tuple
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
def apply_pos_to_series(series: pd.Series, pipeline: str) -> Tuple[pd.Series]:

    if pipeline not in NLP:
        NLP[pipeline] = spacy.load(pipeline)
    texts = series.to_list()
    new_pos = [pos_tags(x, pipeline) for x in texts]
    new = pd.Series(new for new, _ in new_pos)
    pos = pd.Series(pos for _, pos in new_pos)
    return new, pos


# ====================
def pos_tags(doc: str, pipeline: str) -> Tuple[str, str]:

    if pipeline not in NLP:
        NLP[pipeline] = spacy.load(pipeline)
    nlp = NLP[pipeline]
    doc_ = nlp(doc)
    doc_tok = [t for t in doc_]
    doc_pos = [t.pos_ for t in doc_]
    assert len(doc_tok) == len(doc_pos)
    return ' '.join(doc_tok), ' '.join(doc_pos)

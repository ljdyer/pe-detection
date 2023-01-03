from typing import Optional, Union, List
import pandas as pd
import spacy


# ====================
def text_col_to_pos(df: pd.DataFrame, pipeline: str, col_label_or_labels: Optional[Union[str, List[str]]] = 'x') -> str:

    if isinstance(col_label_or_labels, str):
        col_label_or_labels = [col_label_or_labels]
    for c in col_label_or_labels:
        df[col_label_or_labels] = df[col_label_or_labels].apply(lambda x: pos_tags(x, pipeline))
    

# ====================
def pos_tags(doc: str, pipeline: str) -> str:

    nlp = spacy.load(pipeline)
    doc_ = nlp(doc)
    return ' '.join([t.pos_ for t in doc_])

from typing import Optional, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


# ====================
def train_model(train_df: pd.DataFrame,
                x_label: Optional[str] = 'x',
                y_label: Optional[str] = 'y',
                ngram_range: Optional[Tuple[int, int]] = (1, 1)) -> Pipeline:

    text_clf = Pipeline([
        (
            'vect',
            CountVectorizer(
                strip_accents=False,
                lowercase=False,
                tokenizer=lambda text: text.split(),
                ngram_range=ngram_range
            )
        ),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])
    text_clf.fit(train_df[x_label], train_df[y_label])
    return text_clf


# ====================
def evaluate_model(model: Pipeline,
                   test_df: pd.DataFrame,
                   x_label: Optional[str] = 'x',
                   y_label: Optional[str] = 'y') -> float:

    y_true = test_df[y_label].to_list()
    y_pred = model.predict(test_df[x_label])
    return accuracy_score(y_true, y_pred)

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import pandas as pd


# ====================
def train_model(train_df: pd.DataFrame,
                x_label: str = 'x',
                y_label: str = 'y'):

    text_clf = Pipeline([
        (
            'vect',
            CountVectorizer(
                strip_accents=False,
                lowercase=False,
                tokenizer=lambda text: text.split(),
            )
        ),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])
    text_clf.fit(train_df[x_label], train_df[y_label])
    return text_clf



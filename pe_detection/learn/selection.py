import pandas as pd
from typing import List, Tuple
from sklearn.metrics import accuracy_score


# ====================
def get_single_best(metrics_df: pd.DataFrame,
                    metric='accuracy') -> Tuple[str, float]:
    """Given a DataFrame of metrics for multiple models and a metric
    to maximise, return the name of the model with the highest value
    for that metric, and the metric score for that model

    Args:
      metrics_df (pd.DataFrame):
        A DataFrame where each column label is the name of a model
        and each row label is the name of a metric.
      metric (str, optional):
        The metric to maximise. Defaults to 'accuracy'.

    Returns:
      Tuple[str, float]:
        The name of the model with the highest value
        for the metric, and the metric score for that model.
    """    

    return metrics_df.idxmax(metric), metrics_df[metric].max()


# ====================
def get_metrics_df(predictions_df: pd.DataFrame,
                   metrics: List[str] = ['accuracy']) -> pd.DataFrame:
    """Get a DataFrame with each metrics such as F-score and accuracy
    from a DataFrame of predictions for multiple classifiers.

    Args:
      predictions_df (pd.DataFrame):
        A DataFrame with a single column named 'y_true'. All other
        columns are names of classifier models.
      metrics (List[str], optional):
        A list of metrics to get. Defaults to ['accuracy'].

    Returns:
      pd.DataFrame: 
        The DataFrame of metrics.
    """

    model_predictions = predictions_df.drop(columns=['y_true'])
    y_true = predictions_df['y_true']
    metrics_df = pd.DataFrame()
    for model in model_predictions.columns:
        metrics_df.at[model, 'accuracy'] = \
            accuracy_score(y_true, model_predictions[model])
    return metrics_df

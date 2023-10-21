"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from gdp_time_series.pipelines import feature_pipeline,training_pipeline,prediction_pipeline

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    return {
        "__default__":
            feature_pipeline.create_pipeline() + training_pipeline.create_pipeline() +prediction_pipeline.create_pipeline()
    }

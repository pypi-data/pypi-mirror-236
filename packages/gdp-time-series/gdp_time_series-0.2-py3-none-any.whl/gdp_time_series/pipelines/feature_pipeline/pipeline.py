from kedro.pipeline import Pipeline, node, pipeline

from .nodes import column_preprocessing, dataframe_preprocessing, feature_engineering, feature_store

def create_pipeline(**kwargs)-> Pipeline:
    return pipeline([
        node(
            func=column_preprocessing,
            inputs= None,
            outputs="gdp_ts_cp",
            name = "column_preprocessing"
        ),
        node(
            func=dataframe_preprocessing,
            inputs="gdp_ts_cp",
            outputs="gdp_ts_pp",
            name="dataframe_preprocessing"
        ),
        node(
            func=feature_engineering,
            inputs="gdp_ts_pp",
            outputs='gdp_ts_fe',
            name="feature_engineering"
            
        ),
        node(
            func=feature_store,
            inputs="gdp_ts_fe",
            outputs=None,
            name="feature_store"
        )
    
    ])
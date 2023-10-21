from kedro.pipeline import Pipeline, node, pipeline

from .nodes import load_dataset_from_feature_store, train, model_to_feature_store

def create_pipeline(**kwargs)-> Pipeline:
    return pipeline([
        node(
            func=load_dataset_from_feature_store,
            inputs= None,
            outputs="gdp_from_fs",
            name = "load_feature_store"
        )
        ,
        node(
            func=train,
            inputs="gdp_from_fs",
            outputs="forecasts",
            name="training"
        ),
        node(
            func=model_to_feature_store,
            inputs="forecasts",
            outputs=None,
            name="model_feature_store"
            
        )
    
    ])


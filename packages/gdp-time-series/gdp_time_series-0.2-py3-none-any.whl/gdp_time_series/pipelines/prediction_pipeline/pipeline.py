from kedro.pipeline import Pipeline, node, pipeline

from .nodes import load_data_from_feature_store,load_model_and_predict,save_to_GCP

def create_pipeline(**kwargs)-> Pipeline:
    return pipeline([
        node(
            func=load_data_from_feature_store,
            inputs=None,
            outputs=['gdp_pred','gdp_pred_og'],
            name= 'full_load_feature_store'    
        ),
        node(
            func = load_model_and_predict,
            inputs= ['gdp_pred','gdp_pred_og'],
            outputs= ['df_forecasts','df_gdp']
        ),
        node(
            func = save_to_GCP,
            inputs= ['df_forecasts','df_gdp'],
            outputs= None,
            name= 'save_to_gcp'
        )
    
    ])
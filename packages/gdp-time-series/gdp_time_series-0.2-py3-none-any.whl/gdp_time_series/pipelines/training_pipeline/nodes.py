import pandas as pd
import numpy as np
import mlflow
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
import hopsworks
from .settings import SETTINGS
from .auxiliary_functions import process_data,Model_Definition
import joblib
import os


def load_dataset_from_feature_store():
    """Load features from feature store.

    Args:
        feature_view_version (int): feature store feature view version to load data from
        training_dataset_version (int): feature store training dataset version to load data from

    Returns:
        data loaded from the feature store as pandas dataframe.
    """

    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project=SETTINGS["FS_PROJECT_NAME"]
    )
    fs = project.get_feature_store()
    feature_view_version = 1
    training_dataset_version = 1
    
    feature_view = fs.get_feature_view(
            name="gdp_index_view", version=feature_view_version
        )
    data, _ = feature_view.get_training_data(
            training_dataset_version=training_dataset_version
        )
    df = process_data(data)
    
    return df
    
def train(df):
    
    dataset_ts = df.copy()
    dataset_ts = TimeSeries.from_group_dataframe(df=dataset_ts, 
                                             group_cols='Country',
                                             time_col='datetime', 
                                            value_cols='gdp_index')
    scaler = Scaler() 
    dataset_ts_scaled = scaler.fit_transform(dataset_ts)
    
    agent = Model_Definition()
    n_beats_model = agent.model
    
    n_beats_model.fit(dataset_ts_scaled)
    model_path = '/home/lcscrv/projetos/pessoais/gdp_time_series/gdp-time-series/data/06_models'
    n_beats_model.save(model_path + "/n_beats_model.pt")
    forecasts = n_beats_model.predict(n = 4,series = dataset_ts_scaled,verbose = True)
    forecasts = scaler.inverse_transform(forecasts)
    
    return forecasts

def model_to_feature_store(model):
    """Adds the best model artifact to the model registry."""

    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"],project= SETTINGS["FS_PROJECT_NAME"]
    )
    fs = project.get_feature_store()


    # Upload the model to the Hopsworks model registry.
    #model_dir="forecasting_model"
    #if os.path.isdir(model_dir) == False:
    #    os.mkdir(model_dir)

    #joblib.dump(model, model_dir + '/n_beats_forecasting_model.pkl')
    model_dir = '/home/lcscrv/projetos/pessoais/gdp_time_series/gdp-time-series/data/06_models'
    
    mr = project.get_model_registry()
    py_model = mr.torch.create_model("n_beats_forecasting_model")
    
    py_model.save(model_dir)

    return py_model.version
    
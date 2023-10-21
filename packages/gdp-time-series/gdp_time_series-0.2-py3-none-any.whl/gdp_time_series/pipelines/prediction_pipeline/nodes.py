from .settings import SETTINGS
import hopsworks
from darts.dataprocessing.transformers import Scaler
from .utils import prediction_process_data, load_model, get_bucket, write_blob_to, get_logger,timeseries_to_dataframe
from pathlib import Path
from darts.models import NBEATSModel

logger = get_logger(__name__)

def load_data_from_feature_store():
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
    logger.info("Successfully connected to the feature store.")

    logger.info("Loading data from feature store...")
    feature_view_version = 1
    training_dataset_version = 1
    
    
    feature_view = fs.get_feature_view(
            name="gdp_index_view", version=feature_view_version
        )
    data, _ = feature_view.get_training_data(
            training_dataset_version=training_dataset_version
        )
    logger.info("Successfully loaded data from feature store.")
    
    prediction_dataset,prediction_dataset_og = prediction_process_data(data)
    

    
    return prediction_dataset,prediction_dataset_og

def load_model_and_predict(prediction_dataset,prediction_dataset_og):
    
    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project=SETTINGS["FS_PROJECT_NAME"])
    
    logger.info("Loading model from model registry...")
    model_version = 1
    
    mr = project.get_model_registry()
    model_registry_reference = mr.get_model(name="n_beats_forecasting_model", version=model_version)
    model_dir = model_registry_reference.download()
    model_path = Path(model_dir) / "n_beats_model.pt"

    #model = load_model(model_path)
    model = NBEATSModel.load(str(model_path))
    logger.info("Successfully loaded model from model registry.")
    
    logger.info("Making predictions...")
    
    forecasts = model.predict(n = 4, series = prediction_dataset, verbose = True)
    scaler = Scaler()
    scaler.fit(prediction_dataset_og)
    
    forecasts = scaler.inverse_transform(forecasts)
    logger.info("Successfully made predictions.")
    
    df_forecasts = timeseries_to_dataframe(forecasts)
    df_gdp = timeseries_to_dataframe(scaler.inverse_transform(prediction_dataset))
    
    return df_forecasts,df_gdp

def save_to_GCP(df_forecasts,df_gdp):
    bucket = get_bucket()

    logger.info("Saving predictions...")
    # Save the input data and target data to the bucket.
    for df, blob_name in zip(
        [df_gdp, df_forecasts], ["gdp_ts.parquet", "predictions.parquet"]
    ):
        logger.info(f"Saving {blob_name} to bucket...")
        write_blob_to(
            bucket=bucket,
            blob_name=blob_name,
            data=df,
        )
        logger.info(f"Successfully saved {blob_name} to bucket.")
        
        logger.info("Successfully saved predictions.")

    
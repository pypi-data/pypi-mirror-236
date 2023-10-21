import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
import logging
from pathlib import Path
from typing import Optional,Union
from .settings import SETTINGS
import joblib
from google.cloud import storage

def prediction_process_data(df):
    process_df = df.copy()
    process_df = process_df.sort_values(by = 'year'); process_df['year'] = pd.to_datetime(process_df['year']).dt.strftime('%Y-%m-%d')
    process_df = process_df.set_index('year') ; process_df = process_df.drop('unique_id',axis = 1)
    
    wide_process_df = process_df.T
    wide_process_df['Country'] = wide_process_df.index ;wide_process_df = wide_process_df.reset_index()
    wide_process_df = wide_process_df.drop('index',axis = 1)
    wide_process_df.columns.name = None
    
    long_process_df = pd.melt(wide_process_df, id_vars='Country', value_vars= process_df.index, var_name='datetime', value_name='gdp_index')
    
    dataset_ts = long_process_df.copy()
    dataset_ts = TimeSeries.from_group_dataframe(df=dataset_ts, 
                                             group_cols='Country',
                                             time_col='datetime', 
                                            value_cols='gdp_index')
    scaler = Scaler() 
    dataset_ts_scaled = scaler.fit_transform(dataset_ts)
    
    
    return dataset_ts_scaled,dataset_ts

def timeseries_to_dataframe(ts_dataset):
    dataset_list = [dataset.pd_series() for dataset in ts_dataset]
    dataset_names = [dataset.static_covariates['Country'].iloc[0] for dataset in ts_dataset]
    
    data_dict = {dataset_names[i]:dataset_list[i].values for i in range(len(dataset_list))}
    
    return pd.DataFrame(data_dict,index = list(dataset_list[0].index))

def get_logger(name: str) -> logging.Logger:
    """
    Template for getting a logger.

    Args:
        name: Name of the logger.

    Returns: Logger.
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)

    return logger

def load_model(model_path: Union[str, Path]):
    """
    Template for loading a model.

    Args:
        model_path: Path to the model.

    Returns: Loaded model.
    """

    return joblib.load(model_path)

def get_bucket(
    bucket_name: str = SETTINGS["GOOGLE_CLOUD_BUCKET_NAME"],
    bucket_project: str = SETTINGS["GOOGLE_CLOUD_PROJECT"],
    json_credentials_path: str = SETTINGS[
        "GOOGLE_CLOUD_SERVICE_ACCOUNT_JSON_PATH"
    ],
) -> storage.Bucket:
    """Get a Google Cloud Storage bucket.

    This function returns a Google Cloud Storage bucket that can be used to upload and download
    files from Google Cloud Storage.

    Args:
        bucket_name : str
            The name of the bucket to connect to.
        bucket_project : str
            The name of the project in which the bucket resides.
        json_credentials_path : str
            Path to the JSON credentials file for your Google Cloud Project.

    Returns
        storage.Bucket
            A storage bucket that can be used to upload and download files from Google Cloud Storage.
    """

    storage_client = storage.Client.from_service_account_json(
        json_credentials_path=json_credentials_path,
        project=bucket_project,
    )
    bucket = storage_client.bucket(bucket_name=bucket_name)

    return bucket


def write_blob_to(bucket: storage.Bucket, blob_name: str, data: pd.DataFrame):
    """Write a dataframe to a GCS bucket as a parquet file.

    Args:
        bucket (google.cloud.storage.Bucket): The bucket to write to.
        blob_name (str): The name of the blob to write to. Must be a parquet file.
        data (pd.DataFrame): The dataframe to write to GCS.
    """

    blob = bucket.blob(blob_name=blob_name)
    with blob.open("wb") as f:
        data.to_parquet(f)


def read_blob_from(bucket: storage.Bucket, blob_name: str) -> Optional[pd.DataFrame]:
    """Reads a blob from a bucket and returns a dataframe.

    Args:
        bucket: The bucket to read from.
        blob_name: The name of the blob to read.

    Returns:
        A dataframe containing the data from the blob.
    """

    blob = bucket.blob(blob_name=blob_name)
    if not blob.exists():
        return None

    with blob.open("rb") as f:
        return pd.read_parquet(f)
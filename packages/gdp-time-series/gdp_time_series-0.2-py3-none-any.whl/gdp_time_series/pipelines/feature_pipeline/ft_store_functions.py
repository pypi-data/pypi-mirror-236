import hopsworks
from hsfs.feature_group import FeatureGroup
import hsfs
from .settings import SETTINGS
from .utils import get_logger,load_json,save_json
from datetime import datetime
from typing import Optional

logger = get_logger(__name__)


def feature_store_creation(data, feature_group_version) -> FeatureGroup:
    
    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project=SETTINGS["FS_PROJECT_NAME"]
    )
    feature_store = project.get_feature_store()

    # Create feature group.
    energy_feature_group = feature_store.get_or_create_feature_group(
        name="gdp_index_per_year",
        version=feature_group_version,
        description="GDP variation for the years of 1980 to 2023 for several countries, regions and economical groups",
        primary_key=["unique_id"],
        event_time="year",
        online_enabled=False,
    )
    # Upload data.
    energy_feature_group.insert(
        features=data,
        overwrite=False,
        write_options={
            "wait_for_job": True,
        },
    )
    # Update statistics.
    energy_feature_group.statistics_config = {
        "enabled": True,
        "histograms": True,
        "correlations": True,
    }
    energy_feature_group.update_statistics_config()
    energy_feature_group.compute_statistics()

    return energy_feature_group


def feature_view_training_create(
    feature_group_version: Optional[int] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
) -> dict:
    """Create a new feature view version and training dataset
    based on the given feature group version and start and end datetimes.
    Args:
        feature_group_version (Optional[int]): The version of the
            feature group. If None is provided, it will try to load it
            from the cached feature_pipeline_metadata.json file.
        start_datetime (Optional[datetime]): The start
            datetime of the training dataset that will be created.
            If None is provided, it will try to load it
            from the cached feature_pipeline_metadata.json file.
        end_datetime (Optional[datetime]): The end
            datetime of the training dataset that will be created.
              If None is provided, it will try to load it
            from the cached feature_pipeline_metadata.json file.
    Returns:
        dict: The feature group version.
    """

    if feature_group_version is None:
        feature_pipeline_metadata = load_json("feature_pipeline_metadata.json")
        feature_group_version = feature_pipeline_metadata["feature_group_version"]

    if start_datetime is None or end_datetime is None:
        feature_pipeline_metadata = load_json("feature_pipeline_metadata.json")
        start_datetime = datetime.strptime(
            feature_pipeline_metadata["export_datetime_utc_start"],
            feature_pipeline_metadata["datetime_format"],
        )
        end_datetime = datetime.strptime(
            feature_pipeline_metadata["export_datetime_utc_end"],
            feature_pipeline_metadata["datetime_format"],
        )

    project = hopsworks.login(
        api_key_value=SETTINGS["FS_API_KEY"], project=SETTINGS["FS_PROJECT_NAME"]
    )
    fs = project.get_feature_store()

    # Delete old feature views as the free tier only allows 100 feature views.
    # NOTE: Normally you would not want to delete feature views. We do it here just to stay in the free tier.
    try:
        feature_views = fs.get_feature_views(name="gdp_index_view")
    except hsfs.client.exceptions.RestAPIError:
        logger.info("No feature views found for gdp_index_view.")

        feature_views = []

    for feature_view in feature_views:
        try:
            feature_view.delete_all_training_datasets()
        except hsfs.client.exceptions.RestAPIError:
            logger.error(
                f"Failed to delete training datasets for feature view {feature_view.name} with version {feature_view.version}."
            )

        try:
            feature_view.delete()
        except hsfs.client.exceptions.RestAPIError:
            logger.error(
                f"Failed to delete feature view {feature_view.name} with version {feature_view.version}."
            )

    # Create feature view in the given feature group version.
    energy_consumption_fg = fs.get_feature_group(
        "gdp_index_per_year", version=feature_group_version
    )
    ds_query = energy_consumption_fg.select_all()
    feature_view = fs.create_feature_view(
        name="gdp_index_view",
        description="GDP variation for the years of 1980 to 2023 for several countries, regions and economical groups",
        query=ds_query,
        labels=[],
    )

    # Create training dataset.
    logger.info(
        f"Creating training dataset between {start_datetime} and {end_datetime}."
    )
    feature_view.create_training_data(
        description="GDP index training dataset",
        data_format="csv",
        start_time=start_datetime,
        end_time=end_datetime,
        write_options={"wait_for_job": True},
        coalesce=False,
    )

    # Save metadata.
    metadata = {
        "feature_view_version": feature_view.version,
        "training_dataset_version": 1,
    }
    save_json(
        metadata,
        file_name="feature_view_metadata.json",
    )

    return metadata


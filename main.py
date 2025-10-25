from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from NetworkSecurity.entity.aftifact_entity import DataIngestionArtifact
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Intiating data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Intiating data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

        

    except Exception as e:
        raise NetworkSecurityException(e, sys)
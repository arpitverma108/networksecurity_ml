import os
from dotenv import load_dotenv
import sys
import json
import certifi
import pymongo
import pandas as pd
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract:
    
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            logging.info("✅ MongoDB connection established successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            db = self.mongo_client[database]         # ✅ Correct way to get the database
            col = db[collection]                     # ✅ Correct way to get the collection
            col.insert_many(records)
            logging.info(f"✅ Inserted {len(records)} records into {database}.{collection}")
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "ARPITML"
    COLLECTION = "NETWORKSECURITYDATA"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(file_path=FILE_PATH)
    print(f"Total records extracted: {len(records)}")

    no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"✅ Successfully inserted {no_of_records} records into MongoDB.")

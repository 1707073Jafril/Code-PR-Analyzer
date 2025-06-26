import os
import sys
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class ProjectDatabaseHandler:
    def __init__(self):
        load_dotenv()
        self._setup_database()

    def _setup_database(self):
        """Set up the database client and pull request collection."""
        try:
            db_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
            self.db_client = MongoClient(db_uri)
            self.db_instance = self.db_client["pr_analysis_db"]
            self.pr_collection = self.db_instance["pr_analysis_collection"]
            logging.info(f"Database client connected to DB '{self.db_instance.name}'")
        except Exception as err:
            logging.critical(f"Database initialization failed: {err}")
            sys.exit(1) 
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_url = os.getenv('MONGO_DB_URL')

db_client = MongoClient(
    mongodb_url,
    # warning, do not use this on production
     tls=True,
     tlsAllowInvalidCertificates=True
)
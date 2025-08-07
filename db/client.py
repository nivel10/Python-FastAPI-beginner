import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

mongodb_url = os.getenv('MONGO_DB_URL')

db_client_server = MongoClient(
    mongodb_url,
    #region
    # # warning, do not use this on production
    # tls=True,
    # tlsAllowInvalidCertificates=True,
    # # warning, do not use this on production
    #endregion
     tlsCAFIle=certifi.where(),
).python_api
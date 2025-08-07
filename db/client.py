import os
from dotenv import load_dotenv
from pymongo import MongoClient
from db.models.mongo_db import MongoDB, MongoDB_urls, MongoDB_collections
import certifi

load_dotenv()

mongodb_urls: MongoDB_urls = MongoDB_urls(
    local=os.getenv('MONGO_DB_URL_LOCAL'),
    server=os.getenv('MONGO_DB_URL_SERVER')
) 

mongodb_collections: MongoDB_collections = MongoDB_collections(
    users='users'
)

mongodb_obj: MongoDB = MongoDB(
    urls=mongodb_urls,
    certifi=certifi.where(),
    db_name='python_api',
    collections=mongodb_collections,
)

#region
# mongodb_url = os.getenv('MONGO_DB_URL_SERVER')

# db_client_server = MongoClient(
#     mongodb_url,
#     #region
#     # # warning, do not use this on production
#     # tls=True,
#     # tlsAllowInvalidCertificates=True,
#     # # warning, do not use this on production
#     #endregion
#      tlsCAFIle=certifi.where(),
# ).python_api
#endregion

db_client_local = MongoClient(
    mongodb_obj.urls.server,
    tlsCAFIle=mongodb_obj.certifi,
)[mongodb_obj.db_name]

db_client_local = MongoClient(
    mongodb_obj.urls.local,
    # mongodb_obj.urls.server,
    # tlsCAFIle=mongodb_obj.certifi,
)[mongodb_obj.db_name]
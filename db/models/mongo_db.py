class MongoDB_urls():
    local: str
    server: str

    def __init__(self, local: str, server: str):
        self.local = local
        self.server = server

class MongoDB_collections():
    users: str

    def __init__(self, users: str):
        self.users = users

class MongoDB():
    urls: MongoDB_urls
    certifi: str
    db_name: str
    collections: MongoDB_collections

    def __init__(
            self, 
            urls: MongoDB_urls, 
            certifi: str, 
            db_name: str, 
            collections: MongoDB_collections
    ):
        self.certifi = certifi
        self.urls = urls
        self.db_name = db_name
        self.collections = collections
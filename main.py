from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ----------------------- routers
app.include_router(products.router_products)
app.include_router(users.router_users)
app.include_router(basic_auth_users.basic_auth_users_router)
app.include_router(jwt_auth_users.jwt_auth_users_router)
app.include_router(users_db.router_users_db)
app.mount('/static', StaticFiles(directory='static'), name='static')

# server run
## uvicor - uvicorn main:app --reload

# server url
## http://127.0.0.1:8000

# documentation
## swagger /docs
## Redoc /redoc

@app.get('/', tags=['main'])
async def get_rood():
    return {'greeting': 'Hello world...!!!'}

@app.get('/url', tags=['main'])
async def get_url():
    return {'url_cursor': 'https://chejconsultor.com.ve'}
from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ----------------------- routers
app.include_router(products.router_products)
app.include_router(users.router_users)
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
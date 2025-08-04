from fastapi import FastAPI
from routers import products, users

app = FastAPI()

# ----------------------- routers
app.include_router(products.router_products)
app.include_router(users.router_users)

# documentation
## swagger /docs
## Redoc /redoc


@app.get('/', tags=['main'])
async def get_rood():
    return {'greeting': 'Hello world...!!!'}

@app.get('/url', tags=['main'])
async def get_url():
    return {'url_cursor': 'https://chejconsultor.com.ve'}
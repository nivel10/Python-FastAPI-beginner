from fastapi import FastAPI

app = FastAPI()

# documentation
## swagger /docs
## Redoc /redoc

@app.get('/')
async def get_rood():
    return {'greeting': 'Hello world...!!!'}

@app.get('/url')
async def get_url():
    return {'url_cursor': 'https://chejconsultor.com.ve'}
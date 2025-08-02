from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def  read_rood():
    return {'greeting': 'Hello world...!!!'}
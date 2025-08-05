from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

ALGORITHM = 'HS256'

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='/login')

class User(BaseModel):
    user_name: str
    firts_name: str
    last_name: str
    email: str
    disbaled: bool

class UserDB(User):
    password: str

users_db: object = {
    'nikole': {
        'user_name': 'nikole',
        'name': 'Nikole',
        'last_name': 'Herrera',
        'email': 'nikole.herrera@gmail.com',
        'disabled': False,
        'password': '123456'
    },
    'carlos': {
        'user_name': 'carlos',
        'name': 'Carlos',
        'last_name': 'Herrera',
        'email': 'carlos.herrera@gmail.com',
        'disabled': True,
        'password': '123456'
    },
}

def search_user_db(user_name: str):
    if user_name in users_db:
        return users_db[user_name]
    
@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='user not found'
        )
    
    user: UserDB = search_user_db(user_name=form.username)
    if not user['password'] == form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user or password incorrect')
    
    return {'access_token': user['user_name'], 'token_type': 'bearer',}
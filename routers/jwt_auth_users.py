from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ACCESS_TOKEN_ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 60
ACCESS_TOTEN_KEY = '35852669a66715cbe7145ecb9d502e8b9cc86a0c400445fc4ff5bc39e969e27b'

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')
crypt = CryptContext(schemes=['bcrypt'])
 
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
        'password': '$2a$12$4rzUI.K8mERTsagSEFdFT.fgOoe09h1ckK0qEqlLyMeFdtWR7mSiS'
    },
    'carlos': {
        'user_name': 'carlos',
        'name': 'Carlos',
        'last_name': 'Herrera',
        'email': 'carlos.herrera@gmail.com',
        'disabled': True,
        'password': '$2a$12$FUDw2dx1xtaptGulMhqlPejkhmUBKdIyYMLqzIhaLBmRenm16Rxfe'
    },
}

# def search_user(user_name: str):
#     if user_name in users_db:
#         user: User = users_db[user_name]
#         return user

# def search_user_db(user_name: str):
#     if user_name in users_db:
#         return users_db[user_name]

def search_user_db(user_name: str):
    if user_name in users_db:
        return users_db[user_name]

def search_user(user_name: str):
    if user_name in users_db:
        user: User = users_db[user_name]
        return user

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Authentication credentials invalid',
                headers={'www-Authenticate': 'Bearer'}
    )
    try:
        token_decode = jwt.decode(
            token=token, 
            key=ACCESS_TOTEN_KEY, 
            algorithms=ACCESS_TOKEN_ALGORITHM,
        )

        user_name = token_decode.get('sub')
        if user_name == None:
            raise exception

        if not token_decode:
            raise exception
        
    except JWTError:
        raise exception
    
    user: User = search_user(user_name=user_name)
    return user

async def current_user(user: User = Depends(auth_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authentication credentials invalid',
            headers={'www-Authenticate': 'Bearer'}
        )
    
    if user['disabled']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user disabled')
    
    # return user_no_password
    user_not_password: User = {**user}
    user_not_password.pop('password', None)

    # return user
    return user_not_password

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='user not found'
        )
    
    user: UserDB = search_user_db(user_name=form.username) 
    user_password_verify = crypt.verify(form.password, user['password'])
    if not user_password_verify:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user or password incorrect')
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token_payloads: object = {
        'sub': user['user_name'],
        'exp': expire,
    }

    access_token = jwt.encode(
        claims=access_token_payloads,
        key=ACCESS_TOTEN_KEY,
        algorithm=ACCESS_TOKEN_ALGORITHM,
    )

    return {'access_token': access_token, 'token_type': 'bearer',}

@app.get('/users/me')
async def users_me(user: User = Depends(current_user)):
    return user

@app.get('/users')
async def users():
    return users_db
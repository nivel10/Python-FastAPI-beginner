from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

class User(BaseModel):
    user_name: str
    name: str
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

def search_user(user_name: str):
    if user_name in users_db:
        # # return UserDB(users_db[user_name])
        # return UserDB(**users_db[user_name])
        return users_db[user_name]

async def current_user(token: str = Depends(oauth2)):
    user: UserDB = search_user(user_name=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Authentication credentials invalid',
            headers={'www-Authenticate': 'Bearer'}
        )
    
    return user

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not valid')

    user: UserDB = search_user(user_name=form.username)
    if not user['password'] == form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user or password incorrect')
    
    return {'access_token': user['user_name'], 'token_type': 'bearer',}

@app.get('/users/me')
async def users_me(user: User = Depends(current_user)):
    return user
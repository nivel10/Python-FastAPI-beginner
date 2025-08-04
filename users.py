from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# documentation
## swagger /docs
## ReDoc /redoc

class User(BaseModel):
    id: int
    name: str
    last_name: str
    age: int

users: list[User] = []
users.append(User(id=1, name='Nikole', last_name='Smith', age=10))
users.append(User(id=2, name='Carlos', last_name='Hernandez', age=44))
users.append(User(id=3, name='Andres', last_name='Correa', age=25))

@app.get('/users/')
async def users_json():
    return users

@app.get('/users/{id}')
async def user_by_id(id: int):
    return search_user_by_id(id=id)
    
@app.get('/users_query/')
async def user_query(id: int):
    return search_user_by_id(id=id)

@app.post('/users/')
async def user_create(user: User):
    try:
        if type(search_user_by_id(id=user.id)) == User:
            return {'error': 'The user already exists'}
        else:
            users.append(user)
            return search_user_by_id(id=user.id)
    
    except:
        return {'error': 'creating user', 'data': user}

@app.put('/users/{id}')
async def user_update(user: User, id: int):
    try:
        if id != user.id:
            return {'error': 'id parameter is not same than id user propertie'}
        
        user_before: User = search_user_by_id(id=id)
        if type(user_before) != User:
            # return user_before
            return {'error': 'user not found'}
        
        for index, user_data in enumerate(users):
            if user_data.id == id:
                users[index] = user
                break
        
        return {'before': user_before, 'after': user}
    except Exception as ex:
        return {'error': 'updating user', 'data': user, 'ex': ex}

@app.delete('/users/{id}')
async def user_delete_by_id(id: int):
    try:
        user_found = False
        user: User = search_user_by_id(id=id)
        if type(user) != User:
            return {'error': 'user not found'}
        
        for index, user_data in enumerate(users):
            if user_data.id == id:
                user_found = True
                #region
                # users.pop(index)
                # users.remove(user)
                #endregion
                del users[index]
                break

        return {'before': user, } if user_found else {'error': 'user not found'}
    except Exception as ex:
        return {'error': 'deleting user', 'data': id, 'ex': ex, }

# ----------------------------------------
def search_user_by_id(id: int):
    try:
        users_find = filter(lambda user: user.id == id, users)
        return list(users_find)[0]
    except Exception as ex:
        return {'error': 'not found', 'data': id, 'ex': ex, }
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router_users = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'message': 'not found'}}
)

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

@router_users.get('/')
async def users_json():
    return users

@router_users.get('/{id}')
async def user_by_id(id: int):
    return search_user_by_id(id=id)
    
@router_users.get('_query/')
async def user_query(id: int):
    return search_user_by_id(id=id)

@router_users.post('/', response_model=User, status_code=201)
async def user_create(user: User):
    try:
        if type(search_user_by_id(id=user.id)) == User:
            # # return {'error': 'The user already exists'}
            # return HTTPException(status_code=204, detail='The user already exists')
            raise HTTPException(status_code=204, detail='The user already exists')
        else:
            users.append(user)
            return search_user_by_id(id=user.id)
    
    except Exception as ex:
        return {'error': 'creating user', 'data': user, 'ex': ex}

@router_users.put('/{id}')
async def user_update(user: User, id: int):
    try:
        if id != user.id:
            # return {'error': 'id parameter is not same than id user propertie'}
            # return HTTPException(status_code=204, detail='id parameter is not same than id user propertie')
            raise HTTPException(status_code=204, detail='id parameter is not same than id user propertie')
        
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

@router_users.delete('/{id}')
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
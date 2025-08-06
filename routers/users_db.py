from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client

router_users_db = APIRouter(
    prefix='/usersdb',
    tags=['usersdb'],
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'not found'}
    }
)

# documentation
## swagger /docs
## ReDoc /redoc

users: list[User] = []

@router_users_db.get('/', response_model=list[User])
async def users_json():
    users = db_client.python_api.users.find()
    return users_schema(users)

@router_users_db.get('/{id}')
async def user_by_id(id: str):
    return search_user_by_id(id=id)
    
@router_users_db.get('query/')
async def user_query(id: int):
    return search_user_by_id(id=id)

#@router_users_db.post('/', response_model=User, status_code=201)
@router_users_db.post('/', status_code=201)
async def user_create(user: User):
    try:
        if type(search_user_by_username(username=user.username)) == User:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, 
                detail='the username already exists'
            )
        
        if type(search_user_by_email(email=user.email)) == User:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail='the email already exists'
            )

        user_dict = dict(user)
        del user_dict['id']

        user_id = db_client.python_api.users.insert_one(user_dict).inserted_id
        user_find = user_schema(db_client.python_api.users.find_one({'_id': user_id}))
        user = User(**user_find)

        return user
    
    except Exception as ex:
        return {'error': 'creating user', 'data': user, 'ex': ex}

@router_users_db.put('/{id}')
async def user_update(user: User, id: int):
    try:
        if id != user.id:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, 
                detail='id parameter is not same than id user propertie'
            )
        
        user_before: User = search_user_by_id(id=id)
        if type(user_before) != User:
            return {'error': 'user not found'}
        
        for index, user_data in enumerate(users):
            if user_data.id == id:
                users[index] = user
                break
        
        return {'before': user_before, 'after': user}
    except Exception as ex:
        return {'error': 'updating user', 'data': user, 'ex': ex}

@router_users_db.delete('/{id}')
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
def search_user_by_id(id: str):
    try:
        print(id)
        user_find = db_client.python_api.users.find_one({'_id': id})
        print(user_find)
        user_find = user_schema(user_find)
        print(user_find)
        user = User(**user_find)
        return user
    except Exception as ex:
        return {'error': 'not found', 'data': id, 'ex': ex, }
    
def search_user_by_username(username: str):
    try:
        user_find = db_client.python_api.users.find_one({'username': username})
        user_find = user_schema(user_find)
        user = User(**user_find)
        return user
    except Exception as ex:
        return { 'error': 'search user by username', 'ex': ex, }
    
def search_user_by_email(email: str):
    try:
        user_find = db_client.python_api.users.find_one({'email': email})
        user_find = user_schema(user_find)
        user = User(**user_find)
        return user
    except Exception as ex:
        return { 'error': 'search user by email', 'ex': ex, }
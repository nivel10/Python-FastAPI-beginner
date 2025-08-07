from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

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
    # return search_user_by_id(id=id)
    return search_user(key='_id', value=ObjectId(id))
    
@router_users_db.get('/query/')
async def user_query(id: str):
    # return search_user_by_id(id=id)
    return search_user(key='_id', value=ObjectId(id))

#@router_users_db.post('/', response_model=User, status_code=201)
@router_users_db.post('/', status_code=201)
async def user_create(user: User):
    try:
        # if type(search_user_by_username(username=user.username)) == User:
        if type(search_user(key='username', value=user.username)) == User:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, 
                detail='the username already exists'
            )
        
        # if type(search_user_by_email(email=user.email)) == User:
        if type(search_user(key='email', value=user.email)) == User:
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
async def user_delete_by_id(id: str):
    try:
        user: User = search_user(key='_id', value=ObjectId(id))
        if type(user) != User:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found'
            )
        
        db_client.python_api.users.delete_one({'_id': ObjectId(id)})
        return {'before': user, }
    except Exception as ex:
        return {'error': 'deleting user', 'data': id, 'ex': ex, }

# ----------------------------------------
def search_user(key: str, value: str | ObjectId):
    try:
        user_find = db_client.python_api.users.find_one({key: value})
        user_find = user_schema(user_find)
        user = User(**user_find)

        return user
    except Exception as ex:
        return {'error': 'serach user', 'ex': ex, }
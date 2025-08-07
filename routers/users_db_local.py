from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client_local, mongodb_collections
from bson import ObjectId
from pymongo import ReturnDocument
from db.models.mongo_db import MongoDB_collections

router_users_db_local = APIRouter(
    prefix='/usersdb_local',
    tags=['usersdb'],
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'not found'}
    }
)

# documentation
## swagger /docs
## ReDoc /redoc

users: list[User] = []
db_collections: MongoDB_collections = mongodb_collections

@router_users_db_local.get('/', response_model=list[User])
async def users_json():
    # users = db_client_server[db_collections.users].find()
    users = db_client_local[db_collections.users].find()
    return users_schema(users)

@router_users_db_local.get('/{id}')
async def user_by_id(id: str):
    # return search_user_by_id(id=id)
    return search_user(key='_id', value=ObjectId(id))
    
@router_users_db_local.get('/query/')
async def user_query(id: str):
    # return search_user_by_id(id=id)
    return search_user(key='_id', value=ObjectId(id))

## @router_users_db.post('/', response_model=User, status_code=201)
@router_users_db_local.post('/', status_code=201)
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

        user_id = db_client_local[db_collections.users].insert_one(user_dict).inserted_id
        user_find = user_schema(db_client_local[db_collections.users].find_one({'_id': user_id}))
        user = User(**user_find)

        return user
    
    except Exception as ex:
        return {'error': 'creating user', 'data': user, 'ex': ex}

#@router_users_db.put('/{id}', response_model=User)
@router_users_db_local.put('/{id}')
async def user_update(user: User, id: str):
    try:
        user_before: User = search_user(key='_id', value=ObjectId(id))
        if type(user_before) != User:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found'
            )
        
        user_dict = dict(user)
        del user_dict['id']
        
        if user_dict.get('username'):
            user_find = search_user(key='username', value=user.username)
            if type(user_find) == User:
                if not user_find.id == user_before.id:
                    raise HTTPException(
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail='the username is assigned to another user'
                    )
        
        if user_dict.get('email'):
            user_find = search_user(key='email', value=user.email)
            if type(user_find) == User:
                if not user_find.id == user_before.id:
                    raise HTTPException(
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail='the email is assigned to another user'
                    )
    
        user_after = db_client_local[db_collections.users].find_one_and_replace(
            {'_id': ObjectId(id) },
            user_dict,
            return_document=ReturnDocument.AFTER
        )
        
        return {'before': dict(user_before), 'after': user_schema(user_after)}
    except Exception as ex:
        return {'error': 'updating user', 'data': user, 'ex': ex}

@router_users_db_local.delete('/{id}')
async def user_delete_by_id(id: str):
    try:
        user = db_client_local[db_collections.users].find_one_and_delete({'_id': ObjectId(id)})
        if user == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found'
            )
        
        return {'before': user_schema(user), }
    except Exception as ex:
        return {'error': 'deleting user', 'data': id, 'ex': ex, }

# ----------------------------------------
def search_user(key: str, value: str | ObjectId):
    try:
        user_find = db_client_local[db_collections.users].find_one({key: value})
        
        if not user_find == None:
            user_find = user_schema(user_find)
            user = User(**user_find)
            return user
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    except Exception as ex:
        return {
            'error': 'search user', 
            'data': {
                'key': key, 
                'value': str(value) if type(value) == ObjectId else value 
                }, 
            'ex': ex, 
        }
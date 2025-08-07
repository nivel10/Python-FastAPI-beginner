from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from pymongo import ReturnDocument

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

        print(id)
        print(user)
        print({'$set': user_dict})
        print(ObjectId(id))
        return
    
        user_updated = db_client.python_api.users.find_one_and_update(
            {'_id': ObjectId(id) },
            {'$set': user_dict},
            return_document=ReturnDocument.AFTER
        )

        print(user_updated)
        
        return {'before': user_before, 'after': user_updated}
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
        
        if not user_find == None:
            user_find = user_schema(user_find)
            user = User(**user_find)
            return user
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    except Exception as ex:
        return {'error': 'search user', 'ex': ex, }
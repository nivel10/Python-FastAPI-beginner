from fastapi import APIRouter, HTTPException, status
from db.models.user import User

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

@router_users_db.get('/')
async def users_json():
    return users

@router_users_db.get('/{id}')
async def user_by_id(id: int):
    return search_user_by_id(id=id)
    
@router_users_db.get('query/')
async def user_query(id: int):
    return search_user_by_id(id=id)

@router_users_db.post('/', response_model=User, status_code=201)
async def user_create(user: User):
    try:
        if type(search_user_by_id(id=user.id)) == User:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, 
                detail='The user already exists'
            )
        else:
            users.append(user)
            return search_user_by_id(id=user.id)
    
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
def search_user_by_id(id: int):
    try:
        users_find = filter(lambda user: user.id == id, users)
        return list(users_find)[0]
    except Exception as ex:
        return {'error': 'not found', 'data': id, 'ex': ex, }
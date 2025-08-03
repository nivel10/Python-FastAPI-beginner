from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    last_name: str
    age: int

# users: list[User] = [User(name='Nikole', last_name='Herrera', age=10)]
users: list[User] = []
users.append(User(id=1, name='Nikole', last_name='Smith', age=10))
users.append(User(id=2, name='Carlos', last_name='Hernandez', age=44))
users.append(User(id=3, name='Andres', last_name='Correa', age=25))

@app.get('/users')
def users_json():
    # return [
    #     {'message': 'Hello users', "name": 'Carlos'},
    #     {'message': 'Hello users', 'name': 'Nikole'},
    # ]
    return users

@app.get('/users/{id}')
def user_by_id(id: int):
    # try:
    #     users_find = filter(lambda user: user.id == id, users)
    #     return list(users_find)[0]
    # except:
    #     return {'error': 'not found'}
    return search_user_by_id(id=id)
    
@app.get('/user_query/')
def user_query(id: int):
    # try:
    #     users_find = filter(lambda user: user.id == id, users)
    #     return list(users_find)[0]
    # except:
    #     return {'error': 'not found'}
    return search_user_by_id(id=id)
    
def search_user_by_id(id: int):
    try:
        users_find = filter(lambda user: user.id == id, users)
        return list(users_find)[0]
    except:
        return {'error': 'not found'}
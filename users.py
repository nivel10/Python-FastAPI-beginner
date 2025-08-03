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
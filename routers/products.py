from fastapi import APIRouter
from pydantic import BaseModel

router_products = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'message': 'not found'}}
)

# documentation
## swagger /docs
## Redoc / redoc

class Product(BaseModel):
    id: int
    description: str
    price: float

# products = list[str] = ['product 1', 'product 2', 'product 3', 'product 4', 'product 5']
products: list[Product] = []
products.append(Product(id=1, description='Product 1', price=10.45))
products.append(Product(id=2, description='Product 2', price=98.87))
products.append(Product(id=3, description='Product 3', price=254.23))
products.append(Product(id=4, description='Product 4', price=45.00))
products.append(Product(id=5, description='Product 5', price=2014.12))

@router_products.get('/')
async def products_get():
    try:
        return products
    except Exception as ex:
        return {'error': 'proucts get all', 'ex': ex}

@router_products.get('/{id}')
async def product_by_id(id: int):
    try:
        return products_by_id(id=id)
    except:
        return {'error': 'product not found', 'data': id}

# -------------------------------------
def products_by_id(id=id):
    try:
        products_found = filter(lambda product: product.id == id, products)
        return list(products_found)[0]
    except:
        return {'error': 'product not found', 'data': id, }
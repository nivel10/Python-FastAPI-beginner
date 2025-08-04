from fastapi import APIRouter

router_products = APIRouter()

# documentation
## swagger /docs
## Redoc / redoc

@router_products.get('/products')
async def products_get():
    try:
        products: list[str] = ['product 1', 'product 2', 'product 3', 'product 4', 'product 5']
        return products
    except Exception as ex:
        return {'error': 'proucts get all', 'ex': ex}
from datetime import datetime, timezone
from .schemas import ProductOut

PRODUCTS: list[ProductOut] = []
NEXT_ID = 1

def list_products():
    return PRODUCTS

def create_product(data, admin_email: str):
    global NEXT_ID
    product = ProductOut(
        id=NEXT_ID,
        codigo=data.codigo,
        nome=data.nome,
        preco=data.preco,
        status=data.status,
        data_cadastro=datetime.now(timezone.utc),
        email_admin=admin_email,
    )
    PRODUCTS.append(product)
    NEXT_ID += 1
    return product

def delete_product(product_id: int):
    global PRODUCTS
    before = len(PRODUCTS)
    PRODUCTS = [p for p in PRODUCTS if p.id != product_id]
    return len(PRODUCTS) != before
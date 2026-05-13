from fastapi import FastAPI, Depends
from .schemas import ProductCreate, ProductOut
from .auth import require_permission
from .store import list_products, create_product, delete_product

app = FastAPI(title="E-commerce Products API")

@app.get("/products", response_model=list[ProductOut])
def get_products(claims=Depends(require_permission("products:read"))):
    return list_products()

@app.post("/products", response_model=ProductOut, status_code=201)
def post_product(
    payload: ProductCreate,
    claims=Depends(require_permission("products:create")),
):
    admin_email = claims.get("email", "admin@unknown.com")
    return create_product(payload, admin_email)

@app.delete("/products/{product_id}", status_code=204)
def remove_product(
    product_id: int,
    claims=Depends(require_permission("products:delete")),
):
    deleted = delete_product(product_id)
    if not deleted:
        return {"detail": "Produto não encontrado"}
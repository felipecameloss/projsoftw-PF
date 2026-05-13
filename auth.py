import os
import requests
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
ALGORITHMS = ["RS256"]

bearer_scheme = HTTPBearer(auto_error=True)

def _get_signing_key(token: str):
    unverified_header = jwt.get_unverified_header(token)
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url, timeout=5).json()

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return key

    raise HTTPException(status_code=401, detail="Chave pública não encontrada")

def get_current_claims(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials

    try:
        key = _get_signing_key(token)
        claims = jwt.decode(
            token,
            key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        return claims
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_permission(permission: str):
    def checker(claims=Depends(get_current_claims)):
        permissions = claims.get("permissions", [])
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente",
            )
        return claims
    return checker
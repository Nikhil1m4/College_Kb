from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, PyJWKClient, PyJWKClientError
from pydantic import BaseModel

from api.core.profiles import ProfileStore, get_profile_store
from api.core.settings import get_settings


class CurrentUser(BaseModel):
    id: str
    email: str
    role: str

security = HTTPBearer(auto_error=False)

def get_jwks_client() -> PyJWKClient:
    settings = get_settings()
    jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"
    # PyJWKClient caches keys in memory by default.
    return PyJWKClient(jwks_url)

def verify_token(token: str, key_override: Optional[str] = None) -> dict:
    try:
        if key_override:
            key = key_override
        else:
            client = get_jwks_client()
            signing_key = client.get_signing_key_from_jwt(token)
            key = signing_key.key

        settings = get_settings()
        issuer = f"{settings.supabase_url}/auth/v1"
        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience="authenticated",
            issuer=issuer,
            options={"require": ["exp", "aud", "iss"]}
        )
        return claims
    except (PyJWKClientError, InvalidTokenError) as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

async def get_current_user(
    request: Request,
    creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
    store: Annotated[ProfileStore, Depends(get_profile_store)]
) -> CurrentUser:
    if not creds:
        raise HTTPException(
            status_code=401,
            detail="Missing or malformed authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    key_override = getattr(request.app.state, "jwt_key", None)
    claims = verify_token(creds.credentials, key_override=key_override)
    
    user_id = claims.get("sub")
    email = claims.get("email") or ""
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"}
        )

    role = await store.get_role(user_id)
    if not role:
        raise HTTPException(status_code=403, detail="Profile not found")
        
    return CurrentUser(id=user_id, email=email, role=role)

async def require_admin(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

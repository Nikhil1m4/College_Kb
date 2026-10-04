from typing import Annotated

from fastapi import APIRouter, Depends

from api.core.auth import CurrentUser, get_current_user, require_admin

router = APIRouter()

@router.get("/api/me")
async def get_me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    """Return the currently authenticated user's profile."""
    return user

@router.get("/api/admin/ping")
async def admin_ping(user: Annotated[CurrentUser, Depends(require_admin)]) -> dict:
    """Admin-only ping endpoint."""
    return {"ok": True, "role": user.role}

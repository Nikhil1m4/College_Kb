from typing import Optional, Protocol

import httpx
from fastapi import Request

from api.core.settings import get_settings


class ProfileStore(Protocol):
    async def get_role(self, user_id: str) -> Optional[str]: ...

class SupabaseProfileStore:
    def __init__(self, supabase_url: str, service_role_key: str):
        self.url = f"{supabase_url}/rest/v1/profiles"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Profile": "public",
            "Accept": "application/json"
        }

    async def get_role(self, user_id: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}?id=eq.{user_id}&select=role",
                headers=self.headers
            )
            if response.status_code != 200:
                return None
            data = response.json()
            if not data:
                return None
            return data[0].get("role")

class FakeProfileStore:
    def __init__(self, profiles: dict[str, str]):
        self.profiles = profiles

    async def get_role(self, user_id: str) -> Optional[str]:
        return self.profiles.get(user_id)

def get_profile_store(request: Request) -> ProfileStore:
    settings = get_settings()
    return SupabaseProfileStore(settings.supabase_url, settings.supabase_service_role_key)

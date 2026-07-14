import httpx

from app.core.config import settings


async def get_jwks():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.SUPABASE_JWKS_URL
        )

        response.raise_for_status()

        return response.json()
import os
from fastapi import Request, HTTPException
from retell import Retell
from app.core.config import settings

# Initialize Retell client only if key is available
retell_client = Retell(api_key=settings.RETELL_API_KEY) if settings.RETELL_API_KEY else None

async def verify_retell_request(request: Request) -> dict:
    if not retell_client:
        # In case it's local test without env var, or just log
        if settings.ENV != "production":
            return await request.json()
        raise HTTPException(status_code=500, detail="Retell client not configured")

    raw_body = await request.body()
    signature = request.headers.get("X-Retell-Signature", "")
    
    if not retell_client.verify(
        raw_body.decode("utf-8"),
        api_key=settings.RETELL_API_KEY,
        signature=signature,
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    return await request.json()

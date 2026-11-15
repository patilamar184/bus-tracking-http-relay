
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Bus Tracking HTTP Relay")
BACKEND_URL = os.getenv("BACKEND_URL").rstrip("/")

if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL is missing from .env")


@app.get("/")
def home():
    return {"status": "Relay server running"}


@app.post("/api/device/{endpoint}")
async def device_proxy(endpoint: str, request: Request):

    if endpoint not in ["heartbeat", "location"]:
        raise HTTPException(
            status_code=404,
            detail="Device endpoint not found"
        )

    body = await request.body()

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": request.headers.get("X-API-Key", "")
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            result = await client.post(
                f"{BACKEND_URL}/api/device/{endpoint}",
                content=body,
                headers=headers
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Backend connection failed: {str(e)}"
            )

    print(
        f"Backend response [{endpoint}]:",
        result.status_code,
        result.text
    )

    return Response(
        content=result.content,
        status_code=result.status_code,
        media_type=result.headers.get(
            "content-type", "application/json"
        )
    )

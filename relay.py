
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Bus Tracking HTTP Relay")

@app.get("/")
def home():
    return {"status": "Relay server running"}

@app.post("/api/device/heartbeat")
async def heartbeat(request: Request):
    data = await request.json()

    print("Heartbeat received:", data)

    return JSONResponse({
        "status": "received",
        "device_id": data.get("device_id")
    })

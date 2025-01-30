from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

counters = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counters[websocket.client] = 1

    try:
        while True:
            message = await websocket.receive_text()
            current_number = counters[websocket.client]
            
            await websocket.send_json({
                "number": current_number,
                "text": message
            })
            
            counters[websocket.client] += 1

    except Exception:
        del counters[websocket.client]
        await websocket.close()
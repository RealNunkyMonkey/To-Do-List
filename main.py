from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def create_couter(count):
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_number = create_couter(0)

    try:
        while True:
            message = await websocket.receive_text()
            
            await websocket.send_json({
                "number": current_number(),
                "text": message
            })

    except Exception:
        await websocket.close()

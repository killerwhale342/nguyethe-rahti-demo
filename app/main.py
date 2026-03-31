from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
# origins = ["http://localhost:5500"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_name = "Kiet"

@app.get("/")
def read_root():
    return { "msg": f"testing" }

@app.get("/hello")
def read_root():
    return { "msg": f"Hello {my_name}" }

@app.get("/api/ip", response_class=HTMLResponse)
def read_items(request: Request):
    public_ip = request.client.host
    return f"""
    <html>
        <body>
            <h1>Your public IP is {public_ip}</h1>
        </body>
    </html>
    """

@app.get("/api/rawip")
def read_items(request: Request):
    public_raw_ip = request.client.host
    return {"ip":f"{public_raw_ip}"}

@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

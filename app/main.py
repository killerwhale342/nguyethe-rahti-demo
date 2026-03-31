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

#code challenge 1
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

#code challenge 2
rooms = [{"Number": 101, "Available": "Yes"}, {"Number": 102, "Available": "Yes"}, {"Number": 103, "Available": "No"}, {"Number": 104, "Available": "No"}, {"Number": 105, "Available": "No"}, {"Number": 106, "Available": "Yes"}]
@app.get("/rooms")
def hotel_rooms():
    results = []
    for room in rooms:
        if room["Available"] == "Yes":
            results.append(room)
    return results

@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

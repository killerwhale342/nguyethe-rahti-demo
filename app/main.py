from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, create_schema

#origin
app = FastAPI()
origins = ["*"] #accept all origins
#origins = ["http://localhost:5500"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
create_schema()

#in-class
my_name = "Kiet"
@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version()")
        result = cur.fetchone() #fetch one row as dictionary
    return {"msg": f"testing", "db_status":result}
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
rooms = [
    {"Number": 101, "Available": "Yes", "Room_types": "single_room", "price": 30},
    {"Number": 102, "Available": "Yes", "Room_types": "double_room", "price": 60},
    {"Number": 103, "Available": "No", "Room_types": "double_room", "price": 60},
    {"Number": 104, "Available": "No", "Room_types": "double_room", "price": 60},
    {"Number": 105, "Available": "No", "Room_types": "single_room", "price": 30},
    {"Number": 106, "Available": "Yes", "Room_types": "single_room", "price": 30}
]
@app.get("/rooms") #only accept get request
def get_hotel_rooms():
    results = []
    for room in rooms:
        if room["Available"] == "Yes":
            results.append(room)
    return results
@app.get("/hotel")
def get_hotel():
    return rooms
@app.post("/bookings") #only accept post request
def create_booking():
    return {"msg":"Booking created!"}




@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

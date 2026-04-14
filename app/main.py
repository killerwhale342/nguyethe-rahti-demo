from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from app.db import get_conn, create_schema

#origin
app = FastAPI()
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]
#origin = ["http://localhost:5500"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
create_schema()
#data model for booking
class Booking(BaseModel):
    guest_id:int
    room_id:int
    date_from:date
    date_to:date
class Guest(BaseModel):
    first_name: str
    last_name: str

#in-class 1
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
#in-class 2
@app.get("/if/{term}")
def if_test(term:str): #not necessary but a good practice to define a variable
    msg = "Default msg"
    if term == "hello": #parentheses "( )" are not necessary but can be used if the conditions are on next line or combining conditions (and, or)
        msg = "Hello yourself!" #indentation is important because it defines the block
    elif term == "hej" or term == "moi" and 1 == 0: 
        msg = "Hejsan"
    else:
        msg = f"I dont understand {term}"
    return{"msg":msg}

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
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM rooms")
        rooms = cur.fetchall()
    return rooms
@app.post("/bookings") #only accept post request
def create_booking(booking:Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (
                room_id,
                guest_id,
                date_from,
                date_to
            ) VALUES (%s,%s,%s,%s) RETURNING *
        """, [
            booking.room_id, 
            booking.guest_id, 
            booking.date_from, 
            booking.date_to
        ])
        new_booking = cur.fetchone()
    return {"msg":"Booking created!", "id": new_booking['id'], "room_id": new_booking['room_id']}
@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 
                hb.id,
                hb.date_from,
                hb.date_to,
                r.room_number,
                hg.id AS guest_id,
                hg.first_name,
                hg.last_name
            FROM hotel_bookings hb
            JOIN rooms r ON r.id = hb.room_id
            JOIN hotel_guests hg ON hg.id = hb.guest_id
            ORDER BY hb.date_from DESC
        """)
        bookings = cur.fetchall()
    return bookings
@app.post("/guests")
def create_guest(guest: Guest):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_guests (first_name, last_name, address)
            VALUES (%s, %s, %s)
            RETURNING id
        """, [
            guest.first_name,
            guest.last_name,
            "N/A"
        ])
        new_guest = cur.fetchone()
    return {"id": new_guest["id"]}

@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

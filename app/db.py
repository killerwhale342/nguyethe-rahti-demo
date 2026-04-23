import os, psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)
def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        # Create the schema
        cur.execute("""
            CREATE EXTENSION IF NOT EXISTS pgcrypto;
            ----------
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                created_at TIMESTAMP DEFAULT now()
            );
            --multi query need to be seperated by semi-colom
            --add columns
            ALTER TABLE rooms ADD COLUMN IF NOT EXISTS room_type VARCHAR;
            ALTER TABLE rooms ADD COLUMN IF NOT EXISTS price NUMERIC(10, 2);
            ----------
            --code challenge 4
            CREATE TABLE IF NOT EXISTS hotel_guests (
                id SERIAL PRIMARY KEY,
                guest_id INT NOT NULL,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                address VARCHAR NOT NULL,
                other_info VARCHAR
            );
            CREATE TABLE IF NOT EXISTS hotel_bookings (
                id SERIAL PRIMARY KEY,
                guest_id INT REFERENCES hotel_guests(id) NOT NULL,
                room_id INT REFERENCES rooms(id) NOT NULL,
                date_from DATE NOT NULL,
                date_to DATE NOT NULL,
                other_info VARCHAR
            );
            ----------
            ALTER TABLE hotel_guests ADD COLUMN IF NOT EXISTS api_key VARCHAR DEFAULT encode(gen_random_bytes(32), 'hex');
            ALTER TABLE hotel_bookings ADD COLUMN IF NOT EXISTS stars INT;
        """)
        print("DB schema created") #checkpoint for error
        cur.execute("DROP VIEW IF EXISTS bookings_view;")
        cur.execute("""
            CREATE VIEW bookings_view AS
                SELECT 
                    hb.id,
                    hb.date_from,
                    hb.date_to,
                    (date_to - date_from) AS nights,
                    r.room_number,
                    hg.id AS guest_id,
                    hg.first_name,
                    hg.last_name,
                    (date_to - date_from) * r.price AS total_price,
                    hb.stars,
                    hb.other_info
                FROM hotel_bookings hb
                INNER JOIN rooms r ON r.id = hb.room_id
                INNER JOIN hotel_guests hg ON hg.id = hb.guest_id;
        """)
        print("Booking View created") #checkpoint for error
        cur.execute("DROP VIEW IF EXISTS guests_view;")
        cur.execute("""
            CREATE VIEW guests_view AS
                SELECT 
                    hg.id,
                    hg.first_name,
                    hg.last_name,
                    (SELECT count(*)
                        FROM hotel_bookings hb
                        WHERE hb.guest_id = hg.id) AS total_visits
                FROM hotel_guests hg;
        """)
        print("Guest View created") #checkpoint for error
        cur.execute("""
            DROP VIEW IF EXISTS sales_view;
            CREATE VIEW sales_view AS
                SELECT 
                    SUM((hb.date_to - hb.date_from) * r.price) AS revenue,
                    SUM(hb.date_to - hb.date_from) AS number_of_nights,
                    COUNT(*) AS number_of_booking
                FROM hotel_bookings hb
                INNER JOIN rooms r ON r.id = hb.room_id
                INNER JOIN hotel_guests hg ON hg.id = hb.guest_id;
        """)
        print("Sales View created") #checkpoint for error
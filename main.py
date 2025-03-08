from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL for security (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="newsaper_db",
        user="postgres",
        password="Windom56101!",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Allows dictionary-style querying
except Exception as e:
    print("Error connecting to database:", e)

# ✅ Define Data Model
class Newspaper(BaseModel):
    member_name: str
    publisher_name: str
    publisher_email: str
    city: str
    state: str

# ✅ GET all newspapers (returns JSON)
@app.get("/newspapers")
def get_newspapers():
    try:
        cur.execute("SELECT pk_id, member_name, publisher_name, publisher_email, city, state FROM newspapers")
        rows = cur.fetchall()

        # Convert rows to list of dictionaries
        newspapers = [
            {
                "id": row["pk_id"],
                "member_name": row["member_name"],
                "publisher_name": row["publisher_name"],
                "publisher_email": row["publisher_email"],
                "city": row["city"],
                "state": row["state"]
            }
            for row in rows
        ]
        return newspapers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ POST to add a new newspaper
@app.post("/newspapers")
def add_newspaper(newspaper: Newspaper):
    try:
        cur.execute(
            "INSERT INTO newspapers (member_name, publisher_name, publisher_email, city, state) VALUES (%s, %s, %s, %s, %s) RETURNING pk_id",
            (newspaper.member_name, newspaper.publisher_name, newspaper.publisher_email, newspaper.city, newspaper.state)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"message": "Newspaper added", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Close database connection properly when the app shuts down
@app.on_event("shutdown")
def shutdown():
    cur.close()
    conn.close()


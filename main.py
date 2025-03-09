
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os  # Import os module to read environment variables

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Get the database URL from Render's environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL is not set! Check your Render environment variables.")

# ✅ Connect to PostgreSQL
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")  # Ensure SSL is used
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("✅ Successfully connected to the database")
except Exception as e:
    print("❌ Error connecting to database:", e)

# ✅ Define Newspaper Data Model
class Newspaper(BaseModel):
    member_name: str
    publisher_name: str
    publisher_email: str
    city: str
    state: str

# ✅ GET all newspapers
@app.get("/newspapers")
def get_newspapers():
    try:
        cur.execute("SELECT pk_id, member_name, publisher_name, publisher_email, city, state FROM newspapers")
        rows = cur.fetchall()
        return [
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
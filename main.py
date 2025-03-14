from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to PostgreSQL using Render's internal database URL
DATABASE_URL = "postgresql://newspaper_db_8xic_user:RNqisi13cTyGThXkXAKXUPF0POgWC2YL@dpg-cv6evj3tq21c73dic400-a/newspaper_db_8xic"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Use DictCursor for JSON output
    print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Error connecting to the database:", e)

# ✅ GET all newspapers (returns JSON with all fields)
@app.get("/newspapers")
def get_newspapers():
    try:
        cur.execute("SELECT * FROM newspapers")  # Fetch all columns dynamically
        rows = cur.fetchall()
        newspapers = [dict(row) for row in rows]  # Convert rows to JSON-friendly format
        return newspapers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Close database connection properly when the app shuts down
@app.on_event("shutdown")
def shutdown():
    cur.close()
    conn.close()

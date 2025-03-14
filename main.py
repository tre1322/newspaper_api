from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras

app = FastAPI()

# ✅ Enable CORS (Allows frontend to communicate with the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="newspaper_db_8xic",
        user="newspaper_db_8xic_user",
        password="YOUR_DATABASE_PASSWORD",  # Replace with actual database password
        host="dpg-cv6evj3tq21c73dic400-a.ohio-postgres.render.com",
        port="5432"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Enables dictionary-style querying
except Exception as e:
    print("❌ Error connecting to database:", e)
    conn = None
    cur = None

# ✅ GET all newspapers (returns JSON with all fields)
@app.get("/newspapers")
def get_newspapers():
    if cur is None:
        raise HTTPException(status_code=500, detail="Database connection error")

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
    if cur:
        cur.close()
    if conn:
        conn.close()

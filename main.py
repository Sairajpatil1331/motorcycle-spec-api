from fastapi import FastAPI, HTTPException
import sqlite3

# This initializes your API
app = FastAPI(title="Performance Spec API")


# Helper function to connect to the DB
def get_db_connection():
    conn = sqlite3.connect("motorcycles.db")
    # This row_factory makes the SQL results act like Python dictionaries
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint 1: The Home Page
@app.get("/")
def home():
    return {"message": "API is live. Navigate to /docs to see the interface."}


# Endpoint 2: Get all bikes in the database
@app.get("/bikes")
def get_all_bikes():
    conn = get_db_connection()
    # Execute a simple SELECT query
    bikes = conn.execute("SELECT * FROM Bikes").fetchall()
    conn.close()

    # Convert the SQL rows into a clean JSON list
    return [dict(bike) for bike in bikes]


# Endpoint 3: Search for a specific bike (e.g., /bikes/ninja)
@app.get("/bikes/{search_term}")
def search_bike(search_term: str):
    conn = get_db_connection()
    # The % signs allow for partial matches. Searching "GT" will find "Continental GT 650"
    query = "SELECT * FROM Bikes WHERE model_name LIKE ?"
    bike = conn.execute(query, ("%" + search_term + "%",)).fetchone()
    conn.close()

    if bike is None:
        raise HTTPException(status_code=404, detail="Bike not found in database")

    return dict(bike)

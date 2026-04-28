import sqlite3


def setup_db():
    # 1. Connect to the database (this creates the file if it doesn't exist)
    conn = sqlite3.connect("motorcycles.db")
    cursor = conn.cursor()

    # 2. Write the DDL (Data Definition Language) query to create the table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bikes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        horsepower REAL,
        torque REAL,
        weight_kg REAL,
        price_inr INTEGER
    )
    """)

    # Clear old data so we don't get duplicates if we run this file twice
    cursor.execute("DELETE FROM Bikes")

    # 3. Our Seed Data
    bikes = [
        ("Royal Enfield Continental GT 650", 47.0, 52.0, 214.0, 319000),
        ("Kawasaki Ninja 400", 44.7, 37.0, 168.0, 499000),
        ("Aprilia RS 457", 47.6, 43.5, 175.0, 410000),
    ]

    # 4. Write the DML (Data Manipulation Language) query to insert data
    cursor.executemany(
        """
        INSERT INTO Bikes (model_name, horsepower, torque, weight_kg, price_inr) 
        VALUES (?, ?, ?, ?, ?)
    """,
        bikes,
    )

    # 5. Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Database setup complete. 'motorcycles.db' has been created!")


if __name__ == "__main__":
    setup_db()

import sqlite3
import requests
from bs4 import BeautifulSoup


def scrape_and_update():
    # 1. Connect and Setup
    conn = sqlite3.connect("motorcycles.db")
    cursor = conn.cursor()

    # 2. Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bikes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            horsepower REAL,
            torque REAL,
            weight_kg REAL,
            price_inr REAL,
            image_url TEXT
        )
    """)

    # 3. Clear old data
    cursor.execute("DELETE FROM Bikes")

    # 4. Scrape logic (Example data - replace with your BeautifulSoup logic)
    # This is just a placeholder; ensure your actual scraping loop is here!
    sample_bikes = [
        ("Royal Enfield Continental GT 650", 47.0, 52.0, 214.0, 319000),
        ("Kawasaki Ninja 400", 44.7, 37.0, 168.0, 499000),
        ("Aprilia RS 457", 47.6, 43.5, 175.0, 410000),
    ]

    for bike in sample_bikes:
        cursor.execute(
            """
            INSERT INTO Bikes (model_name, horsepower, torque, weight_kg, price_inr)
            VALUES (?, ?, ?, ?, ?)
        """,
            bike,
        )

    # 5. Save and Close
    conn.commit()
    conn.close()
    print("Database updated successfully!")


# This line allows you to run the scraper alone for testing
if __name__ == "__main__":
    scrape_and_update()

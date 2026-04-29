from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3
from scraper import scrape_and_update


def get_db_connection():
    # Connect to the correct database
    conn = sqlite3.connect("motorcycles.db")
    conn.row_factory = sqlite3.Row

    # THE FAILSAFE: Build the table if it doesn't exist
    conn.execute("""
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
    conn.commit()
    return conn  # Return ONLY at the very end


app = FastAPI(title="Performance Spec API")


@app.get("/refresh")
def refresh_data():
    try:
        from scraper import scrape_and_update

        scrape_and_update()  # This runs your scraping logic
        # This sends the user back to the home page after the sync is done
        return HTMLResponse(
            "<html><body><script>alert('Data Synced Successfully!'); window.location.href='/';</script></body></html>"
        )
    except Exception as e:
        return {"error": f"Scraper failed: {str(e)}"}


@app.get("/", response_class=HTMLResponse)
def dashboard():
    conn = get_db_connection()
    bikes = conn.execute("SELECT * FROM Bikes").fetchall()
    conn.close()

    image_map = {
        "royal enfield continental gt 650": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&q=80&w=800",
        "kawasaki ninja 400": "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&q=80&w=800",
        "aprilia rs 457": "https://images.unsplash.com/photo-1614165933026-0750fcd503e8?auto=format&fit=crop&q=80&w=800",
    }

    bike_cards = ""
    for bike in bikes:
        # Clean the name: remove spaces and make it lowercase for easy matching
        clean_name = bike["model_name"].strip().lower()

        # Try to get the image, otherwise use a dynamic Unsplash motorcycle search
        img = image_map.get(
            clean_name,
            f"https://source.unsplash.com/featured/?motorcycle,{clean_name.replace(' ', ',')}",
        )

        bike_cards += f"""
        <div class="card">
            <img src="{img}" alt="{bike["model_name"]}" onerror="this.src='https://images.unsplash.com/photo-1558981806-ec527fa84c39?q=80&w=800'">
            <div class="card-content">
                <h3>{bike["model_name"]}</h3>
                <div class="stats">
                    <span><b>Power:</b> {bike["horsepower"]} bhp</span>
                    <span><b>Torque:</b> {bike["torque"]} Nm</span>
                    <span><b>Weight:</b> {bike["weight_kg"]} kg</span>
                </div>
                <div class="price">₹{bike["price_inr"]:,}</div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MotoSpec Pro</title>
        <style>
            :root {{ --neon: #00e5ff; --bg: #0a0a0a; --card: #161616; }}
            body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: white; margin: 0; padding: 40px; }}
            h1 {{ text-align: center; color: var(--neon); font-size: 2.5rem; letter-spacing: 2px; text-transform: uppercase; }}
            .sync-btn {{ display: block; width: 150px; margin: 20px auto; text-align: center; background: var(--neon); color: black; padding: 12px; border-radius: 30px; text-decoration: none; font-weight: bold; transition: 0.3s; }}
            .sync-btn:hover {{ transform: scale(1.05); box-shadow: 0 0 15px var(--neon); }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 40px auto; }}
            .card {{ background: var(--card); border-radius: 15px; overflow: hidden; border: 1px solid #333; transition: 0.4s ease; display: flex; flex-direction: column; }}
            .card:hover {{ border-color: var(--neon); transform: translateY(-10px); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .card img {{ width: 100%; height: 220px; object-fit: cover; background: #222; display: block; }}
            .card-content {{ padding: 25px; flex-grow: 1; }}
            .card-content h3 {{ margin: 0 0 15px 0; color: var(--neon); font-size: 1.3rem; }}
            .stats {{ display: flex; flex-direction: column; font-size: 0.95rem; color: #bbb; gap: 10px; }}
            .price {{ margin-top: 20px; font-size: 1.6rem; font-weight: bold; color: white; border-top: 1px solid #333; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <h1>MOTOSPEC PREMIER</h1>
        <a href="/refresh" class="sync-btn">SYNC DATA</a>
        <div class="grid">{bike_cards}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Keep your other JSON endpoints below for the API functionality
@app.get("/bikes")
def get_all_bikes():
    conn = get_db_connection()
    bikes = conn.execute("SELECT * FROM Bikes").fetchall()
    conn.close()
    return [dict(bike) for bike in bikes]

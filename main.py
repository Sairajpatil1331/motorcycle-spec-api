from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3
from scraper import scrape_and_update

app = FastAPI(title="Performance Spec API")


@app.get("/refresh")
def refresh_data():
    from scraper import scrape_and_update

    scrape_and_update()  # This runs your scraping logic
    return HTMLResponse(
        "<html><body><script>alert('Data Synced!'); window.location.href='/';</script></body></html>"
    )


def get_db_connection():
    conn = sqlite3.connect("motorcycles.db")
    conn.row_factory = sqlite3.Row
    return conn


# --- NEW STYLED DASHBOARD ENDPOINT ---
@app.get("/", response_class=HTMLResponse)
def dashboard():
    conn = get_db_connection()
    bikes = conn.execute("SELECT * FROM Bikes").fetchall()
    conn.close()

    bike_cards = ""
    for bike in bikes:
        # Fallback image if one isn't found
        img = (
            bike["image_url"]
            if bike["image_url"]
            else "https://via.placeholder.com/300x200"
        )

        bike_cards += f"""
        <div class="card">
            <img src="{img}" alt="{bike["model_name"]}">
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

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MotoSpec Pro</title>
        <style>
            :root {{ --neon: #00e5ff; --bg: #0a0a0a; --card: #161616; }}
            body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: white; margin: 0; padding: 40px; }}
            h1 {{ text-align: center; color: var(--neon); font-size: 2.5rem; letter-spacing: 2px; }}
            .sync-btn {{ display: block; width: 150px; margin: 20px auto; text-align: center; background: var(--neon); color: black; padding: 12px; border-radius: 30px; text-decoration: none; font-weight: bold; transition: 0.3s; }}
            .sync-btn:hover {{ transform: scale(1.05); box-shadow: 0 0 15px var(--neon); }}
            
            .grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 30px; 
                max-width: 1200px; 
                margin: 40px auto; 
            }}
            
            .card {{ 
                background: var(--card); 
                border-radius: 15px; 
                overflow: hidden; 
                border: 1px solid #333; 
                transition: 0.3s; 
            }}
            .card:hover {{ border-color: var(--neon); transform: translateY(-10px); }}
            .card img {{ width: 100%; height: 200px; object-fit: cover; }}
            .card-content {{ padding: 20px; }}
            .card-content h3 {{ margin: 0 0 10px 0; color: var(--neon); }}
            .stats {{ display: flex; flex-direction: column; font-size: 0.9rem; color: #aaa; gap: 5px; }}
            .price {{ margin-top: 15px; font-size: 1.4rem; font-weight: bold; color: white; }}
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

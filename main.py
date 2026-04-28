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

    # Create the HTML table rows using a Python loop
    table_rows = ""
    for bike in bikes:
        table_rows += f"""
        <tr>
            <td>{bike["model_name"]}</td>
            <td>{bike["horsepower"]} bhp</td>
            <td>{bike["torque"]} Nm</td>
            <td>{bike["weight_kg"]} kg</td>
            <td>₹{bike["price_inr"]:,}</td>
        </tr>
        """

    # This is your HTML and CSS combined
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MotoSpec Dashboard</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #121212;
                color: #e0e0e0;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding-top: 50px;
            }}
            h1 {{ color: #00e5ff; margin-bottom: 30px; }}
            table {{
                border-collapse: collapse;
                width: 80%;
                max-width: 1000px;
                background-color: #1e1e1e;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                border-radius: 8px;
                overflow: hidden;
            }}
            th {{
                background-color: #333333;
                color: #00e5ff;
                text-align: left;
                padding: 15px;
                text-transform: uppercase;
                font-size: 14px;
            }}
            td {{
                padding: 15px;
                border-bottom: 1px solid #333;
            }}
            tr:hover {{ background-color: #2a2a2a; transition: 0.3s; }}
            .container {{ width: 100%; display: flex; justify-content: center; }}
        </style>
    </head>
    <body>
        <h1>Performance Motorcycle Tracker</h1>
        <div class="container">
        <a href="/refresh" style="text-decoration:none; background:#00e5ff; color:#121212; padding:10px 20px; border-radius:5px; font-weight:bold; margin-bottom:20px; display:inline-block;">
            Sync Latest Specs
        </a>
            <table>
                <thead>
                    <tr>
                        <th>Model Name</th>
                        <th>Horsepower</th>
                        <th>Torque</th>
                        <th>Weight</th>
                        <th>Price (On-Road)</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>

            </table>
        </div>
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

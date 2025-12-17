from flask import Flask, send_file, request, render_template_string
import pyodbc
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)
os.makedirs("receipts", exist_ok=True)

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=AirportLuggageDB;"
    "Trusted_Connection=yes;"
    "UID=airportUser;"
    "PWD=StrongPassword123!;"
)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baggage Receipt Generator</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {    
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #eef2f6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .main-container {
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .form-container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 400px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            text-align: center;
        }

        .form-header {
            margin-bottom: 30px;
        }

        .form-header h1 {
            font-size: 26px;
            color: #1f2937;
            margin-bottom: 8px;
            font-weight: 700;
        }


        .input-group {
            margin-bottom: 25px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 600;
            color: #1f2937;
        }

        input[type="number"] {
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            font-size: 16px;
            transition: all 0.2s ease;
            background-color: #f9fafb;
            text-align: center;
        }

        input:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
            background-color: #fff;
        }

        .submit-button {
            width: 100%;
            padding: 14px;
            background-color: #2563eb;
            color: white;
            border: none;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        }

        .submit-button:hover {
            background-color: #1d4ed8;
            box-shadow: 0 6px 10px rgba(37, 99, 235, 0.3);
        }

        .submit-button:active {
            transform: translateY(1px);
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="form-container">
            <div class="form-header">
                <h1>Baggage Receipt</h1>
            </div>

            <form method="get" action="/receipt">
                <div class="input-group">
                    <label for="id">Baggage ID</label>
                    <input type="number" id="id" name="id" min="1" placeholder="e.g. 201" required>
                </div>

                <button type="submit" class="submit-button">Download PDF</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/receipt")
def receipt():
    baggage_id = request.args.get("id")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ReceiptVW WHERE Baggage_ID = ?", baggage_id)
    row = cursor.fetchone()

    if not row:
        return "<div style='text-align:center; padding:50px; font-family:sans-serif;'><h2>Baggage not found</h2><a href='/'>Go back</a></div>", 404

    filename = f"receipts/receipt_{baggage_id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    y = 800
    line = 22
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(A4[0] / 2, y,"Baggage Receipt")
    y -= 40
    c.setFont("Helvetica", 13)
    c.drawString(50, y, f"Passenger: {row.Name} {row.Surname}")
    y -= line
    c.drawString(50, y, f"Baggage ID: {row.Baggage_ID}")
    y -= line
    c.drawString(50, y, f"Weight: {row.Weight} kg")
    y -= line
    c.drawString(50, y, f"Fee: {row.Fee} EUR")
    y -= 30
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(A4[0]/2,y,"Flight Information")
    y -= line
    c.setFont("Helvetica", 13)
    c.drawString(50, y, f"Flight: {row.Flight_number}")
    y -= line
    c.drawString(50, y, f"Airline: {row.Airline_Name}")
    y -= line
    c.drawString(50, y, f"From: {row.Origin}")
    y -= line
    c.drawString(50, y, f"To: {row.Destination}")
    y -= line
    c.drawString(50, y, f"Departure: {row.Departure_time}")
    y -= line
    c.drawString(50, y, f"Arrival: {row.Arrival_time}")
    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, y, f"Generated: {timestamp}")
    c.save()

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


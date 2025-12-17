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
    "SERVER=LAPTOP-PF0MT41A;"
    "DATABASE=AirportLuggageDB;"
    "Trusted_Connection=yes;"
)

HTML = """
<!doctype html>
<html>
<head>
    <title>Baggage Receipt</title>
    <style>
        body {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #f5f5f5;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            padding: 45px 55px;
            border-radius: 12px;
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
            text-align: center;
            width: 420px;
        }

        h1 {
            font-size: 30px;
            margin-bottom: 35px;
            font-weight: 600;
        }

        label {
            font-size: 18px;
            display: block;
            margin-bottom: 12px;
        }

        input[type="number"] {
            font-size: 20px;
            padding: 12px;
            width: 100%;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 20px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }

        button {
            font-size: 18px;
            padding: 14px 20px;
            width: 100%;
            background-color: #0078D4;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
        }

        button:hover {
            background-color: #005ea6;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Baggage Receipt Generator</h1>

        <form method="get" action="/receipt">
            <label for="id">Baggage ID</label>
            <input type="number" id="id" name="id" min="1" required>

            <button type="submit">Download PDF</button>
        </form>
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
    cursor.execute(
        "SELECT * FROM ReceiptVW WHERE Baggage_ID = ?",
        baggage_id
    )
    row = cursor.fetchone()

    if not row:
        return "Baggage not found", 404

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


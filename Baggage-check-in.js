const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const sql = require('mssql');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

const config = {
    user: 'airportUser',
    password: 'StrongPassword123!',
    server: 'localhost',
    database: 'AirportLuggageDB',
    options: {
        trustServerCertificate: true
    }
};

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'Baggage-check-in.html'));
});

app.post('/submit-luggage', async (req, res) => {
    const { document_ID, flightNumber, weight, airlineName } = req.body;

    if (!document_ID || !flightNumber || !weight || !airlineName) {
        return res.status(400).send("Missing required fields!");
    }

    try {
        let pool = await sql.connect(config);

        const baggageWeight = parseFloat(weight);
        if (isNaN(baggageWeight) || baggageWeight <= 0) {
            return res.status(400).send("Invalid weight");
        }

        const passengerCheck = await pool.request()
            .input("document_ID", sql.VarChar(50), document_ID)
            .query("SELECT 1 FROM Passenger WHERE Document_ID = @document_ID");

        if (passengerCheck.recordset.length === 0) {
            return res.status(400).send("Passenger does not exist!");
        }

        const airlineResult = await pool.request()
            .input("airlineName", sql.VarChar(100), airlineName)
            .query("SELECT Weight_limit, Fee FROM Airline WHERE Name = @airlineName");

        if (airlineResult.recordset.length === 0) {
            return res.status(400).send("Airline not found!");
        }

        const { Weight_limit, Fee: airlineFee } = airlineResult.recordset[0];

        const fee = baggageWeight > parseFloat(Weight_limit) ? parseFloat(airlineFee) : 0;

        const checkInTime = new Date();
        checkInTime.setMinutes(checkInTime.getMinutes() - checkInTime.getTimezoneOffset());

    
        await pool.request()
            .input("document_ID", sql.VarChar(50), document_ID)
            .input("flightNumber", sql.VarChar(20), flightNumber)
            .input("weight", sql.Decimal(5, 2), baggageWeight)
            .input("status", sql.VarChar(50), "Checked-in")
            .input("fee", sql.Decimal(10,2), fee) 
            .input("check_in_time", sql.DateTime2(0), checkInTime)
            .query(`
                INSERT INTO Baggage 
                    (Passenger_Document_ID, Flight_Number, Weight, Status, Fee, Check_in_time) 
                VALUES 
                    (@document_ID, @flightNumber, @weight, @status, @fee, @check_in_time)
            `);

        res.send(`Luggage Information Saved!`);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database Error");
    }
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));

const express = require('express');
const path = require('path');
const sql = require('mssql');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

const config = {
    user: 'airportUser',
    password: 'StrongPassword123!',
    server: 'localhost',
    database: 'AirportLuggageDB',
    options: { trustServerCertificate: true }
};

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'loading-list.html'));
});

app.get('/api/baggage/flight/:flightNumber', async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const flightNumber = req.params.flightNumber;

        const result = await pool.request()
            .input('flightNumber', sql.VarChar(20), flightNumber)
            .query(`
                SELECT 
                    b.Baggage_ID, 
                    p.Name AS Passenger_Name, 
                    p.Surname AS Passenger_Surname, 
                    p.Document_ID AS Passenger_Document_ID,
                    b.Loading_time_start,
                    b.Loading_time_end,
                    b.Status,
                    b.Container_ID
                FROM Baggage b
                JOIN Passenger p ON b.Passenger_Document_ID = p.Document_ID
                WHERE b.Flight_Number = @flightNumber
                  AND b.Status = 'In Security' OR b.Status = 'Loading'
            `);

        res.json(result.recordset);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database error");
    }
});

app.get('/api/containers/empty', async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const result = await pool.request().query(`
            SELECT ID, Number, Max_load
            FROM Container
            WHERE Status = 'Empty'
        `);
        res.json(result.recordset);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database error");
    }
});

app.put('/api/baggage/:baggageId/assign/:containerId', async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const baggageId = req.params.baggageId;
        const containerId = req.params.containerId;
        const currentTime = new Date();
        currentTime.setMinutes(currentTime.getMinutes() - currentTime.getTimezoneOffset());

        await pool.request()
            .input('baggageId', sql.Int, baggageId)
            .input('containerId', sql.Int, containerId)
            .input('currentTime', sql.DateTime2, currentTime)
            .query(`
                UPDATE Baggage
                SET Container_ID = @containerId,
                    Status = 'Loading',
                    Loading_time_start = @currentTime
                WHERE Baggage_ID = @baggageId
                  AND Container_ID IS NULL
            `);

        res.sendStatus(200);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database error");
    }
});

app.put('/api/baggage/:baggageId/loaded', async (req, res) => {
    try {
        const pool = await sql.connect(config);
        const currentTime = new Date();
        currentTime.setMinutes(currentTime.getMinutes() - currentTime.getTimezoneOffset());

        await pool.request()
            .input('baggageId', sql.Int, req.params.baggageId)
            .input('currentTime', sql.DateTime2, currentTime)
            .query(`
                UPDATE Baggage
                SET Status = 'Loaded',
                    Loading_time_end = @currentTime
                WHERE Baggage_ID = @baggageId
            `);

        res.sendStatus(200);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database error");
    }
});

app.listen(3002, () => console.log('Loading server running at http://localhost:3002'));

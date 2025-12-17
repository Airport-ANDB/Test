const express = require('express');
const path = require('path');
const sql = require('mssql');

const app = express();
app.use(express.json());
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
    res.sendFile(path.join(__dirname, 'public', 'timeline.html'));
});

app.get('/baggage-timeline/:id', async (req, res) => {
    const baggageId = req.params.id;

    try {
        const pool = await sql.connect(config);

        const result = await pool.request()
            .input("baggageId", sql.Int, baggageId)
            .query(`
                SELECT Check_in_time, Security_time, Loading_time_start, Loading_time_end,
                       Routing_time, Unloading_time_start, Unloading_time_end
                FROM Baggage
                WHERE Baggage_ID = @baggageId
            `);

        if (result.recordset.length === 0) {
            return res.status(404).send("Baggage not found");
        }

        res.json(result.recordset[0]);
    } catch (err) {
        console.error(err);
        res.status(500).send("Database Error");
    }
});

app.listen(3001, () => console.log("Timeline Server running on http://localhost:3001"));

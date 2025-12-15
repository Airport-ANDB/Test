use AirportLuggageDB
GO

CREATE VIEW ReceiptVW AS
SELECT b.Baggage_ID, p.Name, p.Surname, b.Weight, b.Fee, f.Flight_number, f.Origin, f.Destination, f.Airline_Name, f.Departure_time, f.Arrival_time
FROM Baggage b
JOIN Passenger p ON b.Passenger_Document_ID=p.Document_ID
JOIN Flight f ON b.Flight_Number=f.Flight_number
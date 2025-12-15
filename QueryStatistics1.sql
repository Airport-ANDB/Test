use AirportLuggageDB;
GO

CREATE VIEW FlightBaggageDailyVW AS
SELECT f.Flight_number, f.Origin, f.Destination, CAST(f.Departure_time AS DATE) AS Flight_Date, COUNT(b.Baggage_ID) AS Total_Baggage, 
	SUM(b.Weight) AS Total_Weight, AVG(b.Weight) AS Avg_Weight, SUM(b.Fee) AS Total_fees
FROM Flight f LEFT JOIN Baggage b ON f.Flight_number=b.Flight_Number
GROUP BY f.Flight_number, f.Origin, f.Destination, CAST(f.Departure_time AS DATE);
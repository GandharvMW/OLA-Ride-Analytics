SELECT 
    *
FROM
    ola_rides;

-- 1. Retrieve all successful bookings:
SELECT 
    *
FROM
    ola_rides
WHERE
    Booking_Status = 'Success';

-- 2. Find the average ride distance for each vehicle type:
SELECT 
    Vehicle_Type,
    ROUND(AVG(Ride_Distance),2) AS Average_Ride_Distance
FROM
    ola_rides
GROUP BY Vehicle_Type;

-- 3. Get the total number of cancelled rides by customers:
SELECT 
    COUNT(*) Total_cancelled_rides_by_customers
FROM
    ola_rides
WHERE
    Booking_Status = 'Canceled by Customer';

-- 4. List the top 5 customers who booked the highest number of rides:
SELECT 
    Customer_ID,
    COUNT(Booking_Status) AS Top_5_customer_highest_rides
FROM
    ola_rides
GROUP BY Customer_ID
ORDER BY COUNT(Booking_Status) DESC
LIMIT 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues:
SELECT 
    COUNT(*) No_of_rides_cancelled_by_drivers
FROM
    ola_rides
WHERE
    Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
SELECT 
    MAX(Driver_Ratings) AS max_driver_rating,
    MIN(Driver_Ratings) AS min_driver_rating
FROM
    ola_rides
WHERE
    Vehicle_Type = 'Prime Sedan' ;

-- 7. Retrieve all rides where payment was made using UPI:
SELECT 
    *
FROM
    ola_rides
WHERE
    Payment_Method = 'UPI';

-- 8. Find the average customer rating per vehicle type:
SELECT 
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 1) AS avg_cutomer_rating
FROM
    ola_rides
GROUP BY Vehicle_Type;

-- 9. Calculate the total booking value of rides completed successfully:
SELECT 
    SUM(Booking_Value) AS Total_booking_value
FROM
    ola_rides
WHERE 
	Booking_Status='Success';

-- 10. List all incomplete rides along with the reason
SELECT 
    Booking_ID,
    Customer_ID,
    Incomplete_Rides,
    Incomplete_Rides_Reason
FROM
    ola_rides
WHERE
    Incomplete_Rides = 'Yes';
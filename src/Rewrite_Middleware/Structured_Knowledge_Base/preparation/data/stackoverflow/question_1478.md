# Fix INSERT conflict with FOREIGN KEY constraint issue
[Link to question](https://stackoverflow.com/questions/77802252/fix-insert-conflict-with-foreign-key-constraint-issue)
**Creation Date:** 1704997213
**Score:** 0
**Tags:** c#, sql-server, ado.net
## Question Body
<p>I'm making a parking reservation system for a project and I'm encountering an issue when trying to insert my data into the database. I'm using C# and ADO.NET</p>
<p>The exact error is:</p>
<blockquote>
<p>The INSERT statement conflicted with the FOREIGN KEY constraint &quot;FK__ParkingRe__UserI__2057CCD0&quot;. The conflict occurred in database &quot;Reservation&quot;, table &quot;dbo.Users&quot;, column 'UserID'</p>
</blockquote>
<pre class="lang-cs prettyprint-override"><code>public bool ReserveParkingSpot(Reservation reservation)
{
    try
    {
        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();

            // Check if the parking spot is available during the specified time
            string availabilityCheckQuery = &quot;SELECT COUNT(*) FROM ParkingReservations &quot; +
                                            &quot;WHERE ParkingSpotID = @ParkingSpotID &quot; +
                                            &quot;AND ((@StartTime &gt;= StartTime AND @StartTime &lt; EndTime) OR &quot; +
                                            &quot;(@EndTime &gt; StartTime AND @EndTime &lt;= EndTime))&quot;;
            using (SqlCommand availabilityCheckCommand = new SqlCommand(availabilityCheckQuery, connection))
            {
                availabilityCheckCommand.Parameters.AddWithValue(&quot;@ParkingSpotID&quot;, reservation.ParkingSpotID);
                availabilityCheckCommand.Parameters.AddWithValue(&quot;@StartTime&quot;, reservation.StartTime);
                availabilityCheckCommand.Parameters.AddWithValue(&quot;@EndTime&quot;, reservation.EndTime);

                int overlappingReservations = (int)availabilityCheckCommand.ExecuteScalar();

                if (overlappingReservations &gt; 0)
                {
                    Console.WriteLine(&quot;Parking spot is not available during the specified time.&quot;);
                    return false;
                }
            }

            // If the parking spot is available, update the IsFree status and proceed with the reservation
            string reserveParkingQuery = &quot;UPDATE ParkingSpots SET IsFree = 0 WHERE ParkingSpotID = @ParkingSpotID; &quot; +
                                         &quot;INSERT INTO ParkingReservations (UserID, VehicleID, ParkingSpotID, StartTime, EndTime) &quot; +
                                         &quot;VALUES (@UserID, @VehicleID, @ParkingSpotID, @StartTime, @EndTime); &quot; +
                                         &quot;SELECT SCOPE_IDENTITY();&quot;; // Retrieve the auto-incremented ReservationID
            using (SqlCommand reserveParkingCommand = new SqlCommand(reserveParkingQuery, connection))
            {
                reserveParkingCommand.Parameters.AddWithValue(&quot;@UserID&quot;, reservation.UserID);
                reserveParkingCommand.Parameters.AddWithValue(&quot;@VehicleID&quot;, reservation.VehicleID);
                reserveParkingCommand.Parameters.AddWithValue(&quot;@ParkingSpotID&quot;, reservation.ParkingSpotID);
                reserveParkingCommand.Parameters.AddWithValue(&quot;@StartTime&quot;, reservation.StartTime);
                reserveParkingCommand.Parameters.AddWithValue(&quot;@EndTime&quot;, reservation.EndTime);

                // Retrieve the auto-incremented ReservationID
                int reservationID = Convert.ToInt32(reserveParkingCommand.ExecuteScalar());

                Console.WriteLine($&quot;Parking spot with ID {reservationID} reserved successfully!&quot;);
                return true;
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($&quot;Error reserving parking spot: {ex.Message}&quot;);
        return false;
    }
}
</code></pre>
<pre class="lang-sql prettyprint-override"><code>CREATE TABLE Users 
(
    UserID INT PRIMARY KEY IDENTITY(1,1),
    [Name] VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    [Password] VARCHAR(255) NOT NULL
);

CREATE TABLE Vehicles 
(
    VehicleID INT PRIMARY KEY IDENTITY(1,1),
    Brand VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    [Year] INT NOT NULL,
    RegistrationPlate VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE ParkingReservations 
(
    ReservationID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    VehicleID INT FOREIGN KEY REFERENCES Vehicles(VehicleID),
    ParkingSpotID INT,
    StartTime DATETIME,
    EndTime DATETIME,
    FOREIGN KEY (ParkingSpotID) REFERENCES ParkingSpots(ParkingSpotID)
);

CREATE TABLE ParkingSpots 
(
    ParkingSpotID INT PRIMARY KEY IDENTITY(1,1),
    IsFree BIT
);

INSERT INTO ParkingSpots (IsFree) 
VALUES (1), (1), (1), (1), (1),
       (1), (1), (1), (1), (1),
       (1), (1), (1), (1), (1),
       (1), (1), (1), (1), (1),
       (1), (1), (1), (1), (1);
</code></pre>
<p>I tried rewriting the whole query, but to no avail. It needs to save the data to the <code>ParkingReservations</code> table</p>

## Answers
### Answer ID: 77802885
<p>I saw that you tried to repost this question so I gave it a second look. It appears that your actual problem is that you are creating the <code>ParkingSpots</code> table after trying to reference it in the foreign key specified in the definition for <code>ParkingReservations</code>.</p>
<p>If you move the definition for <code>ParkingSpots</code> before the definition of <code>ParkingReservations</code> it should solve your issue.</p>
<pre><code>CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    [Name] VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    [Password] VARCHAR(255) NOT NULL
);

CREATE TABLE Vehicles (
    VehicleID INT PRIMARY KEY IDENTITY(1,1),
    Brand VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    [Year] INT NOT NULL,
    RegistrationPlate VARCHAR(20) UNIQUE NOT NULL
);


CREATE TABLE ParkingSpots (
    ParkingSpotID INT PRIMARY KEY IDENTITY(1,1),
    IsFree BIT
);

CREATE TABLE ParkingReservations (
    ReservationID INT PRIMARY KEY IDENTITY(1,1),
    UUID INT FOREIGN KEY REFERENCES Users(UserID),
    CarID INT FOREIGN KEY REFERENCES Vehicles(VehicleID),
    SpotID INT,
    StartTime DATETIME,
    EndTime DATETIME,
    FOREIGN KEY (SpotID) REFERENCES ParkingSpots(ParkingSpotID)
);

INSERT INTO ParkingSpots (IsFree) VALUES (1), (1), (1), (1), (1),
                                         (1), (1), (1), (1), (1),
                                         (1), (1), (1), (1), (1),
                                         (1), (1), (1), (1), (1),
                                         (1), (1), (1), (1), (1)
</code></pre>
<p>As mentioned in the comments above by Thom A it would be good to get in the habit of specifying names for your foreign keys. This can save a lot of issues in the long run.</p>
<p>If you wish to name your constraints simply replace</p>
<pre><code>FOREIGN KEY (ParkingSpotID) REFERENCES ParkingSpots(ParkingSpotID)
</code></pre>
<p>with</p>
<pre><code>CONSTRAINT FK_ParkingReservations_ParkingSpots FOREIGN KEY (SpotID) REFERENCES ParkingSpots(ParkingSpotID)   
</code></pre>
<p>Where <code>FK_ParkingReservations_ParkingSpots</code> is the name of the constraint</p>


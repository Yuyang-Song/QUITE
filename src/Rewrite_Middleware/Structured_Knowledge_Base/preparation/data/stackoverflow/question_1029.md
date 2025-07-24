# Laravel - Integrate big raw query in relationship eagerload
[Link to question](https://stackoverflow.com/questions/55810259/laravel-integrate-big-raw-query-in-relationship-eagerload)
**Creation Date:** 1556019148
**Score:** 0
**Tags:** php, laravel, eloquent, eager-loading, laravel-query-builder
## Question Body
<p>I've been using laravel for about 4 years now but now I'm facing my biggest challenge yet. I'm refactoring and extending an old <code>PHP</code> application used to map the offices where I work. There's this huge <code>SQL</code> query that I need to integrate somehow into Laravel's QueryBuilder to feed an eager loaded relationship.</p>

<p>The flow is something like this</p>

<pre><code>Building =&gt; hasMany: Floor =&gt; hasMany: Seat =&gt; hasMany: BookedSeat =&gt; belongsTo: User
</code></pre>

<p>where <code>Building</code>, <code>Floor</code>, <code>Seat</code> and <code>BookedSeat</code> are <code>Eloquent</code> models.</p>

<p>My huge query selects from <code>BookedSeat</code> the <code>Seat</code> reservations for the current date based on many many other conditions like if the person that booked the seat is in home office, vacation, etc.(these are stored in some other tables) and sets a property on the <code>BookedSeat</code> instance called <code>Status</code> to know if the <code>Seat</code> is taken or not for the current day</p>

<p>Now I'm trying to integrate this raw query into building a <code>JSON</code> hierarchy that I later send to a <code>Vue.js</code> application running on the front-end.</p>

<p>The hierarchy is something like: </p>

<pre><code> {
   "buildings": [
     {
        // properties
        "floors" : [
           {
              //properties
              "seats": [
                  {
                     //properties
                     "booked": [
                        {
                           "user": "some user model",
                           "Status": "some booked status"
                        }
                      ]
                  },
                  // other seats
              ] 
           }, 
           // other floors
        ]
     },
     //other buildings
   ]
}
</code></pre>

<p>The huge query returns an array of objects that I can then use to hydrate a <code>BookedSeat</code> collection with but I have no idea how I can then use this collection or use the huge query directly in order to eager load the <code>BookedSeat</code> for each <code>Seat</code> for each <code>Floor</code> for each <code>Building</code> and let the framework do the heavy lifting for me.</p>

<p>What I tried is building a method like the following: </p>

<pre><code>public static function bookedSeatsForFloor(Relation $seatQuery, Relation $bookedQuery, Carbon $forDate)
    {
        $format = $forDate-&gt;format('Y-m-d H:m:i');
        $bindings = $seatQuery-&gt;getBindings();

        /** @var AvailableSeatsQuerySimple $availableSeats */
        $availableSeats = new AvailableSeatsQuerySimple($bindings, $format); // bindings are my floor id's and I'm feeding them to my big query in order to have control over which floors to load depending on the user's rights 

        return DB::raw($availableSeats-&gt;getRawQuery());
    }
</code></pre>

<p>and call it like this: </p>

<pre><code>Floor::where('id', $someId)-&gt;with(['seats' =&gt; static function ($seatQuery) use ($_that) {

    /**
     * Add to each seat the manager and the active booking
     */
    $seatQuery-&gt;with(['booked' =&gt; static function ($bookedQuery) use ($seatQuery, $_that) {
        return self::bookedSeatsForFloor($seatQuery, $bookedQuery, $_that-&gt;forDate);
    }, 'manager'])-&gt;orderBy('seat_cir');
}]);
</code></pre>

<p>But I'd need to somehow modify the <code>$bookedQuery</code> in the <code>bookedSeatsForFloor</code> method with a <code>$bookedQuery-&gt;select('something')</code> or <code>$bookedQuery-&gt;setQuery('some query builder instance')</code> but I have no idea how to convert the huge query to a Builder instance.</p>

<p>Thanks!</p>

<p>PS: I would preferably want to skip rewriting the huge query into eloquent syntax because of the complexity</p>

<p><strong>ADDED DETAILS:</strong></p>

<p>So, as requested, this is my raw query where I changed some of the database/table names per company policy</p>

<pre><code>    SET NOCOUNT ON;
DECLARE
    @the_date DATETIME;
SET @the_date = (SELECT CONVERT(DATETIME, ?, 120));

SELECT seat_identifier,
       user_id,
       FromDate,
       ToDate,
       Status
FROM (
         SELECT d.seat_identifier,
                d.user_id,
                d.FromDate,
                d.ToDate,
                CASE
                    WHEN d.Status IS NULL
                        THEN 0
                    WHEN d.Status = 2
                        THEN 2
                    WHEN d.Status != 0
                        THEN CASE
                                 WHEN -- New, OnGoing Request in Main_DB_Name
                                             ho.status = 1 -- New StatusType in Main_DB_Name
                                         OR
                                             ho.status = 4 -- Pending StatusType in Main_DB_Name
                                         OR
                                             twl.status = 1 -- New StatusType in Main_DB_Name
                                         OR
                                             twl.status = 4 -- Pending StatusType in Main_DB_Name
                                         OR
                                             li.status = 1 -- New StatusType in Main_DB_Name
                                         OR
                                             li.status = 4 -- Pending StatusType in Main_DB_Name
                                         OR
                                             ctaf.status = 1 -- New StatusType2 in Main_DB_Name
                                         OR
                                             ctaf.status = 2 -- Ongoing StatusType2 in Main_DB_Name
                                     THEN
                                     2 --&gt; Pending seat in MyApplication


                                 WHEN -- Approved Request in Main_DB_Name
                                             ho.status = 2
                                         OR
                                             twl.status = 2
                                         OR
                                             li.status = 1
                                         OR
                                             li.status = 2
                                         OR
                                             ctaf.status = 1
                                         OR
                                             ctaf.status = 2
                                     THEN 0 -- Free Seat MyApplication

                                 ELSE 1 -- Taken  Seat MyApplication
                        END
                    END as 'Status'
         FROM (
                  SELECT seats.seat_identifier as seat_identifier,
                         c.user_id,
                         c.FromDate,
                         c.ToDate,
                         c.Status
                  FROM (
                           SELECT fo_bs.seat_identifier,
                                  fo_bs.user_id,
                                  fo_bs.FromDate,
                                  fo_bs.ToDate,
                                  fo_bs.Status
                           FROM MyApplication.another_schema.BookedSeats fo_bs
                                    INNER JOIN MyApplication.another_schema.seats AS seats ON fo_bs.seat_identifier = seats.seat_identifier
                               WHERE fo_bs.FromDate &lt;= @the_date
                                    AND fo_bs.ToDate &gt;= @the_date
                                    AND fo_bs.Status IN (1, 2)
                                    AND seats.floor_id IN (###FLOOR_IDS###) -- will replace this from php with a list of "?,?,?" depending on how many floor_ids are in the query bindings
                       ) c
                           INNER JOIN MyApplication.another_schema.seats AS seats ON c.seat_identifier = seats.seat_identifier) d
                  LEFT JOIN (SELECT requester, status
                             from Main_DB_Name.schema.HOME_OFFICE
                                 WHERE Main_DB_Name.schema.HOME_OFFICE.from_date &lt;= @the_date
                                      and Main_DB_Name.schema.HOME_OFFICE.to_date &gt;= @the_date) ho ON d.user_id = ho.requester
                  LEFT JOIN (SELECT requester, status
                             from Main_DB_Name.schema.TEMPORARY_WORK_LOCATION
                                 WHERE Main_DB_Name.schema.TEMPORARY_WORK_LOCATION.from_date &lt;= @the_date
                                      and Main_DB_Name.schema.TEMPORARY_WORK_LOCATION.to_date &gt;= @the_date) twl
                            ON d.user_id = twl.requester
                  LEFT JOIN (SELECT employee, status
                             from Main_DB_Name.schema.LEAVE_INVOIRE
                                 WHERE Main_DB_Name.schema.LEAVE_INVOIRE.leave_date = @the_date) li ON d.user_id = li.employee
                  LEFT JOIN (SELECT requester, status
                             from Main_DB_Name.schema.TRAVEL
                                 WHERE Main_DB_Name.schema.TRAVEL.from_date &lt;= @the_date
                                      and Main_DB_Name.schema.TRAVEL.until_date &gt;= @the_date) ctaf
                            ON d.user_id = ctaf.requester
     ) y
</code></pre>

<p>And my models/relationships are as following: </p>

<pre><code>class Building extends Model {
  /* Properties */

   public function floors()
    {
        return $this-&gt;hasMany(Floor::class);
    }
}

class Floor extends Model {
  /* Properties */
   public function building()
    {
        return $this-&gt;belongsTo(Building::class);
    }

   public function seats()
    {
        return $this-&gt;hasMany(Seat::class);
    }
}

class Seat extends Model {
  /* Properties */
   public function floor()
    {
        return $this-&gt;belongsTo(Floor::class);
    }

   public function booked()
    {
        return $this-&gt;hasMany(BookedSeat::class);
    }
}

class BookedSeat extends Model {
  /* Properties */
   public function user()
    {
        return $this-&gt;belongsTo(User::class);
    }

   public function seat()
    {
        return $this-&gt;belongsTo(Seat::class);
    }
}
</code></pre>

## Answers
### Answer ID: 55848690
<p>The problem is quite a difficult one. I was stuck with it trying different things for more than a week in total but couldn't find any nice way of doing it. </p>

<p>I ended up using @Jonas Staudenmeir's suggestion by manually mapping through all my nested relationships and then setting the corresponding <code>booked</code> relation on my <code>Seat</code> model instances from a collection obtained from using <code>BookedSeat::hydrate()</code> with the results from the raw query as an argument.</p>

<pre><code>$availableSeats = new AvailableSeatsQuerySimple($format);

        // Map through all the Buildings
        $this-&gt;template['buildings'] = $this-&gt;template['buildings']
            -&gt;map(static function (Building $building) use ($availableSeats) {

                // Map through all the Floors in a Building
                $floors = $building-&gt;floors-&gt;map(static function (Floor $floor) use ($availableSeats) {
                    /** @var BookedSeat|Collection $booked */
                    $booked = $availableSeats-&gt;execute($floor-&gt;id); // execute the raw query and get the results

                    if(count($booked) &gt; 0) {

                        // Map through all the Seats in a Floor
                        $seats = $floor-&gt;seats-&gt;map(static function (Seat $seat) use ($booked) {

                            // Select the BookedSeat for the corresponding Seat
                            /** @var BookedSeat $bookedSeatForRelation */
                            $bookedSeatForRelation = $booked-&gt;filter(static function (BookedSeat $bookedSeat) use ($seat) {
                                return $bookedSeat-&gt;seat_identifier === $seat-&gt;id;
                            })-&gt;first();

                            // Attach the BookedSeat to the Seat only if the Status IS NOT 0
                            if($bookedSeatForRelation !== null &amp;&amp; $bookedSeatForRelation-&gt;Status !== 0) {
                                return $seat-&gt;setRelation('booked', $bookedSeatForRelation);
                            }

                            return $seat-&gt;setRelation('booked', null);
                        });

                        return $floor-&gt;setRelation('seats', $seats);
                    }

                    return $floor;
                });

                return $building-&gt;setRelation('floors', $floors);
            });
</code></pre>


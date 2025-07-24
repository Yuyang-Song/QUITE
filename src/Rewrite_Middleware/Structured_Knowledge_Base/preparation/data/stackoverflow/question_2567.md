# Haversine formula in DOCTRINE 2
[Link to question](https://stackoverflow.com/questions/40693208/haversine-formula-in-doctrine-2)
**Creation Date:** 1479560526
**Score:** 2
**Tags:** php, mysql, doctrine-orm
## Question Body
<p>I need to transfer the query in PDO below to DOCTRINE:</p>

<pre><code>$query = $con-&gt;query('SELECT *,
            ( 6371 * acos( cos( radians('.$latitude.') ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians('.$longitude.') ) + sin( radians('.$latitude.') ) * sin( radians( latitude ) ) ) ) AS distance, city_name
            FROM event INNER JOIN city ON event_city_id = city_id
            WHERE event_sin_active = 1
            ORDER BY distance');
</code></pre>

<p>So far I've been able to rewrite the doctrine part of this query. The problem appears when inserting in the SELECT the Haversine formula according to the questions: <a href="https://stackoverflow.com/questions/1973878/sql-search-using-haversine-in-doctrine">SQL search using Haversine in Doctrine</a> e <a href="https://stackoverflow.com/questions/21084886/how-to-calculate-distance-using-latitude-and-longtitude">How to calculate distance using latitude and longtitude?</a></p>

<p>The two tables in the database used are Event and City</p>

<pre><code>    CREATE TABLE `event` (
  `event_id` int(11) NOT NULL,
  `event_name` varchar(45) NOT NULL,
  `event_image` varchar(45) DEFAULT NULL,
  `event_city_id` int(11) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `event_tax_service` decimal(10,2) DEFAULT NULL,
  `event_user_id` int(11) NOT NULL,
  `event_sin_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



 CREATE TABLE `city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(100) NOT NULL,
  PRIMARY KEY (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
</code></pre>

<p>When you try to run the query below, the system returns a blank screen and does not tell you which exception.
<strong>What is the correct way to write this query?</strong></p>

<pre><code>$qb = $entityManager-&gt;createQueryBuilder();
            $qb-&gt;select("e, e.eventCityId,c.cityName, (6371 * ACOS(SIN(RADIANS($latitude)) * SIN(RADIANS(e.latitude)) + COS(RADIANS($latitude)) * COS(RADIANS(e.latitude)) * COS(RADIANS(e.longitude) - RADIANS($longitude)))) as distance")
                -&gt;from('\App\Entity\Event', 'e')
                -&gt;innerJoin('\App\Entity\City', 'c', Join::WITH, $qb-&gt;expr()-&gt;eq('e.eventCityId', 'c.cityId'))
                -&gt;where('e.eventSinActive = 1')
                -&gt;orderBy('distance', 'ASC');
</code></pre>

<p>I'm running this code inside a route in slimFramework. PHP and Mysql logs do not indicate error</p>


# Rewriting MySQL query with subqueries to joins
[Link to question](https://stackoverflow.com/questions/4013932/rewriting-mysql-query-with-subqueries-to-joins)
**Creation Date:** 1288004653
**Score:** 1
**Tags:** mysql, join, query-optimization, subquery
## Question Body
<p>I have written a fairly complex SQL query to get some statistics about animals from an animal sampling database. This query includes a number of subqueries and I would now like to see if it is possible to rewrite this query in any way to use joins instead of subqueries. I have a dim idea that this might reduce query time. (it's now about 23s on a mac mini).</p>

<p>Here's the query:</p>

<pre><code>SELECT COUNT(DISTINCT a.AnimalID), TO_DAYS(a.VisitDate) AS day, 
   DATE_FORMAT(a.VisitDate, '%b %d %Y'), a.origin, 
   (
    SELECT COUNT(DISTINCT a.AnimalID)
           FROM samples AS a 
                JOIN
                custom_animals AS b 
                ON a.AnimalID = b.animal_id
                WHERE
                     b.organism = 2
                     AND
                         TO_DAYS(a.VisitDate) = day
    ) AS Goats, 
    (
     SELECT COUNT(DISTINCT a.AnimalID) 
            FROM samples AS a 
                 JOIN custom_animals AS b 
                 ON a.AnimalID = b.animal_id 
                 WHERE
                      b.organism = 2
                      AND 
                         b.sex = 'Female'
                      AND
                         TO_DAYS(a.VisitDate) = day
    ) AS GF,
    (
     SELECT COUNT(DISTINCT a.AnimalID) 
            FROM samples AS a 
                 JOIN custom_animals AS b 
                 ON a.AnimalID = b.animal_id 
                 WHERE 
                      b.organism = 3
                      AND
                         b.sex = 'Female'
                      AND
                         TO_DAYS(a.VisitDate) = day
    ) AS SF
    FROM
        samples AS a 
        JOIN custom_animals AS b 
        ON a.AnimalID = b.animal_id 
        WHERE
             project = 5
             AND
                AnimalID LIKE 'AVD%'
        GROUP BY
                TO_DAYS(a.VisitDate);
</code></pre>

<hr>

<p>Thanks to <a href="https://stackoverflow.com/users/367243/ksogor">ksogor</a> my query is now way faster at;</p>

<pre><code>SELECT  DATE_FORMAT(s.VisitDate, '%b %d %Y') AS date,
    s.origin,
    SUM(IF(project = 5 AND s.AnimalID LIKE 'AVD%', 1, 0)) AS sampled_animals, 
    SUM(IF(ca.organism = 2, 1, 0)) AS sampled_goats,
    SUM(IF(ca.organism = 2 AND ca.sex = 'Female', 1, 0)) AS female_goats,
    SUM(IF(ca.organism = 3 AND ca.sex = 'Female', 1, 0)) AS female_sheep
FROM samples s JOIN custom_animals ca ON s.AnimalID = ca.animal_id
GROUP BY date;
</code></pre>

<p>I would still need to make this query select distinct s.AnimalID though as right now it counts the samples we have taken from these animals instead of the animals themselves. Anyone got any idea?</p>

<hr>

<p>After some more help from <a href="https://stackoverflow.com/users/367243/ksogor">ksogor</a> I now have a great query:</p>

<pre><code>SELECT  DATE_FORMAT(s.VisitDate, '%b %d %Y') AS date,
    s.origin,
    SUM(IF(project = 5 AND s.AnimalID LIKE 'AVD%', 1, 0)) AS sampled_animals, 
    SUM(IF(ca.organism = 2, 1, 0)) AS sampled_goats,
    SUM(IF(ca.organism = 2 AND ca.sex = 'Female', 1, 0)) AS female_goats,
    SUM(IF(ca.organism = 3 AND ca.sex = 'Female', 1, 0)) AS female_sheep
FROM (
    SELECT DISTINCT AnimalID AS AnimalID,
           VisitDate,
           origin,
           project
           FROM samples
) s 
JOIN custom_animals ca ON s.AnimalID = ca.animal_id
GROUP BY date;
</code></pre>

## Answers
### Answer ID: 4014450
<p>You can just use <code>if</code> or <code>case</code> statements, like this:</p>

<pre><code>SELECT  SUM(if(project = 5 AND AnimealID LIKE 'AVD%', 1, 0)) AS countbyproj, 
        TO_DAYS(s.VisitDate) AS day, 
        DATE_FORMAT(s.VisitDate, '%b %d %Y') AS date,
        s.origin,
        SUM(if(ca.organism = 2, 1, 0)) AS countGoats,
        SUM(if(ca.organism = 2 AND ca.sex = 'Female', 1, 0)) AS countGF,
        SUM(if(ca.organism = 3 AND ca.sex = 'Female', 1, 0)) AS countSF
FROM samples s JOIN custom_animals ca ON s.AnimalID = ca.animal_id
GROUP BY TO_DAYS(a.VisitDate);
</code></pre>

<p>I can't check query, I don't know what result you're expected and which tables/relations you have, so this is only example with idea.</p>

<p>If you need count unque AnimealID's for each day:</p>

<pre><code>SELECT SUM(byproj) AS countbyproj,
        day,
        date,
        origin,
        SUM(Goats) AS countGoats,
        SUM(GF) AS countGF,
        SUM(SF) AS countSF
FROM (
    SELECT  s.AnimealID,
            if(project = 5 AND AnimealID LIKE 'AVD%', 1, 0) AS byproj, 
            TO_DAYS(s.VisitDate) AS day, 
            DATE_FORMAT(s.VisitDate, '%b %d %Y') AS date,
            s.origin,
            if(ca.organism = 2, 1, 0)) AS Goats,
            if(ca.organism = 2 AND ca.sex = 'Female', 1, 0) AS GF,
            if(ca.organism = 3 AND ca.sex = 'Female', 1, 0) AS SF
    FROM samples s JOIN custom_animals ca ON s.AnimalID = ca.animal_id
    ) dataset
GROUP BY dataset.day, dataset.AnimealID;
</code></pre>


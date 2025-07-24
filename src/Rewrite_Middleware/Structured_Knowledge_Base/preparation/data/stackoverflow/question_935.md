# Unwanted Carthesian Product
[Link to question](https://stackoverflow.com/questions/50831181/unwanted-carthesian-product)
**Creation Date:** 1528874152
**Score:** 1
**Tags:** sql, join, multiple-tables
## Question Body
<p>I'm supposed to write a SQL query for our Visitor Management System.</p>

<p>To be precise I had one, but thanks to an Database Construction error or Something from a Third Party. There were Entries missing because of missing Values in a Table. The management database assigns a numeric Visitor ID. This Id is the only Key implemented.</p>

<p>To get the missing persons I need to write a query over three tables which are joined on the same identifier, the <code>Visitior ID</code>.</p>

<p>My SQL looks like this:</p>

<pre><code>SELECT
    ROW_NUMBER() OVER(ORDER BY VisitorBooking.Arrival ASC) AS Nr,
    Personalstamm.idPersonalstamm,
    CASE VisitRating.rating 
       WHEN 3 THEN 'Sehr Gut' 
       WHEN 2 THEN 'Gut' 
       WHEN 1 THEN 'Nicht so Gut' 
       ELSE 'Sonstiges' 
    END AS Bewertung, 
    VisitRating.Comment,
    VisitorBooking.Arrival,
    Personalstamm.Name,
    Personalstamm.FirstName,
    Personalstamm.Company,
    Personalstamm.Stadt
FROM
    Personalstamm 
INNER JOIN
    VisitRating ON Personalstamm.idPersonalstamm =  VisitRating.idPersonalstamm 
INNER JOIN
    VisitorBooking ON Personalstamm.idPersonalstamm =  VisitorBooking.idVisitor
WHERE
    Personalstamm.idPersonalstamm IS NOT NULL
ORDER BY
    VisitorBooking.Arrival
</code></pre>

<p>In <code>Personalstamm</code> are the personal dates like name and so on. </p>

<p>In <code>VisitRating</code> is a rating of the stay and a comment. </p>

<p>And I need <code>Visitorbooking</code> to catch the people who are not in visiting for unknown reasons.</p>

<p>My problem is, it does what it should do but builds the unwanted carthesian product out of <code>Visitorbooking</code> and <code>Visitor Rating</code>. What can I do to not get this? </p>

<p>Distinct didn't work, Group By also didn't work.</p>

<p>Sample data:</p>

<p><strong>Personalstamm</strong>:</p>

<pre><code>Name: x
Firstname: MR.
Primary Key ID: 1
Company: X-Files
Town: Gravity Falls
</code></pre>

<p><strong>VisitorBooking</strong>:</p>

<pre><code>Arrival: 06.13.2018 00:00:00
Departure: 01:30:57
ID Visitor: 1
</code></pre>

<p><strong>VisitRating</strong>:</p>

<pre><code>Rating: 3
Comment: I'm anonymous
Date: 06.13.2018
Foreign Key ID: 1
</code></pre>

<p>It should like </p>

<pre><code>1 MR. X Gravity Falls 06.13.2018 Sehr Gut I'm anonymous.
</code></pre>

<p>But there were several cases where everything from <code>Visitrating</code> was empty why I had to rewrite to get:</p>

<pre><code>1 MR. X Gravity Falls 06.13.2018 00:00:00 NULL NULL.
</code></pre>

<p>I replaced date with arrival.</p>

<p>But what I get when he visits more than once is:</p>

<pre><code>1 MR. X Gravity Falls 06.13.2018 00:00:00 Sehr Gut NULL.
1 MR. X Gravity Falls 06.13.2018 00:00:00 GUT NULL.
1 MR. X Gravity Falls 06.13.2018 00:00:00 Nicht so GUT NULL.

1 MR. X Gravity Falls 07.13.2018 00:00:00 Sehr Gut NULL.
1 MR. X Gravity Falls 07.13.2018 00:00:00 GUT NULL.
1 MR. X Gravity Falls 07.13.2018 00:00:00 Nicht so GUT NULL.
</code></pre>

## Answers
### Answer ID: 50836043
<p>If I understand correctly, then you want something like this:</p>

<pre><code>select . . . 
From Personalstamm p left join
     (select vr.*,
             row_number() over (partition by idPersonalstamm order by idPersonalstamm) as seqnum VisitRating vr
     ) vr
     on p.idPersonalstamm =  vr.idPersonalstamm left join
     (select vb.*,
             row_number() over (partition by idPersonalstamm order by idPersonalstamm) as seqnum       from VisitorBooking vb
     ) vb
     on p.idPersonalstamm = vb.idVisitor and
        vp.seqnum = vr.seqnum
where ps.idPersonalstamm is not null 
order by vb.Arrival;
</code></pre>

<p>Two important notes:</p>

<ul>
<li>This assumes that the number of visits is at least as big as the number of bookings.</li>
<li>I introduced table aliases, so you should fix the <code>SELECT</code> clause to use them instead of the full table name.</li>
</ul>


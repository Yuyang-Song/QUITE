# selecting the same column multiple time from 1 table via 3 inner joins
[Link to question](https://stackoverflow.com/questions/19659599/selecting-the-same-column-multiple-time-from-1-table-via-3-inner-joins)
**Creation Date:** 1383053412
**Score:** 0
**Tags:** mysql
## Question Body
<p>Working on a medical database.
We have a prescriptions table, a diagnosis table and an items table (every single item, not just meds).</p>

<p>In the diagnosis table, is a whole set of columns called med# (currently 13, may increase) that lists all the various medication the patient is prescribed. The names of the medicine are stored on the items table (because multi-lingual) To retrieve the name of medication 1~13, I'm using the below query.</p>

<p>It works, but I imagine that it's probably not very efficient.
Is there a better way to rewrite this?
Or maybe even redesign the database?
It's still early stages and the DB design isn't locked down yet.</p>

<pre><code>select d.name_en, e.name_en
from
    diag a
    inner join
pres c
    on a.med1 = c.id
    inner join
pres b
    on a.med2 = b.id
    inner join
items d
    on b.id = d.id
    inner join
items e
    on c.id = e.id
where a.id = 1
</code></pre>

## Answers
### Answer ID: 19659938
<p>You should have a table that holds patient information and another table that holds medication information. This will allow the number of medications to grow without table redesign.</p>

<p>In the medication information table, there should be a column to reference the item in the items table and a column to reference the patient in the patient information table. This will be the primary key of your medication information table.</p>


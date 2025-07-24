# MS Access - subquery does not work in Access (sql works)
[Link to question](https://stackoverflow.com/questions/55981606/ms-access-subquery-does-not-work-in-access-sql-works)
**Creation Date:** 1556965614
**Score:** 0
**Tags:** sql, database, date, ms-access
## Question Body
<p>I have an unusual problem. I'm creating an application in MS Access and while creating the code I came across an error. I started by looking for a solution on my own and finally found it. Generally, my Access code doesn't work because of a "stupid bug".</p>

<p>Look at the second answer with 13 advantages in this thread: <a href="https://stackoverflow.com/questions/1375207/how-do-i-perform-update-query-with-subquery-in-access">How do I perform update query with subquery in Access?</a> As you can see, MS Access does not allow you to perform a subquery (?) in the query. I created the same environment in SQL Server and it worked. Can someone help me rewrite my query?</p>

<p>SQL</p>

<pre><code>UPDATE DANE_BUD_ALL_BR 
SET ID_ewidencji = (
  SELECT ID_ewidencji FROM Ewidencje 
  WHERE Ewidencje.E_numerProjektu LIKE DANE_BUD_ALL_BR.numerProjektu
)
WHERE Identyfikator IN (
  SELECT b.Identyfikator 
  FROM DANE_BUD_ALL_BR b INNER JOIN Ewidencje e 
  ON e.E_numerProjektu = b.numerProjektu 
  WHERE e.E_numerProjektu LIKE b.numerProjektu
);
</code></pre>

<p>I would like the query to be executed in the same way as in SQL Server - because it works there.</p>

<p>//
There are two tables: 'ewidencje' and 'dane'. They are connected with the "ID_ewidencji", in both tables there is a 'numerProjektu' field (ignore the fact that it is a duplication of data in the database). Photo 1 shows the data before the SQL query. After my UPDATE inquiry, I would like the "ID_ewidencji" field in the "data" table to be completed on the basis of the same 'numerProjektu' from both tables. After the query (photo 2) we can see that it happened. However, access throws out an error: operation must use an update table query.</p>

<p><a href="https://i.sstatic.net/EKVoH.jpg" rel="nofollow noreferrer">This is photo 1</a>
<a href="https://i.sstatic.net/2PtHR.jpg" rel="nofollow noreferrer">This is photo 2</a></p>

## Answers
### Answer ID: 55981629
<p>Try phrasing this as:</p>

<pre><code>UPDATE DANE_BUD_ALL_BR
    SET ID_ewidencji = (SELECT ID_ewidencji
                        FROM Ewidencje as e
                        WHERE e.E_numerProjektu LIKE DANE_BUD_ALL_BR.numerProjektu
                       )
    WHERE EXISTS (SELECT 1
                  FROM Ewidencje as e
                  WHERE e.E_numerProjektu LIKE DANE_BUD_ALL_BR.numerProjektu
                 );
</code></pre>

<p>In other words, there is probably no reason to repeat the name of the table being updated in the subquery <code>FROM</code> clause.</p>

<p>EDIT:</p>

<p>Does the simple <code>JOIN</code> work in MS Access?</p>

<pre><code>UPDATE DANE_BUD_ALL_BR as bab INNER JOIN
       Ewidencje as e
       ON e.E_numerProjektu LIKE bab.numerProjektu
    SET bab.ID_ewidencji = e.ID_ewidencji;
</code></pre>

<p>This is the more colloquial way to write the logic in MS Access.</p>


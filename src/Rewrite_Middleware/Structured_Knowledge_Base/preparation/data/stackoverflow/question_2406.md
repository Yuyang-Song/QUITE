# SQL query hangs without error (parallel subquery?)
[Link to question](https://stackoverflow.com/questions/33215283/sql-query-hangs-without-error-parallel-subquery)
**Creation Date:** 1445260077
**Score:** 0
**Tags:** sql-server, stored-procedures
## Question Body
<p>I have a stored procedure running on a Microsoft SQL server 2012 database, which often (but not always!) hangs at a certain point. When I execute the specific update query itself, it runs fine, but if it's executed in the procedure as a whole, nothing happens after this point. This is where it goes wrong:</p>

<pre><code>    UPDATE dbo.gesch_gzp
    SET red_ges=1
    WHERE uitg_verr_id IN (
        SELECT uitg_verr_id
        FROM dbo.gzp_flagging_2
        WHERE flag BETWEEN 2200 AND 2299
            AND flag IN (
                SELECT flag 
                FROM flagging 
                WHERE lts=1
                )
            )
</code></pre>

<p>While looking at the waiting tasks (dm_os_waiting_tasks) I strongly got the impression that it has something to do with parallellism, since multiple subprocesses with the same session_id but different exec_context_id where waiting for each other. 
Therefore I already tried adding the OPTION(MAXDOP 1) and added a DISTINCT to the first select, but not with the desired effect (after restarting the stored procedure, it hang at exactly the same point). </p>

<pre><code>    UPDATE dbo.gesch_gzp
    SET red_ges=1
    WHERE uitg_verr_id IN (
        SELECT DISTINCT(uitg_verr_id)
        FROM dbo.gzp_flagging_2
        WHERE flag BETWEEN 2200 AND 2299
            AND flag IN (
                SELECT flag 
                FROM flagging 
                WHERE lts=1
                )
            )
    OPTION(MAXDOP 1)
</code></pre>

<p>So I'm wondering if there is a way to rewrite this stored procedure to prevent it from hanging. Complicating matter is that this troubled update query happens to be at the end of a long program wich takes >24 hours to execute. And executing the update query itself does not reproduce the problem (it takes a few minutes), so this makes testing a difficult thing.</p>

## Answers
### Answer ID: 33216367
<p>You can rewrite the UPDATE statement like this:</p>

<pre><code>UPDATE  gg
SET     gg.red_ges = 1
FROM    dbo.gesch_gzp gg
        INNER JOIN dbo.gzp_flagging_2 gf2 ON gg.uitg_verr_id = gf2.uitg_verr_id
        INNER JOIN flagging f ON gf2.flag = f.flag
WHERE   gf2.flag BETWEEN 2200 AND 2299
        AND f.lts = 1
</code></pre>

<p>However, I wouldn't think that would necessarily fix your issue.  You need to check what is actually happening while it is hanging.  If you don't have any blocking monitoring set up, start by running <code>exec sp_who2</code> while your query is hanging and check the BlkBy column to see what SPID is blocking.  Once you have the SPID you can find what SQL is blocking it and refactor your SQL.</p>


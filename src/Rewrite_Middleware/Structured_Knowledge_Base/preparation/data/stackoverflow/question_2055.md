# Linq-to-SQL left join on left join/multiple left joins in one Linq-to-SQL statement
[Link to question](https://stackoverflow.com/questions/17145640/linq-to-sql-left-join-on-left-join-multiple-left-joins-in-one-linq-to-sql-statem)
**Creation Date:** 1371465909
**Score:** 4
**Tags:** linq, linq-to-sql, stored-procedures, left-join
## Question Body
<p>I'm trying to rewrite SQL procedure to Linq, it all went well and works fine, as long as it works on small data set. I couldn't really find answer to this anywhere. Thing is, I have 3 joins in the query, 2 are <code>left joins</code> and 1 is <code>inner join</code>, they all join to each other/like a tree. Below you can see SQL procedure:</p>

<pre><code>SELECT ...
    FROM sprawa s (NOLOCK) 
        LEFT JOIN strona st (NOLOCK) on s.ident = st.id_sprawy
        INNER JOIN stan_szczegoly ss (NOLOCK) on s.kod_stanu = ss.kod_stanu
        LEFT JOIN broni b (NOLOCK) on b.id_strony = st.ident
</code></pre>

<p>What I'd like to ask you is a way to translate this to Linq. For now I have this:</p>

<pre><code>var queryOne = from s in db.sprawa
               join st in db.strona on s.ident equals st.id_sprawy into tmp1
               from st2 in tmp1.DefaultIfEmpty()
               join ss in db.stan_szczegoly on s.kod_stanu equals ss.kod_stanu
               join b in db.broni on st2.ident equals b.id_strony into tmp2
               from b2 in tmp2.DefaultIfEmpty()
               select new { };
</code></pre>

<p>Seems alright, but when checked with SQL Profiler, query that is sent to database looks like that:</p>

<pre><code>SELECT ... FROM    [dbo].[sprawa] AS [Extent1] 
           LEFT OUTER JOIN [dbo].[strona] AS [Extent2] 
                ON [Extent1].[ident] = [Extent2].[id_sprawy]    
           INNER JOIN [dbo].[stan_szczegoly] AS [Extent3] 
                ON [Extent1].[kod_stanu] = [Extent3].[kod_stanu]    
           INNER JOIN [dbo].[broni] AS [Extent4] 
                ON ([Extent2].[ident] = [Extent4].[id_strony]) OR 
                (([Extent2].[ident] IS NULL) AND ([Extent4].[id_strony] IS NULL))
</code></pre>

<p>As you can see both SQL queries are bit different. Effect is the same, but latter works incomparably slower (less than a second to over 30 minutes). There's also a <code>union</code> made, but it shouldn't be the problem. If asked for I'll paste code for it.</p>

<p>I'd be grateful for any advice on how to better the performance of my Linq statement or how to write it in a way that is translated properly.</p>

## Answers
### Answer ID: 18359087
<p>I guess I found the solution:</p>

<pre><code>var queryOne = from s in db.sprawa
               join st in db.strona on s.ident equals st.id_sprawy into tmp1
               where tmp1.Any()
               from st2 in tmp1.DefaultIfEmpty()
               join ss in db.stan_szczegoly on s.kod_stanu equals ss.kod_stanu
               join b in db.broni on st2.ident equals b.id_strony into tmp2
               where tmp2.Any()
               from b2 in tmp2.DefaultIfEmpty()
               select new { };
</code></pre>

<p>In other words <code>where table.Any()</code> after each <code>into table</code> statement. It doesn't make translation any better but has sped up execution time from nearly 30minutes(!) to about 5 seconds.</p>

<p>This has to be used carefully though, because it MAY lead to losing some records in result set.</p>


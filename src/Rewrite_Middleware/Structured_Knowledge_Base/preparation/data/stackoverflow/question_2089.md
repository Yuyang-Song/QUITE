# Multiple left joins in one query to Linq statement
[Link to question](https://stackoverflow.com/questions/18357998/multiple-left-joins-in-one-query-to-linq-statement)
**Creation Date:** 1377089659
**Score:** 0
**Tags:** sql, linq, linq-to-sql, stored-procedures
## Question Body
<p>I'm trying to rewrite SQL procedure to Linq, it all went well and works fine, as long as it works on small data set. I couldn't really find answer to this anywhere. Thing is, I have 3 joins in the query, 2 are left joins and 1 is inner join, they all join to each other/like a tree. Below you can see SQL procedure:</p>

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

<p>As you can see both SQL queries are bit different. Effect is the same, but latter works incomparably slower (less than a second to over 1 minute).
There's also a union made, but it shouldn't be the problem. If asked for I'll paste code for it.</p>

<p>I'd be grateful for any advice on how to better the performance of my Linq statement or how to write it in a way that is translated properly.</p>


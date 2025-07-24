# Long SQL subquery trouble
[Link to question](https://stackoverflow.com/questions/53090954/long-sql-subquery-trouble)
**Creation Date:** 1541015360
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>I just registered and want to ask.
I learn sql queries not so long time and I got a trouble when I decided to move a table to another database. A few articles were read about building long subqueries , but they didn't help me. 
Everything works perfect before that my action.
I just moved the table and tried to rewrite the query while whole day.</p>

<pre><code>update [dbo].Full
set [salary] = 1000
where [dbo].Full.id in (
    select distinct k1.id
    from (
        select id, Topic, User 
        from Full
        where User not in (select distinct topic_name from [DB_1].dbo.S_School)
    ) k1
    where k1.id not in (
        select distinct k2.id
        from (
            select id, Topic, User 
            from Full 
            where User not in (select distinct topic_name from [DB_1].dbo.Shool)
        ) k2,
        List_School t3
        where charindex (t3.NameApp, k2.Topic)&gt;5
    )
)
</code></pre>

<p>I moved table <code>List_School</code> to database <code>[DB_1]</code> and I can't to bend with it. 
I can't write <code>[DB_1].dbo.List_School</code>. Should I use one more subquery? 
I even thought about create a few temporary tables but it can influence on speed of execution. </p>

<p>Sql gurus , please invest some your time on me. Thank you in advance. </p>

<p>I will be happy for each hint, which you give me.  </p>

## Answers
### Answer ID: 53093490
<p>There appear to be a number of issues. You are comparing the user column to the topic_name column.  An expected meaning of those column names would suggest you are not comparing the correct columns.  But that is a guess.</p>

<p>In the final subquery you have an ansi join on table List_School but no join columns which means the join witk k2 is a cartesian product (aka cross join) which is not what you would want in most situations. Again a guess as no details of actual problem data or error messages was provided.</p>


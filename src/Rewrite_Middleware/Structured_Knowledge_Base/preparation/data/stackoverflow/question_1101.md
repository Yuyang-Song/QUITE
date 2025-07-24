# Parameter sniffing - only in stored procedures?
[Link to question](https://stackoverflow.com/questions/59197559/parameter-sniffing-only-in-stored-procedures)
**Creation Date:** 1575556928
**Score:** 0
**Tags:** sql-server
## Question Body
<p>We develop an application that works with MS SQL Server - our customers run anything from SQL 2008 Express to 2017 Standard. Our queries are not parameterised and it is impractical to rewrite the whole application so that they are. We therefore have a lot of plans for the same query. I have seen that there is an option in SSMS against the database to set Parameterisation to Forced, so that there will be fewer query plans, but that this can then cause issues with Parameter Sniffing with Stored Procedures.</p>

<p>Before I try changing that option, can I just clarify that Stored Procedures are pieces of code that you explicitly create and store in the database; running queries directly from the application do NOT get turned into Stored Procedures (even temporarily), so it isn't a problem.</p>

## Answers
### Answer ID: 59197798
<p>Parameter sniffing can happen to both stored procedure calls and parameterized queries. In your case, the best option is to fix your application, which will take considerable efforts. So before that can happen, set the Parameterisation to Forced will certainly help to reduce the number of plans and tighten the security.</p>

<p>and no, this will not change your queries to stored procedures.</p>


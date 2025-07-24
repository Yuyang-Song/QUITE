# ORA-00036: maximum number of recursive SQL levels (50) exceeded after configuring toplink to use bind variables
[Link to question](https://stackoverflow.com/questions/6070032/ora-00036-maximum-number-of-recursive-sql-levels-50-exceeded-after-configurin)
**Creation Date:** 1305884127
**Score:** 4
**Tags:** sql, oracle-database, triggers, toplink
## Question Body
<p>I have an application that uses Toplink for persistence and Oracle database. Recently I have had performance problems, especially on the db/query level. I have a big piece of logic in a bunch of triggers and stored procedures, badly written, with workarounds for the mutating trigger problem. The application is in production for a few years now, and rewriting this code the last solution, considering the bureaucracy of getting approval for a new release and other higher priorities. So I am looking for a quick fix.</p>

<p>One solution to improve the performance is to use bind variables. My problem is that after adding bind-all-variables and cache-all-statements in sessions.xml in toplink, on a certain UI, that triggers the crappy code, and worked just fine before making this config change, I get this error:</p>

<p>ORA-00036: maximum number of recursive SQL levels (50) exceeded</p>

<p>My questions are: why is it showing this error only after I add the bind-variable setting? What can I do to make it work with bind variables, without changing the crappy code?</p>

## Answers
### Answer ID: 6078264
<p>"with workarounds for the mutating trigger problem"</p>

<p>That sounds scary as most of those workarounds revolve around autonomous transactions which (a) don't work particularly well and (b) probably count as recursive SQL.</p>

<p>On the other hand, having logic in PL/SQL generally means the problem won't be bind variables, as you need to make a big effort in PL/SQL to not use binds.</p>

<p>In this case, I'd say your time is better spent on addressing/replacing any mutating table workarounds with a solid base rather than bind variable issues.</p>


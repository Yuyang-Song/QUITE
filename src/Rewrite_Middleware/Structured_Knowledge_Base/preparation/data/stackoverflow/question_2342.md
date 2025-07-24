# Entity Framework Issue When running Stored Procedures
[Link to question](https://stackoverflow.com/questions/30093308/entity-framework-issue-when-running-stored-procedures)
**Creation Date:** 1430979547
**Score:** 9
**Tags:** c#, sql-server, entity-framework, stored-procedures
## Question Body
<p>I have an issue with stored procedures and Entity Framework.</p>

<p>Let me explain what is happening... and what I have tried thus far.</p>

<p>I have a stored procedure, which does not do an awful lot</p>

<pre><code>SELECT 
    COUNT(DISTINCT(EmailAddress)) AcceptedQuotes, 
    CONVERT (DATE,QuoteDate) QuoteDate
FROM
    Quote Q
JOIN 
    Person P on Q.PersonPk = P.Pk
JOIN 
    Product Pr on Q.ProductPk = Pr.Pk
JOIN 
    Accepted A on Q.Pk = A.QuotePk
WHERE               
    QuoteDate between @startDate and @endDate
    AND CompanyPk = @companyPk
    AND FirstName != 'Test'
    AND FirstName != 'test'
    AND FirstName != 'EOH'
</code></pre>

<p>I want to execute this, and it works fine in SSMS and does not even take 1 second.</p>

<p>Now, I import this in to Entity Framework, it times out and I set the command timeout to 120...</p>

<p>Ok so what I have tried thus far and what I have tested.</p>

<p>If I use <code>SqlCommand</code>, <code>SqlDataAdapter</code>, <code>DataTable</code> way, with my own connection string, it executes as expected. When I use Entity Framework connection string in this scenario, it times out.</p>

<p>I altered my stored procedure to include "Recompile" option and also tried the <code>SET ARITHABORT</code> way, no luck, it times out when run through the EF.</p>

<p>Is this a bug in EF?</p>

<p>I have now just about decided to rewrite this using "old school" data access.</p>

<p>Also note that the EF executes fine with other stored procs, from the same database.</p>

<p>Any ideas or help would be greatly appreciated...</p>

<p>PS. I found this article, but no help either :(</p>

<p><a href="http://www.sommarskog.se/query-plan-mysteries.html">http://www.sommarskog.se/query-plan-mysteries.html</a></p>

## Answers
### Answer ID: 30286355
<p>This may be caused by <a href="http://blogs.technet.com/b/mdegre/archive/2012/03/19/what-is-parameter-sniffing.aspx" rel="nofollow">Parameter Sniffing</a></p>

<p>When a stored procedure is compiled or recompiled, the parameter values passed for that invocation are "sniffed" and used for cardinality estimation.  The net effect is that the plan is optimized as if those specific parameter values were used as literals in the query.</p>

<blockquote>
  <ol>
  <li>Using dummy variables that are not directly displayed on parameters also ensure execution plan stability without need to add recompile
  hint, example below:</li>
  </ol>
  
  <p>create procedure dbo.SearchProducts 
      @Keyword varchar(100) As Declare @Keyworddummy as varchar(100) Set @Keyworddummy = @Keyword select * from Products where Keyword like
  @Keyworddummy</p>
  
  <ol start="2">
  <li>To prevent this and other similar situations, you can use the following query option:</li>
  </ol>
  
  <p>OPTIMIZE FOR RECOMPILE</p>
  
  <ol start="3">
  <li>Disable auto-update statistics during the batch</li>
  </ol>
</blockquote>


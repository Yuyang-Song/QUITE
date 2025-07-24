# Best way to avoid repeated sub queries in SQL select statement
[Link to question](https://stackoverflow.com/questions/56684747/best-way-to-avoid-repeated-sub-queries-in-sql-select-statement)
**Creation Date:** 1561029179
**Score:** 3
**Tags:** sql, sql-server, t-sql, stored-procedures
## Question Body
<p>I am using a SQL stored procedure to retrieve data from my database. since am using multiple subqueries the query speed is very slow, please suggest the best way to rewrite the below query to avoid the subquery.</p>

<pre><code>    Select Companyid, 
           companyname, 
          (select count(distinct Identifier.SID) 
                  from CompaniesUsers   
                  join Identifier on CompaniesUsers.UniqueId = Identifier.UniqueId  
                 where Companies.CompanyId = CompaniesUsers.CompanyId 
                 and CompaniesUsers.IsActive = 1 
                 and Identifier.IsActive = 1 ) as CustomerCount,
         (select count(distinct CompaniesUsers.UniqueId) 
                 from CompaniesUsers    
                 where Companies.CompanyId = CompaniesUsers.CompanyId    
                 and CompaniesUsers.IsActive = 1 
                 and CompaniesUsers.UniqueId != '-'     )
         -      (Same query used in the CustomerCount) as AnonymousCustomerCount        
         from Companies where Companies.isactive = 1
</code></pre>

<p>Here I want to reuse the customer count query for the AnonymousCustomerCount. what is the best way to do this?</p>

## Answers
### Answer ID: 56684858
<p>You should be able to use a common table expression to make the query easier to read:</p>

<pre><code>with 
 customer_count as 
   (select query with joining of 2 tables), 
 user_count as
   (Subquery to get total count by joining 2 tables)

Select Companyid,
companyname,
customer_count.column_name, 
customer_count.column_name - user_count.column_name
from CompanyTable
join customer_count on ?
join user_count on ?
</code></pre>

<p>It's not certain this will improve performance though...</p>

### Answer ID: 56684854
<p>Try Outer Apply and see if it works for you:</p>

<pre><code>Select Companyid,
companyname,
CustomerCount.Count,
TotalCount.Total - CustomerCount.Count as AnonymousCustomerCount
from CompanyTable
OUTER APPLY (
select Count
  joining of 2 tables
) AS CustomerCount
OUTER APPLY (
  Subquery Total to get total count by joining 2 tables
) AS TotalCount
</code></pre>


# MS SQL query optimization
[Link to question](https://stackoverflow.com/questions/29744091/ms-sql-query-optimization)
**Creation Date:** 1429522359
**Score:** 0
**Tags:** sql-server, optimization
## Question Body
<p>I experiencing performance issues with pretty simple query. </p>

<pre><code>--All Windows Servers
with t1 (Name, [OS Name]) as
(
(select Name, [OS Name] from ComputerInfo where [OS Name] like '%windows%server%')

union all

--All non-Windows Servers
(select Name, [OS Name] from ComputerInfo
except
select Name, [OS Name] from ComputerInfo where [OS Name] like '%windows%')
)

select distinct ci.guid,t1.Name, t1.[OS Name],
    'System Type' = case
        when ci.[System Type] = ''
        then 'Unknown'
        else ci.[System Type]
    end, 
    'Virtualization Status' = case
        when (ci.guid in (select guid from VirtualMachineInfo))
        then 'Virtual'
        else 'Physical'
    end,
ci.Server
from t1
join ComputerInfo ci on t1.Name = ci.Name
order by t1.Name
</code></pre>

<p>The idea is that i select and separate virtual and physical servers by using existing inventory data that stored in our DB. The issue is that this query runs very, VERY slowly even on test DB needless to say about production.</p>

<p>I understand that probably i have chosen not optimal way to get the data i want, but unfortunately because of lack of skills i'm unable to rewrite or optimise this query.</p>

<p>I really appreciate any help, and would be glad to see any advice.</p>


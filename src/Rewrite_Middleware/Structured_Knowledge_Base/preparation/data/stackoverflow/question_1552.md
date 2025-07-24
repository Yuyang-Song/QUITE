# What causes this error: &quot;There is insufficient system memory in resource pool &#39;internal&#39; to run this query&quot;?
[Link to question](https://stackoverflow.com/questions/9432515/what-causes-this-error-there-is-insufficient-system-memory-in-resource-pool-i)
**Creation Date:** 1330094353
**Score:** 2
**Tags:** sql-server, tridion
## Question Body
<p>I occasionally get this error message on a Tridion 2011 SP1 development machine:</p>

<blockquote>
  <p>There is insufficient system memory in resource pool 'internal' to run this query.
  Unable to save Schema (tcm:0-0-0). A database error occurred while executing Stored Procedure "EDA_ORG_ITEMS_FINDUNIQUENESSCONFLICTS".EDA_ORG_ITEMS_FINDUNIQUENESSCONFLICTS</p>
</blockquote>

<p>Searching for the error message here on StackOverflow suggests rewriting the stored procedure to not use temporary tables. Without doing that, does anyone know how to get rid of this error message?</p>

## Answers
### Answer ID: 9624039
<p>Although it is hard to be certain that the upgrade fixed it, the problem hasn't occurred anymore after upgrading SQL Server 2008 R2 to SP1.</p>


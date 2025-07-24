# Regex with SQL Server 2008 CLR performance issues
[Link to question](https://stackoverflow.com/questions/31278059/regex-with-sql-server-2008-clr-performance-issues)
**Creation Date:** 1436298707
**Score:** 1
**Tags:** regex, sql-server-2008, sqlclr
## Question Body
<p>I am trying to understand why is it taking so long to execute a simple query.
In my local machine it takes 10 seconds but in production it takes 1 min.
(I imported the database from production into my local database)</p>

<pre><code>select * 
from JobHistory
where dbo.LikeInList(InstanceID, 'E218553D-AAD1-47A8-931C-87B52E98A494') = 1
</code></pre>

<p>The table <code>DataHistory</code> is not indexed and it has 217,302 rows</p>

<pre><code>public partial class UserDefinedFunctions
{
    [SqlFunction]
    public static bool LikeInList([SqlFacet(MaxSize = -1)]SqlString value, [SqlFacet(MaxSize = -1)]SqlString list)
    {
        foreach (string val in list.Value.Split(new char[] { ',' }, StringSplitOptions.None))
        {
            Regex re = new Regex("^.*" + val.Trim() + ".*$", RegexOptions.IgnoreCase);

            if (re.IsMatch(value.Value))
            {
                return(true);
            }
        }

        return (false);
    }
};
</code></pre>

<p>And the issue is that if a table has 217k rows then I will be calling that function 217,000 times! not sure how I can rewrite this thing.</p>

<p>Thank you</p>

## Answers
### Answer ID: 31288390
<p>There are several issues with this code:</p>

<ol>
<li>Missing <code>(IsDeterministic = true, IsPrecise = true)</code> in <code>[SqlFunction]</code> attribute. Doing this (mainly just the <code>IsDeterministic = true</code> part) will allow the SQLCLR UDF to participate in parallel execution plans. Without setting <code>IsDeterministic = true</code>, this function will prevent parallel plans, just like T-SQL UDFs do.</li>
<li>Return type is <code>bool</code> instead of <code>SqlBoolean</code></li>
<li>RegEx call is inefficient: using an instance method once is expensive. Switch to using the static <code>Regex.IsMatch</code> instead</li>
<li><p>RegEx pattern is <em>very</em> inefficient: wrapping the search string in "^.*" and ".*$" will require the RegEx engine to parse <em>and</em> retain in memory as the "match", the entire contents of the <code>value</code> input parameter, for every single iteration of the <code>foreach</code>. Yet the behavior of Regular Expressions is such that simply using <code>val.Trim()</code> as the entire pattern would yield the exact same result.<br>
<br></p></li>
<li><p>(optional) If <em>neither</em> input parameter will ever be over 4000 characters, then specify a <code>MaxSize</code> of <code>4000</code> instead of <code>-1</code> since <code>NVARCHAR(4000)</code> is much faster than <code>NVARCHAR(MAX)</code> for passing data into, and out of, SQLCLR objects.</p></li>
</ol>


# Dynamic Cursor Function to calculate running total
[Link to question](https://stackoverflow.com/questions/23400132/dynamic-cursor-function-to-calculate-running-total)
**Creation Date:** 1398902680
**Score:** 0
**Tags:** sql-server
## Question Body
<p><strong>Background:</strong></p>

<p>I frequently need to calculate running totals for several different tables in a database.</p>

<p>Afer several hours of research on running total calculations (the most useful explanation for me was probably <a href="https://stackoverflow.com/questions/11310877/calculate-running-total-running-balance">this</a> post on Stackoverflow which gives a brief summary of each method) I chose the cursor approach which works very well.</p>

<p><strong>Problem:</strong></p>

<p>I have to rewrite the running total cursor for each of the different tables I want to calculate running totals for and I want to know whether there are any workarounds for this? Is it possible to create a function that takes table/column names as input parameters and returns a table with the running total?</p>

<p><strong>My Attempt:</strong></p>

<p>My first step was to create a dynamic query which uses several variables (I do have checks in place to make sure the table and columns exist):</p>

<pre><code>    SET @SQLStatement   = '
            DECLARE rt_cursor CURSOR
                FOR
             SELECT ' + @DateColumn + ', SUM(' + @ValueColumn + ')
               FROM ' + @TableName + '
           GROUP BY ' + @DateColumn + '
           ORDER BY ' + @DateColumn

   EXEC sp_executesql @sqlstatement

   OPEN rt_cursor
</code></pre>

<p>which works well...</p>

<p>I then tried to incorporate this into a function however (for reasons that are now very clear to me) this didn't work (EXEC IN Function Does Not Work)</p>

<p>...So I decided to ask for help.</p>

<p><strong>PS:</strong> I'm a novice, newbie, what-ever-you-like-to-call-it and while I appreciate criticism, I just want to get this working as best I can. I only do this part-part-time and don't have time to learn all the ins-and-outs and dos-and-donts of proper SQL so a solution rather than a theory lesson would be appreciated - even if it is just "This Won't Work".</p>

<p>Thanks everyone!</p>

## Answers
### Answer ID: 23401651
<p>It sounds like you just need to create a stored procedure instead, which will allow you to do everything you want.  The procedure would take in your variables as parameters (@DateColumn, @TableName, etc.). </p>

<p>You've got a couple of options for returning your results:</p>

<ol>
<li>You could create a temp table before calling the procedure that the procedure fills.</li>
<li>Return the results at the end of the procedure, and upon calling, you can drop the results into a table.</li>
<li>If you already have a table to store results, just insert them at the end of your procedure</li>
</ol>


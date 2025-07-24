# In PL/SQL, how do I use a varaible in a SELECT *without* using an INTO?
[Link to question](https://stackoverflow.com/questions/25412274/in-pl-sql-how-do-i-use-a-varaible-in-a-select-without-using-an-into)
**Creation Date:** 1408560623
**Score:** 2
**Tags:** oracle-database, plsql, oracle-sqldeveloper, plsqldeveloper
## Question Body
<p>I'm experimenting with queries in an Oracle database (Using Oracle SQl Developer and PL/SQL Developer)</p>

<p>If I run a simple query: (<code>SELECT * FROM myTable WHERE id = 1234</code>) the results display in a nice grid in a lower pane of the SQL tool.</p>

<p>Now, how do I rewrite that query, using a variable for the <code>1234</code>, And STILL have the results spill out into the results pane.  Everything I've tried either won't compile, or requires me to do a <code>SELECT...INTO</code> and then manually output the results.</p>

<p>I just want to do something along the lines of this, and have it work:</p>

<pre><code> DECLARE p0 = 1234;
 SELECT * FROM myTable WHERE id = p0;
</code></pre>

<p>UPDATE:
In the actual query I'm working on, the variables will be more like:</p>

<pre><code> DECLARE p0 = to_date('1/15/2014 7:11:05 AM','MM/DD/YYYY HH:MI:SS PM');
         p1 = p0 + .0007; -- one minute later.
</code></pre>

<p>So being able to write that in code is important.</p>

## Answers
### Answer ID: 38460689
<p>As a minor variation on Luke's excellent answer, you don't even need a ref cursor if you just want to display a variable's value. Put this in a Test window:</p>

<pre><code>declare
    p0 date := to_date('1/15/2014 7:11:05 AM', 'MM/DD/YYYY HH:MI:SS PM');
begin
    :p1 := p0 + .0007;
end;
</code></pre>

<p>then set up the <code>p1</code> bind variable in the lower panel. Executing it will display the value.</p>

### Answer ID: 25413408
<p>One thing you can try is to create a bind variable named <code>cur</code>, for example, of type <code>REFCURSOR</code>, use <code>OPEN :cur FOR SELECT ...</code> in your PL/SQL block and then <code>PRINT</code> the cursor out.  Here's an example with a very simple query:</p>

<pre><code>VARIABLE cur REFCURSOR

BEGIN
  OPEN :cur FOR SELECT * FROM DUAL;
END;
/

PRINT cur
</code></pre>

<p>This works in SQL*Plus and SQL Developer, although in the latter it will only work if you use the 'Run Script (F5)' button, not the 'Run Statement (Ctrl+Enter)' button.  Also, you don't get a table with the results in, just the query output in preformatted text.  Also,  it won't necessarily work in other tools, as <code>VARIABLE</code> and <code>PRINT</code> are not part of SQL nor PL/SQL - SQL*Plus and SQL Developer both understand them and can interpret them.</p>

<p>In PL/SQL Developer you can use a Test Window for this kind of thing.  For example, enter into a Test Window a PL/SQL block such as </p>

<pre><code>BEGIN
  OPEN :cur FOR SELECT * FROM DUAL;
END;
</code></pre>

<p>Then, either add the variable <code>cur</code> of type 'Cursor' to the variables table at bottom of the window, (or choose Scan Variables from the context menu.  Note that PL/SQL Developer won't necessarily get the type right; you may well still have to change the type.  Once you run the block, the results from the cursor can be obtained in a separate window by clicking the '...' button in the row in the variables table for <code>cur</code>. </p>

### Answer ID: 25413271
<p>In Toad (or sqlplus or SQL Developer) you would do:</p>

<pre><code>define x='20140820';
select to_date(&amp;x, 'YYYYMMDD') from dual;
</code></pre>

<p>And run as a Script (important).</p>

<p>In Toad, the Output grid would be:</p>

<pre><code>old: select to_date(&amp;x, 'YYYYMMDD') from dual
new: select to_date(20140820, 'YYYYMMDD') from dual

TO_DATE(20140820,'YYYYMMDD')
----------------------------
20-AUG-2014                 
1 row selected.
</code></pre>

<p>And Grid1 would just show the results in table grid format.</p>

<p>Note that you can suppress the old/new in output by doing:</p>

<pre><code>set verify off
</code></pre>

<p>at top of script.</p>


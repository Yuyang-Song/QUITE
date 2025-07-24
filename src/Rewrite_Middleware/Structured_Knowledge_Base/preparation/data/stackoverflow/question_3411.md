# Clarification of converting Implicit outer joins to ANSI joins
[Link to question](https://stackoverflow.com/questions/78933065/clarification-of-converting-implicit-outer-joins-to-ansi-joins)
**Creation Date:** 1725036642
**Score:** 1
**Tags:** sql, sql-server, t-sql, sybase
## Question Body
<p>As part of the modernization effort (move from Sybase ASE to SQL Server), we are removing old implicit join operators and rewriting SQL using ANSI join style.</p>
<p>When running both queries, I saw that my new query was wrong (returned fewer rows) and figured out how to fix it...</p>
<p>Implicit join SQL:</p>
<pre><code>SELECT c.code_id ,  
    c.code_type_id ,  
    c.code_desc,  
    'N' AS orig_status,  
    'N' AS current_status,  
    sr.staff_role_id AS staff_role_id 
FROM code c, staff_role sr 
WHERE c.code_id *= sr.staff_role_cd 
    AND c.code_type_id = :app_cd  -- strings beginning with : are parameters to be swapped out, like @app_cd.
    AND code_active = 'Y'  
    AND sr.staff_id = :staff_id 
</code></pre>
<p>Fixed ANSI join style SQL</p>
<pre><code>SELECT c.code_id ,  
    c.code_type_id,  
    c.code_desc,  
    'N' AS orig_status,  
    'N' AS current_status,  
    sr.staff_role_id AS staff_role_id 
FROM code c  
LEFT OUTER JOIN  staff_role AS sr ON (c.code_id = sr.staff_role_cd)  
    AND sr.staff_id = :staff_id  &quot; &lt;---- WHY did this need to move here?
WHERE 
    c.code_type_id = :app_cd 
    AND code_active = 'Y'  
    //&lt;- sr.staff_id check used to be here...
</code></pre>
<p>I get that the table uses <code>staff_id</code> in it's join, but I don't understand why it had to be moved from the <code>where</code> clause and into the <code>on</code> clause.</p>
<p><code>staff_role_code</code> is a table that lets us connect a
<code>staff(staff table, PK staff_id)</code>,</p>
<p>to the code <code>(Code table, PK code_id, contains the code for all the roles, (and a bunch of other stuff))</code></p>
<p>That's used for a role.</p>
<p>So I don't understand why we needed to move the <code>staff_id</code> check, but not the code check.</p>
<p>What exactly is changed with and in the join clause instead of the where, and what does it do?</p>
<p>How do I identify when this change is needed in the future? All I have now is running both SQL in the ASE database and seeing if the results match.</p>
<h2>Note on possible duplicate</h2>
<p>Please notice that the table that was added was not the right or left-hand table in the outer join, so the linked questions don't seem to address this particular case, where the added &quot;join&quot; is on a Foreign Key shared by the two tables, not a primary key of either of the tables.</p>


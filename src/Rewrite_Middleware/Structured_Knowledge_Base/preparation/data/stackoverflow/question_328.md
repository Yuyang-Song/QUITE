# Database Technology - postgresql
[Link to question](https://stackoverflow.com/questions/20915908/database-technology-postgresql)
**Creation Date:** 1388800872
**Score:** -2
**Tags:** sql, database, postgresql
## Question Body
<p>I am quite new to postgresql. Could any expert help me solve this problem please.     </p>

<p>Consider the following PostgreSQL tables created for a university system recording which students take which modules:</p>

<pre><code>CREATE TABLE module (id bigserial, name text);
CREATE TABLE student (id bigserial, name text);
CREATE TABLE takes (student_id bigint, module bigint);
</code></pre>

<ol>
<li><p>Rewrite the SQL to include sensible primary keys. </p>

<pre><code>CREATE TABLE module
(
m_id bigserial,
name text,
CONSTRAINT m_key PRIMARY KEY (m_id)
);

CREATE TABLE student
(
s_id bigserial,
name text
CONSTRAINT s_key PRIMARY KEY (s_id)
);

CREATE TABLE takes
(
student_id bigint,
module bigint,
CONSTRAINT t_key PRIMARY KEY (student_id)
);
</code></pre></li>
</ol>

<p>Given this schema I have the following questions:</p>

<ol>
<li><p>Write an SQL query to count how many students are taking DATABASE.</p>

<pre><code>SELECT COUNT(name) 
FROM student
WHERE module = 'DATABASE' AND student_id=s_id 
</code></pre></li>
<li><p>Write an SQL query to show the student IDs and names (but nothing else) of all student taking DATABASE</p>

<pre><code>SELECT s_id, name
FROM Student, take 
WHERE module = 'DATABASE' AND student_id = s_id
</code></pre></li>
<li><p>Write an SQL query to show the student IDs and names (but nothing else) of all students not taking DATABASE. </p>

<pre><code>SELECT s_id, name
FROM Student, take 
WHERE student_id = s_id AND module != 'DATABASE'
</code></pre></li>
</ol>

<p>Above are my answers. Please correct me if I am wrong and please comment the reason. Thank you for your expertise.</p>

## Answers
### Answer ID: 20917122
<p>This looks like homework so I'm not going to give a detailed answer. A few hints:</p>

<ul>
<li><p>I found one case where you used <code>´</code> quotes instead of <code>'</code> apostrophes. This suggests you're writing SQL in something like Microsoft Word, which does so-called "smart quotes. Don't do that. Use a sensible text editor. If you're on Windows, Notepad++ is a popular choice. (Fixed it when reformatting the question, but wanted to mention it.)</p></li>
<li><p>Don't use the legacy non-ANSI join syntax <code>JOIN table1, table2, table3 WHERE ...</code>. It's horrible to read and it's much easier to make mistakes with. You should never have been taught it in the first place. Also, qualify your columns - <code>take.module</code> not just <code>module</code>. Always write ANSI joins, e.g. in your example above:</p>

<pre><code>FROM Student, take 
WHERE module = 'DATABASE' AND student_id = s_id
</code></pre>

<p>becomes</p>

<pre><code>FROM student 
INNER JOIN take 
        ON take.module = 'DATABASE' 
       AND take.student_id = student.s_id;
</code></pre>

<p>(if the table names are long you can use <em>aliases</em> like <code>FROM student s</code> then <code>s.s_id</code>)</p></li>
<li><p>Query 3 is totally wrong. Imagine if <code>take</code> has two rows for a student, one where the student is taking <code>database</code> and one where they're taking <code>cooking</code>. Your query will still return a result for them, even though they're taking <code>database</code>. (It'd also return the same student ID multiple times, which you don't want). Think about <a href="http://www.postgresql.org/docs/current/static/functions-subquery.html" rel="nofollow">subqueries</a>. You will need to query the <code>student</code> table, using a  <code>NOT EXISTS (SELECT .... FROM take ...)</code> to <em>filter out</em> students who are not taking <code>database</code>. The rest you get to figure out on your own.</p></li>
</ul>

<p>Also, your schemas don't actually enforce the constraint that a student may only take <code>DATABASE</code> once at a time. Either add that, or consider in your queries the possibility that a student might be registered for <code>DATABASE</code> twice.</p>


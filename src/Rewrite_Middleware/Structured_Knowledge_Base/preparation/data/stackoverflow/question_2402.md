# Preventing SQL Injection in PHP without parameterized queries?
[Link to question](https://stackoverflow.com/questions/32903339/preventing-sql-injection-in-php-without-parameterized-queries)
**Creation Date:** 1443774755
**Score:** 5
**Tags:** php, mysql, security, sql-injection
## Question Body
<p>I know this topic has been covered to death but I would like some feedback from the community regarding security within our web application.</p>

<p>We have standard LAMP stack web app which contains a large number of database queries which are executed using <code>mysqli_query</code>. These queries are not parameterized and at the moment but there is some naive escaping of the inputs using <code>addslashes</code>.</p>

<p>I have been tasked with making this system safer as we will be penetration tested very shortly. The powers above know that parameterized queries are the way to go to make the system safer however they don't want to invest the time and effort into re-writing all the queries in the application and also changing the framework we have to make them all work correctly.</p>

<p>So basically I'm asking what my options are here?</p>

<p>I've run <code>mysqli_real_escape_string</code> over the inputs. I've setup a filter which doesn't allow words like SELECT, WHERE, UNION to be passed in which I guess makes it safer. I know <code>mysqli_query</code> only allows one query to be run at once so there's some security there (from concatenating updates onto the end of of selects).</p>

<p>Do I have any other options here?</p>

<p>Edit: I should probably add that if anyone is able to provide an example of an attack which is completely unavoidable without parameterized queries that would also be helpful. We have a query which looks like this:</p>

<pre><code>SELECT
pl.created
p.LoginName,
pl.username_entered,
pl.ip_address
FROM loginattempts pl
LEFT JOIN people p ON p.PersonnelId = pl.personnel_id
WHERE p.personnelid = $id
AND pl.created &gt; $date1
AND pl.created &lt; $date2
</code></pre>

<p>I've substituted a UNION query into the $id <code>UNION SELECT * FROM p WHERE 1 = 1</code> sort of thing and I can prevent that by not allowing SELECT/UNION but then I'm sure there are countless other types of attack which I can't think of. Can anyone suggest a few more?</p>

<p><strong>Update</strong></p>

<p>I've convinced the powers that be above me that we need to rewrite the queries to parameterized statements. They estimate it will take a few months maybe but it has to be done. Win. I think?</p>

<p><strong>Update2</strong></p>

<p>Unfortunately I've not been able to convince the powers that be that we need to re-write all of our queries to parameterized ones.
The strategy we have come up with is to test every input as follows:</p>

<p>If the user supplied input is_int that cast it as so.
Same for real numbers.
Run mysqli_real_escape_string over the character data.
Change all the parameters in the queries to quoted strings i.e.</p>

<pre><code>WHERE staffName = ' . $blah . '
</code></pre>

<p>In accordance with <a href="https://stackoverflow.com/a/12118602/1261671">this</a> answer we are 100% safe as we are not changing the character set at any time and we are using PHP5.5 with latin1 character set at all times.</p>

<p><strong>Update 3</strong></p>

<p>This question has been marked as a duplicate however in my mind the question is still not followed answered. As per update no.2 we have found some strong opinion that the mysqli_real_escape string function can prevent attacks and is apparently "100% safe". No good counter argument has since been provided (i.e. a demonstration of an attack which can defeat it when used correctly).</p>

## Answers
### Answer ID: 32903496
<blockquote>
<p>Do I have any other options here?</p>
</blockquote>
<p>No. No external measure, like ones you tried to implement, has been proven to be of any help. Your site is still vulnerable.</p>
<blockquote>
<p>I've run mysqli_real_escape_string over the inputs</p>
</blockquote>
<p>Congratulations, you just reinvented the notorious <code>magic_quotes</code> feature, that proven to be useless and now expelled from the language.</p>
<p>JFYI, mysqli_real_escape_string has nothing to do with SQL injections at all.</p>
<p>Also, combining it with existing <code>addslashes()</code> call, you are spoiling your data, by doubling number of slashes in it.</p>
<blockquote>
<p>I've setup a filter which I guess makes it safer.</p>
</blockquote>
<p>It is not. SQL injection is not about adding some words.</p>
<p>Also, this approach is called &quot;Black-listing&quot; it is proven to be essentially unreliable. A black list is essentially incomplete, no matter how many &quot;suggestions&quot; you can get.</p>
<blockquote>
<p>I know mysqli_query only allows one query to be run at once so there's some security there</p>
</blockquote>
<p>There is not. SQL injection is not about adding another query.</p>
<hr />
<h3>Why did I close this question as a duplicate for &quot;How can I prevent SQL-injection in PHP?&quot;?</h3>
<p>Because these questions are mutually exclusive, and cannot coexist on the same site.</p>
<p>If we agree, that the only proper answer is using prepared statements, then a question asks &quot;How can I protect using no prepared statements&quot; makes very little sense.</p>
<p>At the same time, if the OP manages to force us to give the positive answer they desperately wants, it will make the other question obsoleted. Why use prepared statements if everything is all right without them?</p>
<p>Additionally, this particular question is too localized as well. It seeks not insight but <em>excuse</em>. An excuse for nobody but the OP personally only. An excuse that let them to use an approach that proven to be insecure. Although it's up to them, but this renders this question essentially useless for the community.</p>

### Answer ID: 32903713
<ul>
<li>check every single user input for datatype and where applicabile with regular expressions (golden rule is: never EVER trust user input)</li>
<li>use prepared statements</li>
<li>seriously: prepared statements :)</li>
</ul>

<p>it's a lot of work especially if your application is in bad shape (like it seems to be in your case) but it's the best way to have a decent security level</p>

<p>the other way (which i'm advising against) could be virtual patching using mod_security or a WAF to filter out injection attempts but first and foremost: try to write robust applications
(virtual patching might seem to be a lazy way to fix things but takes actually a lot of work and testing too and should really only be used on top of an already strong application code)</p>


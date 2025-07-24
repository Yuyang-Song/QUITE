# Host will not allow Mysql Sub Queries, Can this be done any other way?
[Link to question](https://stackoverflow.com/questions/20378202/host-will-not-allow-mysql-sub-queries-can-this-be-done-any-other-way)
**Creation Date:** 1386168005
**Score:** -1
**Tags:** php, mysql, subquery
## Question Body
<pre><code>SELECT * FROM(SELECT * FROM `finishes` Order by `finish`, `fdate` DESC) AS `output`
GROUP BY `finish`
</code></pre>

<p>The above works perfectly on my localhost machine, but on uploading it to my Servage hosting (naming and shaming!) it falls over and throws out a syntax error, when i asked Servage why this was and whether support for subqueries could be enabled, they flatly refused saying its not supported on their servers! (poor customer service as usual, which ive come to expect from them.)</p>

<p>Anyhow.. is there any way to rewrite the above without sub queries, all i want to do is get the latest entry in the table , grouped by finish , but it needs to show other data that belongs to that row. I tried max (fdate), and although this pulled the right date, it still showed data in other columns from the first entry in the database, not the last.</p>

<p>Scratching my head on this one.</p>

<p>Paul</p>

## Answers
### Answer ID: 20378463
<p>It may work perfectly for you now, but it may not always work perfectly. (MySQL allows you to use a GROUP BY clause like this, but does not guarantee which values for the other fields will be returned)</p>

<p>Try this</p>

<pre><code>SELECT `finishes`.*
FROM `finishes`
JOIN (SELECT `finish`, MAX(fdate) as `latest`
      FROM `finishes`
      GROUP BY `finish`) AS T1
  ON T1.`finish` = `finishes`.`finish`
   AND T1.`latest` = `finishes`.`fdate`
</code></pre>


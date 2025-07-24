# SQL join or union
[Link to question](https://stackoverflow.com/questions/16390286/sql-join-or-union)
**Creation Date:** 1367797432
**Score:** -2
**Tags:** mysql, sql
## Question Body
<p>I have 1 union query already done, the issue is it prints out the entire course list from the database. here is my statement:</p>

<pre><code>SELECT id, parent, name, 'category' AS `type`
FROM course_categories
UNION ALL
SELECT ( 1000 + id ) AS id, category, fullname, 'fullname' AS `type`
FROM course
</code></pre>

<p>I want to join with this table: </p>

<p>org_courses
id
orgid
courseid</p>

<p>I'm having issues getting the correct results and I'm trying to keep the aliases the same in the first query because i have a rendertree function that prints these out in a nice ul, li, so i'm tryng not to have to rewrite it. Any help in joining these is much appreciated.</p>

## Answers
### Answer ID: 16390332
<p>Put the first one in a sub-query like this:</p>

<pre><code>SELECT *
FROM (
  SELECT id, parent, name, 'category' AS `type`
  FROM course_categories
  UNION ALL
  SELECT ( 1000 + id ) AS id, category, fullname, 'fullname' AS `type`
  FROM course
) courses
INNER JOIN org_courses 
  ON org_course.courseid = courses.id
</code></pre>


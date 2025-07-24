# MySQL - How to indicate whether a user apply for a job or not?
[Link to question](https://stackoverflow.com/questions/8410177/mysql-how-to-indicate-whether-a-user-apply-for-a-job-or-not)
**Creation Date:** 1323229852
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have a database schema like this picture:</p>

<p><img src="https://i.sstatic.net/yBAnZ.png" alt="enter image description here"></p>

<p>I want to write a query that select data of all 6 tables and a field that indicate whether a specific user applied for a job or not.</p>

<p>I've tried:</p>

<pre><code>SELECT j.id, j.expired_date, j.title, j.views, j.status
   , j.unread, j.applicants, j.location, j.created_date
   , j.contract_type, c.country
   , group_concat(DISTINCT jp.page_name) AS fan_pages
   , group_concat(DISTINCT jp.id_page) AS id_pages
   , app.id AS applied
FROM jobs AS j
INNER JOIN country AS c ON c.id = j.country
LEFT JOIN job_pages AS jp ON jp.id_job = j.id
LEFT JOIN applications AS app ON app.id_job = j.id
LEFT JOIN resumes AS res ON res.id = app.id_resume
LEFT JOIN applicants AS alc ON alc.id = res.id_applicant
   AND alc.id_user = 15
WHERE ( j.status = 0 )
   AND ( j.expired_date = 0
      OR j.expired_date &gt; 1323228856 )
GROUP BY `j`.`id`
ORDER BY `j`.`id` desc
LIMIT 5 OFFSET 5
</code></pre>

<p>But it return a result that indicates a job was applied by any user. How can I rewrite this query?</p>

## Answers
### Answer ID: 8411619
<p>-- Edit --</p>

<p>Below is a basic ERD for how it would be easier to track users who have applied to jobs. I made the relationship between User and Resume a 1:M, in case you wanted to track resume versions. If not, it should be a 1:1 relationship. </p>

<p>So given the ERD, you have a user apply to a job with a resume. If you want to make the resume optional, then you remove the Resume table from the M:M with Job and link directly to User.</p>

<p>Just some ideas...</p>

<p><img src="https://i.sstatic.net/lSsVD.png" alt="enter image description here"> </p>

<p>-- Original --</p>

<p>Just some advice. </p>

<p>Seems to me that you may need to re-visit the schema design. It seems like the applicants table should be a pivot table between the users and jobs tables. The users and jobs table have a M:M relationship in that many users can apply to many jobs and many jobs can be applied to by many users. The applicants table should act as a transactional table when a user applies to a job.</p>

<p>Also, shouldn't the resumes table be directly linked to the users table? How can an application own a resume?</p>

<p>User owns a resume.</p>

<p>User applies to a job with a resume (applicant).</p>

### Answer ID: 8411488
<p>Try it,</p>

<pre><code>SELECT j.id_user as creator, alc.id_user as applier, j.id , j.expired_date, j.title, j.views, j.status
   , j.unread, j.applicants, j.location, j.created_date
   , j.contract_type, c.country
   , group_concat(DISTINCT jp.page_name) AS fan_pages
   , group_concat(DISTINCT jp.id_page) AS id_pages
   , MAX(app.id) AS applied
FROM jobs AS j
INNER JOIN country AS c ON c.id = j.country
LEFT JOIN job_pages AS jp ON jp.id_job = j.id
LEFT JOIN applications AS app ON app.id_job = j.id
LEFT JOIN resumes AS res ON res.id = app.id_resume
LEFT JOIN applicants AS alc ON alc.id = res.id_applicant
WHERE
 (  alc.id_user = 15 or alc.id_user IS NULL) AND
( j.status = 0 )
   AND ( j.expired_date = 0
      OR j.expired_date &gt; 1323228856 )
GROUP BY `j`.`id`
ORDER BY `j`.`id` desc
</code></pre>

<h2>UPDATE</h2>

<p>I believe that, now the query is better:</p>

<pre><code>SELECT 
    j.id, j.expired_date, j.title, j.views, j.status
   , j.unread, j.applicants, j.location, j.created_date
   , j.contract_type, c.country
   , group_concat(DISTINCT jp.page_name) AS fan_pages
   , group_concat(DISTINCT jp.id_page) AS id_pages
   , max(app.id) AS applied
FROM users AS u
LEFT JOIN jobs AS j ON 1
INNER JOIN country AS c ON c.id = j.country
LEFT JOIN job_pages AS jp ON jp.id_job = j.id
LEFT JOIN applicants AS alc ON alc.id_user = u.id
LEFT JOIN resumes AS res ON res.id_applicant = alc.id
LEFT JOIN applications AS app  ON app.id_resume = res.id AND app.id_job = j.id
WHERE u.id = 16 AND
        ( j.status = 0 )
       AND ( j.expired_date = 0 OR j.expired_date &gt; 1323228856 )
GROUP BY j.id
ORDER BY j.id
</code></pre>

<p>New updates:</p>

<ol>
<li>Use MAX function if you want to get app.id because when you group one or more rows the max function will return correctly the id you want, else only first row will be return and it could be wrong with NULL</li>
<li>Join with the tables users and jobs</li>
<li>And join with applications should be with id_resume and id_job</li>
</ol>


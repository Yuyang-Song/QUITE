# Maria DB 10.1 DATETIME Blank Value
[Link to question](https://stackoverflow.com/questions/41817611/maria-db-10-1-datetime-blank-value)
**Creation Date:** 1485214595
**Score:** 4
**Tags:** mysql, string, datetime
## Question Body
<p>I am supporting a legacy PHP system. They are planning on moving database servers. We are currently on MariaDB 10.1 and the new server is also MariaDB 10.1. I have hundreds (or maybe thousands) of queries that look like this:</p>

<pre><code>UPDATE ontime_assets
SET AssetName = '117 J19', PlateDate = '20161224', InspectionDate = ''
WHERE AssetID = 7;
</code></pre>

<p>On the current database this processes just fine. On the new one I get this error: </p>

<blockquote>
  <p>Error updating record: Incorrect datetime value: '' for column
  'InspectionDate' at row 1.</p>
</blockquote>

<p>They tell me that the database was migrated and is structurally identical, but obviously it isn't. <code>InspectionDate</code> is a DATETIME that is not required and is set to accept NULL values.</p>

<p>Good code or not, a code rewrite to take out the empty string is not feasible. Does anyone have any idea what MariaDB setting it is, that would allow this query to work currently but would be set differently on the new server?</p>

## Answers
### Answer ID: 41831132
<p>OK I was up all night but I figured it out! </p>

<p>There is a setting called SQL_MODE that is configured in the etc/my.cnf file AND if the DB was upgraded from a prior version in the usr/my.cnf file (which over rides the etc file so much frustration but I found it!).</p>

<p>You can find your sql_mode setting by running the query: SELECT @@sql_mode;</p>

<p>The OLD DB did not have STRICT_TRANS_TABLES set, the NEW DB did, hence the error for empty string dates on the new but not the old. I took STRICT_TRANS_TABLES out of both the usr and etc my.cnf files and had them recycle the mysql server process, and low and behold the code works just like on the old box!</p>

### Answer ID: 41817700
<blockquote>
  <p>Does anyone have any idea what MariaDB setting it is that would allow this query to work currently but would be set differently on the new server?</p>
</blockquote>

<p>No.  If the <code>InspectionDate</code> column be <code>datetime</code>, then assigning empty string is simply not permitted.  Most likely, the queries were running previously because <code>InspectionDate</code> was a text column.  This is unattractive because then you can't take advantage of the date functionality which the database has.</p>

<p>Just assign <code>NULL</code> to the <code>InspectionDate</code> column as a placeholder instead of assigning empty string:</p>

<pre><code>UPDATE ontime_assets
SET AssetName = '117 J19',
    PlateDate = '20161224',
    InspectionDate = NULL
WHERE AssetID = 7
</code></pre>

<p>If you need help updating the scripts, maybe someone here can give you a regex to selectively replace <code>InspectionDate = ''</code> with <code>InspectionDate = NULL</code>.</p>


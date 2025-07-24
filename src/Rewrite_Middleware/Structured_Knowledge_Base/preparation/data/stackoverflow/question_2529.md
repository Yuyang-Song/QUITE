# Error (1046, &#39;No database selected&#39;) happened in Python program, but not in mysql workbench
[Link to question](https://stackoverflow.com/questions/38494938/error-1046-no-database-selected-happened-in-python-program-but-not-in-mysq)
**Creation Date:** 1469075672
**Score:** 2
**Tags:** python, mysql, database, error-handling, mysql-workbench
## Question Body
<p>I have encounter a weird problem when using python to update a record in mysql database. That is, the error 1046 was thrown by python group, but the same mysql statement worked pretty fine in mysql workbench.</p>

<p>Here is the mysql statement,</p>

<pre><code>UPDATE r resultant_data d
        INNER JOIN
    (SELECT 
        uid,
            SUBSTRING_INDEX(GROUP_CONCAT(login_type
                ORDER BY device_ct DESC), ',', 1) devices
    FROM
        (SELECT 
        uid, login_type, COUNT(*) AS device_ct
    FROM
       login_record l
    WHERE
        l.ctime &gt; 1451577600
            AND l.ctime &lt; 1454256000
    GROUP BY uid , login_type
    ORDER BY device_ct DESC) a
    GROUP BY uid) ct ON d.uid = ct.uid AND d.month_id = 1 
SET 
    d.device = ct.devices
;
</code></pre>

<p>My task is to update the most used login device of one user during one month into table resultant_data based on the login_record table. So step one (innermost query): create a table that showcases uid, login_device, login times(i.e. device_ct). Step two (the second innermost query): based on the device_ct, find out the uid and login_type which is associated with the most device_ct. Step three (the update layer): match the uid and update the record into resultant_data. </p>

<p>So does the problem come from the python? Or mysql statement? I suspect the problem is due to "inner join" command (although it works fine in mysql workbench_. I have a similar problem before, which I solved by rewriting "inner join" as "where uid in (select....)". But for this task, is there a way to rewrite or restructure the statement? </p>

<p>Many thanks.</p>

## Answers
### Answer ID: 65586546
<p>I don't think your problem is your SQL. Make sure when you are making your database connection in python that you include the database aka schema name that the table resides in:</p>
<pre><code>db_connection = mysql.connector.connect(
    host=&quot;192.168.1.101&quot;,
    user=&quot;myusername&quot;,
    passwd=&quot;mypassword&quot;,
    database=&quot;database_table_lives_in&quot;
)
</code></pre>


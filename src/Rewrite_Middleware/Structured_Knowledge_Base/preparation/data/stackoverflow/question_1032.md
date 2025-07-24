# Insert values into a table using a trigger with values from stored procedure
[Link to question](https://stackoverflow.com/questions/55941306/insert-values-into-a-table-using-a-trigger-with-values-from-stored-procedure)
**Creation Date:** 1556737474
**Score:** 1
**Tags:** mysql, stored-procedures, triggers
## Question Body
<p>I'm a newbie here. So, please feel free to correct me if my code or  thinking approach can be worked upon.</p>

<p>I am working in MySQL Workbench and MySQL 8.0 Command Line Client. I have a database called <em>ds_testdb2</em> with its tables
structured as follows:</p>

<p><em>ds_testdb2</em> </p>

<p>-Tables:</p>

<ol>
<li><p>asset_sensor_table </p></li>
<li><p>device_table</p></li>
<li>mapped_readings_table</li>
<li>readings_table</li>
<li>sensor_table</li>
</ol>

<p>I need to execute the following SELECT statement every time a record is inserted in my <em>readings_table</em> (insertion into the readings_table happens approx. every 1 minute). This SELECT statement joins 4 tables and produces a mapping of the device's imei with other device attributes such as device_id, subscription_id,etc from another database named <em>agiletest</em>. This SELECT statement works correctly.</p>

<pre><code>SELECT r.imei, r.send_time, r.latitude, r.longitude, r.temperature, r.ground_velocity,
        d.sys_id  AS device_id, d.model_id, d.Subscription_ID,
        s.id AS sensor_id, s.type_id AS sensor_type,
        a_s.asset_id, a_s.start_time, a_s.end_time
        FROM 
        ds_testdb2.readings_table r JOIN agiletest.device d ON  r.imei= d.imei
        JOIN agiletest.sensor s ON d.sys_id= s.device_id 
        JOIN agiletest.asset_sensor a_s ON s.id= a_s.sensor_id; 
</code></pre>

<p>So, I put this SELECT statement in a Stored Procedure. This SP works correctly as well.</p>

<pre><code>DELIMITER $$
CREATE PROCEDURE `ds_testdb2`.`mapping_2`()
    BEGIN
        INSERT INTO `ds_testdb2`.`mapped_readings_table`  -- mapped_readings-table already existed, but was empty.
        (`imei`, `send_time`, `latitude`, `longitude`,`temperature`,`ground_velocity`,
        `device_id`,`model_id`,`subscription_id`,
        `sensor_id`,`sensor_type`,
        `asset_id`,`start_time`,`end_time`) -- no 'VALUES' keyword      
        SELECT r.imei, r.send_time, r.latitude, r.longitude, r.temperature, r.ground_velocity,
        d.sys_id  AS device_id, d.model_id, d.Subscription_ID,
        s.id AS sensor_id, s.type_id AS sensor_type,
        a_s.asset_id, a_s.start_time, a_s.end_time
        FROM 
        ds_testdb2.readings_table r JOIN agiletest.device d ON  r.imei= d.imei
        JOIN agiletest.sensor s ON d.sys_id= s.device_id 
        JOIN agiletest.asset_sensor a_s ON s.id= a_s.sensor_id;    
    END  $$ 
</code></pre>

<p>I then run the Stored Procedure:</p>

<pre><code>mysql&gt; call mapping_2;
Query OK, 4 rows affected (0.02 sec)
</code></pre>

<p>Now, this SP needs to be executed every time a record is inserted in my readings_table. So, I created a trigger that says:</p>

<pre><code>mysql&gt; DELIMITER $$
mysql&gt; CREATE TRIGGER initial_table_mapping_1 AFTER INSERT ON readings_table
    -&gt; FOR EACH ROW
    -&gt; BEGIN
    -&gt; call mapping_2();
    -&gt; END $$
Query OK, 0 rows affected (0.04 sec) 
</code></pre>

<p>Now, To check the execution of the trigger, I am doing the following steps in MySQLWorkbench:</p>

<p>--Step 1. Insert 1 record into the readings_table</p>

<pre><code>INSERT INTO readings_table -- (imei,send_time, latitude, longitude, temperature, ground_velocity)
VALUES
(354721090118251, '2019-04-07 21:26:48',43.63218, -79.51890, 108, 50);
</code></pre>

<blockquote>
  <blockquote>
    <p>Error Code: 1415. Not allowed to return a result set from a trigger</p>
  </blockquote>
</blockquote>

<p><code> </code>
--Step 2. execute the trigger<br>
-already ran it in the MySQL Command Prompt<br>
-Response was:  Query OK, 0 rows affected (0.04 sec)</p>

<p>Step 3. check if the mapped_readings_table was updated(current #rows= 16)</p>

<pre><code>select * from mapped_readings_table;   
</code></pre>

<p>-still stuck with the Error from Step1.</p>

<p>My Question is: In Step1, how can I rewrite my trigger such that-  the result  set from my Stored Procedure gets stored in my <em>mapped_readings_table</em>, everytime  a record is inserted in my <em>readings_table</em>? And, are my steps (Step 1,2,3) to verify the execution of my trigger, correct?</p>

<p>A similar question is here: <a href="https://stackoverflow.com/questions/41624559/update-table-in-a-trigger-with-values-from-stored-procedure">Update table in a trigger with values from stored procedure</a></p>

## Answers
### Answer ID: 56030408
<p>Here is the solution:
My trigger above worked perfectly, and is the right trigger to do the job I had in mind. The problem was that I had created many dummy-triggers to see if my trigger was working. </p>

<p>So, AFTER INSERT ON readings_table, it was these old, dummy triggers that were getting executed, not the final one. The problem was solved once I deleted the old triggers and only had the right trigger in my system.</p>


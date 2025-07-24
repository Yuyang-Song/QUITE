# how can i get ORM to work with 2 separate databases without foriegn keys defined in the tables?
[Link to question](https://stackoverflow.com/questions/3154295/how-can-i-get-orm-to-work-with-2-separate-databases-without-foriegn-keys-defined)
**Creation Date:** 1277942605
**Score:** 3
**Tags:** php, mysql, orm, kohana
## Question Body
<p>I'm not even sure if this is possible. I am using Kohana framework(ver 2.3). I have 2 separate databases. One called 'employees' and another called 'tracker'. The databases are used in 2 different websites. I want to eliminate a table in the tracker database called 'csr', which contains identical employee data, and link the tracker to the employee info in the employees database.</p>

<p>In my tracker application I have a model setup for employees which references the external 'employees' database. I can query it with ORM from the tracker application and all is well. the unique key for employees is 'id'.</p>

<p>In my tracker database I have a model for 'records' table with about 12k entries. None of the field names correspond to any field names in the employees table from the employees database but some fields do contain identical information. The unique key for 'records' is Transaction_Number</p>

<p>Please note I did not write this application or design the databases. I am trying to "retro-fit" the tracker application to use the, now centralized, employee data .</p>

<p>There are 9 fields in 'records' that contain matching information in the employees database. This 9 fields contain employee id's and names but are not all the same id.</p>

<p>I can change the data in these 9 fields so that they are all employee id's if it would help but I need to be able to get employee data: names, addresses, etc., based on the id in any of those 9 fields</p>

<p>Redesigning the database would cause a rewrite of the tracker application and I really don't have the time to do all that.</p>

<p>To save some reading, I am not including the table structures here but I can add them if needed.</p>

<p>What can I do to link these two tables together?</p>

<p>EDIT: Added table structure for tracker.records</p>

<pre><code>TRACKER.RECORDS
Transaction_Number (PK AI not null)
date
accountnumber
reasoncode
reasondesc
actioncode
actiondesc
comments
supervisor        -    employee-&gt;id (supervisor that created the record)
supername         -    employee-&gt;name
supersuper        -    employee-&gt;parent-&gt;name
superman          -    employee-&gt;parent-&gt;parent-&gt;name
eid               -    employee-&gt;id  (employee that the record is about)
Service_Rep       -    employee-&gt;name
ServRepSupervisor -    employee-&gt;parent-&gt;name
ServRepManager    -    employee-&gt;parent-&gt;parent-&gt;name
csrfollow         -    employee-&gt;name  (who to follow up with)
Important
Read
Followup_Read
followup_Important
</code></pre>

<p>the employee table is using ORM_Tree to be self relational.</p>

<p>I need to be able to get employee info for any of those fields. I can change the data in each of those fields to be an employee id and i think i can eliminate some of them. the only ones I rally need are supervisor(employee->id), eid(employee->id) and csrfollow(can be changed to employee->id). the other fields can be discovered based on the employee->id. I still need to have those 3 fields point to the employee.id field in the employees database.</p>

## Answers
### Answer ID: 3154317
<p>Are you aware that MySQL allows foreign keys to reference tables across databases, as long as both databases are hosted on the same instance of MySQL?</p>

<pre><code>CREATE TABLE `employees` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY
  -- other columns...
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `records` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_id` bigint(20) unsigned DEFAULT NULL,
  -- other columns...
  FOREIGN KEY (`employee_id`) REFERENCES `employees`.`employees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
</code></pre>

<p>You just have to qualify the referenced table name with its database name.</p>

<hr>

<p>Re your update:  You can change the name of RECORDS to RECORDS_BASE with the distinct data that belongs in TRACKER.  </p>

<pre><code>TRACKER.RECORDS_BASE
Transaction_Number (PK AI not null)
date
accountnumber
reasoncode
reasondesc
actioncode
actiondesc
comments
supervisor_id
eid
Important
Read
Followup_Read
followup_Important
</code></pre>

<p>Then create a new VIEW called RECORDS that joins RECORDS_BASE to multiple rows in EMPLOYEES:</p>

<pre><code>CREATE VIEW TRACKER.RECORDS AS
SELECT rb.*,
  s.id AS supervisor,
  s.name AS supername,
  ss.name AS supersuper,
  sss.name AS superman,
  emp.name AS Service_Rep,
  srs.name AS ServRepSupervisor,
  srm.name AS ServRepManager,
  ??? AS csrfollow
FROM TRACKER.RECORDS_BASE AS rb
JOIN EMPLOYEES.EMPLOYEES AS s ON rb.supervisor_id = s.id
JOIN EMPLOYEES.EMPLOYEES AS ss ON s.parent_id = ss.id
JOIN EMPLOYEES.EMPLOYEES AS sss ON ss.parent_id = sss.id
JOIN EMPLOYEES.EMPLOYEES AS emp ON rb.eid = emp.id
JOIN EMPLOYEES.EMPLOYEES AS srs ON emp.parent_id = srs.id
JOIN EMPLOYEES.EMPLOYEES AS srm ON srs.parent_id = srm.id;
</code></pre>

<p>I can't tell from your description what belongs in the csrfollow column.  Whose name is it?  Anyway I'll leave that for you to decide.  I've shown how you can get a reference to each of the relevant rows in the employees table, so take your pick. </p>


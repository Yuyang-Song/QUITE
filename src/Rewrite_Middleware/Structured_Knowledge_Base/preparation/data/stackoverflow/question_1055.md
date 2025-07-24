# Rewrite data in a MySQL table in PHP using a primary key
[Link to question](https://stackoverflow.com/questions/56880757/rewrite-data-in-a-mysql-table-in-php-using-a-primary-key)
**Creation Date:** 1562215403
**Score:** -1
**Tags:** php, mysql, sql
## Question Body
<p>I am building a chatbot in PHP and the objective is for an employee to change his password in a database using his Employee Id,  I have a database table which has columns
Employee Id(1768,
1347,
1966,
1344)<br>
Password(abc,
def,
ijk,
lmn)</p>

<p>So i want to use Employee Id as primary key to identify whose employee's password i want to change, and then i want to rewrite the data in password column. What is the exact query to achieve that and how could i achieve that in PHP ?
Plus I also want to save the password in encrypted form in the database</p>

## Answers
### Answer ID: 56880957
<p>As you mentioned that employee_id is the primary key. Employee_id_value can be replaced as your value in below code:  </p>

<pre><code>UPDATE employee SET password = new_password 
WHERE employee_id = Employee_id_value
</code></pre>


# Why is Google Cloud SQL MySQL driver not returning all field values that have the same name?
[Link to question](https://stackoverflow.com/questions/70736270/why-is-google-cloud-sql-mysql-driver-not-returning-all-field-values-that-have-th)
**Creation Date:** 1642390809
**Score:** 0
**Tags:** mysql, firebase, google-cloud-functions, google-cloud-sql
## Question Body
<p>I'm writing a firebase function that executes query <code>SELECT A.*, B.* FROM A INNER JOIN B ON ... WHERE ...</code> against a MySQL database hosted on Google Cloud SQL. The two tables A and B have some columns with identical names. In particular, both have an &quot;id&quot; column. However, the result only contains one <code>id</code> column and it always has the value of <code>B.id</code>.</p>
<p>I can work around this by not using <code>A.*, B.*</code> and instead selecting specific column names, but there are a lot of columns, which make the <code>*</code> so much more convenient. Is there a way to have the database driver return all columns suitably marked with the tablename alias, or is rewriting the query without <code>A.*, B.*</code> the only way?</p>
<p>As a partial fix I can <code>SELECT A.id AS A_id, B.id AS B_id, A.*, B.*</code> which does get those two values separately. But then (a) there is still a spurious <code>id</code> column in the result set, which is an ugly copy of <code>B.id</code>, and (b) there are other pairs of identically named columns between the tables. So I'm hoping for a generic solution, like some option to have the driver label the output fields with the tablename aliases.</p>
<p>Those columns are very much part of the result set so it's amazing to me that this driver is effectively dropping some columns just because the name is the same.</p>
<p>Thank you.</p>
<p>EDIT: Here is a simple example. First the tables:</p>
<pre><code>mysql&gt; describe A;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| code  | varchar(255) | YES  |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.04 sec)

mysql&gt; describe B;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| code  | varchar(255) | YES  |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.06 sec)

mysql&gt; select * from A;
+----+------+
| id | code |
+----+------+
|  1 | abc  |
|  2 | def  |
|  3 | ghi  |
+----+------+
3 rows in set (0.06 sec)

mysql&gt; select * from B;
+----+------+
| id | code |
+----+------+
|  4 | xyz  |
|  5 | abc  |
|  6 | def  |
+----+------+
3 rows in set (0.05 sec)

mysql&gt; select A.*, B.* from A INNER JOIN B on A.code = B.code;
+----+------+----+------+
| id | code | id | code |
+----+------+----+------+
|  1 | abc  |  5 | abc  |
|  2 | def  |  6 | def  |
+----+------+----+------+
2 rows in set (0.06 sec)
</code></pre>
<p>Then the firebase call to retrieve this query, with error handling and other stuff removed.</p>
<pre><code>export const sql = functions.https.onRequest((req, res) =&gt; {
  return corsFn(req, res, async () =&gt; {      
    const query = 'select A.*, B.* from A INNER JOIN B on A.code = B.code';
    
    const pool: mysql.Pool = mysql.createPool({
      // cloud sql proxy
      host: &quot;127.0.0.1&quot;,
      port: 3306,
      user: functions.config().cloud_sql.user,
      password: functions.config().cloud_sql.password,
      database: functions.config().cloud_sql.database,
      connectionLimit: 20,
    });
    pool.query(query, [], (err: mysql.MysqlError | null, results: any) =&gt; {
      if (err) {
        res.status(404).send(err);
      } else {
        res.status(200).send(results);
      }
    });
  });
});
</code></pre>
<p>And finally here is the JSON result:</p>
<pre><code>[
 {&quot;id&quot;:5,&quot;code&quot;:&quot;abc&quot;},
 {&quot;id&quot;:6,&quot;code&quot;:&quot;def&quot;}
]
</code></pre>
<p>There is only one &quot;id&quot; in the result and that is from the second table. So I'm simply asking if there's a way to use &quot;*&quot; in the select and have it return all columns, with the <code>A.id</code> and <code>B.id</code> marked differently somehow.</p>


# rewrite Hibernate query without huge list parameter
[Link to question](https://stackoverflow.com/questions/13798868/rewrite-hibernate-query-without-huge-list-parameter)
**Creation Date:** 1355134477
**Score:** 9
**Tags:** java, sql, hibernate, postgresql
## Question Body
<p>In my database I have a <code>zip</code> table with a <code>code</code> column. The user can upload a list of Zip codes and I need to figure out which ones are already in the database. Currently, I do this using the following Hibernate query (HQL):</p>

<pre><code>select zip.code from Zip zip
where zip.code in (:zipCodes)
</code></pre>

<p>The value of the <code>:zipCodes</code> parameter is the list of codes uploaded by the user. However, in the version of Hibernate I'm using there's <a href="https://hibernate.onjira.com/browse/HHH-2166">a bug</a> which limits the size of such list parameters and on occasions we're exceeding this limit.</p>

<p>So I need to find another way to figure out which of the (potentially very long) list of Zip codes are already in the database. Here are a few options I've considered</p>

<h2>Option A</h2>

<p>Rewrite the query using SQL instead of HQL. While this will avoid the Hibernate bug, I suspect the performance will be terrible if there are 30,000 Zip codes that need to be checked.</p>

<h2>Option B</h2>

<p>Split the list of Zip codes into a series of sub-lists and execute a separate query for each sub-list. Again, this will avoid the Hibernate bug, but performance will likely still be terrible</p>

<h2>Option C</h2>

<p>Use a temporary table, i.e. insert the Zip codes to be checked into a temporary table, then join that to the <code>zip</code> table. It seems the querying part of this solution should perform reasonably well, but the creation of the temporary table and insertion of up to 30,000 rows will not. But perhaps I'm not going about it the right way, here's what I had in mind in pseudo-Java code</p>

<pre><code>/**
 * Indicates which of the Zip codes are already in the database
 *
 * @param zipCodes the zip codes to check
 * @return the codes that already exist in the database
 * @throws IllegalArgumentException if the list is null or empty
 */
List&lt;Zip&gt; validateZipCodes(List&lt;String&gt; zipCodes) {

  try {
    // start transaction

    // execute the following SQL
    CREATE TEMPORARY TABLE zip_tmp
    (code VARCHAR(255) NOT NULL) 
    ON COMMIT DELETE ROWS;

    // create SQL string that will insert data into zip_tmp
    StringBuilder insertSql = new StringBuilder()

    for (String code : zipCodes) {
      insertSql.append("INSERT INTO zip_tmp (code) VALUES (" + code + ");")
    }     

    // execute insertSql to insert data into zip_tmp

    // now run the following query and return the result   
    SELECT z.*
    FROM zip z
    JOIN zip_tmp zt ON z.code = zt.code

  } finally {
    // rollback transaction so that temporary table is removed to ensure
    // that concurrent invocations of this method operate do not interfere
    // with each other
  }    
}
</code></pre>

<p>Is there a more efficient way to implement this than in the pseudo-code above, or is there another solution that I haven't thought of? I'm using a Postgres database.</p>

## Answers
### Answer ID: 13799060
<p>Have you tryed to use subqueries IN ?</p>

<p><a href="http://docs.jboss.org/hibernate/orm/3.5/api/org/hibernate/criterion/Subqueries.html" rel="nofollow">http://docs.jboss.org/hibernate/orm/3.5/api/org/hibernate/criterion/Subqueries.html</a></p>

<p>would be something like this</p>

<pre><code>DetachedCriteria dc = DetachedCriteria.forClass(Zip.class, "zz");
//add restrictions for the previous dc

Criteria c = session.createCriteria(Zip.class, "z");
c.add(Subqueries.in("z.code" dc));
</code></pre>

<p>sry if I mistaken the code, its beeing a while since I dont use Hibernate</p>

### Answer ID: 13799995
<p>There are around 45'000 Zip Codes in the US and the seem to be updated anualy. If this is an anual job, dont write it in java. Create a sql script which loads the zip codes into a a new table and write an insert statement with</p>

<p><code>insert XXX into zip where zip.code not in (select code from  ziptemp)</code></p>

<p>Have your operation guys run this two line SQL script once a year and dont buy yourself with this in the java code. Plus if you keep this out of java, you can basically take any approach, because no one cares if this runs for thirty minutes in offpeak times.</p>

<p><em>divide et impera</em></p>

### Answer ID: 13799003
<p>Option D:<br>
Loading all existing zip codes from the database (pagination?) and make the compare in your application.</p>

<p>Regarding your Option A:<br>
I remember a limitation of the SQL query lenght but that was on DB2, I don't know if there is a limit on PostgreSQL.</p>

### Answer ID: 13799785
<p>Suppose you "validate" 1000 codes against a table of 100000 records in which the code is the primary key and has a clustered index.</p>

<ul>
<li>Option A is not an improvement, Hibernate is going to build the same SELECT ... IN ... you could write on your own.</li>
<li>Option B, as well as your current query, might fail to use the index.</li>
<li>Option D might be good if you are sure the zipcodes don't change at arbitrary times, which is unlikely, or if you can recover from trying to process existing codes. </li>
<li><p>Option C (Creating a temp table, issuing 1000 INSERT statements and joining 1000 rows against 100000 in a single SELECT) isn't competitive with just issuing 1000 simple and index-friendly queries for a single new code each:</p>

<p>SELECT COUNT(*) FROM Zip WHERE Zip.code = :newCode</p></li>
</ul>

### Answer ID: 13799052
<p>Load all the Zip codes in the database to a List. And on the user inputed list of Zip codes do a <code>removeAll(databaseList)</code>.</p>

<p>Problem solved!</p>


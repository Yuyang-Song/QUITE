# JPA Query optimization by avoiding JOIN to lookup table?
[Link to question](https://stackoverflow.com/questions/3661829/jpa-query-optimization-by-avoiding-join-to-lookup-table)
**Creation Date:** 1283886415
**Score:** 6
**Tags:** java, hibernate, jpa, jakarta-ee, jpql
## Question Body
<p>Imagine a table <strong>emp</strong>:</p>

<pre><code>CREATE TABLE emp
( id           NUMBER
, name         VARCHAR
, dept_code    VARCHAR
)
</code></pre>

<p>and a table <strong>dept</strong>:</p>

<pre><code>CREATE TABLE dept
( code         VARCHAR
, name         VARCHAR
)
</code></pre>

<p><code>emp.dept_code</code> references <code>dept.code</code> as a ForeignKey.</p>

<p>These tables are mapped to JPA Entities, and the ForeignKey is modeled as an association:</p>

<pre><code>@ManyToOne
@JoinColumn(name = "dept_code")
private Department department;
</code></pre>

<p>Given following data:</p>

<pre><code>emp                     dept    
----------------        ------------------
1    John   SALS        SALS     Sales
2    Louis  SALS        SUPT     Support
3    Jack   SUPT 
4    Lucy   SUPT  
</code></pre>

<p>I would like to write a JPA query that returns all Emloyees in the Support Department.  Assume I <em>know</em> the PrimaryKey of the Support Department (<code>SUPT</code>)</p>

<p>I guess that would be:</p>

<pre><code>SELECT emp
  FROM Employee emp JOIN emp.department dept
 WHERE dept.code = 'SUPT'
</code></pre>

<p><strong>Question:</strong></p>

<p>As the Department key <code>SUPT</code> code is available in the <strong>emp</strong> table, is there a way to rewrite the JPA query <strong><em>by avoiding</em></strong> the JOIN to the Department Entity?</p>

<p>Would this result in a performance improvement?  Or is a JPA implementation (like Hibernate)  smart enough to avoid the database join to the <strong>dept</strong> table?</p>

## Answers
### Answer ID: 3662022
<p>You would usually write the query as</p>

<pre><code>select emp
from employee emp
where emp.department.code = 'SUPT'
</code></pre>

<p>and let your provider figure out the best way to come up with the result.  In the case of hibernate, yes, it is smart enough to realize it can just look at the join column.</p>

<p>edit : It is worth noting, that you haven't set up lazy loading in your annotations, so it's going to join the table in to create the department entity anyway :)</p>


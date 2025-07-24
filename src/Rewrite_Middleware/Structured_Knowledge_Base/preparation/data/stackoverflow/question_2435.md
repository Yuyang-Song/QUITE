# JPA Query returning nulls - Composite Key with null column
[Link to question](https://stackoverflow.com/questions/34079524/jpa-query-returning-nulls-composite-key-with-null-column)
**Creation Date:** 1449193281
**Score:** 11
**Tags:** java, sql, hibernate, jpa, composite-primary-key
## Question Body
<p>I have a legacy database (Cobol files actually) that I am accessing using a proprietary JDBC driver with Hibernate/JPA.</p>

<p>The Entity has a composite primary key with 2 columns: <code>CODE</code> and <code>SITE</code>.</p>

<p>In the legacy data there are records for the same <code>CODE</code> that can have either a specific value for <code>SITE</code>, or there can be a record with NULL in the <code>SITE</code> column which represents 'All Sites'. The theory of this file is, if you cannot find the <code>CODE</code> for your specific <code>SITE</code> then you lookup the record with NULL in the <code>SITE</code> (the 'catch-all').</p>

<p>I cannot change the structure of this 'table' as it would involve rewriting large parts of the legacy Cobol system which we don't want to do. I also cannot create views of the data.</p>

<p>Now when I do an <code>em.find</code> with the primary composite key class containing a specific <code>code</code> and a null for <code>site</code>, then Hibernate correctly finds the matching record with the NULL value in the column - All good!</p>

<p>But if I try to do a query using <code>em.createQuery</code> similar to the following:</p>

<pre><code>SELECT x FROM TareWeight x WHERE x.pk.code = 'LC2'
</code></pre>

<p>for which there are 2 records, it returns a null object in the resulting list for the record with the NULL in the <code>SITE</code> column.</p>

<p>If I take the SQL that Hibernate uses for this query, then the 'database' returns two records, one with the NULL site and one with a specific site. It seems that when Hibernate loads the Entities from these results, it is mapping it to a null Entity object.</p>

<p>So either Hibernate supports it or it doesn't. Why would the <code>em.find</code> work but not the <code>em.createQuery</code>?</p>

<p>I know that <a href="https://stackoverflow.com/questions/15687837/jpa-composite-primary-key-with-null-value">this question</a> is similar, but the answers seem to suggest that it is impossible. But clearly Hibernate can do the find correctly, so why does the query not work?</p>

<hr>

<p><strong>EDIT:</strong> OK, so I found a <code>NullableStringType</code> class definition on <a href="https://hibernate.atlassian.net/browse/HHH-1109" rel="nofollow noreferrer">this Hibernate JIRA Issue</a> and added it to my project.</p>

<p>If I add a <code>@Type</code> definition on the <code>site</code> column of the PK using this type class, then I can successfully get non-null Entities back from the SELECT query, with the <code>site</code> field containing whatever String text I define as the representation of <code>null</code>.</p>

<p>However, it is still behaving differently. The <code>find</code> returns an Entity with the <code>site</code> field containing <code>null</code>, but the query returns an Entity with the <code>site</code> field containing "NaN" (the default representation of <code>null</code>).</p>

<p>It still feels like these should behave the same.</p>

<hr>

<p><strong>UPDATE 2:</strong> Some of you want to know specifics about the 'database' in question.</p>

<p>It is the Genesis RDBMS engine, written by <a href="http://www.trifox.com/" rel="nofollow noreferrer">Trifox Inc.</a>. The data is stored in AcuCobol (now Micro Focus) Vision indexed files.</p>

<p>We have the configuration set to translate blank (SPACES) alphanumeric fields to NULL, hence our file records which contain spaces for the PK field are being translated to NULL. I can specifically select the appropriate record by using <code>WHERE site_id IS NULL</code>, so the RDBMS <strong>is</strong> treating these blank fields as an SQL NULL.</p>

<p>Having said all that I do not believe that this issue has anything to do with the 'database', apart from the fact that it is unusual to have PK fields being null.</p>

<p>What's more, if I log the SQL that Hibernate is using for both the <code>find</code> and the query, they are almost identical.</p>

<p>Here's the SQL for the find:</p>

<pre><code>select tareweight0_.CODE as CODE274_0_, tareweight0_.SITE as SITE274_0_, 
       tareweight0_.WEIGHT as WEIGHT274_0_ from TARE_WEIGHT tareweight0_ 
       where tareweight0_.CODE=? and tareweight0_.SITE=?
</code></pre>

<p>And here's the SQL for the Query:</p>

<pre><code>select tareweight0_.CODE as CODE274_, tareweight0_.SITE as SITE274_, 
       tareweight0_.WEIGHT as WEIGHT274_ from TARE_WEIGHT tareweight0_ 
       where tareweight0_.CODE=? and tareweight0_.SITE=?
</code></pre>

<p>As you can see, the only difference is the column alias names.</p>

<hr>

<p><strong>UPDATE 3:</strong> Here's some example data:</p>

<pre><code>select code, site, weight from tare_weight where code like 'LC%';

 CODE   SITE    WEIGHT
 ------ ------ -------
 LC1               .81
 LC2               .83
 LC2    BEENLH     .81
 LC3              1.07
 LC3    BEENLH    1.05
 LC4              1.05
 LCH1              .91
 LCH2              .93
 LCH2   BEENLH     .91
 LCH6             1.13
 LCH6   BEENLH    1.11
</code></pre>

<p>And searching specifically for NULL:</p>

<pre><code>select code, site, weight from tare_weight where code like 'LC%' and site IS NULL;

 CODE   SITE    WEIGHT
 ------ ------ -------
 LC1               .81
 LC2               .83
 LC3              1.07
 LC4              1.05
 LCH1              .91
 LCH2              .93
 LCH6             1.13
</code></pre>

## Answers
### Answer ID: 34122997
<blockquote>
  <p>"So either they support it or they don't"</p>
</blockquote>

<p><strong>TL;DR</strong> That expectation/feeling is unjustified. The unsupported functionality in your link (&amp; mine below) is exactly yours. "Not supporting" it means that if you do it then Hibernate can do anything they want. You are lucky that they (seem to) return reasonable values. (Although it's just a <em>guess</em> how they are acting. You don't have a specification.) There is no reason to expect anything, let alone consistency. When behaviour is just a consequence of some unsupported case arising, any "why" is most likely just an artifact of how the code was written with other cases in mind.</p>

<hr>

<p>Here is a(n old) support thread answered by the <a href="https://forum.hibernate.org/viewtopic.php?f=1&amp;t=961522">Hibernate Team</a>:</p>

<p>Post subject: Composite key with null value for one column<br>
PostPosted: Mon Jul 03, 2006 2:21 am  </p>

<blockquote>
  <p>I have table with composite primary key and I created following
  mapping for the table.As it is possible to insert a null value for any
  column in composite key as long as the combination of all columns is
  Unique, I have record in teh table which has null value for V_CHAR2
  column ( which is part of composite key ) . when I execute a query on
  this entity I get null values for the records which are having null
  value of V_CHAR2 column. What's wrong in my mapping and
  implementation..</p>
</blockquote>

<p>Posted: Tue Jul 11, 2006 9:09 am<br>
Hibernate Team  </p>

<blockquote>
  <p>a primary key cannot be null (neither fully or partial)</p>
</blockquote>

<p>Posted: Sat Jan 06, 2007 5:35 am<br>
Hibernate Team  </p>

<blockquote>
  <p>sorry to disapoint you but null in primary key is not supported -
  primarily because doing join's and comparisons will require alot of
  painfullly stupid code that is just not needed anywhere else.....think
  about it and you will see (e.g. how do you do a <em>correct</em> join with
  such a table)</p>
</blockquote>

<p>This is not surprising, because NULL is not allowed in a PK column in SQL. A PRIMARY KEY declaration is a synonym for UNIQUE NOT NULL. NULL is not equal to anything with the (misguided) intent that some unrecorded value is not known to be equal. (Your expectations of some kind of exception for at least some occasions of NULL in a PK <em>equaling</em> a NULL in a condition is contrary to SQL.) Given that NULL is not allowed in PK values, we can expect PK optimizations related to 1:1 mappings and to sets rather than bags of rows to assume there are no NULLs when it's convenient. One can expect that Hibernate decided to not worry about what their implementation did with cases that shouldn't arise in the SQL. Too bad they don't tell you that on compilation or execution. Hopefully it is in documentation.)</p>

<p>Even <code>find</code> differing from <code>createQuery</code>re NULL is not surprising. The former involves one value while the latter involves what are expected to be sets (not bags) of rows without NULLs (but aren't).</p>

<p>A workaround may be to not treat any column of a primary key as NULL but as the actual string of spaces in storage. (Whatever this means given your storage/DBMS/hibernate/JPA/Java stack. You haven't given us enough information to know whether your Cobol view of the database would be impeded by not mapping spaces to NULL for your JPA). With your data you can still declare a UNIQUE index on the columns.</p>


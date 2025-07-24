# Database architecture change from local to distributed
[Link to question](https://stackoverflow.com/questions/1680617/database-architecture-change-from-local-to-distributed)
**Creation Date:** 1257427991
**Score:** 0
**Tags:** database, architecture, distributed, data-access-layer
## Question Body
<p>Our company has a product which relies on local database to work (it allows more client to connect to same database and share data between them).  </p>

<p><strong>DBMS</strong>: Microsoft SQL Server 2008</p>

<p>Now, we need to create a single database, accessible through internet (i am not interested in the <em>how</em>, for now), which will allow more users to use it as if it is their own.</p>

<p>Simple examples to follow.<br>
By supposing that our program will manage (insert/modify/delete) books and their sellers:</p>

<pre><code>Table Seller:
   IdSeller          PRIMARY
   Name

Table Books:
   IdBook            PRIMARY
   IdSeller          NOT NULL
   Description
</code></pre>

<p>Now, we need to distribute it, and categorize data by "Company"</p>

<pre><code> Table Company:
    IdCompany        PRIMARY
    LicenseNumber
</code></pre>

<p>Our idea was to modify <em>primary</em> (??) tables like this:  </p>

<pre><code> Table Seller (NEW VERSION):
    IdSeller         PRIMARY
    IdCompany        NOT NULL
    Name
</code></pre>

<p>In this way we are sure Books will belong to specific sellers who will belong to specific companies.<br>
Conceptually this is working, but we will have then to change all the queries made in our DataAccessLayer!  </p>

<p>We thought of a couple of solutions:  </p>

<ul>
<li>company-filtered-views for each <em>primary</em> table</li>
<li>rewrite all the queries</li>
</ul>

<p>How would you handle this problem?  </p>

## Answers
### Answer ID: 1680868
<p>First you need to decide what the entities in this new schema will represent...  Is the new seller table the same entity as the old one? or will each row in the new table represent an association of a seller with a company?  I.e., can the same seller be with two different companies?  Same question for books.  The answer will determine how best to modify the table schema to provide the functionality you need.</p>

### Answer ID: 1680685
<p>Off the cuff, I would re-do the queries in your DAL.</p>

<p>The problem is, this is a highly situational problem.  How frequently do you update this program?  Are there major revisions in the work?  How equipped is your company to do a large refactoring?</p>

<p>Sometimes, in the business world, hacking a quick solution is optimal :'(</p>

### Answer ID: 1680659
<p>You can create a WCF/web service accessible through internet rathaer than exposing SQL Server. WCF/web service can contain all the logic regarding which records to give to the client from database and which to restrict. And your client can simply access the WCF/Web service. </p>

<p>Let me know if I'm not understanding your problem well.</p>


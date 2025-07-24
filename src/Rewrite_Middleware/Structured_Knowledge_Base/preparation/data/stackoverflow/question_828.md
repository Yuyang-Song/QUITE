# What&#39;s the point of a view constraint?
[Link to question](https://stackoverflow.com/questions/4435034/whats-the-point-of-a-view-constraint)
**Creation Date:** 1292289066
**Score:** 3
**Tags:** oracle-database
## Question Body
<p>Where are <a href="http://download.oracle.com/docs/cd/B14117_01/server.101/b10759/clauses002.htm#i1002565" rel="nofollow">view constraints</a> useful? By that I mean, Oracle allows a constraint to be created on a view. They are not enforced by the database. It seems to be just more metadata that can be used by the database, but I'm trying to understand under what circumstances they are useful.</p>

<p>Tom Kyte <a href="http://asktom.oracle.com/pls/asktom/f?p=100:11:0%3a%3a%3a%3aP11_QUESTION_ID:636499119911" rel="nofollow">answered</a> in a question:</p>

<blockquote>
  <p>They are used for complex query rewrites with materialized views and such.  It is more "meta data" 
  -- it gives the optimizer more information, allows for a broader range of query rewriting to take 
  place.</p>
</blockquote>

<p>... but that's a bit brief. </p>

## Answers
### Answer ID: 4440172
<p>Minor use in an Oracle product. In the Designer-generated PL/SQL web applications, components based on views needed a primary key defined on the view. That allowed the application to hyperlink from a list of records to a single-record display.</p>

<p>I remember seeing a few cases with Hibernate where it generated better code when there were PK and FK constraints defined on views. (Can anybody else confirm that?)</p>

<p>And Tom points to query rewrite. </p>

<p>So I think the answer is "if your tools can use the information, then it's better to supply it." Of course, it's going to be hard to figure out which tools will use it. </p>

<p>I try to include them because</p>

<ul>
<li>It's not much work, though the scripts to recreate views are somewhat more complicated.</li>
<li>It helps in making the physical implementation of the logical model complete</li>
<li>It reminds me of real data constraints that I need to implement somehow, via triggers or background packages or in a "constraint violation" report.</li>
</ul>

### Answer ID: 4435058
<p>From <a href="http://download.oracle.com/docs/cd/B13789_01/server.101/b10736/constra.htm" rel="nofollow">Oracle Documentation</a> :</p>

<p>View Constraints</p>

<p>You can create constraints on views. The only type of constraint supported on a view is a RELY constraint.</p>

<p>This type of constraint is useful when queries typically access views instead of base tables, and the database administrator thus needs to define the data relationships between views rather than tables. View constraints are particularly useful in OLAP environments, where they may enable more sophisticated rewrites for materialized views.</p>

<p>Quoted another Oracle Documentation page, but never used constraints on views anyway.</p>


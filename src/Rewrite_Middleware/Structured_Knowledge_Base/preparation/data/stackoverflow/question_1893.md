# getting Oracle materialized view to refresh
[Link to question](https://stackoverflow.com/questions/11315781/getting-oracle-materialized-view-to-refresh)
**Creation Date:** 1341335185
**Score:** 1
**Tags:** oracle-database, plsql, materialized-views
## Question Body
<p>I've traced a bug in my Java EE application to the Oracle database: there is a materialized view which is not refreshing correctly.  If I do a query against the MV, it gives me foreign keys which are bad and appear to be old.</p>

<p>So how can I fix or replace this materialized view?  Any thoughts are welcome.</p>

<p>I tried refreshing manually, like this:</p>

<pre><code>DBMS_MVIEW.REFRESH('PRODUCTDESCRIPTIONS', 'C');
</code></pre>

<p>I got the error "ORA-00942: table or view does not exist".  I don't understand this, because when I run the MV's subquery by hand, it looks fine.</p>

<p>The Apex Web interface indicates that the MV has not refreshed for over a year, so this is not a new problem.</p>

<p>I looked for any logging from the refresh process, but couldn't find the file refresh.log.</p>

<p>I've tried replacing the materialized view with a simple query, but it's too slow.  I'd be happy to rewrite/reconfigure/reinstall the MV somehow.</p>

<p>Database and OS version:</p>

<pre><code>Oracle Database 10g Express Edition Release 10.2.0.1.0 - Product
PL/SQL Release 10.2.0.1.0 - Production

uname -a:
Linux &lt;server name&gt; 2.6.9-78.0.22.ELsmp #1 SMP Thu Apr 30 19:14:39 EDT 2009 i686 i686 i386 GNU/Linux
</code></pre>

<p>Source code for the materialized view:</p>

<pre><code>CREATE MATERIALIZED VIEW  "PRODUCTDESCRIPTIONS"
  ORGANIZATION HEAP PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS" 
  BUILD IMMEDIATE
  USING INDEX 
  REFRESH COMPLETE ON DEMAND
  USING DEFAULT LOCAL ROLLBACK SEGMENT
  DISABLE QUERY REWRITE
  AS SELECT prdcts.primarykey AS product, 
prdcts.upcid AS productupcid, 
prdcts.description AS productdescription, 
prdctctgrs.primarykey AS productcategory, 
prdctctgrs.id AS productcategoryid, 
prdctctgrs.name AS productcategoryname, 
prdctpkgs.primarykey AS productpackage, 
prdctpkgs.name AS productpackagename FROM prdctctgrs, 
prdcts, 
prdctpkgs, 
prdctctgrstoprdcts, 
prdctstoprdctpkgs 
WHERE 
prdctctgrstoprdcts.productcategory = prdctctgrs.primarykey 
AND prdctctgrstoprdcts.product = prdcts.primarykey 
AND prdctstoprdctpkgs.product = prdcts.primarykey 
AND prdctstoprdctpkgs.productpackage = prdctpkgs.primarykey 
AND bitand(prdctctgrs.metaflags, 1)+0 = 0 
AND bitand(prdcts.metaflags, 1)+0 = 0 
AND bitand(prdctpkgs.metaflags, 1)+0 = 0 
AND bitand(prdctctgrstoprdcts.metaflags, 1)+0 = 0 
AND bitand(prdctstoprdctpkgs.metaflags, 1)+0 = 0
/
</code></pre>

## Answers
### Answer ID: 20572277
<p>Just to confirm my comment on the original question: dropping and recreating the MV fixed the problem.</p>

### Answer ID: 11316396
<p>When you run the refresh procedure, are you executing it as the owner of the tables you're selecting from? Are all of the tables you're accessing directly granted to you? If the tables are granted to you via roles, then the refresh procedure won't be able to see them.</p>


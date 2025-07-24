# Synonyms causing an expensive plan
[Link to question](https://stackoverflow.com/questions/19341018/synonyms-causing-an-expensive-plan)
**Creation Date:** 1381629037
**Score:** 2
**Tags:** oracle-database, oracle11g, synonym, sql-execution-plan
## Question Body
<p>I had the following problem with our Oracle 11 database and although there's a fix,
I want to understand why its reacting this way.</p>

<p>We have two schemas: a "dev" schema which contains all the tables, views, plsql, ... and
a "app" schema which contains synonyms to the dev-objects, i.e. statements don't contain
schema names.</p>

<p>A dev-view references tables (<code>select * from a a1 -&gt; b -&gt; a a2 union select * from c</code>)
in which there's a common column which is used for the selection, i.e. the selection
predicate is pushed into table "a" (300k rows) and "b" (90k rows) selection via seperate
index access, resulting in a very performant plan.</p>

<p>dev-fun is a deterministic, parallel function which simply does some string manipulation
without further database access.</p>

<p>The selection on the view looks like: <code>select * from view where common-column = fun(string)</code>
This works as expected on the dev schema, but if this is executed on the app schema,
the plan becomes relatively very expensive, i.e. the result of <code>fun(string)</code> is not pushed down,
but the tables are hash joined and the result is scanned for the element.</p>

<p>Still in the app schema, when I replace <code>fun(string)</code> with the function-result the plan becomes
cheap again.</p>

<p>To solve the problem, I duplicated the view in the app schema instead of referencing it via
a synonym, but in case of view/table-changes that means a potential source of defect, as we
normally don't check the app schema ...
The call to the function is still via the synonym and the view was duplicated as-is, i.e. it
accesses the synonyms for the underlying tables ... and the plan is the same as if it was executed
on the dev schema.</p>

<p>Apart of having selection grants on all underlying tables, I've also tried granting "query rewrite", "references" on the tables and "references" on the view. Furthermore I've tried the authid-options on the function. I have to admit, that I haven't yet checked for <a href="https://stackoverflow.com/questions/781224/why-would-an-oracle-synonym-return-a-different-number-of-rows-to-the-underlying">row-level security</a>, but we are not using them.</p>

<p>What else can I check for?</p>

<p>The oracle version is 11.0.2.2. Opening a oracle-ticket would be only a theoretical option,
as we don't have direct support access and the layer in-between is even more frustrating as
living with the maintaining issue.</p>

<p>I know that typically a explain-plan would be helpful, but lets try it first without it, as
I suspect the problem somewhere else.</p>

<p>Update (14.10.2013):</p>

<ul>
<li>Hinting to use nested loops doesn't work. </li>
<li>function based index aren't used.</li>
</ul>

<p>Indexed access: <code>select * from v_vt_betreuer where vtid = 11803056;</code></p>

<p><img src="https://i.sstatic.net/74LgZ.png" alt="enter image description here"></p>

<p>Hashed access: <code>select * from v_vt_betreuer where vtid =  VTNRVOLL_TO_VTID(11803056);</code></p>

<p><img src="https://i.sstatic.net/ZUOaI.png" alt="enter image description here"></p>

<p>Copied view: i.e. when the view is copied into the app schema</p>

<p><code>select * from v_vt_betreuer where vtid =  VTNRVOLL_TO_VTID(11803056);</code></p>

<p><img src="https://i.sstatic.net/l8jmn.png" alt="enter image description here"></p>

## Answers
### Answer ID: 19469559
<p>Are you sure that you are NOT using actual function in schema NPS_WEBCC, but a synonym to a function in schema NPS_WEBCC_DEV?</p>

<p>Condition can't be pushed if DEV schema is not allowed to access objects in APP schema.
You must grant permission for synonym to DEV schema, because view is in DEV schema. That is why it starts working when you copy view into APP schema.</p>

<p>Another problem may occur if you use extended statistics in DEV schema based on DEV function, but that needs to be sorted out after the permissions problem.</p>

<p>You can verify it by checking explain plans of following queries. They shall give optimized result:</p>

<pre><code>-- q1
-- "v_vt_betreuer" is a synonym in app schema to a view in dev schema 
select * from v_vt_betreuer where vtid = NPS_WEBCC_DEV.VTNRVOLL_TO_VTID(11803056);

-- q2
select * from NPS_WEBCC_DEV.v_vt_betreuer where vtid=NPS_WEBCC_DEV.VTNRVOLL_TO_VTID(11803056);
</code></pre>

<p><em>UPD</em>
According to additional investigation most likely problem happens because MERGE grant is missing on the view. It must be granted for the view and all sub-views that are used inside it.</p>

<pre><code>GRANT MERGE VIEW ON v_vt_betreuer TO NPS_WEBCC;
</code></pre>

### Answer ID: 19343246
<p>Try creating an index like this:</p>

<pre><code>CREATE INDEX func_index ON agency(fun(common_column))
</code></pre>

<p>This is called a function based index. </p>

<p>My guess is that this type of queries:</p>

<pre><code>select a1.vtid, a2.* 
from agency a1 join agency_employee b on (b.vtid = a1.vtid)
join agency a2 on (a2.vtid = b.employee_vtid)
</code></pre>

<p>is causing the query optimizer to do this:</p>

<pre><code>select a1.vtid, a2.* 
from agency a1 join agency_employee b on (func(b.vtid) = func(a1.vtid))
join agency a2 on (func(a2.vtid) = func(b.employee_vtid))
</code></pre>

<p><a href="http://www.akadia.com/services/ora_function_based_index_2.html" rel="nofollow">http://www.akadia.com/services/ora_function_based_index_2.html</a>
<a href="http://www.oracle-base.com/articles/8i/function-based-indexes.php" rel="nofollow">http://www.oracle-base.com/articles/8i/function-based-indexes.php</a></p>

<p>If this approach does not help, check if you have ROW LEVEL SECURITY:</p>

<p><a href="http://docs.oracle.com/cd/E16655_01/server.121/e17609/tdpsg_ols.htm" rel="nofollow">http://docs.oracle.com/cd/E16655_01/server.121/e17609/tdpsg_ols.htm</a>
<a href="http://docs.oracle.com/cd/B19306_01/network.102/b14266/apdvcntx.htm#i1007410" rel="nofollow">http://docs.oracle.com/cd/B19306_01/network.102/b14266/apdvcntx.htm#i1007410</a></p>


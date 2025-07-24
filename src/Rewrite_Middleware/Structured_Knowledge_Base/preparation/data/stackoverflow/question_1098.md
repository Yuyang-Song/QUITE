# How to read all &quot;last_changed&quot; records from Firebird DB?
[Link to question](https://stackoverflow.com/questions/59071948/how-to-read-all-last-changed-records-from-firebird-db)
**Creation Date:** 1574863441
**Score:** 2
**Tags:** sql, triggers, firebird
## Question Body
<p>My question is a bit tricky, because it's mostly a logical problem.<br>
I've tried to optimize my app speed by reading everything into memory but only those records, which changed since <em>"last read"</em> = greatest timestamp of records last time loaded.  </p>

<p>FirebirdSQL database engine does not allow to update a field in an "After Trigger" directly, so it's obviously using "before update or insert" triggers to update the field <code>new.last_changed = current_timestamp;</code>  </p>

<h2>The problem:</h2>

<p>As it turns out, this is a totally WRONG method, because those triggers fire on transaction <strong>start</strong>!<br>
So if there is a transaction that takes some more time than an other, the saved "last changed time" will be lower than a short-burst transaction fired and finished in between.<br>
<code>1. tr.:  13:00:01.400 .............................Commit</code>  &lt;&lt; this record will be skipped !<br>
<code>2. tr.:           13:00.01.500......Commit</code> &lt;&lt; reading of data will happen here.<br>
The next read will be <code>&gt;= 13:00.01.500</code>  </p>

<h2>I've tried:</h2>

<p>to rewrite all triggers, so they fire <strong>after</strong> and call an <code>UPDATE orders SET ...</code> &lt;&lt; <em>but this causing circular, self-calling endless events.</em><br>
Would a <code>SET_CONTEXT</code> <a href="https://stackoverflow.com/a/9290926">lock</a> interfere with <strong>multi-row</strong> update and <strong>nested</strong> triggers?<br>
 <em>(I do not see any possibility this method would work <strong>good</strong> if running multiple updates in the same transaction.)</em>  </p>

<p>What is the common solution for all this?</p>

<h2>Edit1:</h2>

<p>What I want to happen is to read <strong>only</strong> those records from DB actually changed since last read. For that to happen, I need the engine to update records AFTER COMMIT. (Not during it, "in the middle".)<br>
This trigger is NOT good, because it will fire on the moment of change, (not after Commit):  </p>

<pre><code>alter trigger SYNC_ORDERS active after insert or update position 999 AS
declare variable N timestamp; 
begin
  N = cast('NOW' as timestamp);
  if (new.last_changed &lt;&gt; :N) then
    update ORDERS set last_changed= :N where ID=new.ID;
end
</code></pre>

<p>And from the application I do:  </p>

<pre><code>Query1.SQL.Text := 'SELECT * FROM orders WHERE last_changed &gt;= ' + DateTimeToStr( latest_record );  
Query1.Open;  
 latest_record := Query1.FieldByName('last_changed').asDateTime;   
</code></pre>

<p><em>.. this code will list only the record commited in the 2th transaction (earlier) and never the first, longer running transaction (commited later).</em></p>

<h2>Edit2:</h2>

<p>It seems I have the same question as <a href="https://stackoverflow.com/questions/3809751/determining-row-changes-since-last-access-in-sql-server">here...</a> , but specially for FirebirdSQL.<br>
There are not really any good solutions there, but gave me an idea:<br>
- What if I create an extra table and log changes earlier than 5 minutes there per table?<br>
- Before each SQL query, first I will ask for any changes in that table, sequenced via ID grow!<br>
- Delete lines older than 23 hours  </p>

<pre><code>ID  TableID  Changed
===========================
1   5   2019.11.27 19:36:21
2   5   2019.11.27 19:31:19
</code></pre>

<h2>Edit3:</h2>

<p>As Arioch already suggested, one solution is to:</p>

<ul>
<li>create a "logger table" filled on every <code>BEFORE INSERT OR UPDATE</code>
trigger by every table </li>
<li>and update the "last_changed" sequence of it
by the <code>ON TRANSACTION COMMIT</code> trigger</li>
</ul>

<p>But, would not be ...</p>

<h2>a better approach?:</h2>

<ul>
<li>adding 1-1 <code>last_sequence INT64 DEFAULT NULL</code> column to every table</li>
<li>create a global generator <code>LAST_GEN</code></li>
<li>update every table's every NULL row with a gen_id(LAST_GEN,1) inside the <code>ON TRANSACTION COMMIT</code> trigger</li>
<li>SET to NULL again on every <code>BEFORE INSERT OR UPDATE</code> trigger</li>
</ul>

<p>So basically switching the <code>last_sequence</code> column of a record to:<br>
 <code>NULL &gt; 1 &gt; NULL &gt; 34</code> ... every time it gets modified.<br>
This way I :</p>

<ul>
<li>do not have to fill the DB with log data, </li>
<li>and I can query the tables directly with <code>WHERE last_sequence&gt;1;</code>. </li>
<li>No needed to pre-query the "logger table" first.</li>
</ul>

<p>I'm just afraid: WHAT happens, if the <code>ON TRANSACTION COMMIT</code> trigger is trying to update a <code>last_sequence</code> field, <strong>while</strong> a 2th transaction's ON BEFORE trigger is locking the record (of an other table)?<br>
Can this happen at all?  </p>

## Answers
### Answer ID: 59160005
<p>The final solution is based on the idea, that:</p>
<ol>
<li>Each table's <code>BEFORE INSERT OR UPDATE</code> trigger can push a time of the transaction: <code>RDB$SET_CONTEXT('USER_TRANSACTION', 'table31', current_timestamp</code>);</li>
<li>The global <code>ON TRANSACTION COMMIT</code> trigger can insert a sequence + time into a &quot;logging table&quot;, if receiving such a context.</li>
<li>It can even take care of &quot;daylight saving changes&quot; and &quot;intervals&quot;, by logging only &quot;big time differences&quot;, like &gt;=1 minute, to reduce the amount of records.)</li>
<li>A stored procedure can ease and speed up the calculation of 'LAST_QUERY_TIME' of each query's.</li>
</ol>
<h2>Example:</h2>
<p>1.)</p>
<pre class="lang-sql prettyprint-override"><code>create trigger ORDERS_BI active before insert or update position 0 AS
BEGIN
  IF (NEW.ID IS NULL) THEN
    NEW.ID = GEN_ID(GEN_ORDERS,1);
  RDB$SET_CONTEXT('USER_TRANSACTION', 'orders_table', current_timestamp);  
END
</code></pre>
<p>2, 3.)</p>
<pre class="lang-sql prettyprint-override"><code>create trigger TRG_SYNC_AFTER_COMMIT ACTIVE ON transaction commit POSITION 1 as 
  declare variable N TIMESTAMP;
  declare variable T VARCHAR(255);
begin
  N = cast('NOW' as timestamp);
  T = RDB$GET_CONTEXT('USER_TRANSACTION', 'orders_table');

  if (:T is not null) then begin
    if (:N &lt; :T) then T = :N; --system time changed eg.: daylight saving&quot; -1 hour
    if (datediff(second from :T to :N) &gt; 60 ) then --more than 1min. passed
      insert into &quot;SYNC_PAST_TIMES&quot; (ID, TABLE_NUMBER, TRG_START, SYNC_TIME, C_USER)
        values (GEN_ID(GEN_SYNC_PAST_TIMES, 1), 31, cast(:T as timestamp), :N, CURRENT_USER);
  end;  

-- other tables too:
  T = RDB$GET_CONTEXT('USER_TRANSACTION', 'details_table');
-- ...

  when any do EXIT;
end 
</code></pre>
<h1>Edit1:</h1>
<p>It is possible to speed up the readout of the &quot;last-time-changed&quot; value from our <code>SYNC_PAST_TIMES</code> table with a help of a Stored Procedure. Logically, You have to store in memory both the ID <code>PT_ID</code> + the time <code>PT_TM</code> in your program to call it for each table.</p>
<pre class="lang-sql prettyprint-override"><code>CREATE PROCEDURE SP_LAST_MODIF_TIME (
    TABLE_NUMBER SM_INT,
    LAST_PASTTIME_ID BG_INT,
    LAST_PASTTIME TIMESTAMP)
RETURNS (
    PT_ID BG_INT,
    PT_TM TIMESTAMP)
AS
  declare variable TEMP_TIME TIMESTAMP;
  declare variable TBL       SMALLINT;
begin

  PT_TM   = :LAST_PASTTIME;
  FOR SELECT p.ID, p.SYNC_TIME, p.TABLA FROM SYNC_PAST_TIMES p WHERE (p.ID &gt; :LAST_PASTTIME_ID)
    ORDER by p.ID ASC
    INTO PT_ID, TEMP_TIME, TBL DO --the PT_ID gets an increasing value immediately
  begin
    if (:TBL = :TABLE_NUMBER) then
      if (:TEMP_TIME&lt; :MI_TIME) then 
        PT_TM = :TEMP_TIME; --searching for the smallest
  end
  
  if (:PT_ID IS NULL) then begin
    PT_ID  = :LAST_PASTTIME_ID;
    PT_TM = :LAST_PASTTIME;
  end
  
  suspend;
END
</code></pre>
<p>You can use this procedure by including in your select, using the <code>WITH .. AS</code> format:</p>
<pre class="lang-sql prettyprint-override"><code>with UTLS as (select first 1 PT_ID, PT_TM from SP_LAST_MODIF_TIME (55, -- TABLE_NUMBER
  0, '1899.12.30 00:00:06.000') ) -- last PT_ID, PT_TM from your APP 
  select first 1000 u.PT_ID, current_timestamp as NOWWW, r.*
  from UTLS u, &quot;Orders&quot; r
  where (r.SYNC_TIME &gt;= u.PT_TM);
</code></pre>
<p>Using <code>FIRST 1000</code> is a must to prevent reading the whole table if all values are changed at once.
<em>Upgrading the SQL, adding a new column, etc. makes <code>SYNC_TIME</code> changing to <code>NOW</code> at the same time at all rows of the table.</em><br />
You may adjust it per table individually, just like the interval of seconds to monitor changes. Add a <strong>check</strong> to your APP, how to handle the case, if the new data reaches 1000 lines at once ...</p>


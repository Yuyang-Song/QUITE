# SQL Server Deadlock by IX pagelock
[Link to question](https://stackoverflow.com/questions/52094622/sql-server-deadlock-by-ix-pagelock)
**Creation Date:** 1535624421
**Score:** 1
**Tags:** sql-server, entity-framework, deadlock
## Question Body
<p>I have a deadlock and I don't see how coult it be solved. I have already fixed some other queries coming from EF side that caused the same deadlock (at same row in the sp) but this one cannot be modified, it's a very basic query and I think there must be an easier way rewriting the SP instead or modifying indexes to avoid page locks.</p>

<p><strong>Three tables:</strong></p>

<ul>
<li>Workitems(Id, DMC,...)</li>
<li>Charges(Id, ...)</li>
<li>ChargeItems(Id, Charge_Id, Workitem_Id, ...)</li>
</ul>

<p><strong>Two processes:</strong></p>

<ul>
<li>An EF query that is called many times. (~5-10/minute)</li>
<li>A stored procedure which is archiving data by moving archives into an other database and deleting them from source.</li>
</ul>

<p><strong>The deadlock:</strong></p>

<p>It is thrown at the very last step when the SP tries to remove empty Charges, where ChargeItems has no records. To this point it has already deleted all ChargeItems and only empty charges and workitems has to be deleted.</p>

<p><a href="https://i.sstatic.net/weWT7.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/weWT7.png" alt="Deadlock graph"></a></p>

<p>The query run by EF is searching for a Workitem by its DMC while the SP tries to remove Charges.</p>

<pre><code>SELECT 
    [Limit1].[Id] AS [Id], 
    [Limit1].[DMC] AS [DMC], 
    [Limit1].[FirstSeen] AS [FirstSeen], 
    [Limit1].[DrawingNo] AS [DrawingNo], 
    [Limit1].[MachineId] AS [MachineId], 
    [Limit1].[WorkItemState_Id] AS [WorkItemState_Id], 
    [Limit1].[ItemType_Id] AS [ItemType_Id], 
    [Limit1].[Repaired] AS [Repaired], 
    [Limit1].[MachineCycle] AS [MachineCycle], 
    [Limit1].[FirstSeenCheck] AS [FirstSeenCheck], 
    [Limit1].[LastSeen] AS [LastSeen], 
    [Limit1].[Archive] AS [Archive], 
    [Limit1].[CastingDateString] AS [CastingDateString], 
    [Limit1].[Deleted] AS [Deleted], 
    [Limit1].[DMC2] AS [DMC2], 
    [Limit1].[Id1] AS [Id1], 
    [Limit1].[WorkPlace_Id] AS [WorkPlace_Id], 
    [Limit1].[CastingFormIdent_Id] AS [CastingFormIdent_Id], 
    [Limit1].[FormIdentItemType_Id] AS [FormIdentItemType_Id]
    FROM ( SELECT TOP (1) 
        [Extent1].[Id] AS [Id], 
        [Extent1].[DMC] AS [DMC], 
        [Extent1].[FirstSeen] AS [FirstSeen], 
        [Extent1].[DrawingNo] AS [DrawingNo], 
        [Extent1].[MachineId] AS [MachineId], 
        [Extent1].[WorkItemState_Id] AS [WorkItemState_Id], 
        [Extent1].[ItemType_Id] AS [ItemType_Id], 
        [Extent1].[Repaired] AS [Repaired], 
        [Extent1].[MachineCycle] AS [MachineCycle], 
        [Extent1].[FirstSeenCheck] AS [FirstSeenCheck], 
        [Extent1].[LastSeen] AS [LastSeen], 
        [Extent1].[Archive] AS [Archive], 
        [Extent1].[CastingDateString] AS [CastingDateString], 
        [Extent1].[Deleted] AS [Deleted], 
        [Extent1].[DMC2] AS [DMC2], 
        [Extent1].[WorkPlace_Id] AS [WorkPlace_Id], 
        [Extent1].[CastingFormIdent_Id] AS [CastingFormIdent_Id], 
        [Extent1].[FormIdentItemType_Id] AS [FormIdentItemType_Id], 
        [Extent2].[Id] AS [Id1]
        FROM WorkItems AS [Extent1]
        LEFT OUTER JOIN [dbo].[ChargeItems] AS [Extent2] ON [Extent1].[Id] = [Extent2].[WorkItem_Id]
        WHERE ([Extent1].[DMC] = '') OR (([Extent1].[DMC] IS NULL))
    )  AS [Limit1]
</code></pre>

<p><strong>Execution plan of the select:</strong></p>

<p><a href="https://i.sstatic.net/4HyK5.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/4HyK5.jpg" alt="Execution plan of the select statement from a different run. (Not caused deadlock.)"></a></p>

<p><strong>Part of the SP:</strong></p>

<pre><code>;with chargesToDelete(id, ciid) as (
                    select c.id, ci.Id from @chargeids c
                    left join dbo.chargeitems ci on ci.Charge_Id = c.id
                    where ci.id is null
                )

                delete from dbo.charges
                    where Id in (select id from chargesToDelete)
</code></pre>

<p><strong>Deadlock graph xml:</strong></p>

<pre><code>    &lt;deadlock&gt;
 &lt;victim-list&gt;
  &lt;victimProcess id="process6472ad498" /&gt;
 &lt;/victim-list&gt;
 &lt;process-list&gt;
  &lt;process id="process6472ad498" taskpriority="5" logused="152924" waitresource="PAGE: 5:1:531207 " waittime="794" ownerId="10001638" transactionname="DELETE" lasttranstarted="2018-08-29T11:50:14.510" XDES="0x6ff07f078" lockMode="IX" schedulerid="7" kpid="7620" status="suspended" spid="89" sbid="0" ecid="0" priority="-5" trancount="2" lastbatchstarted="2018-08-29T11:22:53.457" lastbatchcompleted="2018-08-29T11:22:53.457" lastattention="1900-01-01T00:00:00.457" clientapp="Microsoft SQL Server Management Studio - Query" hostname="PCSERVER151" hostpid="6480" loginname="PRC\administrator" isolationlevel="read uncommitted (1)" xactid="10001638" currentdb="5" lockTimeout="4294967295" clientoption1="673187936" clientoption2="390200"&gt;
   &lt;executionStack&gt;
    &lt;frame procname="LP_R.dbo.Archive_Finish" line="190" stmtstart="12876" stmtend="13044" sqlhandle="0x03000500063ecd76e962c80014a9000001000000000000000000000000000000000000000000000000000000"&gt;
delete from LP_R.dbo.workitems where id in (select id from @workitemIds);    &lt;/frame&gt;
    &lt;frame procname="LP_R.dbo.Archive" line="64" stmtstart="5142" stmtend="5244" sqlhandle="0x030005007886b57874f2b30014a9000001000000000000000000000000000000000000000000000000000000"&gt;
exec Archive_Finish @Day, @Dryrun, @MaxWorkitems;    &lt;/frame&gt;
    &lt;frame procname="adhoc" line="4" stmtstart="62" stmtend="200" sqlhandle="0x0100050010f3f82c309a63770600000000000000000000000000000000000000000000000000000000000000"&gt;
EXEC    @return_value = [dbo].[Archive]
        @Day = 450,
        @Dryrun = 0    &lt;/frame&gt;
   &lt;/executionStack&gt;
   &lt;inputbuf&gt;

DECLARE @return_value int

EXEC    @return_value = [dbo].[Archive]
        @Day = 450,
        @Dryrun = 0

SELECT  'Return Value' = @return_value

   &lt;/inputbuf&gt;
  &lt;/process&gt;
  &lt;process id="process66f184558" taskpriority="0" logused="0" waitresource="PAGE: 5:1:114492 " waittime="913" ownerId="10002051" transactionname="SELECT" lasttranstarted="2018-08-29T11:50:15.210" XDES="0x6b379ad00" lockMode="S" schedulerid="5" kpid="3860" status="suspended" spid="67" sbid="2" ecid="0" priority="0" trancount="0" lastbatchstarted="2018-08-29T11:50:15.210" lastbatchcompleted="2018-08-29T11:50:15.210" lastattention="1900-01-01T00:00:00.210" clientapp="EntityFramework" hostname="PCSERVER151" hostpid="3520" loginname="sa" isolationlevel="read committed (2)" xactid="10002051" currentdb="5" lockTimeout="4294967295" clientoption1="671088672" clientoption2="128056"&gt;
   &lt;executionStack&gt;
    &lt;frame procname="adhoc" line="1" stmtstart="56" sqlhandle="0x02000000412fd7099fe0d3410b538a2193192ac8c5143cf20000000000000000000000000000000000000000"&gt;
SELECT 
    [Limit1].[Id] AS [Id], 
    [Limit1].[DMC] AS [DMC], 
    [Limit1].[FirstSeen] AS [FirstSeen], 
    [Limit1].[DrawingNo] AS [DrawingNo], 
    [Limit1].[MachineId] AS [MachineId], 
    [Limit1].[WorkItemState_Id] AS [WorkItemState_Id], 
    [Limit1].[ItemType_Id] AS [ItemType_Id], 
    [Limit1].[Repaired] AS [Repaired], 
    [Limit1].[MachineCycle] AS [MachineCycle], 
    [Limit1].[FirstSeenCheck] AS [FirstSeenCheck], 
    [Limit1].[LastSeen] AS [LastSeen], 
    [Limit1].[Archive] AS [Archive], 
    [Limit1].[CastingDateString] AS [CastingDateString], 
    [Limit1].[Deleted] AS [Deleted], 
    [Limit1].[DMC2] AS [DMC2], 
    [Limit1].[Id1] AS [Id1], 
    [Limit1].[WorkPlace_Id] AS [WorkPlace_Id], 
    [Limit1].[CastingFormIdent_Id] AS [CastingFormIdent_Id], 
    [Limit1].[FormIdentItemType_Id] AS [FormIdentItemType_Id]
    FROM ( SELECT TOP (1) 
        [Extent1].[Id] AS [Id], 
        [Extent1].[DMC] AS [DMC], 
        [Extent1].[FirstSeen] AS [FirstSeen], 
        [Extent1    &lt;/frame&gt;
    &lt;frame procname="unknown" line="1" sqlhandle="0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"&gt;
unknown    &lt;/frame&gt;
   &lt;/executionStack&gt;
   &lt;inputbuf&gt;
(@p__linq__0 nvarchar(4000))SELECT 
    [Limit1].[Id] AS [Id], 
    [Limit1].[DMC] AS [DMC], 
    [Limit1].[FirstSeen] AS [FirstSeen], 
    [Limit1].[DrawingNo] AS [DrawingNo], 
    [Limit1].[MachineId] AS [MachineId], 
    [Limit1].[WorkItemState_Id] AS [WorkItemState_Id], 
    [Limit1].[ItemType_Id] AS [ItemType_Id], 
    [Limit1].[Repaired] AS [Repaired], 
    [Limit1].[MachineCycle] AS [MachineCycle], 
    [Limit1].[FirstSeenCheck] AS [FirstSeenCheck], 
    [Limit1].[LastSeen] AS [LastSeen], 
    [Limit1].[Archive] AS [Archive], 
    [Limit1].[CastingDateString] AS [CastingDateString], 
    [Limit1].[Deleted] AS [Deleted], 
    [Limit1].[DMC2] AS [DMC2], 
    [Limit1].[Id1] AS [Id1], 
    [Limit1].[WorkPlace_Id] AS [WorkPlace_Id], 
    [Limit1].[CastingFormIdent_Id] AS [CastingFormIdent_Id], 
    [Limit1].[FormIdentItemType_Id] AS [FormIdentItemType_Id]
    FROM ( SELECT TOP (1) 
        [Extent1].[Id] AS [Id], 
        [Extent1].[DMC] AS [DMC], 
        [Extent1].[FirstSeen] AS [F   &lt;/inputbuf&gt;
  &lt;/process&gt;
 &lt;/process-list&gt;
 &lt;resource-list&gt;
  &lt;pagelock fileid="1" pageid="531207" dbid="5" subresource="FULL" objectname="LP_R.dbo.WorkItems" id="lock6d7b2d800" mode="S" associatedObjectId="72057594043891712"&gt;
   &lt;owner-list&gt;
    &lt;owner id="process66f184558" mode="S" /&gt;
   &lt;/owner-list&gt;
   &lt;waiter-list&gt;
    &lt;waiter id="process6472ad498" mode="IX" requestType="wait" /&gt;
   &lt;/waiter-list&gt;
  &lt;/pagelock&gt;
  &lt;pagelock fileid="1" pageid="114492" dbid="5" subresource="FULL" objectname="LP_R.dbo.WorkItems" id="lock5cd1a2b00" mode="IX" associatedObjectId="72057594043891712"&gt;
   &lt;owner-list&gt;
    &lt;owner id="process6472ad498" mode="IX" /&gt;
   &lt;/owner-list&gt;
   &lt;waiter-list&gt;
    &lt;waiter id="process66f184558" mode="S" requestType="wait" /&gt;
   &lt;/waiter-list&gt;
  &lt;/pagelock&gt;
 &lt;/resource-list&gt;
&lt;/deadlock&gt;
</code></pre>

## Answers
### Answer ID: 52099414
<p>First, since there are S lock in this deadlock, consider switching the database to READ COMMITTED SNAPSHOT, so that your SELECT queries will use row versioning instead of S locks to read the database.  This will solve all S/X deadlock and other blocking in one fell swoop, but you will need to test.</p>

<p>Second, to address this deadlock, use a transaction in your stored procedure and get a big lock early.  For instance instead of an IX lock force it to acquire an exclusive table lock with the TABLOCKX hint.  Deadlocks only happen when two sessions <em>first</em> get compatible locks, then <em>later</em> try to get incompatible locks.  IX and S locks are the start of this deadlock, so you can head it off by making sure that the stored procedure doesn't acquire the puny IX, and wait until it can acquire a lock that will enable it to complete successfully.</p>

### Answer ID: 52095383
<p>(as a side-note)</p>

<pre><code>delete c 
from dbo.charges c
inner join @chargeids t
  on t.id = c.id
where not exists(
  select 1 from dbo.chargeitems ci 
  where ci.Charge_id = c.id
)
</code></pre>

<p>I suppose there are no <code>chargeitems</code> already at this stage actually. And they were probably deleted just before this delete statement. So archiving process transaction could be much longer then it's shown.</p>

<p>So, your delete process is deleting specific <code>rows</code> and places an intent-X lock on pages, whilst reading process is scanning <code>pages</code>, probably, in different order. <code>FK</code>s could place some more locks if there are any. </p>

<h1>TIPS</h1>

<p>Have a look at select statement's actual execution plan. It is requesting <code>TOP 1</code> with no order, uses far not precise <code>where</code> predicate and joins <code>chargeitems</code> on <code>workitem_id</code> (which perhaps has no index on it). Fixing it could help getting rid of <code>scan</code> (if any) while reading. May be you could try to select <code>top1 workitem</code> and only after that select <code>top1 chargeitem</code> for it.</p>

<p>You could try to apply <code>READPAST</code> hint on reading statement (will not be waiting for locked pages) or raise granularity of delete statements to <code>PAGLOCK</code> for example. Try <code>TABLOCK</code> for delete process if it's rarely executed, and if it's fine for this system.</p>

<h1>UPD</h1>

<p>Actually I missed the major point: you pointed at delete from <code>charges</code> whereas deadlock is on <code>WorkItem</code> (as deadlock graph is clearly showing). But this does not cancel the rest of my assumptions.
As the execution plan shows <code>WorkItem</code> is truly scanned whilst this delete is performed on specific rows:</p>

<pre><code>delete from LP_R.dbo.workitems where id in (select id from @workitemIds); 
</code></pre>

<p>You can apply tips from my post to select statement and/or delete statement (all of them within archiving proc).</p>


# Slow query where index isn&#39;t used
[Link to question](https://stackoverflow.com/questions/24497055/slow-query-where-index-isnt-used)
**Creation Date:** 1404154714
**Score:** 1
**Tags:** postgresql, indexing
## Question Body
<h1>Overview</h1>

<p>I've been working on Netdot trying to speed up some of the queries.  Some of them can benefit from SQL changes because of unneeded joins or broad searches, but some have proven harder to track down.</p>

<p>In this particular case I've got two tables.  fwtableentry has 132,233,684 rows.  fwtable has 2,178,088 rows.</p>

<h2>hardware / software versions</h2>

<p>This is a virtual machine running debian_version 7.5 (wheezy).  The disks are on a SAN with raid 0+1.  The machine has 4GB of ram allocated to it.  I/O and memory don't appear to be an issue but I can allocate more resources if need be.</p>

<pre><code>Linux netdot 3.2.0-4-amd64 #1 SMP Debian 3.2.57-3+deb7u2 x86_64 GNU/Linux
</code></pre>

<p>Running Postgres 9.1.13-0wheezy1 (debian package version)</p>

<h3>Sysctl Options</h3>

<pre><code>kernel.shmmax = 1500000000
vm.overcommit_memory = 2
</code></pre>

<h3>Postgres Options</h3>

<p>I started with the defaults.  I've now modified them referencing another server that I had previously tuned according to one of the postgres tuning docs.  The changes don't seem to help for the slow queries but might be helping for other things.</p>

<pre><code>shared_buffers = 1GB            # min 128kB
work_mem = 64MB             # min 64kB
maintenance_work_mem = 256MB        # min 1MB
wal_buffers = 16MB          # min 32kB, -1 sets based on shared_buffers
checkpoint_segments = 32        # in logfile segments, min 1, 16MB each
checkpoint_timeout = 10min      # range 30s-1h
checkpoint_completion_target = 0.9  # checkpoint target duration, 0.0 - 1.0
random_page_cost = 2.5          # same scale as above
effective_cache_size = 2GB
</code></pre>

<h2>Explain showing the problem</h2>

<pre><code>netdot=# explain analyze SELECT   ft.tstamp
              FROM     fwtableentry fte, fwtable ft
              WHERE    fte.physaddr=9115
                AND    fte.fwtable=ft.id
              GROUP BY ft.tstamp
              ORDER BY ft.tstamp DESC
              LIMIT 10
;
                                                                    QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=53610.80..53610.82 rows=10 width=8) (actual time=27436.502..27436.631 rows=10 loops=1)
   -&gt;  Sort  (cost=53610.80..53617.92 rows=2849 width=8) (actual time=27436.220..27436.258 rows=10 loops=1)
         Sort Key: ft.tstamp
         Sort Method: top-N heapsort  Memory: 25kB
         -&gt;  HashAggregate  (cost=53520.74..53549.23 rows=2849 width=8) (actual time=27417.749..27425.805 rows=2876 loops=1)
                -&gt;  Nested Loop  (cost=125.79..53500.91 rows=7933 width=8) (actual time=98.801..27367.988 rows=3562 loops=1)
                      -&gt;  Bitmap Heap Scan on fwtableentry fte  (cost=125.79..18909.68 rows=7933 width=8) (actual time=97.718..26942.693 rows=3562 loops=1)
                            Recheck Cond: (physaddr = 9115)
                           -&gt;  Bitmap Index Scan on "FWTableEntry3"  (cost=0.00..123.81 rows=7933 width=0) (actual time=86.433..86.433 rows=3562 loops=1)
                                 Index Cond: (physaddr = 9115)
                      -&gt;  Index Scan using pk_fwtable on fwtable ft  (cost=0.00..4.35 rows=1 width=16) (actual time=0.069..0.077 rows=1 loops=3562)
                            Index Cond: (id = fte.fwtable)
 Total runtime: 27449.802 ms
</code></pre>

<h2>Here are the two tables</h2>

<h3>fwtable</h3>

<pre><code>netdot=# \d fwtable
                                           Table "public.fwtable"
 Column |            Type             |                              Modifiers
 --------+-----------------------------+---------------------------------------------------------------------
  device | bigint                      | not null
  id     | bigint                      | not null default nextval('fwtable_id_seq'::regclass)
  tstamp | timestamp without time zone | not null default '1970-01-02 00:00:01'::timestamp without time zone
Indexes:
    "pk_fwtable" PRIMARY KEY, btree (id)
    "fwtable1" UNIQUE CONSTRAINT, btree (device, tstamp)
    "FWTable2" btree (device)
    "FWTable3" btree (tstamp)
Foreign-key constraints:
     "fk_device" FOREIGN KEY (device) REFERENCES device(id) DEFERRABLE
Referenced by:
     TABLE "fwtableentry" CONSTRAINT "fk_fwtable" FOREIGN KEY (fwtable) REFERENCES fwtable(id) DEFERRABLE
</code></pre>

<h3>fwtableentry</h3>

<pre><code>netdot=# \d fwtableentry
                          Table "public.fwtableentry"
  Column   |  Type  |                         Modifiers
-----------+--------+-----------------------------------------------------------
 fwtable   | bigint | not null
 id        | bigint | not null default nextval('fwtableentry_id_seq'::regclass)
 interface | bigint | not null
 physaddr  | bigint | not null
Indexes:
    "pk_fwtableentry" PRIMARY KEY, btree (id)
    "FWTableEntry1" btree (fwtable)
    "FWTableEntry2" btree (interface)
    "FWTableEntry3" btree (physaddr)
Foreign-key constraints:
    "fk_fwtable" FOREIGN KEY (fwtable) REFERENCES fwtable(id) DEFERRABLE
    "fk_interface" FOREIGN KEY (interface) REFERENCES interface(id) DEFERRABLE
    "fk_physaddr" FOREIGN KEY (physaddr) REFERENCES physaddr(id) DEFERRABLE
</code></pre>

<h2>Here is a sample of the two tables</h2>

<h3>first fwtableentry:</h3>

<pre><code> fwtable |    id     | interface | physaddr
---------+-----------+-----------+----------
  675157 |  39733332 |     29577 |     9115
  674352 |  39686929 |     29577 |     9115
     344 |     19298 |     29577 |     9115
    1198 |     68328 |     29577 |     9115
    1542 |     88107 |     29577 |     9115
  675960 |  39779466 |     29577 |     9115
  675750 |  39766468 |     39946 |     9115
    2994 |    168721 |     29577 |     9115
    3895 |    218228 |     29577 |     9115
    4795 |    267949 |     29577 |     9115
    5695 |    324905 |     29577 |     9115
  674944 |  39720652 |     39946 |     9115
    6595 |    375149 |     29577 |     9115
    7501 |    425045 |     29577 |     9115
    8400 |    475265 |     29577 |     9115
    9298 |    524985 |     29577 |     9115
   10200 |    575136 |     29577 |     9115
   11104 |    626065 |     29577 |     9115
   12011 |    677963 |     29577 |     9115
  676580 |  39814792 |     39946 |     9115
   12914 |    731390 |     29577 |     9115
  677568 |  39871297 |     29577 |     9115
   13821 |    784435 |     29577 |     9115
  676760 |  39825496 |     29577 |     9115
</code></pre>

<h3>fwtable (minus the device column):</h3>

<pre><code>   id    |       tstamp
---------+---------------------
 2178063 | 2014-06-10 17:00:13
 2177442 | 2014-06-10 16:00:06
 2176816 | 2014-06-10 15:00:07
 2176190 | 2014-06-10 14:00:09
 2175566 | 2014-06-10 13:00:07
 2174941 | 2014-06-10 12:00:07
 2174316 | 2014-06-10 11:00:07
 2173689 | 2014-06-10 10:00:06
 2173065 | 2014-06-10 09:00:06
 2172444 | 2014-06-10 08:00:06
(10 rows)
</code></pre>

<h2>Problem as far as I can tell</h2>

<p>So, the problem is you need to know what ids to send to fwtable, but you can't know which ones match the 10 latest timestamps so you need to send them all, then let the index on fwtable determine which ones to throw away.</p>

<pre><code>netdot=# select count(*) from fwtableentry where physaddr = 9115;
 count
-------
  3562
(1 row)
</code></pre>

<p>This is also the reason that, once cached, the query is fast.  The joined datasets aren't huge so once it has an idea of what to do it can cache everything needed.</p>

<p>You might ask why not just pick the latest 10 timestamps and match against those, but the issue is that those timestamps might not have any results with that physaddr, so you need to check the results of the join.</p>

<h2>Rewriting the query</h2>

<pre><code>select ft.tstamp from fwtable ft where ft.id in (select fwtable from fwtableentry where physaddr = 9115) order by ft.tstamp desc limit 10;
</code></pre>

<p>Still gives the same query plan but makes it easier for me to visualize the problems. Actually, ordering the query this way forces using of the plan even if you drop the sort.</p>

<p>You would think an index on fwtable (id, tstamp DESC) might help but it doesn't seem to get used.  I can see how any index would be confused since it's taking a bunch of results from all over the place.</p>

<p>I thought it might help to tell the database that the relationship between id and tstamp was 1:1, so I added a unique index for the two.  It didn't.</p>

<p>Dropping the limit doesn't affect the plan.  It's only the sort that kills the performance.</p>

<p>Short of a materialized view with the three needed columns (which is impractical due to table size I think..) I'm not sure of a way to resolve this, but I might just not be SQL smart enough to realize the real problem.</p>

<h1>Final notes</h1>

<p>You can drop the GROUP BY in the first query, it's unneeded.  I've dropped off a few tables from the joins that weren't needed for this example.  They don't affect query speed as much as this issue and aren't needed in general so I'll probably rewrite the code to permanently leave them out.</p>

<p>I should also mention that drastic changes to the schema aren't really something I can do.  I may be able to propose it as a last ditch measure if it is the only solution to the problem, but Netdot isn't my program so I don't know how much I can change to fix something that may bother me more than other people.</p>

## Answers
### Answer ID: 24498331
<p>Try rewiting into an <code>exists(...)</code> instead of an <code>IN(...)</code> Plus remove the (unneeded) <code>GROUP BY</code>;  this may avoid aggregation</p>

<pre><code>SELECT ft.tstamp
FROM  fwtable ft
WHERE EXISTS(
    SELECT *
    FROM  fwtableentry fte
    WHERE fte.physaddr=9115
    AND   fte.fwtable=ft.id
    )
-- GROUP BY ft.tstamp -- you don't need this
ORDER BY ft.tstamp DESC
LIMIT 10 -- LIMIT could kill your performance...
;
</code></pre>

### Answer ID: 24497829
<p>If you can constrain the query by timestamp too, then you might find an index on (tstamp, physaddr) useful*. It's a question of whether a query of the "top 10 in the last 30 days" is acceptable. As it stands I don't think there's anything smarter the planner could do, there's no reason for it to expect physaddr values to appear anywhere in particular.</p>

<p>* or perhaps (physaddr,tstamp) - it will depend upon the distribution of values.</p>


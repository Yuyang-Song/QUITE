# Query runs in original DB with local tables but not when tables migrated to SQL Server - Error: &quot;Too many fields defined&quot;
[Link to question](https://stackoverflow.com/questions/16826185/query-runs-in-original-db-with-local-tables-but-not-when-tables-migrated-to-sql)
**Creation Date:** 1369874694
**Score:** 0
**Tags:** ms-access, ms-access-2007
## Question Body
<p>I'm migrating the tables in an Access database to SQL Server via the SQL Server Migration Assistant (SSMA).  I've come across a strange query that runs successfully in the original version of the database, with local tables, but not in the migrated database, with linked tables linking to a SQL Server backend database.</p>

<p>In the migrated database, when I try to run the query I get an error message: "Too many fields defined".</p>

<p>My question is: Why should this query run with local tables but fail with too many fields with linked tables?</p>

<p>The query explicitly lists the fields, it doesn't use SELECT *.  By my count there are 69 fields in the query, although several of them are calculated fields, summing up to 14 fields in the underlying tables each.  </p>

<p>A forum post I've read <a href="http://www.access-programmers.co.uk/forums/showthread.php?t=204336" rel="nofollow">here</a> suggests Access counts the underlying fields in the tables or queries that are joined to make the query.  Is that correct?  If so, perhaps that is the cause of the problem, as the migration process adds SSMA_TimeStamp columns to the migrated tables.  If this is the problem, does anyone know a way around it?  Would splitting some of the calculated fields out into another query and reading from that new query work?</p>

<p>Here's the query:</p>

<pre><code>SELECT maininfo.id, 
       department.deptgroup, 
       department.deptgrp_desc, 
       department.dept_code, 
       department.dept_name, 
       logs_id_plan.dcpickdate, 
       maininfo.instore_date, 
       maininfo.dc_delivery, 
       Iif([idtotal] = 0, [totalsingleqty] * 0.7, [idtotal]) AS 
       [ID Estimate Qty], 
       [s1_total] + [s2_total] + [s3_total] + [s4_total] 
       + [s5_total] + [s6_total] + [s7_total] + [s8_total] 
       + [s9_total] + [s10_total] + [s11_total] 
       + [s12_total] + [s13_total] + [s14_total]             AS TotalSingleQty, 
       Nz([idpacka], 0) + Nz([idpackb], 0)                   AS IDTotal, 
       [totalapacks] * [ppa_total_ratio]                     AS IDPackA, 
       [totalbpacks] * [ppb_total_ratio]                     AS IDPackB, 
       [totalaa] + [totalab] + [totalac] + [totalad] 
       + [totalae]                                           AS TotalAPacks, 
       [totalba] + [totalbb] + [totalbc] + [totalbd] 
       + [totalbe]                                           AS TotalBPacks, 
       [gradeaqty] * [pa_qty_a]                              AS TotalAA, 
       [gradebqty] * [pa_qty_b]                              AS TotalAB, 
       [gradecqty] * [pa_qty_c]                              AS TotalAC, 
       [gradedqty] * [pa_qty_d]                              AS TotalAD, 
       [gradeeqty] * [pa_qty_e]                              AS TotalAE, 
       [gradebqty] * [pb_qty_a]                              AS TotalBA, 
       [gradebqty] * [pb_qty_b]                              AS TotalBB, 
       [gradecqty] * [pb_qty_c]                              AS TotalBC, 
       [gradedqty] * [pb_qty_d]                              AS TotalBD, 
       [gradeeqty] * [pb_qty_e]                              AS TotalBE, 
       [pac1_total] + [pac2_total] + [pac3_total] 
       + [pac4_total] + [pac5_total] + [pac6_total] 
       + [pac7_total] + [pac8_total] + [pac9_total] 
       + [pac10_total]                                       AS PPA_Total_Ratio, 
       [pbc1_total] + [pbc2_total] + [pbc3_total] 
       + [pbc4_total] + [pbc5_total] + [pbc6_total] 
       + [pbc7_total] + [pbc8_total] + [pbc9_total] 
       + [pbc10_total]                                       AS PPB_Total_Ratio, 
       [ppac1s1] + [ppac1s2] + [ppac1s3] + [ppac1s4] 
       + [ppac1s5] + [ppac1s6] + [ppac1s7] + [ppac1s8] 
       + [ppac1s9] + [ppac1s10] + [ppac1s11] + [ppac1s12] 
       + [ppac1s13] + [ppac1s14]                             AS PAC1_Total, 
       [ppac2s1] + [ppac2s2] + [ppac2s3] + [ppac2s4] 
       + [ppac2s5] + [ppac2s6] + [ppac2s7] + [ppac2s8] 
       + [ppac2s9] + [ppac2s10] + [ppac2s11] + [ppac2s12] 
       + [ppac2s13] + [ppac2s14]                             AS PAC2_Total, 
       [ppac3s1] + [ppac3s2] + [ppac3s3] + [ppac3s4] 
       + [ppac3s5] + [ppac3s6] + [ppac3s7] + [ppac3s8] 
       + [ppac3s9] + [ppac3s10] + [ppac3s11] + [ppac3s12] 
       + [ppac3s13] + [ppac3s14]                             AS PAC3_Total, 
       [ppac4s1] + [ppac4s2] + [ppac4s3] + [ppac4s4] 
       + [ppac4s5] + [ppac4s6] + [ppac4s7] + [ppac4s8] 
       + [ppac4s9] + [ppac4s10] + [ppac4s11] + [ppac4s12] 
       + [ppac4s13] + [ppac4s14]                             AS PAC4_Total, 
       [ppac5s1] + [ppac5s2] + [ppac5s3] + [ppac5s4] 
       + [ppac5s5] + [ppac5s6] + [ppac5s7] + [ppac5s8] 
       + [ppac5s9] + [ppac5s10] + [ppac5s11] + [ppac5s12] 
       + [ppac5s13] + [ppac5s14]                             AS PAC5_Total, 
       [ppac6s1] + [ppac6s2] + [ppac6s3] + [ppac6s4] 
       + [ppac6s5] + [ppac6s6] + [ppac6s7] + [ppac6s8] 
       + [ppac6s9] + [ppac6s10] + [ppac6s11] + [ppac6s12] 
       + [ppac6s13] + [ppac6s14]                             AS PAC6_Total, 
       [ppac7s1] + [ppac7s2] + [ppac7s3] + [ppac7s4] 
       + [ppac7s5] + [ppac7s6] + [ppac7s7] + [ppac7s8] 
       + [ppac7s9] + [ppac7s10] + [ppac7s11] + [ppac7s12] 
       + [ppac7s13] + [ppac7s14]                             AS PAC7_Total, 
       [ppac8s1] + [ppac8s2] + [ppac8s3] + [ppac8s4] 
       + [ppac8s5] + [ppac8s6] + [ppac8s7] + [ppac8s8] 
       + [ppac8s9] + [ppac8s10] + [ppac8s11] + [ppac8s12] 
       + [ppac8s13] + [ppac8s14]                             AS PAC8_Total, 
       [ppac9s1] + [ppac9s2] + [ppac9s3] + [ppac9s4] 
       + [ppac9s5] + [ppac9s6] + [ppac9s7] + [ppac9s8] 
       + [ppac9s9] + [ppac9s10] + [ppac9s11] + [ppac9s12] 
       + [ppac9s13] + [ppac9s14]                             AS PAC9_Total, 
       [ppac10s1] + [ppac10s2] + [ppac10s3] + [ppac10s4] 
       + [ppac10s5] + [ppac10s6] + [ppac10s7] + [ppac10s8] 
       + [ppac10s9] + [ppac10s10] + [ppac10s11] 
       + [ppac10s12] + [ppac10s13] + [ppac10s14]             AS PAC10_Total, 
       [ppbc1s1] + [ppbc1s2] + [ppbc1s3] + [ppbc1s4] 
       + [ppbc1s5] + [ppbc1s6] + [ppbc1s7] + [ppbc1s8] 
       + [ppbc1s9] + [ppbc1s10] + [ppbc1s11] + [ppbc1s12] 
       + [ppbc1s13] + [ppbc1s14]                             AS PBC1_Total, 
       [ppbc2s1] + [ppbc2s2] + [ppbc2s3] + [ppbc2s4] 
       + [ppbc2s5] + [ppbc2s6] + [ppbc2s7] + [ppbc2s8] 
       + [ppbc2s9] + [ppbc2s10] + [ppbc2s11] + [ppbc2s12] 
       + [ppbc2s13] + [ppbc2s14]                             AS PBC2_Total, 
       [ppbc3s1] + [ppbc3s2] + [ppbc3s3] + [ppbc3s4] 
       + [ppbc3s5] + [ppbc3s6] + [ppbc3s7] + [ppbc3s8] 
       + [ppbc3s9] + [ppbc3s10] + [ppbc3s11] + [ppbc3s12] 
       + [ppbc3s13] + [ppbc3s14]                             AS PBC3_Total, 
       [ppbc4s1] + [ppbc4s2] + [ppbc4s3] + [ppbc4s4] 
       + [ppbc4s5] + [ppbc4s6] + [ppbc4s7] + [ppbc4s8] 
       + [ppbc4s9] + [ppbc4s10] + [ppbc4s11] + [ppbc4s12] 
       + [ppbc4s13] + [ppbc4s14]                             AS PBC4_Total, 
       [ppbc5s1] + [ppbc5s2] + [ppbc5s3] + [ppbc5s4] 
       + [ppbc5s5] + [ppbc5s6] + [ppbc5s7] + [ppbc5s8] 
       + [ppbc5s9] + [ppbc5s10] + [ppbc5s11] + [ppbc5s12] 
       + [ppbc5s13] + [ppbc5s14]                             AS PBC5_Total, 
       [ppbc6s1] + [ppbc6s2] + [ppbc6s3] + [ppbc6s4] 
       + [ppbc6s5] + [ppbc6s6] + [ppbc6s7] + [ppbc6s8] 
       + [ppbc6s9] + [ppbc6s10] + [ppbc6s11] + [ppbc6s12] 
       + [ppbc6s13] + [ppbc6s14]                             AS PBC6_Total, 
       [ppbc7s1] + [ppbc7s2] + [ppbc7s3] + [ppbc7s4] 
       + [ppbc7s5] + [ppbc7s6] + [ppbc7s7] + [ppbc7s8] 
       + [ppbc7s9] + [ppbc7s10] + [ppbc7s11] + [ppbc7s12] 
       + [ppbc7s13] + [ppbc7s14]                             AS PBC7_Total, 
       [ppbc8s1] + [ppbc8s2] + [ppbc8s3] + [ppbc8s4] 
       + [ppbc8s5] + [ppbc8s6] + [ppbc8s7] + [ppbc8s8] 
       + [ppbc8s9] + [ppbc8s10] + [ppbc8s11] + [ppbc8s12] 
       + [ppbc8s13] + [ppbc8s14]                             AS PBC8_Total, 
       [ppbc9s1] + [ppbc9s2] + [ppbc9s3] + [ppbc9s4] 
       + [ppbc9s5] + [ppbc9s6] + [ppbc9s7] + [ppbc9s8] 
       + [ppbc9s9] + [ppbc9s10] + [ppbc9s11] + [ppbc9s12] 
       + [ppbc9s13] + [ppbc9s14]                             AS PBC9_Total, 
       [ppbc10s1] + [ppbc10s2] + [ppbc10s3] + [ppbc10s4] 
       + [ppbc10s5] + [ppbc10s6] + [ppbc10s7] + [ppbc10s8] 
       + [ppbc10s9] + [ppbc10s10] + [ppbc10s11] 
       + [ppbc10s12] + [ppbc10s13] + [ppbc10s14]             AS PBC10_Total, 
       [totalaa] + [totalba]                                 AS ID_AStores, 
       [totalab] + [totalbb]                                 AS ID_BStores, 
       [totalac] + [totalbc]                                 AS ID_CStores, 
       [totalad] + [totalbd]                                 AS ID_DStores, 
       [totalae] + [totalbe]                                 AS ID_EStores, 
       [c1s1] + [c2s1] + [c3s1] + [c4s1] + [c5s1] + [c6s1] 
       + [c7s1] + [c8s1] + [c9s1] + [c10s1]                  AS S1_Total, 
       [c1s2] + [c2s2] + [c3s2] + [c4s2] + [c5s2] + [c6s2] 
       + [c7s2] + [c8s2] + [c9s2] + [c10s2]                  AS S2_Total, 
       [c1s3] + [c2s3] + [c3s3] + [c4s3] + [c5s3] + [c6s3] 
       + [c7s3] + [c8s3] + [c9s3] + [c10s3]                  AS S3_Total, 
       [c1s4] + [c2s4] + [c3s4] + [c4s4] + [c5s4] + [c6s4] 
       + [c7s4] + [c8s4] + [c9s4] + [c10s4]                  AS S4_Total, 
       [c1s5] + [c2s5] + [c3s5] + [c4s5] + [c5s5] + [c6s5] 
       + [c7s5] + [c8s5] + [c9s5] + [c10s5]                  AS S5_Total, 
       [c1s6] + [c2s6] + [c3s6] + [c4s6] + [c5s6] + [c6s6] 
       + [c7s6] + [c8s6] + [c9s6] + [c10s6]                  AS S6_Total, 
       [c1s7] + [c2s7] + [c3s7] + [c4s7] + [c5s7] + [c6s7] 
       + [c7s7] + [c8s7] + [c9s7] + [c10s7]                  AS S7_Total, 
       [c1s8] + [c2s8] + [c3s8] + [c4s8] + [c5s8] + [c6s8] 
       + [c7s8] + [c8s8] + [c9s8] + [c10s8]                  AS S8_Total, 
       [c1s9] + [c2s9] + [c3s9] + [c4s9] + [c5s9] + [c6s9] 
       + [c7s9] + [c8s9] + [c9s9] + [c10s9]                  AS S9_Total, 
       [c1s10] + [c2s10] + [c3s10] + [c4s10] + [c5s10] 
       + [c6s10] + [c7s10] + [c8s10] + [c9s10] + [c10s10]    AS S10_Total, 
       [c1s11] + [c2s11] + [c3s11] + [c4s11] + [c5s11] 
       + [c6s11] + [c7s11] + [c8s11] + [c9s11] + [c10s11]    AS S11_Total, 
       [c1s12] + [c2s12] + [c3s12] + [c4s12] + [c5s12] 
       + [c6s12] + [c7s12] + [c8s12] + [c9s12] + [c10s12]    AS S12_Total, 
       [c1s13] + [c2s13] + [c3s13] + [c4s13] + [c5s13] 
       + [c6s13] + [c7s13] + [c8s13] + [c9s13] + [c10s13]    AS S13_Total, 
       [c1s14] + [c2s14] + [c3s14] + [c4s14] + [c5s14] 
       + [c6s14] + [c7s14] + [c8s14] + [c9s14] + [c10s14]    AS S14_Total, 
       maininfo.vendor, 
       logs_id_plan.dcbooked, 
       kn_idinfo.eta 
FROM   kn_idinfo 
       RIGHT JOIN (department 
                   RIGHT JOIN (logs_id_plan 
                               RIGHT JOIN ((prepackb 
                                            RIGHT JOIN (prepacka 
                                                        RIGHT JOIN maininfo 
                                                                ON prepacka.id = 
                                                                   maininfo.id) 
                                                    ON prepackb.id = 
                                           maininfo.id) 
                                           LEFT JOIN qty_table 
                                                  ON maininfo.id = qty_table.id) 
                                       ON logs_id_plan.id = maininfo.id) 
                           ON department.dept_code = maininfo.dept) 
               ON kn_idinfo.[purchase order(on)] = maininfo.sap_po_num 
WHERE  (( ( department.dept_code ) NOT LIKE "us*" )); 
</code></pre>

<p>I'll be the first to admit the query is a beast but I'm trying to migrate the database without rewriting everything from scratch, as in a few months time the Access front end will be replaced by a web-based application.</p>

## Answers
### Answer ID: 16955133
<p>In the end I moved the calculations of the total columns (eg PAC1_Total, S1_Total, etc) into views on the SQL Server, created linked tables in Access pointing to the new views, then modified the query to use those new linked tables, in addition to the other tables.  I suspect the calculated columns were nested too deeply (since in Access calculated columns can be referenced by other calculated columns in the same SQL stateement).</p>

<p>Still doesn't explain why the query worked with local tables and not with linked ones, though.</p>


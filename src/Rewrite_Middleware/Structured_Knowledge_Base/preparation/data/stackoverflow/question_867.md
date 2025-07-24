# Need help building good indexes for informix table
[Link to question](https://stackoverflow.com/questions/47198695/need-help-building-good-indexes-for-informix-table)
**Creation Date:** 1510221149
**Score:** 1
**Tags:** sql, indexing, informix
## Question Body
<p>I have an Informix 11.7 server with a database table that has 30 million rows.
The table schema is like this:</p>

<pre><code>CREATE TABLE ppd (
    datum DATE,
    obrabot INTEGER,
    rb_obr INTEGER,
    blag_sif_transakcija INTEGER,
    tip_transakcija CHAR(20),
    tabela_kod CHAR(5),
    vrska_sif_transakcija INTEGER,
    ekspozitura CHAR(3),
    valuta CHAR(3),
    iznos_p DECIMAL(20,2),
    iznos_d DECIMAL(20,2),
    smetka CHAR(15),
    podsmetka CHAR(9),
    client_id CHAR(13),
    client_tip CHAR(1),
    client_naziv CHAR(100),
    adresa CHAR(100),
    edb CHAR(13),
    pasos CHAR(20),
    maticen_broj CHAR(20),
    vid_rabota CHAR(2),
    smetka_primac CHAR(15),
    naziv_primac CHAR(100),
    broj_primac CHAR(20),
    smetka_davac CHAR(15),
    naziv_davac CHAR(100),
    broj_davac CHAR(20),
    edb_fl CHAR(13),
    sifra_plakanje CHAR(6),
    namena CHAR(100),
    vo_valuta CHAR(3),
    vo_iznos DECIMAL(20,2),
    datum_vreme DATETIME YEAR TO SECOND,
    operator CHAR(3),
    flag INTEGER,
    potpisnik CHAR(10)
);
</code></pre>

<p>On this table there are 6 indexes, that are very similar one to each other and I think that they are written wrong and that's the reason why running queries on this table is slow. For 19000 rows it takes 30 minutes. 
Here is what the indexes look like:</p>

<pre><code>CREATE INDEX ix_ppd_1 ON ppd (datum,operator,client_id,obrabot);
CREATE INDEX ix_ppd_2 ON ppd (datum,operator,edb,obrabot);
CREATE INDEX ix_ppd_3 ON ppd (datum,operator,maticen_broj,obrabot);
CREATE INDEX ix_ppd_4 ON ppd (datum,operator,rb_obr,obrabot);
CREATE INDEX ix_ppd_5 ON ppd (datum,operator,edb,edb_fl);
CREATE INDEX ix_ppd_6 ON ppd (datum,operator,rb_obr,tabela_kod); 
</code></pre>

<p>As you can see the fields datum and operator repeat in every index.
Could someone help me with rewriting them in order to optimize my table?</p>

<p>Till now I needed to run <code>UPDATE STATISTICS HIGH FOR TABLE ppd</code> like every 2 weeks in order to optimize the table <code>ppd</code>, but that's not a good solution, right?</p>

## Answers
### Answer ID: 47210967
<p>If your queries do not specify conditions (preferably equality conditions) on <code>datum</code> and <code>operator</code>, those indexes are useless. The server will have to resort to scanning the whole table, or building indexes on the fly (and dropping them too).  For example, with the query:</p>

<pre><code>SELECT *
  FROM ppd
 WHERE datum = DATE('2017-11-04')
   AND operator = 'JKL'
   AND …
</code></pre>

<p>any of those indexes could be useful, depending on what conditions are specified in the <code>…</code> part.</p>

<p>If the conditions specify ranges on <code>datum</code> or <code>operator</code> rather than equality, the indexes are less useful, though not necessarily useless.  If you do something like <code>WHERE operator MATCHES '*'</code>, you get no benefit from the index.  For example:</p>

<pre><code>SELECT *
  FROM ppd
 WHERE datum BETWEEN DATE('2017-11-04') AND DATE('2017-11-08')
   AND operator = 'JKL'
   AND …
</code></pre>

<p>The optimizer might use the indexes, but it would select data for all the operator values recorded for each of the 5 dates implied by the <code>BETWEEN</code> clause.  The <code>'JKL'</code> filter would probably not help the optimizer much.  With a fixed date and a range of operators, you might get more benefit from the indexes, but it is still somewhat limited.</p>

<p>If you had a query like:</p>

<pre><code>SELECT *
  FROM ppd
 WHERE client_id = 'ABC123DEF456Z'
   AND obrabot = 12345
   AND …{no mention of datum or operator}…
</code></pre>

<p>then none of the indexes can be used at all.</p>

<p>Consequently, you need to look at and show the slow-running queries.  You need to review their query plans (SET EXPLAIN output).  Keeping statistics updated is important, but it is no help if the optimizer can't use the indexes; indeed, in that case, the indexes are counter-productive.  They take up space and the require maintenance by the system as rows are inserted, updated, deleted — but they aren't used when the queries are run.  You add indexes to enforce uniqueness constraints, or to speed queries.  If your indexes are not used for either purpose, they are pointless (you would do better to drop them).</p>

<p>It's worrying that none of the indexes is unique, too.  It means you don't have a defined primary key on the table.  You should have one.</p>

<p>Note that there are multiple other factors that will affect the performance.  Which other tables do you join this one with?  You have 5 columns of type <code>CHAR(100)</code> and a moderate number of other columns; your row size is 794 bytes, which means that only 2 rows fit on a page if Informix uses 2K pages on your system (5 rows per page with a 4K page size).  They're all fixed size fields which simplifies things.  However, these are very much secondary issues compared with "what does the slow SQL look like".  Of course, if you're joining with other ill-indexed tables, then the combination could be catastrophic for performance.</p>


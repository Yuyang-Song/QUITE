# SQL Oracle 01722 Invalid Number
[Link to question](https://stackoverflow.com/questions/68710437/sql-oracle-01722-invalid-number)
**Creation Date:** 1628504413
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<p>Iam a SQL newbie but I need to rewrite something to get data from several databases.</p>
<p>First, the code I try to execute:</p>
<pre><code>SELECT aeabwbbn
       || aeeancode                           AS EAN,
       ( lglagerbestand - lgauftragsbestand ) AS BESTAND,
       aeform
       || aequal
       || aefb                                AS ARTIKELNUMMER,
       aefb,
       lgfb
FROM   lagerbestand
       join artikelean
         ON lgfirma = artikelean.aefirma
            AND lgform = artikelean.aeform
            AND lgqual = artikelean.aequal
            AND lggroesse = artikelean.aegroesse
            AND lgfb = artikelean.aefb 
</code></pre>
<p>the problem is the last row. Everything is working fine till I inclute the last row.
I thought it is because it has a different format, but every output is numeric. There are just numbers in this query.</p>
<p>So I tried <code>CAST(LGFB AS INTEGER) = ARTIKELEAN.AEFB</code> and <code>LGFB = CAST(ARTIKELEAN.AEFB AS INTEGER)</code> but that didn't work neither.</p>
<p>What could cause this problem?</p>

## Answers
### Answer ID: 68710476
<p>If one value is a number and the other a string, then Oracle (and SQL in general) will do the comparison as a number -- causing the conversion problem.</p>
<p>The simplest method is to convert the values to strings rather than integers:</p>
<pre><code>TO_CHAR(LGFB) = TO_CHAR(ARTIKELEAN.AEFB)
</code></pre>
<p>Note that this might not do what you actually want.  For instance, one value might be <code>'0001'</code> and the other <code>1</code> and these would not be equal as strings.</p>


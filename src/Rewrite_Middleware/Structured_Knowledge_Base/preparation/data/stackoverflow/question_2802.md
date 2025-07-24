# Rewrite OUTER APPLY to Redshift with subquery
[Link to question](https://stackoverflow.com/questions/53040915/rewrite-outer-apply-to-redshift-with-subquery)
**Creation Date:** 1540799104
**Score:** 1
**Tags:** sql, amazon-redshift, lateral-join
## Question Body
<p>I rewriting sql server scripts to redshift database queries</p>

<p>I have OUTER APPLY construction</p>

<pre><code>OUTER APPLY
   (
   SELECT  q.*
   FROM    (
           SELECT  ROW_NUMBER() OVER(ORDER BY ca.Id DESC) AS rn,
                   ca.StateProvince,
                   ca.ZipPostalCode,
                   ca.ContactId
           FROM    public.contact_addresses ca 
           WHERE   ca.OrganizationId = &lt;Parameters.DemographicsOrgId&gt;
                   AND ca.DeletedDate IS NULL
                   AND ca.TypeId = 7
                   AND ca.ContactId = cc.Id
           ) q
   WHERE   q.rn = 1
   ) ca
</code></pre>

<p>But Redshift don't has outer apply. How Ican correctly rewrite it with LEFT JOIN?</p>

<p><strong>UPDATE</strong></p>

<p>I think about rewrite it like this</p>

<pre><code>LEFT JOIN
   (
   SELECT  q.*,
           q.rn = 1
   FROM    (
           SELECT  ROW_NUMBER() OVER(ORDER BY ca.Id DESC) AS rn,
                   ca.StateProvince,
                   ca.ZipPostalCode,
                   ca.ContactId
           FROM    public.contact_addresses ca
           WHERE   ca.OrganizationId = &lt;Parameters.DemographicsOrgId&gt;
                   AND ca.DeletedDate IS NULL
                   AND ca.TypeId = 7
                   AND ca.ContactId = cc.Id
           ) q
   GROUP BY q.rn
   ) ca
ON ca.rn = 1
</code></pre>

<p>But is this correctly?</p>

## Answers
### Answer ID: 53044034
<p>No, it does not look right.  I would guess:</p>

<pre><code>LEFT JOIN
(SELECT ca.OrganizationId,
        ROW_NUMBER() OVER (ORDER BY ca.Id DESC) AS rn,
        ca.StateProvince,
        ca.ZipPostalCode,
        ca.ContactId
 FROM  public.contact_addresses ca 
 WHERE ca.DeletedDate IS NULL AND
       ca.TypeId = 7
 GROUP BY ca.OrganizationId, ca.ContactId
) ca
ON ca.ContactId = cc.ID AND
   ca.OrganizationId = &lt;Parameters.DemographicsOrgId&gt; AND
   ca.rn = 1
</code></pre>

<p>Basically, you need to aggregate by the correlation conditions (if they are equality) and then use them for the outer <code>ON</code> conditions.</p>

### Answer ID: 53041089
<p>The OUTER APPLY operator returns all the rows from the left table expression irrespective of its match with the right table expression. For those rows for which there are no corresponding matches in the right table expression, it contains NULL values in columns of the right table expression</p>

<p>so your approach is correct </p>


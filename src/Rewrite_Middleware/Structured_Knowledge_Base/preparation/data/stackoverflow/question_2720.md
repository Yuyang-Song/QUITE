# New columns for occasional cases : new columns or separate table or json column
[Link to question](https://stackoverflow.com/questions/49092748/new-columns-for-occasional-cases-new-columns-or-separate-table-or-json-column)
**Creation Date:** 1520145820
**Score:** 0
**Tags:** mysql, database, sharding, entity-attribute-value
## Question Body
<p>We are rewriting an existing system where in the main inventory table, some new columns are being introduced, due to need of these columns in roughly 15-20% of overall cases. This means 80-85% of the time, these columns would be null. These new column data type would include decimal, varchar, smallint.</p>

<p>Now, we have three choices:</p>

<ul>
<li>Include new columns as mentioned above, and let 80% of the rows have null values in these columns. This has demerit of null values existing in like 5-6 columns 80% of the time.</li>
<li>Have separate table for these columns, and join with main table only when these columns are needed. This join will happen only in 20% of the cases, since it will be driven by API request. This approach has demerit of a join.</li>
<li>Add json column in existing table for fields which don't need to be queried and for queried fields, add separate columns.</li>
</ul>

<p>I think second option seems most appropriate, but I need opinions according as per your experience</p>

<p>P.S.: The plan is to basically also move this database from single instance to sharded databases. And the sql instance is MySQL.</p>

## Answers
### Answer ID: 49092947
<p>I will go with <code>option (2)</code>. Let's call the main table as <code>Table A</code>, the sub table as <code>Table B</code>.</p>

<p>Since 80% of the time, the new columns' values are NULL, so <code>Table A</code> to <code>Table B</code> relation can be <code>1-to-1</code> or <code>1-to-0</code>. Which means when values are NULL, no record needs to be inserted into <code>Table B</code>. </p>

<p>This makes <code>Table B</code> relatively small, so the <code>JOIN</code> operation shouldn't impose much performance issue.</p>

<p>JSON column can be another option, but there is less strict checking on each field's type within it.</p>


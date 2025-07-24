# How can I select individual rows related to multiple Ids?
[Link to question](https://stackoverflow.com/questions/44225702/how-can-i-select-individual-rows-related-to-multiple-ids)
**Creation Date:** 1495963430
**Score:** 2
**Tags:** sql-server, t-sql
## Question Body
<p>I need to select related Ids from a table based on a list of provided Ids - effectively an Adjacency List problem. I have a working query for a single Id, but it is frankly inelegant at best even though it works! I would welcome suggestions for improvements and for ways to move the single Id solution to a multiple Id solution.</p>

<p>I have a database table like so:</p>

<pre><code>CREATE TABLE [BookingLines]
(
    [BookingLineId] BIGINT NOT NULL IDENTITY (138, 1),
    [BookingId] BIGINT NOT NULL,

    ---- Additional Columns Redacted for brevity

    [ContractNumber] INT NOT NULL DEFAULT 0,
    [ContractSubNumber] DECIMAL NOT NULL DEFAULT 0,

    ---- Additional Columns Redacted for brevity

);
</code></pre>

<p>There will be records in this table, and in some cases there will be 1 or more pairs of records relating to the same Booking Id.  The differentiation is in the ContractSubNumber column, where one value in the pair will be n.0 and the other n.1.  So if there were three consecutive pairs, the Contract SubNumbers would be:</p>

<pre><code>LineId    BookingId     SubNumber
1          1            0.0
2          1            0.1
3          1            1.0
4          1            1.1
5          1            2.0
6          1            2.1
</code></pre>

<p>I may need to start from the Line Id representing either of the sub numbers, and collect the opposing one.  So, if I am starting from LineId 1, I need to retrieve LineId 2 being the related row. I can do this on a single Id using multiple sub selects, like this:</p>

<pre><code>SELECT BookingLineId 
FROM
(
    SELECT BookingLineId 
    FROM   BookingLines
    WHERE  BookingId = 1 
    AND    FLOOR(ContractSubNumber) = 
    (
        SELECT FLOOR(ContractSubNumber) 
        FROM   BookingLines 
        WHERE  BookingId = 1 AND BookingLineId = (1)
    )
)
WHERE BookingLineId &lt;&gt; 1; 
</code></pre>

<p>This works correctly, returning the value 2 in this case.</p>

<ol>
<li>How can I make this more elegant and efficient?</li>
<li><p>How can I rewrite this to return the opposing values of all Ids in a specified  list e.g.  </p>

<p>WHERE BookingId = 1 AND BookingLineId IN (1,3,5))</p></li>
</ol>

<p>and have it return the result 2,4,6?</p>

<p>All suggestions gratefully received.  </p>

<p><strong>EDIT</strong></p>

<p>I have corrected the typo in the SQL provided in the original question, and using the framework proposed by @McNets this is the solution I went for:</p>

<pre><code>SELECT BL.BookingLineId 
FROM BookingLines BL
INNER JOIN BookingLines ABL ON ABL.BookingId = BL.BookingId
AND ABL.BookingLineId IN (22, 24, 26)
AND FLOOR(BL.ContractSubNumber) = FLOOR(ABL.ContractSubNumber)
WHERE BL.BookingId = 3 AND BL.BookingLineId NOT IN (22,24,26);
</code></pre>

<p>I am very grateful for the contributions and for the final answer. Thanks guys!</p>

## Answers
### Answer ID: 44226152
<p>As far as there is no information about <code>AgencyBookingLines</code> and no sample data I cannot set up a <a href="http://dbfiddle.uk/?rdbms=sqlserver_2016&amp;fiddle=b8fd9801e14f8429b0f1a1cd7584ab8a" rel="nofollow noreferrer">fiddle</a> example, but I think you can move the <code>AgencyBookingLines</code> subquery to the ON clause.</p>

<pre><code>SELECT     BL.BookingLineId 
FROM       BookingLines BL
INNER JOIN AgencyBookingLines ABL
ON         ABL.BookingId = BL.BookinId
AND        ABL.BookingLineId = 1
AND        FLOOR(BL.ContractSubNumber) = FLOOR(ABL.ContractSubNumber
WHERE      BL.BookingId = 1
AND        BL.BookingLineId &lt;&gt; 1;
--
-- AND     BL.BookingLineId IN (2,4,6);
</code></pre>

### Answer ID: 44226119
<p>Will it sub numbers always *.0 &amp; *.1. Then you could try the below</p>

<pre><code>SELECT oppo.* 
FROM AgencyBookingLines AS main
INNER JOIN AgencyBookingLines AS oppo ON 
oppo.BookingId = main.BookingId
AND oppo.SubNumber &lt;&gt; main.SubNumber
AND FLOOR(oppo.SubNumber) = FLOOR(main.SubNumber)
WHERE main.BookingId = 1
      AND main.LineId IN (1,3,5)
</code></pre>


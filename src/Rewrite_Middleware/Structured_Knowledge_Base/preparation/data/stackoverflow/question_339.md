# How count the 1&#39;s and 0&#39;s with a bit return type and return it in two separate columns
[Link to question](https://stackoverflow.com/questions/21430564/how-count-the-1s-and-0s-with-a-bit-return-type-and-return-it-in-two-separate-c)
**Creation Date:** 1390996972
**Score:** 0
**Tags:** c#, sql
## Question Body
<p>I would like my sql query to select all the fields in a table by one date or between two dates, 3 of the fields in my database have the return type as bits. This is somewhat my database looks</p>

<pre><code>ID||Name || Surname || Age || Country || SumOfInfection || SumOfOtherInfection|| HasPersonContacted
</code></pre>

<p>SumOfInfection, SumOfOtherInfection&amp; HasPersonContacted have the return type of bits. For these three fields i; need to sum the numbers of True(1) and False(0) into two separate columns.</p>

<p>Name|| Surname|| .... ||HasPersonContacted(sum of 1's based on a userID) || HasPersonContacted(sum of 0's based on a userID) .....
so what i am looking for </p>

<pre><code>SumOfInfection &lt;- all the 1's for that ID
output= 10 &lt;- so the person had 10 infection
SumOfInfection &lt;- all the 0's for that ID
output= 3 - so the person had no infection for 3 times
</code></pre>

<p>i would like to do same for SumOfOtherInfection and HasPersonContacted .</p>

<p>This is what i have done but it only shows the sum of SumOfInfection how do i get all these data in one go? i rely like to use Select * because in future if i am looking for more data i dont have to rewrite my query.   </p>

<pre><code>SELECT COUNT(NULLIF(SumOfInfection,1)) 
From [TableName] 
where ID='1234' AND Cast([Time] AS DATE) &gt;'2012-01-09' AND CAST([Time] AS DATE) &lt; '2014-01-01' 
</code></pre>

## Answers
### Answer ID: 21430866
<p>Try using conditional <code>sum()</code>:</p>

<pre><code>SELECT sum(case when SumOfInfection = 1 then 1 else 0 end) as NumInfection1,
       sum(case when SumOfInfection = 0 then 1 else 0 end) as NumInfection0
From [TableName] 
where ID='1234' AND Cast([Time] AS DATE) &gt;'2012-01-09' AND CAST([Time] AS DATE) &lt; '2014-01-01' ;
</code></pre>

<p>Alternatively, you can cast the bit as an integer:</p>

<pre><code>SELECT sum(cast(SumOfInfection as int)) as NumInfection1,
       sum(1 - cast(SumOfInfection as int)) as NumInfection1
</code></pre>

<p>EDIT:</p>

<p>I think the full query is more like:</p>

<pre><code>select Name, Surname,
       sum(case when HasPersonContacted = 1 then 1 else 0 end) as NumPersonContacted1,
       sum(case when HasPersonContacted = 0 then 1 else 0 end) as NumPersonContacted0,
       . . .
from t
group by Name, Surname;
</code></pre>


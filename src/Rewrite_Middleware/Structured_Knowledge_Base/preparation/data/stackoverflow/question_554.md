# MySQL CDR Concurrent Call Query
[Link to question](https://stackoverflow.com/questions/31293909/mysql-cdr-concurrent-call-query)
**Creation Date:** 1436361518
**Score:** 0
**Tags:** mysql, concurrency
## Question Body
<p>I am trying to construct a query to get concurrent calls of of my Asterisk CDR that I uploaded into MySQL.</p>

<p>I have tried the following examples located on these threads:<br />
<a href="https://stackoverflow.com/questions/21420744/mysql-query-peak-concurrent-calls-cdr-data">mysql query - peak concurrent calls CDR data</a> but my results were not what I expected.
<br />
<a href="https://stackoverflow.com/questions/13322489/fetch-max-number-of-concurrent-phone-calls-from-call-log">fetch max number of concurrent phone calls from call_log</a> and this seems to take forever and the results are not what I expected either.</p>

<p>I cant even rewrite them because the base was not what I expected so I wouldnt even know where to start.</p>

<p>What I would like are the following:<br />
1 - query for peak calls for the system as a whole for the day</p>

<pre><code>2015-06-01 | 134
</code></pre>

<p>2 - query to get a list of times of the top 10 concurrent calls for a selected period. <br /></p>

<pre><code> 2015-06-01 9:32:21 | 50
 2015-06-01 10:15:11 | 43
 2015-06-01 15:45:14 | 40
 .......
</code></pre>

<p>I have other complex queries but for now this would get me started.</p>

<p>Eventually, I want to get max concurrent calls of a specified day where src or dst equals a pool of specified DIDs</p>

<p>My MySQL database is in the format of </p>

<pre><code>source  destination     calldate    endtime     duration    uniqueid 
</code></pre>

<p>Any help is appreciated.</p>

## Answers
### Answer ID: 35013859
<p>Here is the required Query to Find max concurrent calls on a specified day.</p>

<pre><code>SET @Start = '2015-12-03 00:00:00';
SET @END = '2015-12-03 23:59:59';
SET @SRC = ('DID1','DID2');
SET @DST = ('DID3','DID4');
SELECT DATE(calldate) as 'Date', 
MAX((SELECT COUNT(*) FROM cdr c2 WHERE (c2.source IN @SRC or c2.destination IN @DST ) and c2.calldate between @Start and @END AND UNIX_TIMESTAMP(c1.calldate) BETWEEN UNIX_TIMESTAMP(c2.calldate) AND (UNIX_TIMESTAMP(c2.calldate)+c2.duration))) AS 'Channels' 
FROM cdr c1 WHERE (c1.source IN @SRC or c1.destination IN @DST ) and c1.calldate between @Start and @END GROUP BY 1;
</code></pre>

<p>Please modify @SRC and @DST with manual addition of list of DIDs.
Or you can manually add DIDs list on the places of @SRC and @DST.</p>


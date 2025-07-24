# How can I display which column has the latest date?
[Link to question](https://stackoverflow.com/questions/51069924/how-can-i-display-which-column-has-the-latest-date)
**Creation Date:** 1530126802
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>My employers often have me run reports directly off of our databases, and I seem to have run into a snag on one of them. I need to find out whether a claim is logged in or out of our system and we have 2 different columns (Log_In_Date and Log_MAIL_Date) in the table that tracks our claims (Claimlog) for part of a report that I am generating. </p>

<pre><code>CREATE TABLE CLAIMLOG(
   LOG_DEALER    VARCHAR(16) NOT NULL PRIMARY KEY
  ,LOG_IN_DATE   VARCHAR(19) NOT NULL
  ,LOG_BATCH     INTEGER  NOT NULL
  ,LOG_BSEQ      INTEGER  NOT NULL
  ,LOG_CLAIM     INTEGER  NOT NULL
  ,LOG_CSEQ      INTEGER  NOT NULL
  ,LOG_MAIL_DATE VARCHAR(19) NOT NULL
  ,LOG_NUMBER    INTEGER  NOT NULL
  ,LOG_TYPE      VARCHAR(1) NOT NULL
  ,LOG_DELETE    VARCHAR(1)
  ,LOG_REJECT    VARCHAR(1)
  ,LOG_CLAIM_SUB VARCHAR(2)
  ,LOG_RO_DATE   VARCHAR(19) NOT NULL
  ,LOG_ID        INTEGER  NOT NULL
);

INSERT INTO CLAIMLOG VALUES ('OH025',  '2017-06-01 00:00:00',533996,1, 682543,1,'2017-06-06 00:00:00',43,'M',NULL,NULL,NULL,'2017-05-30 00:00:00',2393818);
INSERT INTO CLAIMLOG VALUES ('OH025',  '2017-06-01 00:00:00',533995,1, 682581,1,'2017-06-08 00:00:00',90,'R',NULL,NULL,NULL,'2017-05-30 00:00:00',2393819);
INSERT INTO CLAIMLOG VALUES ('163369', '2017-01-30 00:00:00',486838,8, 117664,1,'2017-01-31 00:00:00',32,'M',NULL,NULL,NULL,'2017-01-27 00:00:00',2239381);
INSERT INTO CLAIMLOG VALUES ('132729', '2017-09-11 00:00:00',573238,13,239381,1,'2017-09-14 00:00:00',56,'M',NULL,NULL,NULL,'2017-09-07 00:00:00',2519220);
INSERT INTO CLAIMLOG VALUES ('08285',  '2018-05-14 00:00:00',671898,1, 239381,1,'2018-05-17 00:00:00',33,'M',NULL,NULL,NULL,'2018-05-10 00:00:00',2819892);
INSERT INTO CLAIMLOG VALUES ('06240',  '2013-11-15 00:00:00',780029,1, 239381,1,'2013-12-13 00:00:00',4, 'C',NULL,'X', 'A', '2013-11-11 00:00:00',944206);
INSERT INTO CLAIMLOG VALUES ('04839',  '2018-06-07 00:00:00',681150,1, 239381,2, NULL,                1, 'C',NULL,NULL,NULL,'2018-04-11 00:00:00',2785317);
INSERT INTO CLAIMLOG VALUES ('04839',  '2018-04-16 00:00:00',660798,1, 239381,1,'2018-04-30 00:00:00',53,'M',NULL,NULL,NULL,'2018-04-11 00:00:00',2785317);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533928,3, 387468,1,'2017-06-01 00:00:00',85,'M',NULL,NULL,NULL,'2017-05-30 00:00:00',2393813);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533928,2, 387462,1,'2017-06-01 00:00:00',85,'M',NULL,NULL,NULL,'2017-05-30 00:00:00',2393816);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533928,1, 387358,1,'2017-06-02 00:00:00',85,'M',NULL,NULL,NULL,'2017-05-26 00:00:00',2393814);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533927,2, 387458,1,'2017-06-01 00:00:00',4, 'R',NULL,NULL,NULL,'2017-05-30 00:00:00',2393811);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533927,1, 387290,1,'2017-06-01 00:00:00',4, 'R',NULL,NULL,NULL,'2017-05-24 00:00:00',2393810);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533926,2, 387257,1,'2017-06-01 00:00:00',4, 'C',NULL,NULL,NULL,'2017-05-24 00:00:00',2393815);
INSERT INTO CLAIMLOG VALUES ('01563-5','2017-05-31 00:00:00',533926,1, 386930,1,'2017-07-05 00:00:00',4, 'C',NULL,NULL,NULL,'2017-05-17 00:00:00',2393812);
INSERT INTO CLAIMLOG VALUES ('01429-4','2014-09-12 00:00:00',179427,2, 32051, 1,'2014-09-19 00:00:00',12,'M',NULL,NULL,NULL,'2014-09-04 00:00:00',1239381);
INSERT INTO CLAIMLOG VALUES ('01087',  '2015-02-20 00:00:00',239381,1, 45427, 1,'2015-02-24 00:00:00',11,'M',NULL,NULL,NULL,'2015-02-19 00:00:00',1431193);
</code></pre>

<p>I originally used a case statement:</p>

<pre><code>SELECT LOG_DEALER,
 LOG_CLAIM,
  CASE WHEN Log_In_Date &gt; Log_Mail_Date THEN 'In' ELSE 'Out' END AS 'Log In Status'
FROM CHANGELOG
</code></pre>

<p>This worked for the most part, but I've run into some duplicate results with both "In" and "Out" returns. After doing some research, I adjusted the query to:</p>

<pre><code>SELECT CASE WHEN LogInDate &gt; COALESCE(LogOutDate, '2000-01-01') THEN 'In' ELSE 'Out' END AS 'Log In Status'
</code></pre>

<p>to account for null values.  Unfortunately, I'm still getting the return of both In and Out for the same entries:</p>

<pre><code>  LOG_DEALER   LOG_CLAIM   LoggedInStatus  
 ------------ ----------- ---------------- 
  04839        239831      In              
  04839        239831      Out             
  01563-5      387468      Out    
</code></pre>

<p>I've tried replacing <code>COALESCE</code> with <code>NOTNULL</code> and rewriting the select statement as:</p>

<pre><code>SELECT IIF(LogInDate &gt; LogOutDate, 'In','Out')
</code></pre>

<p>Still no luck getting the results. Does anyone have any suggestions on how to properly query this?</p>

## Answers
### Answer ID: 51091917
<p>Try using <code>GROUP BY</code>:</p>

<pre><code>SELECT LOG_DEALER,
 LOG_CLAIM,
  CASE WHEN MAX( Log_In_Date ) &gt; COALESCE( MAX( Log_Mail_Date ), '2000-01-01') THEN 'In' ELSE 'Out' END AS 'Log In Status'
FROM #CLAIMLOG
GROUP BY LOG_DEALER, LOG_CLAIM
</code></pre>

<p>This will return only distinct <code>LOG_DEALER, LOG_CLAIM</code> combinations. By using <code>MAX</code> you will be picking up latest dates:</p>

<pre><code>LOG_DEALER       LOG_CLAIM   Log In Status
---------------- ----------- -------------
01429-4          32051       Out
01087            45427       Out
163369           117664      Out
04839            239381      In
06240            239381      Out
08285            239381      Out
132729           239381      Out
01563-5          386930      Out
01563-5          387257      Out
01563-5          387290      Out
01563-5          387358      Out
01563-5          387458      Out
01563-5          387462      Out
01563-5          387468      Out
OH025            682543      Out
OH025            682581      Out
</code></pre>

<p>I also hope that you are not storing dates as <code>VARCHAR</code>.</p>

### Answer ID: 51071676
<p>According to the sample data and query, LOG_MAIL_DATE has the constraint NOT NULL. This is preventing the insert of the following values:</p>

<pre><code>    INSERT INTO #mytable VALUES ('04839',  '2018-06-07 00:00:00',681150,1, 239381,2, NULL,                1, 'C',NULL,NULL,NULL,'2018-04-11 00:00:00',2785317);
</code></pre>

<p>Also, the values inserted have duplicate rows for LOG_DEALER = '04839'. By default, SQL Server considers NULL to be the highest value. Therefore, for the two rows, the following results occur:</p>

<ol>
<li><p>Here, Log_In_Date = '2018-06-07 00:00:00'and  Log_Mail_Date = NULL
Since NULL > '2018-06-07 00:00:00', It results in LoggedInStatus = 'Out'</p>

<pre><code>INSERT INTO mytable VALUES ('04839',  '2018-06-07 00:00:00',681150,1, 239381,2, NULL,                1, 'C',NULL,NULL,NULL,'2018-04-11 00:00:00',2785317);
</code></pre></li>
<li><p>The second case yields Log_In_Date > Log_Mail_Date. Therefore the condition satisfies and results in LoggedInStatus = 'In'.</p>

<pre><code>INSERT INTO mytable VALUES ('04839',  '2018-04-16 00:00:00',660798,1, 239381,1,'2018-04-30 00:00:00',53,'M',NULL,NULL,NULL,'2018-04-11 00:00:00',2785317);
</code></pre></li>
</ol>


# Do delta import will loss some documents, when the documents added in the duration of delta import
[Link to question](https://stackoverflow.com/questions/39328078/do-delta-import-will-loss-some-documents-when-the-documents-added-in-the-durati)
**Creation Date:** 1473069434
**Score:** 0
**Tags:** solr, solrcloud
## Question Body
<p><p>I met a problem when i using the solrcloud mode. When the solr instance run delta-import, it may take 
some time to be finished( my data source is mysql database). So during this time, the new added documents
will loss, the deltaQuery, i use SUBDATE(${dih.last_index_time}, INTERVAL 2 MINUTE), 
let it run the delta-import 2 mins earlier than the last_index_time, if the delta-import's duration is 5 mins, it will loss the records at the first 3 mins.</p>

<p>Our servers doesn't use solr cloud mode before, we deal with this issue is tring to rewrite dataimport.properties file, 
query the max(sys_time_stamp), which will help to record the max time stamp, and let the solr can run delta import standing 
by the time found in the file, of course, it will never miss docuements.</p>

<p>But now, we use solrcloud, the dataimport.properties is on the zookeeper, and we may have multiple collections for the 
same core.how can i update the dataimport.properties file now in colleciton now? Do you have any solution to help record
the max(sys_time_stamp) in dataimport.properties, rather than using the time of delta-import start to run?</p>

<p>Cheers</p>

## Answers
### Answer ID: 39585332
<p>My solution is that, i tested the recent days new added documents, and get
the max delta-import duration time, and set the interval larger than this time.
So that next time, the solr instance run delta-import can also include the new
added documents at the first 3 mins. And i added a new cronjob to run the delta-import daily, with the start time as last_index_time - 24 hours, in case there 
will have some missing documents in one day, so the risk will be very low. </p>

<p>And i found there are "Custom Parameters", the key-value pairs can set when run the delta-import, and can be used as ${dih.request.XXXX} in dataConfig file, which will help to set delta-import start time.</p>

<p>Not the perfect solution, but works for my system.</p>


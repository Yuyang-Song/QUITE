# Can a query be optimized so that running analyze isn&#39;t necessary?
[Link to question](https://stackoverflow.com/questions/57877819/can-a-query-be-optimized-so-that-running-analyze-isnt-necessary)
**Creation Date:** 1568147385
**Score:** 1
**Tags:** mysql, query-optimization, innodb
## Question Body
<p>I have a Drupal site with a MySQL db (all innodb tables) that "crashes" (read: runs slowly) every once in awhile. The server hosting is cloud based and the "crashing" happens when the database is moved to a new a container.  A query that joins about 10 tables and returns a single row starts running extremely slowly (1 minute) after the move and everything grinds to a halt. Normally the query executes very quickly (less than .1 seconds) and is not an issue.</p>

<p>It was determined that the move causes the "crash" because the MySQL server loses its "analyze" information - that's stored in memory and it gets lost when the database is moved.</p>

<p>It's not currently possible to automatically run analyze after the move. The hosting company is suggesting that the query be re-written so that analyze isn't necessary. I wanted to ask the community if this makes sense and how I might approach rewriting it.</p>

<hr>

<p>Here is info copied from the OP's pastebin:</p>

<blockquote>
  <p>Query_time: 0.052842 Lock_time: 0.000530 Rows_sent: 1 Rows_examined: 61031</p>
</blockquote>

<pre><code>SELECT node__field_last_sl_play.field_last_sl_play_value AS node__field_last_sl_play_field_last_sl_play_value, node_field_data.nid AS nid, node_field_data_node__field_album.nid AS node_field_data_node__field_album_nid, node_field_data_node__field_artist.nid AS node_field_data_node__field_artist_nid, node_field_data_node__field_event.nid AS node_field_data_node__field_event_nid, votingapi_result_node_field_data.id AS votingapi_result_node_field_data_id, node_field_data_node__field_lifestyle.nid AS node_field_data_node__field_lifestyle_nid
FROM
node_field_data node_field_data
LEFT JOIN node__field_album node__field_album ON node_field_data.nid = node__field_album.entity_id AND node__field_album.deleted = '0' AND (node__field_album.langcode = node_field_data.langcode OR node__field_album.bundle = 'track')
LEFT JOIN node_field_data node_field_data_node__field_album ON node__field_album.field_album_target_id = node_field_data_node__field_album.nid
LEFT JOIN node__field_artist node_field_data_node__field_album__node__field_artist ON node_field_data_node__field_album.nid = node_field_data_node__field_album__node__field_artist.entity_id AND node_field_data_node__field_album__node__field_artist.deleted = '0' AND (node_field_data_node__field_album__node__field_artist.langcode = node_field_data_node__field_album.langcode OR node_field_data_node__field_album__node__field_artist.bundle = 'album')
LEFT JOIN node_field_data node_field_data_node__field_artist ON node_field_data_node__field_album__node__field_artist.field_artist_target_id = node_field_data_node__field_artist.nid
LEFT JOIN node__field_event node__field_event ON node_field_data.nid = node__field_event.entity_id AND node__field_event.deleted = '0' AND (node__field_event.langcode = node_field_data.langcode OR node__field_event.bundle = 'track')
LEFT JOIN node_field_data node_field_data_node__field_event ON node__field_event.field_event_target_id = node_field_data_node__field_event.nid
LEFT JOIN votingapi_result votingapi_result_node_field_data ON node_field_data.nid = votingapi_result_node_field_data.entity_id AND (votingapi_result_node_field_data.entity_type = 'node' AND votingapi_result_node_field_data.function = 'vote_sum' AND votingapi_result_node_field_data.type = 'vote')
LEFT JOIN node__field_lifestyle node__field_lifestyle ON node_field_data.nid = node__field_lifestyle.entity_id AND node__field_lifestyle.deleted = '0'
LEFT JOIN node_field_data node_field_data_node__field_lifestyle ON node__field_lifestyle.field_lifestyle_target_id = node_field_data_node__field_lifestyle.nid
LEFT JOIN node__field_last_sl_play node__field_last_sl_play ON node_field_data.nid = node__field_last_sl_play.entity_id AND node__field_last_sl_play.deleted = '0'
WHERE (node_field_data.status = '1') AND (node_field_data.type IN ('track'))
ORDER BY node__field_last_sl_play_field_last_sl_play_value DESC
LIMIT 1 OFFSET 0;
</code></pre>

<p>EXPLAIN report for this query:</p>

<pre><code>EXPLAIN
1   SIMPLE  node_field_data index_merge node_field__type__target_id,node__status_type   node_field__type__target_id,node__status_type   34,35   
    NULL
    2288    Using intersect(node_field__type__target_id,node__status_type); Using where; Using index; Using temporary; Using filesort   
1   SIMPLE  node__field_album   ref PRIMARY,bundle  PRIMARY 5   dbname.node_field_data.nid,const    1   Using where 
1   SIMPLE  node_field_data_node__field_album   ref PRIMARY,node__id__default_langcode__langcode    PRIMARY 4   dbname.node__field_album.field_album_target_id  1   Using where; Using index    
1   SIMPLE  node_field_data_node__field_album__node__field_artist   ref PRIMARY,bundle  PRIMARY 5   dbname.node_field_data_node__field_album.nid,const  1   Using where 
1   SIMPLE  node_field_data_node__field_artist  ref PRIMARY,node__id__default_langcode__langcode    PRIMARY 4   dbname.node_field_data_node__field_album__node__field_artist.field_artist_target_id 1   Using where; Using index    
1   SIMPLE  node__field_event   ref PRIMARY,bundle  PRIMARY 5   dbname.node_field_data.nid,const    1   Using where 
1   SIMPLE  node_field_data_node__field_event   ref PRIMARY,node__id__default_langcode__langcode    PRIMARY 4   dbname.node__field_event.field_event_target_id  1   Using where; Using index    
1   SIMPLE  votingapi_result_node_field_data    ref vote_result_field__type__target_id,vote_result_field__entity_id__target_id  vote_result_field__entity_id__target_id 5   dbname.node_field_data.nid  1   Using where 
1   SIMPLE  node__field_lifestyle   ref PRIMARY PRIMARY 5   dbname.node_field_data.nid,const    1       
1   SIMPLE  node_field_data_node__field_lifestyle   ref PRIMARY,node__id__default_langcode__langcode    PRIMARY 4   dbname.node__field_lifestyle.field_lifestyle_target_id  1   Using where; Using index    
1   SIMPLE  node__field_last_sl_play    ref PRIMARY PRIMARY 5   dbname.node_field_data.nid,const    1       
</code></pre>

<p>Table definition:</p>

<pre><code>CREATE TABLE `node_field_data` (
 `nid` int(10) unsigned NOT NULL,
 `vid` int(10) unsigned NOT NULL,
 `type` varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'The ID of the target entity.',
 `langcode` varchar(12) CHARACTER SET ascii NOT NULL,
 `title` varchar(255) NOT NULL,
 `uid` int(10) unsigned NOT NULL COMMENT 'The ID of the target entity.',
 `status` tinyint(4) NOT NULL,
 `created` int(11) NOT NULL,
 `changed` int(11) NOT NULL,
 `promote` tinyint(4) NOT NULL,
 `sticky` tinyint(4) NOT NULL,
 `revision_translation_affected` tinyint(4) DEFAULT NULL,
 `default_langcode` tinyint(4) NOT NULL,
 `rh_action` varchar(255) DEFAULT NULL,
 `rh_redirect` varchar(255) DEFAULT NULL,
 `rh_redirect_response` int(11) DEFAULT NULL,
 PRIMARY KEY (`nid`,`langcode`),
 KEY `node__id__default_langcode__langcode` (`nid`,`default_langcode`,`langcode`),
 KEY `node__vid` (`vid`),
 KEY `node_field__type__target_id` (`type`),
 KEY `node_field__created` (`created`),
 KEY `node_field__changed` (`changed`),
 KEY `node__frontpage` (`promote`,`status`,`sticky`,`created`),
 KEY `node__status_type` (`status`,`type`,`nid`),
 KEY `node__title_type` (`title`(191),`type`(4)),
 KEY `node_field__uid__target_id` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='The data table for node entities.'
</code></pre>

## Answers
### Answer ID: 57938547
<p>codesmith, There is NOTHING wrong with your query.  It runs in .1 second when your tables have reasonable indexes rather than 1 minute.  Since you and your HOSTING company know that a MOVE to another container REQUIRES ANALYZE to complete the process, why is this not a PART of their process?  "FWIW this is a reputable hosting company that uses Google for its containerization."  Try to convince the hosting company to the extra mile and ANALYZE every table - just after their 'move' to avoid this discovery in the next few days (or weeks)  when the 'abnormally long running query' shows up.  I would still like to Skype TALK with you when time permits.</p>


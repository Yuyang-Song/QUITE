# Tagging schema - quick when queries run separately, slow when run in one SELECT
[Link to question](https://stackoverflow.com/questions/8563545/tagging-schema-quick-when-queries-run-separately-slow-when-run-in-one-select)
**Creation Date:** 1324308594
**Score:** 3
**Tags:** mysql, performance, optimization, subquery, tagging
## Question Body
<p>I have a strange performance problem with a query used to create a "filter by tags" widget for Delicious-like bookmarking webapp. The specific, relatively complex query performs much (1000 to 10000 times) faster if run as few, separate queries.</p>

<p>I've tested it on following environments:</p>

<ul>
<li>Windows XP / MySQL 5.1.37 (server &amp; client)</li>
<li>Ubuntu 11.10 / MySQL 5.1.58 (server &amp; client)</li>
</ul>

<p>The problem didn't show up in small, development database. I caught it during production use, after large increase of records in database (currently about 100K rows in link_tags table &amp; 11K unique tags).</p>

<p>I use following DB schema:</p>

<pre><code>CREATE TABLE IF NOT EXISTS `link_tags` (
  `link_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  UNIQUE KEY `link_tag_id` (`link_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  KEY `link_id` (`link_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
</code></pre>

<p>The schema is straightforward (see also <a href="http://www.pui.ch/phred/archives/2005/04/tags-database-schemas.html" rel="nofollow">http://www.pui.ch/phred/archives/2005/04/tags-database-schemas.html</a>), so it shouldn't require further explanation. </p>

<p>Technically speaking, the problematic query (below) retrieves tags related to given set of tags (specifically, all tags attached to links tagged by specified set of tags) and counts number of links for each found tag AND set of tags.</p>

<pre><code>[ORIGINAL QUERY]

SELECT COUNT(*) AS link_count, tag FROM (
    SELECT
        t.tag AS tag,
        CONCAT(lt.tag_id,':',lt.link_id) AS tag_link_hash
    FROM
        link_tags lt, tags t
    WHERE
        t.id = lt.tag_id
        AND lt.link_id IN (
            SELECT
                link_id
            FROM
                link_tags lt2, links l2
            WHERE
                l2.id = lt2.link_id
                AND l2.created_by = ?  &lt;-- user to filter tags for
                AND lt2.tag_id IN (
                   SELECT id FROM tags t2 WHERE tag IN (?)  &lt;-- tags set to filter by
                )
            GROUP BY
                link_id
            HAVING
                COUNT(*) = ?)  &lt;-- number of tags in filter
    GROUP BY
        tag_link_hash) tmp
GROUP BY
    tag
ORDER BY
    link_count DESC,
    tag ASC
[Results in X minutes - up to 4 hours]
</code></pre>

<p>In production database (as I mentioned - about 100K link_tags and 11K tags) the query runs in minutes to hours (depends on occurrence frequency of specified tags).
Strangely, everything goes smooth if I separate it into few queries:</p>

<p>1) Find <code>id</code>s for given tag names.</p>

<pre><code>[REPLACEMENT QUERY 1]

SELECT id FROM tags t2 WHERE tag IN (?)

[Results in 0,0011 seconds]
</code></pre>

<p>2) Find all <code>link_id</code>s for given set of tags (intersection!).</p>

<pre><code>[REPLACEMENT QUERY 2]

SELECT
    link_id
FROM
    link_tags lt2, links l2
WHERE
    l2.id = lt2.link_id
    AND l2.created_by = 1
    AND lt2.tag_id IN ( ? )  &lt;-- here goes imploded result of query 1
GROUP BY
    link_id
HAVING
    COUNT(*) = ?  &lt;-- number of tags

[Results in 0,0996 seconds]
</code></pre>

<p>3) Find all tags for given set of <code>link_id</code>s and group tags by count of links.</p>

<pre><code>[REPLACEMENT QUERY 3]

SELECT COUNT(*) AS link_count, tag FROM (
    SELECT
        t.tag AS tag,
        CONCAT(lt.tag_id,':',lt.link_id) AS tag_link_hash
    FROM
        link_tags lt, tags t
    WHERE
        t.id = lt.tag_id
        AND lt.link_id IN ( ? )  &lt;-- here goes imploded result of query 2
    GROUP BY
        tag_link_hash) tmp
GROUP BY
    tag
ORDER BY
    link_count DESC,
    tag ASC

[Results in 0,0543 seconds]
</code></pre>

<p>Do you have any idea what is going on? EXPLAIN shows roughly the same plans for large query as for the sum of separated ones. The difference is in number of rows processed in each step (and this is also strange).</p>

<p>Could you help to rewrite original query, hint the MySQL optimizer to run it efficiently or point me to the MySQL bug that causes this behavior?</p>

<p>EXPLAIN results for original query:</p>

<pre><code>id  select_type table       type    possible_keys   key         key_len ref                     rows    Extra
1   PRIMARY     &lt;derived2&gt;  ALL     N8LL            N8LL        N8LL    N8LL                    32      Using temporary; Using filesort
2   DERIVED     lt          index   tag_id          link_tag_id 8       N8LL                    78162   Using where; Using index; Using temporary; Using filesort
2   DERIVED     t           eq_ref  PRIMARY         PRIMARY     4       lstack_prod.lt.tag_id   1
3   DEPENDENT   t2          range   PRIMARY,tag     tag         767     N8LL                    2       Using where; Using temporary; Using filesort
    SUBQUERY
3   DEPENDENT   lt2         ref     link_tag_id,    tag_id      4       lstack_prod.t2.id       7
    SUBQUERY                        tag_id,link_id
3   DEPENDENT   l2          eq_ref  PRIMARY,        PRIMARY     4       lstack_prod.lt2.link_id 1       Using where
    SUBQUERY                        created_by
</code></pre>

## Answers
### Answer ID: 8564002
<p>the <code>WHERE IN (select values from table)</code> is extremely inefficient in MySQL, and will trigger full table scans and file sorts all the time.  Generally, you should replace these with an INNER JOIN.</p>

<p>I THINK this should help, but I haven't tried to re-create your DB, and haven't run this query, so there might be typos.</p>

<pre><code>SELECT COUNT(*) AS link_count, tag FROM (
    SELECT
        t.tag AS tag,
        CONCAT(lt.tag_id,':',lt.link_id) AS tag_link_hash
    FROM
        link_tags lt
    JOIN tags t on t.id = lt.tag_id
    JOIN (SELECT
                link_id
            FROM
                link_tags lt2
            JOIN links l2 on l2.id = lt2.link_id
            JOIN tags t2 on t2.id = lt2.tag_id                
            WHERE
                AND l2.created_by = ?  &lt;-- user to filter tags for
                AND t2.tag IN (?)  &lt;-- tags set to filter by
            GROUP BY
                link_id
            HAVING
                COUNT(*) = ?) as eligible_links on eligible_links.link_id = lt.link_id
    GROUP BY
        tag_link_hash) tmp
GROUP BY
    tag
ORDER BY
    link_count DESC,
    tag ASC
</code></pre>

<p>However, an explain plan would be very helpful.</p>


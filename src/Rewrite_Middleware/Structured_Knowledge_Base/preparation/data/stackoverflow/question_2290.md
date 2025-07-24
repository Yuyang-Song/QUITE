# How to map URL requests for vBulletin posts to Drupal 7 Forum comments after migration?
[Link to question](https://stackoverflow.com/questions/27825011/how-to-map-url-requests-for-vbulletin-posts-to-drupal-7-forum-comments-after-mig)
**Creation Date:** 1420651420
**Score:** 0
**Tags:** url, drupal, migration, forum, vbulletin
## Question Body
<p>I need help to map requests for vBulletin posts to their new location on a Drupal 7 forum.</p>

<p>I inherited a Drupal site after it was migrated from Drupal 5 with vBulletin, to Drupal 7 with native Drupal Forum + Advanced Forum. The new sit also uses PathAuto.</p>

<p>Every day I get many http requests using the old D5/vBulletin URL scheme, and there is no mapping in place to rewrite the target.</p>

<p>I believe I can use Apache mod_rewrite or Drupal Global Redirect to handle this, if I can map the old system to the new one.</p>

<p>For requests for "thread", e.g. <code>example.com/forums/showthread.php?t=1</code> it seems possible to map, because the Drupal 7 path alias to the node for the thread has already been created using the existing node's title. So I can look up in the vBulletin database the old node title using the incoming query's 't' argument, edit that string according to the PathAuto settings in use on the new system, and create a URL alias. [Would love to know if there's a better way.]</p>

<p>But for incoming requests for "post", e.g. <code>example.com/</code>I can't see how to do it. The vBulletin database has the posts in the "post" table, but in Drupal 7 Forum anything after the initial post is a "comment" and has not had a URL alias created for it (because it doesn't have a title in vBulletin in most cases).</p>

<p>I suppose I could find the thread that the post belonged to and redirect the user to the top of the thread, as a workaround, but I'd like to have an accurate map.</p>

<p>Please any solutions for this ?</p>

## Answers
### Answer ID: 27847839
<p>Drupal Migrate creates and saves tables in the database mapping the old resource ID to the new ID.</p>
<p>You just have to be careful since the schema are different between vBulletin and Drupal Forum; primarily in that Forum posts in D7 (other than the first post in a thread) are not nodes, but comments.</p>
<p>But I was able to use a Join SQL query to find the new resource ID:</p>
<pre><code>mysql&gt; SELECT m.sourceid1, m.destid1, c.cid, c.nid, c.subject FROM migrate_map_forum_posts m  LEFT JOIN comment c ON c.cid = m.destid1 LIMIT 3;
+-----------+---------+-------+-------+-----------------+
| sourceid1 | destid1 | cid   | nid   | subject         |
+-----------+---------+-------+-------+-----------------+
|         2 |   35837 | 35837 | 10426 | RE: Test        |
|         3 |   35838 | 35838 | 10426 |                 |
|         4 |   35839 | 35839 | 10426 | I see a picture |
+-----------+---------+-------+-------+-----------------+
</code></pre>
<p>This solution only relies on the new Drupal 7 database and that's okay if the migration went perfectly (I guess if it was perfect the mapping would have been done at the time, lol). But the migration map tables don't always have all the data you need.</p>
<p>If you have access to the old vBulletin database you can dig deeper. In the migration that I inherited, some of the vBulletin 'posts' did not make it into the D7 migration map tables. But through doing more queries I was able to get the 'threadid' that the post belonged to from the vBulletin database and find the node ID for the Forum topic on D7 so I can at least get the user on to the right discussion.</p>


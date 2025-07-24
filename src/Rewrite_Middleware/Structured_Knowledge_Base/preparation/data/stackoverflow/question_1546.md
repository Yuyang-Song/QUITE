# Manual Drupal node inserts
[Link to question](https://stackoverflow.com/questions/9196982/manual-drupal-node-inserts)
**Creation Date:** 1328717126
**Score:** 1
**Tags:** php, mysql, drupal, drupal-6
## Question Body
<p>I attempted to import images from a custom CMS to Drupal using direct MySQL insert queries to the Drupal database. The images are copied to a path within the drupal site: </p>

<pre><code>sites/default/files/images/import
</code></pre>

<p>The nodes show up in lists but the direct links (someurl/node/1234) cause 404 errors. They are all of type media_image and have a valid uid assigned. I also did associated inserts to <code>files</code> and <code>content_type_media_image</code></p>

<p>Is there an internal Drupal process that needs to happen to finalize this import? Is it at all possible without rewriting as a proper Drupal import module?</p>

<p>Sample node insert:</p>

<pre><code>INSERT INTO node SET
    type='media_image',
    language='en',
title='apicture.jpg',
uid='4',
status=1,
created=1328644135,
changed=1328644135;

// grab nid as last mysql_insert()
INSERT INTO files SET
uid = 4,
filename = 'apicture.jpg',
filepath = 'sites/default/files/images/import',
filemime = 'image/jpeg',
filesize = 40069,
status = 1,
timestamp = 1328644136;

INSERT INTO content_type_media_image SET
vid = 683,
nid = 683,
field_image_fid = 539,
field_image_list = 1,
field_image_data = 'a:3:{s:11:"description";s:0:"";s:3:"alt";s:0:"";s:5:"title";s:0:"";}';
</code></pre>

<p>Note: the queries above are the generated queries.</p>

## Answers
### Answer ID: 9226183
<p>I think going for direct SQL inserts is a lot too much hassle. Drupal proposes many solutions to import content, my favourite one being Feeds : <a href="http://drupal.org/project/feeds" rel="nofollow">http://drupal.org/project/feeds</a>. It automates everything, accepts almost any input format and provides very flexible mapping mechanisms.</p>

<p>Going the direct database way means you bypass all the power Drupal provides, and you'll probably reinvent the wheel.</p>

### Answer ID: 9198669
<p>If you're getting a 404 it's because the return from the internal <a href="http://api.drupal.org/api/drupal/modules%21node%21node.module/function/node_load/6" rel="nofollow"><code>node_load()</code> function</a> is NULL/FALSE.</p>

<p>If you step through that function you'll see that an <code>INNER JOIN</code> is made from the <code>node</code> table to the <code>node_revisions</code> table...so if there's no matching record in the <code>node_revisions</code> table as far as Drupal's concerned there is no node.</p>

<p>To fix the error you'll just need to populate the <code>node_revisions</code> table with its required columns - most notably the <code>nid</code> and <code>vid</code> (which is the version ID), and title and body. You may also want to set the text format for the body text in the <code>format</code> column (it's related to the key in the <code>filter_formats</code> table).</p>

<p>Incidentally this version ID should also be added to the <code>node</code> table itself, as that's what the <code>INNER JOIN</code> is made on. I think the safest way to get the next available ID is:</p>

<pre><code>SELECT MAX(vid) + 1 FROM node
</code></pre>

<p>If you don't have revisions turned on for any content types it's likely the <code>vid</code> will always be the same as the <code>nid</code> though.</p>


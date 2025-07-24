# Drupal 6 To 7 Migration
[Link to question](https://stackoverflow.com/questions/7794331/drupal-6-to-7-migration)
**Creation Date:** 1318857471
**Score:** 3
**Tags:** drupal-6, drupal-7
## Question Body
<p>We have a drupal site written in drupal 6. We know we will have to rewrite it for drupal 7 (mostly)</p>

<p>But the big part is migrating the data. CCK migrate was only able to migrate about 90% of the fields.</p>

<p>I am looking for a clean way to migrate the drupal 6 data to drupal 7.</p>

<p>We used content_multigroup as a module which is basically like a field collection...How would that be migrated?</p>

<p>I am looking for some general strategies...I am thinking of bootstrapping drupal 7 and just write queries against the drupal 6 database and save nodes.</p>

## Answers
### Answer ID: 31047505
<p>Upgrade Drupal6 to Drupal7</p>

<h2>        Make a full backup of all files, directories, and your database(s)</h2>

<p>*Notes:
        It is wise to try an update or upgrade on a test copy of your site before applying it to your live site. Even minor updates can cause your site's behavior to change.</p>

<p>Step 1:</p>

<pre><code>Make note of non-core drupal modules(no need drupal core modules) and search if that all modules are available in drupal 7. If the modules are not available, then search “is there any alternate module for drupal 7”. Make sure of it. (*step 1 is important)
</code></pre>

<p>Step 2:</p>

<pre><code>Disable all non-core module. 

Drush:      drush pm-disable `drush pm-list --no-core --type=module –pipe`
</code></pre>

<p>Step 3:</p>

<pre><code>Change the default theme as “Garland”.

Drush:      drush vset theme_default garland, drush vset admin_theme garland
</code></pre>

<p>Step 4:</p>

<pre><code>Update the drupal6.

Drush:      drush up drupal
</code></pre>

<p>Step 5:</p>

<pre><code>Dump the DataBase.

Drush:      drush sql-dump &gt; /path-to-dump/my-sql-dump-file-name.sql
Terminal:   mysqldump -u [username] -p [database name] &gt; [database name].sql
</code></pre>

<p>Step 6:</p>

<pre><code>Download the latest Drupal7.

Drush:      drush dl drupal --select`option to select the version`
</code></pre>

<p>Step 7:</p>

<pre><code>Copy “files” folder from old instance(Drupal6) to new instance(Drupal7) and change the folder permissions.
</code></pre>

<p>Step 8:</p>

<pre><code>Import the dumped DB to new instance.

Drush:  (drush sql-drop, drush sql-cli &lt; /path-of-dump/my-sql-dump-file-name.sql)
Terminal:   mysql -u [username] -p newdatabase &lt; [database name].sql
</code></pre>

<p>Step 9:</p>

<pre><code>Go to Drupal Root &gt; sites &gt; default &gt; settings.php and change into $update_free_access to TRUE in the settings file and then run update.php.
</code></pre>

<p>Step 10:</p>

<pre><code>Download all the contributed modules : include `views and views related modules`.  
</code></pre>

<p>Step 11:</p>

<pre><code>Must download Content Construction Kit (CCK) module. Enable the CCK, Content Migrate modules.

Drush:      drush dl cck, drush en cck

Go to “Admin-Structure &gt; Migrate fields”.
</code></pre>

<p>Step 12:</p>

<pre><code>In that Migrate fields,



After enable click “Migrate fields” in “Available fields” the fields are come under the “Converted Fields”. Once again run “update.php”.
</code></pre>

<p>*Refer this: <code>https://drupal.org/update/themes/6/7</code></p>

### Answer ID: 13361714
<p>The <a href="http://drupal.org/project/migrate" rel="nofollow">Migrate</a> module has evolved a lot since this question was asked. Also the <a href="http://drupal.org/project/migrate_d2d" rel="nofollow">Migrate D2D module</a> is a great starting point for a Drupal 6 to Drupal 7 migration.</p>

<p>Check the <a href="http://drupal.org/node/1813498" rel="nofollow">documentation</a> and you should get a pretty good idea of how to go about it. </p>

<p>Admittedly, the Migrate module seems to have a steep learning curve but using the Migrate D2D Examples you should get up to speed quickly enough.</p>

### Answer ID: 8235451
<p>Have you looked at <a href="http://drupal.org/project/feeds" rel="nofollow">http://drupal.org/project/feeds</a> (which, because of its name, often flies under the radar for its very good use as a data migration tool) ?</p>

<p>What kind of fields are you dealing with?</p>

<p>If that fails, and since you are looking for general strategies, I'll say the following: I would encourage you to use the API, rather than direct queries, as much as possible.</p>

<p>From my own experience, in choosing between the two options:</p>

<p>a) having a script run under D6 and push via SQL to the D7 DB
or
b) having a script run under D7 and pull via SQL to the D6 DB</p>

<p>I would choose b) to make sure that node_save ultimately gets to do all it's work.</p>


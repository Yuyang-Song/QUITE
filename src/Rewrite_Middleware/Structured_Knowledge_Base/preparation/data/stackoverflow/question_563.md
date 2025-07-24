# Uploading images through PHP into SVN and storing meta data in multiple databases
[Link to question](https://stackoverflow.com/questions/3170609/uploading-images-through-php-into-svn-and-storing-meta-data-in-multiple-database)
**Creation Date:** 1278140239
**Score:** 2
**Tags:** php, mysql, image, svn
## Question Body
<p>We're currently designing a rewrite of our PHP website. The new version will be under SVN version control and have a separate database for development and live sites.</p>

<p>Currently we have about 200,000 images on the site and we add around 5-10 a month. We'd like to have these images under SVN as well. </p>

<p>The current plan is to store and serve the images from the file system while serving their meta data from the database. Images will be served through a PHP imaging system with Apache rewrite rules so that <a href="http://host/image/ImageID" rel="nofollow noreferrer">http://host/image/ImageID</a> will access a PHP script that queries the database for an image with the specified ID and (based on a <code>path</code> column in the table) returns the appropriate image.</p>

<p>The issue I'm having is keeping the image files and their meta data in sync between live and development sites.</p>

<p>Adding new images is (awkward, but) easy for the development team: we can add the image to our SVN repository in the same manner we do all files and manually create the meta data in both the live and test databases.</p>

<p>The problem arises when our employees need to upload new images through the website itself.</p>

<p>One viable solution I've been able to come up with is having our PHP upload script commit the new images to SVN and send INSERT queries to both live and development databases. But to me this seems inefficient. Plus SVN support in PHP is still experimental and I dislike having to rely on exec() calls.</p>

<p>I've also considered a third, separate database just for image meta data. As well as not storing the images in SVN (but they are part of the application and not just 'content' images that would be better off just being backed up).</p>

<p>I'd really like to keep images in SVN and if I do I need them to stay consistent with their meta data between the live and development site. I also have to provide a mechanism for user uploaded images.</p>

<p>What is the best way of handling this type of scenario?</p>

## Answers
### Answer ID: 3217833
<p>The best way to handle this would be to use a separate process to keep your images and meta data in sync between live and dev.  For the image files you can use a bash script running from cron to do a "svn add" and "svn commit" for any images uploaded to your live environment.  Then you can run a periodic "svn up" in your dev environment to ensure that dev has the latest set.  Mysql replication would be the best way to handle keeping the live and dev databases in sync given your data set.  This solution assumes two things:  1)  Data flows in one direction, from prod to dev and not the other way around.  2)  Your users can tolerate a small degree of latency (the amount of time for which live and dev will be out of sync).  The amount of latency will be directly proportional to the amount of data uploaded to prod.  Given the 5 - 10 images added per month, latency should be infinitesimal.</p>

### Answer ID: 3183135
<p>If you already have a solution to deal with data migration from dev to prod for your databases, why not store the actual images as BLOBs in the DB, along with the metadata?  </p>

<p>As the images are requested, you can have a script write them to flat files on the server (or use something like mem_cache to help serve up common images) the first time, and then treat them as files afterwords (doing a <code>file_exists()</code> check or similar).  Have your mod_rewrite script handle the DB lookup.  This way, you will get the benefit of still having the majority of your users access 'flat' image files handled by your mod_rewrite script, and everything being nicely in sync with the various DBs.  The downside is that your DBs get big of course.</p>

### Answer ID: 3170968
<p>I've had to solve this sort of problem for a number of different environments.  Here's some of the techniques that I've used; some combination may solve your problem, or at least give you the right insight to solve your problem.</p>

<h2>Version controlling application data during development</h2>

<p>I worked on a database application that needed to be able to deliver certain data as part of the application.  When we delivered a new version of the application, the database schema was likely to evolve, so we needed SQL scripts that would either (1) create all of the application tables from scratch, or (2) update all of the existing tables to match the new schema, add new tables, and drop unneeded tables.  In addition, we needed to be able to prove that the upgrade scripts would work no matter which version of the application was being upgraded (we had no control of the deployment environment or upgrade schedules, so it was possible that a given site might need to upgrade from 1.1 to 1.3, skipping 1.2).</p>

<p>In this instance, what I did was take a tool that would dump the database as one large SQL script containing all of the table definitions and data.  I then wrote a tool that split apart this huge script into separate files (fragments) for each table, stored procedure, function, etc.  I wrote another tool that would take all of the fragments and produce a single SQL script.  Finally, I wrote a third tool that was used during installation that would determine which scripts to run during installation based upon the state of the database and installed application.  Once I was happy with the tools, I ran them against the current database, and then edited the fragments to eliminate extraneous data to leave only the parts that we wanted to ship.  I then version-controlled the fragments along with a set of database dumps representing databases from the field.</p>

<p>My regression test for the database would involve restoring a database dump, running the installer to upgrade the database, and the dumping the result and splitting the dump into fragments, and then comparing the fragments against the committed version.  If there were any differences, then that pointed to problems in the upgrade or installation fragments.</p>

<p>During development, the developers would run the installation tool to initialize (really upgrade) their development databases, then make their changes.  They'd run the dump/split tool, and commit the changed fragments, along with an upgrade script that would upgrade any existing tables to match the new schema.  A continuous integration server would check out the changes, build everything, and run all of the unit tests (including my database regression tests), then point the finger at any developer that forgot to commit all of their database changes (or the appropriate upgrade script).</p>

<h2>Migrating Live data to a Test site</h2>

<p>I build websites using Wordpress (on PHP and MySQL) and I need to keep 'live' and 'test' versions of each site.  In particular, I frequently need to pull all of the data from 'live' to 'test' so that I can see how certain changes will look with live data.  The data in this case is web pages, uploaded images, and image metadata, with the image metadata stored in MySQL.  Each site has completely independent files and databases.</p>

<p>The approach that I worked out is a set of scripts that do the following:</p>

<ol>
<li>Pull two sets (source and target) of database credentials and file locations from the configuration data.</li>
<li>Tar up the files in question for the source website.</li>
<li>Wipe out the file area for the target website.</li>
<li>Untar the files into the target file area.</li>
<li>Dump the tables in question for the source database to a file.</li>
<li>Delete all the data from the matching tables in the target database.</li>
<li>Load the table data from the dump file.</li>
<li>Run SQL queries to fix any source pathnames to match the target file area.</li>
</ol>

<p>The same scripts could be used bidirectionally, so that they could be used to pull data to test from live or push site changes from test to live.</p>


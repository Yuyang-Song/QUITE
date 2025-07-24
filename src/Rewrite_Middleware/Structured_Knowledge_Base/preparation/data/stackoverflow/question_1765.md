# Best practices for migrating database content from one very poor structure to one very logical?
[Link to question](https://stackoverflow.com/questions/6973452/best-practices-for-migrating-database-content-from-one-very-poor-structure-to-on)
**Creation Date:** 1312728241
**Score:** 17
**Tags:** mysql, database, database-design, migration, relational-database
## Question Body
<p><strong>TL;DR what's the best way to migrate lots of data between one very poorly structured database (with much repetition of columns, no interrelations, and duplicate data), to another highly organised and relational structure?</strong> - Sorry about the long read!</p>

<p>I've recently taken on a very complex job. It's rewriting an entire company's web-based IT platform. I'm afraid I can't give too many details because we can't let the old developer know (he has a metaphorical gun against the company's head, in that he's the only one who knows how to do critical things like invoice generation, and is demanding more and more money).</p>

<p>The major problem is that the entire web platform (used by all the staff and all the customers) was coded by a guy who's skills were <em>less than amateur</em>. It's made up of ~300 individual code files. There's no template library - it's all hardcoded into each file. There's no logical database structure - it was practically made up as he went along. There's no security - it's shocking. Anyway, we will be rewriting this whole platform over a ~3-month period.</p>

<p>However the boss says that on the morning it goes live, no customer data can be lost anywhere. The whole database contents has to be copied over directly. The structure of the database is currently so poor it's nearly impossible to work with, but this week we  will be (attempting to!) write some scripts to migrate it over to our new, highly relational structure which is far more logical. <strong>The question is, what's the best way to do this?</strong></p>

<p>One example is addresses. In the old database, addresses are used in about 12 tables (of 44 total...). In ours, we are having one <code>addresses</code> table which will be cross-referenced by other tables (e.g. <code>address_id</code>) to keep things clean. The main problem is that in about half of his tables, the addresses are stored as <code>line1</code>, <code>line2</code>, <code>town</code>, <code>city</code>, etc, which is fine, but in the other half he just has a single <code>address</code> field which stores the whole thing!</p>

<p>A second example is dates - in some tables he has seconds-since-Epoch dates, in others MySQL <code>NOW()</code> dates, and in others he literally stores it in 6 columns per row - <code>year</code>, <code>month</code>, <code>day</code>, <code>hour</code>, <code>minute</code>, <code>second</code> - ouch...</p>

<ul>
<li><p>What's a good way to go about trying to tackle this? <strong>Should we look at <em>our</em> tables and work out where we need to pull <em>his</em> data from into ours, or should we reverse this and look at <em>his</em> tables and work out where his data needs to go into ours?</strong></p></li>
<li><p><strong>From a programming standpoint, how should we tackle this?</strong> A lot of data needs dynamic formatting (e.g. dates) so we were thinking of plucking data one row at a time, formatting it correctly, then re-inserting it into the right places in our scripts. </p></li>
<li><p><strong>Speed and efficiency of queries is not an issue for us,</strong> as we will only need to run this once (after testing), on our local machines. His database is currently ~800MB when SQL dumped, but again a lot of this is his useless test data, or just totally unnecessary. </p></li>
</ul>

<p>Any ideas on the best way to tackle this? For reference our system will be re-written in PHP so any PHP-based recommendations would be nice. The database is currently (and still will be) in MySQL.</p>

## Answers
### Answer ID: 6974220
<p>First in designing your new structure include columns to hold the record identifiers from the old system and the table it came from. You can drop these after the move was proven to be successful, but they will help tremendously in migrating the data and testing that it is correct after migration and in answering questions about where the data came from when users are surprised at what they see. If the old data doesn't have PKs, then create them with some type of automnumber field.  </p>

<p>Work from the parent tables down. If addresses are stored in more than one place, determine which order you want to grab the addresses from and which will take precendence if there are multiple records that are different. You may want to store different addresses as well (the address table is a one-to-many with the person table yes?) but you may need to have additional address types available. </p>

<p>You need to deal with issues of the old data not matching the new data type or size or constraints (say you want something to be required and they didn't have a value). Decide how you want to handle before you start and get buy off from the stakeholders. You might want to use a vlaue of "Unknown" if street 1 is required and you only have city and state for instance.</p>

<p>Send any data that is transformed in conversion to meet new standards or which you cannot figure out how to change at all to an exception table. The stakeholders or users may have to deal with them to get new required data or tell you what to change. </p>

<p>Likely you will need to run this several times. First on a dev box, then on a QA box. When moving to prod, if the tranisition takes longer than you can afford to be down, you may need to move the bulk of the data once well before launch and then at launch time just move new or changed data. </p>

<p>There is a lot of work to do and 3 months is extremely tight for this sort of migration.  Good luck.</p>

### Answer ID: 6974141
<p>There's not solution here. No magic. Just plain hard work.</p>

<p>You have your new model, and the only way to get this done is to go to each of the tables and convert them individually, logically, on paper, on a white board, etc. in to the new model.</p>

<p>You will have more than just simple formatting issues to deal with. You will also have data duplication issues to deal with. If you have 12 tables with addresses, but only 1 client, which address wins?</p>

<p>That decision alone may simplify a lot of the processing (perhaps you can ignore the other addresses than the one blessed address linked off the master client record, for example).</p>

<p>And that brings you to the final problem. "Not losing any data" during the conversion.</p>

<p>That is quite likely a non-starter from day one depending on what "not losing any data" means. If you're discarding addresses, for example, there's data loss right there. Sure, each component "has an address", but not necessarily the one they had before. Before they may have all been identical, but also they may not. It's going to be very messy.</p>

<p>Once you have your mapping and other processes done, coding them is straightforward in most any language. Scripting languages work well for this. You could bulk load each of the tables "as is" in to a new DB and write store procedures to do the conversion. Whatever you're conversant with. Your conversion will likely be several steps, and most of this code will likely be "one off" solely for facilitating the conversion.</p>

<p>It will be tedious. These things always are. There's simply too much detail. All of the reasons this is a horrible system are reasons why the conversion will be horrible. And do not be surprised if you haven't budgeted enough time to pull it off.</p>

<p>Finally, if you have a LOT of data, you may have some time constraints to deal with if you can't perform the cut over during business down time (over the weekend, over night whatever). That will be a whole other kettle of fish if you're doing this on the run with updating data. I can't strongly recommend enough not doing that if at all possible.</p>

### Answer ID: 6974132
<p>I've recently done a couple of larger migrations and during that gradually developed a few practical best practices for myself. It's nothing really ground-breaking but you might find some of them helpful:</p>

<p><strong>General hints</strong></p>

<ul>
<li>Before your start make sure you understand the existing data model and the requirements for the new version of the system.</li>
<li>Design the new database schema as best as you can and try to not stress yourself by the fact that you'll need to migrate the old content.</li>
<li>Use a framework with a solid ORM. Not only will it be easier to develop the new version but also the migration will be much easier.</li>
</ul>

<p><strong>Migration</strong></p>

<p>The code dealing with the data migration will be part of your project for some time so It's a good idea to dedicate it a package/folder (i.e. <code>legacy</code>). In this package keep your conversion scripts and other files related to the legacy system. After some time you'll be able to get rid of it by simple <code>rm -rf legacy</code>.</p>

<p>The scripts should do the conversion in small steps. It's better to loop over a table several times and keep the steps small, simple and debuggable than having one big script that does everything although faster. </p>

<p>It's also a good idea to run each of the steps in its own transaction and commit only after it's successfully finished so that you don't need to re-run the whole migration again when one step fails.</p>

<p>The whole migration process as well as particular steps or groups of steps should be possible to be run with one command from the command line, because you'll run it many times until you reach the final version so the more automated you are the better. </p>

<p>The main script  (i.e. <code>legacy/bin/full-migration</code>) should perform the whole process (i.e. fetch a fresh copy of the legacy production DB, (re-)create the new DB and tables in it, run the whole migration) and it should be exactly the same process as you'll eventually run after you deploy the new version in the production server(s) (only with different configuration). It will allow you test it thoroughly in your development environment.</p>

<p>Because the conversion can take a long time it is beneficial to log every action (plain <code>print action +  object_id</code> should do). Often there are a couple of rows that have some unexpected differences which make your script crash or cause a reference integrity error. In cases like that it's good see which object it was so that you can immediately go to the DB, inspect the data, update the script accordingly and run the failed step again.</p>

<p>One thing that has proven very useful for me was to define model classes also for the legacy databases tables using the ORM. I've done this a couple of time in Django which supports multiple database connections and per-model routing so I was able to write scripts that looked roughly like this (Python):</p>

<pre><code>from legacy import models as old
from catalog import models as new

# Loop through all products from the legacy DB
for old_product in old.Product.objects.all():  
    # Create an instance of the new product model class
    new_product = new.Product() 
    # Copy and modify attributes as needed
    new_product.name = old_product.product_name.strip()
    # ...
    # Save it to the new database
    new_product.save()
</code></pre>

<p>Also, the more restrictive the new schema is the better (ie. NOT NULL where possible, foreign key checks, etc.) because it will help you to see where your assumptions about the old schema are wrong and also prevent the incorrect data from entering your new system (InnoDB as the backend for MySQL is a good idea).</p>

<p>Other good practice is to preserve the old primary keys in the new database where possible. If you see something strange in the new data after the migration you can go back and lookup the item by its ID in the legacy system.</p>

### Answer ID: 6973805
<p>One thing to think about...</p>

<p>Why not hide the new, fixed, shiny schema behind views that make it look like the old one?</p>

<p>This means you have 2 client code bases on the same data, each has their own "API" in the database though.</p>

<p>This also means that the old system is never actually switched off on "go live".</p>

### Answer ID: 6973717
<p>The first step of doing a rewrite is fully understanding the current data structure and the code that runs over it. There may be some data which appears redundant but the code requires it to be so for some odd reason. Is it poor design? Probably - but make sure you completely understand each bit of code that writes or accesses data, so you can determine what can be dropped, what must be refactored, and what must be left as is.</p>

<p>Tools can help automate the process - but without a deep grasp of the current system, they can automate you into a corner.</p>

<p>I would design the new data structure, write scripts to transfer the old structure to the new, then test the functionality. If there are problems, alter the new structure and / or the import scripts, then run the data transfer routine again and repeat the whole process until sure that no data or functionality are being lost. At this point, arrange a date to shut down the old system, do the data migration, then bring up the new system.</p>

<p>Missing from all this of course is training the users on the new / improved system. This is vital! Don't leave it out of your plan or the best new shiny improved system will be sunk due to user unhappiness.</p>


# InnoDb working some of the time but not others
[Link to question](https://stackoverflow.com/questions/698807/innodb-working-some-of-the-time-but-not-others)
**Creation Date:** 1238443350
**Score:** 1
**Tags:** mysql, innodb
## Question Body
<p>I'm in the process of swapping over a database for a rewrite of my program and part of that is writing both a conversion script and a script to create new tables.</p>

<p>I'm renaming tables, changing indexes and generally altering most of the table in some way, part of that is that I'm changing from MyISAM to InnoDB tables.</p>

<p>The conversion script works flawlessly but the script to create new tables falls over at a specific point.</p>

<pre><code>Query:
create table team_resources
(
     amount double not null default 0,
     resource int unsigned not null default 0,
     team int unsigned not null default 0,
     primary key (resource,team)
) ENGINE = InnoDB
</code></pre>

<p>I get <a href="http://forums.mysql.com/read.php?22,33999,33999" rel="nofollow noreferrer">error 121</a> which is the error given when a table cannot be created. The script is run from a Python file but I get the same error in both my SQL program and phpMyAdmin in both raw script and the table wizard helper form thingie.</p>

<p>The tables all converted to InnoDB just fine so I'm stumped as to why it has issues creating new ones. This query works if I take out the InnoDB part.</p>

<p>Any suggestions?</p>

## Answers
### Answer ID: 698837
<p><a href="http://bugs.mysql.com/bug.php?id=26507" rel="nofollow noreferrer">Bug 26507</a> sheds some light on this. Looks like creating/dropping tables isn't quite atomic.</p>

<p>One option is to do a mysqldump and try loading into a freshly installed database.</p>

<p>Another way to handle this is described at the end of <a href="http://bugs.mysql.com/bug.php?id=17546" rel="nofollow noreferrer">Bug 17546</a>, but you should verify the issues is with the frm file.</p>

### Answer ID: 698820
<p>I'm able to run that statement fine on a MySQL 5.0.32 install.  It may be a bug that's been fixed.</p>


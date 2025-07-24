# sqldf package in R, querying a data frame
[Link to question](https://stackoverflow.com/questions/8219747/sqldf-package-in-r-querying-a-data-frame)
**Creation Date:** 1321916351
**Score:** 4
**Tags:** macos, r, sqldf
## Question Body
<p>I'm trying to rewrite some code using the sqldf library in R, which should allow me to run SQL queries on data frames, but I am having an issue in that whenever I  try to run a query, R seems like it tries to query the actual real MySQL db con that I use and look for a table by the name of a the data frame that I am trying to search by.  </p>

<p>When I run this:</p>

<pre><code>    sqldf("SELECT COUNT(*) from work.class_scores")
</code></pre>

<p>I get:</p>

<p>Error in mysqlNewConnection(drv, ...) : 
  RS-DBI driver: (Failed to connect to database: Error: Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
)</p>

<p>When I try to specify the location using two different ways (the first form the googlecode page, the second which should be right based on the docs)</p>

<pre><code>&gt;     sqldf("SELECT COUNT(*) from work.class_scores", sqldf.driver = "SQLite")
Error in sqldf("SELECT COUNT(*) from work.class_scores", sqldf.driver = "SQLite") : 
  unused argument(s) (sqldf.driver = "SQLite")
&gt;     sqldf("SELECT COUNT(*) from work.class_scores", drv = "SQLite")
Loading required package: tcltk
Loading Tcl/Tk interface ... Error : .onLoad failed in loadNamespace() for 'tcltk', details:
  call: dyn.load(file, DLLpath = DLLpath, ...)
  error: unable to load shared library '/Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so':
  dlopen(/Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so, 10): Library not loaded: /usr/local/lib/libtcl8.5.dylib
  Referenced from: /Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so
  Reason: image not found
Error: require(tcltk) is not TRUE
</code></pre>

<p>So, I'm thinking it might be a a problem with this package tcltk, which I have never heard of, so I try and take care of that and find some issues:</p>

<pre><code> &gt; install.packages("tcltk")
Warning in install.packages :
  argument 'lib' is missing: using '/Users/michaeldiscenza/Library/R/2.11/library'
Warning in install.packages :
  package ‘tcltk’ is not available
&gt; install.packages("tcltk2", lib="/Applications/RStudio.app/Contents/Resources/R/library")
trying URL 'http://lib.stat.cmu.edu/R/CRAN/bin/macosx/leopard/contrib/2.11/tcltk2_1.1-5.tgz'
Content type 'application/x-gzip' length 940835 bytes (918 Kb)
opened URL
==================================================
downloaded 918 Kb


The downloaded packages are in
    /var/folders/Y1/Y1gdz9tKFiSnWsGP9+BDcU+++TI/-Tmp-//RtmpL07KTL/downloaded_packages
&gt; library("tcltk")
Loading Tcl/Tk interface ... Error : .onLoad failed in loadNamespace() for 'tcltk', details:
  call: dyn.load(file, DLLpath = DLLpath, ...)
  error: unable to load shared library '/Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so':
  dlopen(/Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so, 10): Library not loaded: /usr/local/lib/libtcl8.5.dylib
  Referenced from: /Library/Frameworks/R.framework/Resources/library/tcltk/libs/x86_64/tcltk.so
  Reason: image not found
Error: package/namespace load failed for 'tcltk'
</code></pre>

<p>Error in !dbPreExists : invalid argument type</p>

<p>Here, I just really don't know what the issue is, do I need to move something around?</p>

<p>Another approach that I tried was before running the query on the data frame object, setting my database connection so R would look there rather than trying to connect to the actual local MySQL database.  But that didn't work.  Back to the problem with the socket (even though I can query the local DB itself without any issues.</p>

<pre><code>&gt;     con &lt;- sqldf()
Error in mysqlNewConnection(drv, ...) : 
  RS-DBI driver: (Failed to connect to database: Error: Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
)
</code></pre>

<p>Eventually, I want to query to get the count of records where the value for C is larger than 2 for example, and I feel comfortable doing that.  The only problem is I don't know if there is another way to specify that what I am querying is a data frame and not an actual db.  Am I missing something really silly and easy here?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 8221833
<p>This answer has been transferred from my earlier comments.</p>

<p>The post and comments indicate that:</p>

<ol>
<li><p>it is desired to use SQLite with sqldf even though RMySQL is loaded
and </p></li>
<li><p>there was a message about tcltk being missing</p></li>
<li><p>there was a problem regarding: <code>sqldf("select count(*) from work.class_scores")</code> 
where <code>work.class_scores</code> is a data frame.</p></li>
</ol>

<p>On the <a href="http://sqldf.googlecode.com">sqldf home page</a> FAQ #7 addresses (1) above and FAQ #5 addresses (2).  (3) is due to the fact that dot is an SQL operator so such data frame names need to be quoted or else their name changed to remove the dot.</p>

<p>Below we provide  reproducible example that implements the above three solutions.  </p>

<p>The <code>sqldf.driver</code> option is used to force SQLite to be used even though RMySQL is loaded.  </p>

<p>Regarding tcltk there are three approaches: (i) The <code>gsubfn.engine</code> option causes R code to be used in place of tcltk so that the tcltk package won't be needed.  See example code below.  (ii) Alternately install tcltk.  (iii) This question was asked when sqldf 0.4-4 was the current version but now that sqldf 0.4-5 is out note that additional tcltk package detection has been added which makes it more likely that it will automatically handle all this without the user having to set any options and without having to install tcltk.  Thus the easiest solution may be to just upgrade to sqldf 0.4-5 or later.</p>

<p>We quote the data frame name having a dot in it or replace the data frame name with a name not containing a dot:</p>

<pre><code>options(sqldf.driver = "SQLite") # as per FAQ #7 force SQLite
options(gsubfn.engine = "R") # as per FAQ #5 use R code rather than tcltk

library(RMySQL)
library(sqldf)

work.class_scores &lt;- BOD # BOD is built in
sqldf("select count(*) from 'work.class_scores'")

# or
work_class_scores &lt;- work.class_scores
sqldf("select count(*) from work_class_scores")
</code></pre>

<p>EDIT:</p>

<p>Added info about sqldf 0.4-5.</p>

### Answer ID: 8221379
<p>Can you try installing the <code>tcl</code> package from <a href="http://cran.r-project.org/bin/macosx/tools/" rel="nofollow">here</a>?
(this is assuming you are on a mac).</p>


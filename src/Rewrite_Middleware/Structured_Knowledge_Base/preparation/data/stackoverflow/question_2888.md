# Speeding up a ton of short-lived `psql` sessions on Windows
[Link to question](https://stackoverflow.com/questions/57193662/speeding-up-a-ton-of-short-lived-psql-sessions-on-windows)
**Creation Date:** 1564023189
**Score:** 2
**Tags:** bash, postgresql, performance
## Question Body
<p>I have inherited an application which is written in dozens (maybe hundreds, I haven't counted exactly) of PostgreSQL functions. In order to check the application code into git and be able to easily work on specific functions, I used <a href="https://github.com/omniti-labs/pg_extractor" rel="nofollow noreferrer">pg_extractor</a> to export the database into a separate file for each function.</p>

<p>In order to easily apply updates from git (both on developer machines and in production), I wrote a bash script that uses the <code>psql</code> command line client to run all of the function files, which causes the database server to be updated to match the files from git.</p>

<p>The gist of it looks like this (with some initialization code replaced by comments for brevity):</p>

<pre><code>#!/bin/bash

# Check if a .env file is present and load it to set the PGHOST, PGPORT, PGUSER, PGPASSWORD, and PGDATABASE environment variables

# Check that `psql` is on the PATH

# Check the the database set in PGDATABASE exists on the server

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

makeFunction () {
    echo -n "CREATE OR REPLACE FUNCTION $2"
    psql -q -x &lt; "$DIR/$1/functions/$2.sql" &gt; /dev/null
    if [ $? -eq 0 ]; then
        echo -e " - ${GREEN}COMPLETE${NC}"
    else
        echo -e " - ${RED}FAILED${NC}"
        exit 1
    fi
}

for schema in admin admin_internal main main_internal
do
    if [ -d "$DIR/$schema/functions" ]; then
        for function in $DIR/$schema/functions/*.sql
        do
            makeFunction $schema $(basename "$function" .sql)
        done
    fi
done
</code></pre>

<p>On most of our Linux machines (development and production, Ubuntu 16.04 and 18.04) this script takes 15-20 seconds. Example:</p>

<pre><code>real    0m14.324s
user    0m6.894s
sys     0m1.742s
</code></pre>

<p>However, on our Windows development machines (when run using git-bash) it usually takes around three minutes to run the same script. Example:</p>

<pre><code>real    3m0.825s
user    0m3.525s
sys     0m11.943s
</code></pre>

<p>(Thinking the issue might be with Bash on Windows, I tried converting the script to PowerShell, only to see the same issue. Thankfully I saw that it wouldn't make a difference while doing partial testing before spending too much time on it.)</p>

<p>It turns out that the problem is in actually making the connection to the PostgreSQL server. For example, using <code>time psql -lqt</code> to time listing all databases on the server (these are example numbers, but dozens of test runs have shown that they are consistently the similar to these):</p>

<ul>
<li><p>On Ubuntu:</p>

<pre><code>real    0m0.055s
user    0m0.032s
sys     0m0.020s
</code></pre></li>
<li><p>On Windows:</p>

<pre><code>real    0m0.852s
user    0m0.000s
sys     0m0.030s
</code></pre></li>
</ul>

<p>As you can see, it takes 15 times longer on Windows. Extend that out to all the times we are calling <code>psql</code> in the update script, and it's no wonder that it takes 9 times longer to run the full script on Windows than on Linux.</p>

<p>It is well known that Postgres performance will never be as good on Windows as Linux because of the one-process-per-connection model and the lack of <code>fork()</code> on Windows, but that should be a bottleneck in the creation of the connection, not in the execution of the commands. (That the bottleneck is in the connection and not the query execution is evidenced by the fact that a single example command is consistently 15x slower, but the whole script with much larger queries being run is only 9-12x slower.)</p>

<p>Is there a way to make this faster for our Windows users? Is there some way to reuse an existing <code>psql</code> session and pipe additional files into it? Or is my only option to rewrite this in some other language and write my own database communication code that reads the files and pipes them to PostgreSQL myself?</p>

## Answers
### Answer ID: 57194366
<p>Running the connection through <a href="https://pgbouncer.github.io/" rel="nofollow noreferrer"><code>PgBouncer</code></a> instead of directly to Postgres makes a huge difference.</p>

<p>Using it, my script run on Windows is reduced to around 30 seconds.</p>

<p>It's still not quite as fast as on Linux, but I can live with "only" a 6x improvement.</p>

<pre><code>real    0m33.232s
user    0m2.740s
sys     0m9.785s
</code></pre>


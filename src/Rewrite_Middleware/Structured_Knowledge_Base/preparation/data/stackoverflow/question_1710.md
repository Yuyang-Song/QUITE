# Design Advise: Sending signals to daemons through HTTP
[Link to question](https://stackoverflow.com/questions/4690084/design-advise-sending-signals-to-daemons-through-http)
**Creation Date:** 1295000888
**Score:** 2
**Tags:** perl, security, network-programming, cgi
## Question Body
<p>I'm using Apache on Ubuntu.  I have a Perl script which basically read the files names of a directory, then rewrites a text file,  then sends a signal to a daemon.  How can this be done, as secure as possible through a web-page?</p>

<p>Actually I can run a simplified cgi in the code below, but not if I remove the comments. I'm looking for advise considering any of:</p>

<ul>
<li>Using HTTP Requests? </li>
<li>How about Apache file permissions on the directory shown in code?</li>
<li>Is htaccess enough to enable user/pass access to the cgi?</li>
<li>Should I use a database instead of writing to a file and run a cron querying the db with permission granted to write and send the signal?</li>
<li>Granting as less permissions as possible to the webserver.</li>
<li>Should I set a VPN?</li>
</ul>

<p><br/> </p>

<pre><code>#!/usr/bin/perl -wT
use strict;
use CGI;
#@fileList = &lt;/home/user/*&gt;; #read a directory listing
my $query = CGI-&gt;new();

print $query-&gt;header( "text/html" ),
$query-&gt;p( "FirstFileNameInArray" ),
#$query-&gt;p( $fileList[0] ), #output the first file in directory
$query-&gt;end_html;
</code></pre>

## Answers
### Answer ID: 4690310
<p>Presumably, the error you're getting from the commented lines is a permission denied when trying to read the <code>/home/user</code> directory.  The way to fix this is (surprise, surprise) to give the apache user[1] to read that directory.  There are three primary approaches to doing this:</p>

<ol>
<li><p>In most environments, there's
really no good reason to hide all
filenames within a user's home
directory, so you could make the
directory world-readable with <code>chmod
a+r /home/user</code>.  Unless you have a
specific reason to prevent the
general public from knowing the
names of the files in the user's
home directory, I'd tend to
recommend this approach.</p></li>
<li><p>If you want to be a bit more
restrictive about it, you could
change <code>/home/user</code> to be owned by a
group which the apache user belongs
to (or add the apache user to the
group that currently owns
<code>/home/user</code>) and then set
<code>/home/user</code> to be group-readable. 
This will make it accessible to all
members of that group, but not the
general public.</p></li>
<li><p>If you need to have standard
filesystem permissions applied to
web access, you can look at
configuring <code>suexec</code> so that
individual requests can take on
permissions of users other than the
apache user.  This is normally the
user who owns the code which is
being run to handle the request
(e.g., in this case, the user who
owns your directory-listing script),
but, if you're using htaccess-based
authentication, it may be possible
to configure <code>suexec</code> to decide
which user's permissions to take on
based on what user you log in as. 
(I avoid <code>suexec</code> myself, so I'm not
100% certain if this can be done and
have no idea how to go about it if
it can.)</p></li>
</ol>

<p>[1] ...by which I mean the user that apache is running as; depending on your system config, this user may be named "apache", "httpd", "nobody", "www-data", or something else entirely.</p>


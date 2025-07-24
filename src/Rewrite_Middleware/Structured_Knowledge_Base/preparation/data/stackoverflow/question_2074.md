# Can&#39;t access database through phpMyAdmin
[Link to question](https://stackoverflow.com/questions/18027666/cant-access-database-through-phpmyadmin)
**Creation Date:** 1375486429
**Score:** 1
**Tags:** mysql, authentication, phpmyadmin, xampp
## Question Body
<p>Basically, I have a problem with my config.inc.php file.  But I'll describe the sequence of events in case I've mangled something else that I'm not aware of.</p>

<p>I've built a database in phpMyAdmin which I've been using for a few months on localhost.  It was installed with XAMPP.  It's <code>phpMyAdmin Version 3.5.7</code>, according to the <code>XAMPP/xamppfiles/phpMyAdmin/README</code> file.</p>

<p>For awhile, I had left <code>['controluser'] = 'pma' and ['controluserpass'] = 'pmapass'</code>.  A few weeks ago, I changed those values, but that apparently created a problem, since phpMyAdmin started showing me the </p>

<blockquote>
  <p>"Connection for controluser as defined in your configuration failed"</p>
</blockquote>

<p>warnings all the time.  Nevertheless, I was still able to do everything I needed to do; so I kept using my database.</p>

<p>Yesterday I had to kill a query that had gone on for over 8 hours.  After that, phpMyAdmin seemed to be loading other databases and tables a bit slow.  So I opened XAMPP and pressed the stop button for MySQL.  Evidently, this button no longer stops MySQL for me.  The icon simply spins and spins as if thinking.  So, as of today, I've been stopping and starting MySQL directly from the terminal rather than through the XAMPP Control interface.</p>

<p>Since I was seeing warnings for the controluser, I decided to rewrite the config.inc.php file to cure whatever problem was there.  Unfortunately, I've only made things worse.  Now I can't access my database at all.</p>

<p>I've spent 5 hours today researching how to set up my config.inc.php file, but I'm still unable to access my database.  In the past, I had it set up with the 'config' option and never had to enter a password.  Ideally I'd prefer to have password security.  But at this stage, I'd be happy just to regain access to my database.</p>

<p>Right now, <code>localhost/phpmyadmin</code> goes to the login page, where it defaults to having "root" entered for "username".  But I can't seem to log in.  Depending on the adjustments I've made to config.inc.php, sometimes the "username" defaults to gibberish; and other times an error message appears instead of the login.  No matter what I enter for the password, phpMyAdmin won't accept it:</p>

<blockquote>
  <p>2002 Cannot log in to the MySQL server</p>
</blockquote>

<p>Other times,  I get this error:</p>

<blockquote>
  <p>2002 - Can't connect to local MySQL server through socket
  '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock' (2) The server
  is not responding (or the local server's socket is not correctly
  configured).</p>
</blockquote>

<p>I've tried switching back and forth between</p>

<pre><code>$cfg['Servers'][$i]['auth_type'] = 'cookie'
</code></pre>

<p>and</p>

<pre><code>$cfg['Servers'][$i]['auth_type'] = 'config'
</code></pre>

<p>and between</p>

<pre><code>$cfg['Servers'][$i]['connect_type'] = 'tcp'
</code></pre>

<p>and</p>

<pre><code>$cfg['Servers'][$i]['connect_type'] = 'socket'
</code></pre>

<p>and between</p>

<pre><code>$cfg['Servers'][$i]['AllowNoPassword'] = false
</code></pre>

<p>and</p>

<pre><code>$cfg['Servers'][$i]['AllowNoPassword'] = true
</code></pre>

<p>and between</p>

<pre><code>$cfg['Servers'][$i]['host'] = 'localhost'
</code></pre>

<p>and</p>

<pre><code>$cfg['Servers'][$i]['host'] = '127.0.0.1'
</code></pre>

<p>Nothing seems to allow to access my database.</p>

<p>At the moment, I'm getting the login screen and this error:</p>

<blockquote>
  <p>2002 Cannot log in to the MySQL server</p>
</blockquote>

<p>What should I change?  Below is my config.inc.php file:</p>

<pre><code>&lt;?php

$cfg['blowfish_secret'] = '89x7a3f';

$i = 0;

$i++;

$cfg['Servers'][$i]['auth_type'] = 'cookie';

$cfg['Servers'][$i]['host'] = 'localhost';

$cfg['Servers'][$i]['AllowRoot'] = true;

$cfg['Servers'][$i]['connect_type'] = 'tcp'; 

$cfg['Servers'][$i]['compress'] = true;

$cfg['Servers'][$i]['extension'] = 'mysqli';
$cfg['Servers'][$i]['AllowNoPassword'] = false;

$cfg['Servers'][$i]['user'] = 'root';
$cfg['Servers'][$i]['password'] = 'pass';

// $cfg['Servers'][$i]['controlhost'] = '';

$cfg['Servers'][$i]['controluser']   = 'pma';
$cfg['Servers'][$i]['controlpass']   = 'pmapass';

$cfg['Servers'][$i]['pmadb'] = 'phpmyadmin';
$cfg['Servers'][$i]['bookmarktable'] = 'pma_bookmark';
$cfg['Servers'][$i]['relation'] = 'pma_relation';
$cfg['Servers'][$i]['table_info'] = 'pma_table_info';
$cfg['Servers'][$i]['table_coords'] = 'pma_table_coords';
$cfg['Servers'][$i]['pdf_pages'] = 'pma_pdf_pages';
$cfg['Servers'][$i]['column_info'] = 'pma_column_info';
$cfg['Servers'][$i]['history'] = 'pma_history';

//$cfg['DefaultConnectionCollation'] = 'utf8_general_ci';

$cfg['Servers'][$i]['table_uiprefs'] = 'pma_table_uiprefs';
$cfg['Servers'][$i]['tracking'] = 'pma_tracking';
$cfg['Servers'][$i]['designer_coords'] = 'pma_designer_coords';
$cfg['Servers'][$i]['userconfig'] = 'pma_userconfig';
$cfg['Servers'][$i]['recent'] = 'pma_recent';

// $cfg['Servers'][$i]['auth_swekey_config'] = '/etc/swekey-pma.conf';

$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';

$cfg['DefaultLang'] = 'en';


?&gt;
</code></pre>

## Answers
### Answer ID: 18038529
<p>Well after 2 days spent trying everything and anything anybody had ever posted online, I solved the problem.  That doesn't mean I know how the problem happened, or how to prevent it from happening again, or why the solution worked, or what any of it means.  But here's what I discovered, and here's how I fixed the issue.</p>

<p>I noticed that when I entered the following into the terminal</p>

<pre><code>locate mysql.sock
</code></pre>

<p>I got a surprising result:</p>

<pre><code>/private/var/mysql/mysql.sock
</code></pre>

<p>I was expecting a different file path for mysql.sock.  Someone else online had solved a similar problem by using a symbolic link between the 2 file paths.  In my case, the whole issue was resolved with one command in the terminal:</p>

<pre><code>ln -s /private/var/mysql/mysql.sock /Applications/xampp/xamppfiles/var/mysql/mysql.sock
</code></pre>

<p>Now I'm able to edit my config.inc.php file without problems.  Also, I'm now able to stop MySQL through XAMPP Control.  Most importantly, I can access my database again through phpMyAdmin.  </p>

<p>So my problem is 99% solved.  One thing that puzzles me a bit is this, though:  In "relation view", I used to see 2 columns -- one for foreign keys and another for keys internal to the table.  Now I just see foreign keys.  So I'm wondering what needs to be changed in config.inc.php to regain the other option, which I believe I had used in at least one table.</p>

### Answer ID: 18027693
<p>If you just need access to your database and you know your login credentials, try using adminer:</p>

<p><a href="http://www.adminer.org/" rel="nofollow">http://www.adminer.org/</a></p>

<p>It's just a single PHP file that you drop in to your web server, and doesn't have the history of security holes that phpMyAdmin does. We've replaced all our phpMyAdmin installs with adminer on both MySQL and Postgres and it works great.</p>


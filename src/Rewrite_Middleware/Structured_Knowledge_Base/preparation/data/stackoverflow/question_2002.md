# PHP and MySQL - Lot of queries causing timeout of 300 seconds
[Link to question](https://stackoverflow.com/questions/15251027/php-and-mysql-lot-of-queries-causing-timeout-of-300-seconds)
**Creation Date:** 1362582833
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>I got a PHP application that causes performance issues with MySQL. What happens is this: After the database entries extend a certain amount; it starts to randomly timeout the PHP page for 300 seconds.</p>

<p>I know I have to rewrite my code, since it is messy, out-dated, and I'm basically running a lot of queries which could be much more efficient.</p>

<p>But, I'm very curious what is able to cause this, and if there is a short-term solution for this. The php application works perfectly, but after browsing some pages with the results of the query behaving like it should, sometimes the load-time changes to 300 seconds. After which the page with database results show perfectly. After that I'm able to view some pages again, after which the process randomly starts over. During the 300 seconds the page is loading, the SQL processlist shows the command "Sleep" for the full loading time, with no query attached.</p>

## Answers
### Answer ID: 15251288
<p>Assuming that the problem is really MySQL related, you could try to assign more memory to MySQL server and see if performance improves. See the "huge" my.cnf configuration here:</p>

<p><a href="http://fts.ifac.cnr.it/cgi-bin/dwww/usr/share/doc/mysql-server-5.0/examples/my-huge.cnf.gz" rel="nofollow">http://fts.ifac.cnr.it/cgi-bin/dwww/usr/share/doc/mysql-server-5.0/examples/my-huge.cnf.gz</a></p>

<p>Also, if you don't need InnoDB features but your database is InnoDB, you can switch to MyISAM and gain some performance.</p>

<p>You should also check session locking and collision, this sometimes can create timeouts. You should release session as soon as you've read/written data on it because the session file stays locked until you close the session or the script has ended.</p>

### Answer ID: 15251156
<p>If the process list doesn't show running queries, than the problem is probably located at your application, and not at MySQL. Take a look at this: <a href="https://stackoverflow.com/questions/9468332/how-can-i-find-out-which-php-script-a-process-is-running-in-linux">How can I find out which PHP script a process is running in Linux?</a>.</p>


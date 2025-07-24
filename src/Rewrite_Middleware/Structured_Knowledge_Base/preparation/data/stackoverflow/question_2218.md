# mysql-proxy not running lua script
[Link to question](https://stackoverflow.com/questions/24397170/mysql-proxy-not-running-lua-script)
**Creation Date:** 1403647710
**Score:** 2
**Tags:** mysql, lua, mysql-proxy
## Question Body
<p>I know there are many mysql-proxy questions on SO, however I have read through many of them and none seem to solve my problem. I am simply trying to get mysql-proxy up and running, with the eventual purpose of rewriting some queries that go through the proxy. I am using ubuntu 14.04, I have mysql-proxy version 0.8.1, and mysql version 5.5.37. To start mysql-proxy I run the following line on the command line</p>

<pre><code>sudo mysql-proxy --defaults-file=mysql-proxy.cnf
</code></pre>

<p>where the file mysql-proxy.cnf looks like the following:</p>

<pre><code>[mysql-proxy]
log-file=                   /var/log/mysql/proxy-error.log
log-level=                  debug
admin-lua-script=           /usr/lib/mysql-proxy/lua/admin.lua
proxy-lua-script=       /path/to/lua/script/example.lua
admin-username =            myusername
admin-password =            mypassword
proxy-skip-profiling =      true
proxy-address =             localhost:4040
proxy-backend-addresses =   localhost:3306
plugins =                   proxy,admin
</code></pre>

<p>My example.lua script is very simple, and meant only to verify that the mysql-proxy query is being altered. example.lua is pasted below</p>

<pre><code>-- first_example.lua
function read_query(packet)
    if string.byte(packet) == proxy.COM_QUERY then
        print("Hello world! Seen the query: " .. string.sub(packet, 2))
    end
end
</code></pre>

<p>Since I don't run this with the --daemon flag, when I run that line above in the command line it just loops indefinitely, which is expected.</p>

<p>Finally, in separate terminal session, I run the following on the command line and enter my password in order to connect with the proxy</p>

<pre><code>mysql -u myusername -p -h localhost -P 4040
</code></pre>

<p>I then select a database to use, and run a simple SELECT query on one of the tables. Based on multiple articles/tutorials I've read on mysql-proxy, my first console session, the one that ran mysql-proxy, should print out some data based on the example.lua file. However this does not happen, in fact nothing happens.</p>

<p>I'm not sure if the following bit of information makes any difference, but in my "my.cnf" mysql configuration file, I have these couple of lines</p>

<pre><code>bind-address            = 255.255.255.255
#bind-address           = 127.0.0.1
</code></pre>

<p>where I have replaced my actual ip address with 255.255.255.255 because I do not want to display my ip address publicly.</p>

<p>Please, I have been trying to figure this out for several days, and no amount of new lua scripts, or changing the host:port parameters in the mysql-proxy.cnf file have solved anything. I</p>


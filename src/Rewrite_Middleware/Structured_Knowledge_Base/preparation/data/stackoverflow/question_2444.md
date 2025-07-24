# Move MYSQL data folder on Ubuntu
[Link to question](https://stackoverflow.com/questions/34529861/move-mysql-data-folder-on-ubuntu)
**Creation Date:** 1451479671
**Score:** 0
**Tags:** mysql, ubuntu
## Question Body
<p>I am aware of the very same thread here, <a href="https://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory">How to change MySQL data directory?</a>, but as i tried all of the methods i could find (including this one of course) and still no luck.</p>

<p>I would like to store my database on "/dlab/data/MYSQL".
This directory (/dlab) is actually an NFS folder if that matters.</p>

<p>My /etc/mysql/my.cnf file:</p>

<pre><code>#
# The MySQL database server configuration file.
#
# You can copy this to one of:
# - "/etc/mysql/my.cnf" to set global options,
# - "~/.my.cnf" to set user-specific options.
# 
# One can use all long options that the program supports.
# Run program with --help to get a list of available options and with
# --print-defaults to see which it would actually understand and use.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

# This will be passed to all mysql clients
# It has been reported that passwords should be enclosed with ticks/quotes
# escpecially if they contain "#" chars...
# Remember to edit /etc/mysql/debian.cnf when changing the socket location.
[client]
port        = 3306
socket      = /var/run/mysqld/mysqld.sock

# Here is entries for some specific programs
# The following values assume you have at least 32M ram

# This was formally known as [safe_mysqld]. Both versions are currently parsed.
[mysqld_safe]
socket      = /var/run/mysqld/mysqld.sock
nice        = 0

[mysqld]
#
# * Basic Settings
#
user        = mysql
pid-file    = /var/run/mysqld/mysqld.pid
socket      = /var/run/mysqld/mysqld.sock
port        = 3306
basedir     = /usr
datadir     = /dlab/data/MYSQL
tmpdir      = /tmp
lc-messages-dir = /usr/share/mysql
skip-external-locking
#
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
bind-address        = 127.0.0.1
#
# * Fine Tuning
#
key_buffer      = 16M
max_allowed_packet  = 16M
thread_stack        = 192K
thread_cache_size       = 8
# This replaces the startup script and checks MyISAM tables if needed
# the first time they are touched
myisam-recover         = BACKUP
#max_connections        = 100
#table_cache            = 64
#thread_concurrency     = 10
#
# * Query Cache Configuration
#
query_cache_limit   = 1M
query_cache_size        = 16M
#
# * Logging and Replication
#
# Both location gets rotated by the cronjob.
# Be aware that this log type is a performance killer.
# As of 5.1 you can enable the log at runtime!
#general_log_file        = /var/log/mysql/mysql.log
#general_log             = 1
#
# Error log - should be very few entries.
#
log_error = /var/log/mysql/error.log
#
# Here you can see queries with especially long duration
#log_slow_queries   = /var/log/mysql/mysql-slow.log
#long_query_time = 2
#log-queries-not-using-indexes
#
# The following can be used as easy to replay backup logs or for replication.
# note: if you are setting up a replication slave, see README.Debian about
#       other settings you may need to change.
#server-id      = 1
#log_bin            = /var/log/mysql/mysql-bin.log
expire_logs_days    = 10
max_binlog_size         = 100M
#binlog_do_db       = include_database_name
#binlog_ignore_db   = include_database_name
#
# * InnoDB
#
# InnoDB is enabled by default with a 10MB datafile in /var/lib/mysql/.
# Read the manual for more InnoDB related options. There are many!
#
# * Security Features
#
# Read the manual, too, if you want chroot!
# chroot = /var/lib/mysql/
#
# For generating SSL certificates I recommend the OpenSSL GUI "tinyca".
#
# ssl-ca=/etc/mysql/cacert.pem
# ssl-cert=/etc/mysql/server-cert.pem
# ssl-key=/etc/mysql/server-key.pem



[mysqldump]
quick
quote-names
max_allowed_packet  = 16M

[mysql]
#no-auto-rehash # faster start of mysql but no tab completition

[isamchk]
key_buffer      = 16M

#
# * IMPORTANT: Additional settings that can override those from this file!
#   The files must end with '.cnf', otherwise they'll be ignored.
#
!includedir /etc/mysql/conf.d/
</code></pre>

<p>According to the mentioned thread i tried:</p>

<p>Editing the /etc/apparmor.d/usr.sbin.mysqld file, it looks like this:</p>

<pre><code># vim:syntax=apparmor
# Last Modified: Tue Jun 19 17:37:30 2007
#include &lt;tunables/global&gt;

/usr/sbin/mysqld {
  #include &lt;abstractions/base&gt;
  #include &lt;abstractions/nameservice&gt;
  #include &lt;abstractions/user-tmp&gt;
  #include &lt;abstractions/mysql&gt;
  #include &lt;abstractions/winbind&gt;

  capability dac_override,
  capability sys_resource,
  capability setgid,
  capability setuid,

  network tcp,

  /etc/hosts.allow r,
  /etc/hosts.deny r,

  /etc/mysql/*.pem r,
  /etc/mysql/conf.d/ r,
  /etc/mysql/conf.d/* r,
  /etc/mysql/*.cnf r,
  /usr/lib/mysql/plugin/ r,
  /usr/lib/mysql/plugin/*.so* mr,
  /usr/sbin/mysqld mr,
  /usr/share/mysql/** r,
  /var/log/mysql.log rw,
  /var/log/mysql.err rw,

  # /var/lib/mysql/ r,
  # /var/lib/mysql/** rwk,

  /dlab/data/MYSQL/ r,
  /dlab/data/MYSQL/** rwk,

  /var/log/mysql/ r,
  /var/log/mysql/* rw,
  /var/run/mysqld/mysqld.pid rw,
  /var/run/mysqld/mysqld.sock w,
  /run/mysqld/mysqld.pid rw,
  /run/mysqld/mysqld.sock w,

  /sys/devices/system/cpu/ r,

  # Site-specific additions and overrides. See local/README for details.
  #include &lt;local/usr.sbin.mysqld&gt;
}
</code></pre>

<p>This did not work, when i start MYSQL, it fails.</p>

<p>I tied to change the ownership of the folder to mysql:mysql, did not help either. </p>

<p>Tried the mentioned alias as well, my /etc/apparmor.d/tunables/alias file:</p>

<pre><code># ------------------------------------------------------------------
#
#    Copyright (C) 2010 Canonical Ltd.
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of version 2 of the GNU General Public
#    License published by the Free Software Foundation.
#
# ------------------------------------------------------------------

# Alias rules can be used to rewrite paths and are done after variable
# resolution. For example, if '/usr' is on removable media:
# alias /usr/ -&gt; /mnt/usr/,
#
# Or if mysql databases are stored in /home:
alias /var/lib/mysql/ -&gt; /dlab/data/MYSQL,
</code></pre>

<p>If anyone has any solution for me, that would be very nice!</p>

<p>EDIT 1:</p>

<p>Here is the error log, it seems to be something with the permissions...</p>

<pre><code>151230 13:30:22 mysqld_safe mysqld from pid file /var/run/mysqld/mysqld.pid ended
151230 13:35:11 mysqld_safe Starting mysqld daemon with databases from /dlab/data/MYSQL
151230 13:35:11 [Warning] Using unique option prefix key_buffer instead of key_buffer_size is deprecated and will be removed in a future release. Please use the full name instead.
151230 13:35:11 [Note] /usr/sbin/mysqld (mysqld 5.5.46-0ubuntu0.14.04.2) starting as process 12902 ...
151230 13:35:11 [Warning] Can't create test file /dlab/data/MYSQL/dlab5.lower-test
151230 13:35:11 [Warning] Can't create test file /dlab/data/MYSQL/dlab5.lower-test
151230 13:35:11 [Warning] Using unique option prefix myisam-recover instead of myisam-recover-options is deprecated and will be removed in a future release. Please use the full name instead.
151230 13:35:11 [Note] Plugin 'FEDERATED' is disabled.
151230 13:35:11 InnoDB: The InnoDB memory heap is disabled
151230 13:35:11 InnoDB: Mutexes and rw_locks use GCC atomic builtins
151230 13:35:11 InnoDB: Compressed tables use zlib 1.2.8
151230 13:35:11 InnoDB: Using Linux native AIO
151230 13:35:11 InnoDB: Initializing buffer pool, size = 128.0M
151230 13:35:11 InnoDB: Completed initialization of buffer pool
151230 13:35:11  InnoDB: Operating system error number 13 in a file operation.
InnoDB: The error means mysqld does not have the access rights to
InnoDB: the directory.
InnoDB: File name ./ibdata1
InnoDB: File operation call: 'open'.
InnoDB: Cannot continue operation.
</code></pre>

<p>The given folder has the proper permissions (I guess):</p>

<pre><code>drwxrwxr-x    4 mysql mysql  4096 Dec 30 13:09 MYSQL
</code></pre>

## Answers
### Answer ID: 34814125
<p>The problem was with the permission as pointed out by Richard St-Cyr after giving the folder 777 and following the tips at <a href="https://stackoverflow.com/questions/1795176/how-to-change-mysql-data-directory">How to change MySQL data directory?</a> i managged to solve the problem!</p>


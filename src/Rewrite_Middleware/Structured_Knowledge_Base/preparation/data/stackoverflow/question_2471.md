# Significant performance decrease after upgrading MySQL from 5.0.67 to 5.5.44-MariaDB
[Link to question](https://stackoverflow.com/questions/36207945/significant-performance-decrease-after-upgrading-mysql-from-5-0-67-to-5-5-44-mar)
**Creation Date:** 1458845650
**Score:** 0
**Tags:** mysql, mariadb
## Question Body
<p>I have recently migrated a MySQL database from 5.0.67 to 5.5.44-MariaDB and I have a query which takes less than a second to execute in 5.0.67 but it takes over 100 seconds in 5.5.44.  </p>

<p>Before I begin to rewrite the query, I would like to find the difference between the two servers, my guess is that it could be a setting that isn't ideal in MariaDB but I can't find it.</p>

<p>Config of 5.0.67:</p>

<pre><code>set-variable = innodb_buffer_pool_size=2M
set-variable = innodb_additional_mem_pool_size=500K
set-variable = innodb_log_buffer_size=500K
set-variable = innodb_thread_concurrency=2
[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
timezone=America/Chicago

set-variable = innodb_buffer_pool_size=2M
set-variable = innodb_additional_mem_pool_size=500K
set-variable = innodb_log_buffer_size=500K
set-variable = innodb_thread_concurrency=2

#increse lock wait timout
innodb_lock_wait_timeout = 120
</code></pre>

<p>Config of 5.5.44:</p>

<pre><code>key_buffer_size = 16M
max_allowed_packet = 1M

sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M

innodb_buffer_pool_size = 16M
innodb_additional_mem_pool_size = 2M
innodb_log_buffer_size = 8M

[mysqldump]
quick
max_allowed_packet = 16M

[mysql]
no-auto-rehash

[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M

[mysqlhotcopy]
interactive-timeout
</code></pre>

<p>The query:</p>

<pre><code>SELECT
    node.user_id,
    node.user_id as id,
    node.name,
    node.status,
    node.left_id,
    node.right_id,
    node.locked,
    CONCAT(   node.name, ' ', node.surname) as fullname,
    (COUNT(parent.name) - (sub_tree.level + 1)) AS level
FROM
    users AS node ,
    users AS parent  ,
    users AS sub_parent  ,
    (
    SELECT
        node.name,
        node.user_id,
        (COUNT(parent.name) - 1) AS level
    FROM
        users AS node,
        users AS parent 
    WHERE
        node.left_id BETWEEN parent.left_id AND parent.right_id
    AND
        node.user_id = '29151'
    GROUP BY node.name
    ORDER BY node.left_id
    ) AS sub_tree
WHERE
    node.left_id BETWEEN parent.left_id AND parent.right_id
AND
    node.left_id BETWEEN sub_parent.left_id AND sub_parent.right_id
AND
    sub_parent.user_id = sub_tree.user_id      
GROUP BY
    node.user_id
HAVING
    1 = 1
    and node.locked = 0
      and level  in ( 1,2,3,4)          
 ORDER BY node.left_id ;
</code></pre>


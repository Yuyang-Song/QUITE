# MariaDB having syntax in a new MariaDB install
[Link to question](https://stackoverflow.com/questions/58862018/mariadb-having-syntax-in-a-new-mariadb-install)
**Creation Date:** 1573750539
**Score:** 0
**Tags:** sql, mariadb, pymysql
## Question Body
<p>I have developed some Python scripts that inserts data into a MariaDB database using PyMySQL library. </p>

<p>The scripts was working well until yesterday. Yesterday the HDD of the server died. I just installed 3 disks (1 for boot and SWAP, the other two are in a raid 1 with EXT4 and / mounting point). When the main packages are ready, I found the scripts aren't working well due to the next query </p>

<pre><code>INSERT
INTO
    devices(
        source_id,
        serialnumber,
        NAME,
        location_desc
    )
SELECT
    2,
    '5996B',
    'Barbate',
    'CADIZ'
WHERE NOT EXISTS
    (
    SELECT
        1
    FROM
        devices
    WHERE
        serialnumber = '5996B'
)
</code></pre>

<p>This query insert a device into devices table if the device not exists. The scripts work well in my local MariaDB server, but not in the production one, giving the next error: </p>

<pre><code>Error

SQL query: Documentation

INSERT
INTO
    devices(
        source_id,
        serialnumber,
        NAME,
        location_desc
    )
SELECT
    2,
    '5996B',
    'Barbate',
    'CADIZ'
WHERE NOT EXISTS
    (
    SELECT
        1
    FROM
        devices
    WHERE
        serialnumber = '5996B'
)

MariaDB said: Documentation
#1064 - You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'WHERE NOT EXISTS
    (
    SELECT
        1
    FROM
        devices
    W' at line 14
</code></pre>

<p>I think that is a compatibility issue with a newer version of MariaDB. How can I fix it without rewriting my Python scripts?</p>

<p>EDIT:</p>

<p>Results for:
<code>SELECT VERSION();</code></p>

<p>Response in local server (where the SQL statement works):
<code>10.4.6-MariaDB</code></p>

<p>Response in production server (where the SQL statement doesn't work):
<code>10.3.17-MariaDB-0+deb10u1</code></p>

## Answers
### Answer ID: 58863603
<p>I found a solution:</p>

<p><code>FROM DUAL</code> is required in some mysql-server version, so to get it working the query needs to be changed to: </p>

<pre><code>INSERT
INTO
    devices(
        source_id,
        serialnumber,
        NAME,
        location_desc
    )
SELECT
    2,
    '5996B',
    'Barbate',
    'CADIZ'
FROM DUAL
WHERE NOT EXISTS
    (
    SELECT
        1
    FROM
        devices
    WHERE
        serialnumber = '5996B'
)
</code></pre>

<p>I hope somebody find this useful</p>


# MySQL C API - Bulk insert performance question
[Link to question](https://stackoverflow.com/questions/57912475/mysql-c-api-bulk-insert-performance-question)
**Creation Date:** 1568312338
**Score:** 0
**Tags:** mysql, c
## Question Body
<p>I'm working on a  rewrite of a popular add-on module (NDOUtils) for an even more popular application (Nagios). This module adds functionality to Nagios by making the objects/statuses/histories of each object available in a database.</p>

<p>The current available version takes the data from Nagios (via some registered callbacks/function pointers) and sends it over a socket where an additional process listens and queues the data up. Finally, an additional process then pops the data from the queue and builds mysql queries for insertion.</p>

<p>Although it works, and has worked for quite some time, we encounter problems on larger systems (15k+ objects defined in Nagios configurations). We decided to start over and re-write the module to handle the database calls directly (via mysql c api prepared statements).</p>

<p>This works beautifully for the status data. One problem we face is that on startup, we need to get the object definitions into the database. Since the definitions can change each time the process starts, we truncate the appropriate tables and recreate each object. This works fine for most systems...</p>

<p>But for large systems, this process can take upwards of several minutes - and this is a blocking process - several minutes is unacceptable, and this is exacerbated on critical monitoring setups.</p>

<p>So, to get this rewrite underway, I kept things simple. To begin with, I looped over each object definition, and built a simple query and then inserted. Once each of that type of object were inserted, I looped back over the objects for all of the objects that are related (for example, each host definition likely has a contact or contactgroup associated with it. Those relationships need to be identified). This was the easiest to read, but extremely slow on a system with 15k hosts and 25k services. <em>Extremely</em> slow as in 3 minutes.</p>

<p>Of course we can do better than that. I rewrote the major functions (hosts and services) to only need to loop over the object list twice each, and instead of sending an individual query per object or relationship, we build a bulk insert query. The code for this looks something like this:</p>

<pre><code>#define MAX_OBJECT_INSERT 50

/* this is large because the reality is that the contact/host/services object queries
   are several thousand characters before any concatenation happens */
#define MAX_SQL_BUFFER ((MAX_OBJECT_INSERT * 150) + 8000)

#define MAX_SQL_BINDINGS 400

MYSQL_STMT * ndo_stmt = NULL;
MYSQL_BIND ndo_bind[MAX_SQL_BINDINGS];
int ndo_bind_i = 0;

int ndo_max_object_insert_count = 20;



int ndo_write_hosts()
{
    host * tmp = host_list;
    int host_object_id[MAX_OBJECT_INSERT] = { 0 };
    int i = 0;

    char query[MAX_SQL_BUFFER] = { 0 };

    char * query_base = "INSERT INTO nagios_hosts (instance_id, config_type, host_object_id, name) VALUES ";
    size_t query_base_len = strlen(query_base);
    size_t query_len = query_base_len;

    char * query_values = "(1,?,?,?),";
    size_t query_values_len = strlen(query_values);

    char * query_on_update = " ON DUPLICATE KEY UPDATE instance_id = VALUES(instance_id), config_type = VALUES(config_type), host_object_id = VALUES(host_object_id), name = VALUES(name)";
    size_t query_on_update_len = strlen(query_on_update);

    /* lock the tables */
    mysql_query(mysql_connection, "LOCK TABLES nagios_logentries WRITE, nagios_objects WRITE, nagios_hosts WRITE");

    strcpy(query, query_base);

    /* reset mysql bindings */
    memset(ndo_bind, 0, sizeof(ndo_bind));
    ndo_bind_i = 0;

    while (tmp != NULL) {

        /* concat the query_values to the current query */
        strcpy(query + query_len, query_values);
        query_len += query_values_len;

        /* retrieve this object's object_id from `nagios_objects` */
        host_object_id[i] = ndo_get_object_id_name1(TRUE, NDO_OBJECTTYPE_HOST, tmp-&gt;name);

        ndo_bind[ndo_bind_i].buffer_type = MYSQL_TYPE_LONG;
        ndo_bind[ndo_bind_i].buffer      = &amp;(config_type);
        ndo_bind_i++;

        ndo_bind[ndo_bind_i].buffer_type = MYSQL_TYPE_LONG;
        ndo_bind[ndo_bind_i].buffer      = &amp;(host_object_id[i]);
        ndo_bind_i++;

        ndo_bind[ndo_bind_i].buffer_type   = MYSQL_TYPE_STRING;
        ndo_bind[ndo_bind_i].buffer_length = MAX_BIND_BUFFER;
        ndo_bind[ndo_bind_i].buffer        = tmp-&gt;name;
        ndo_tmp_str_len[ndo_bind_i]        = strlen(tmp-&gt;name);
        ndo_bind[ndo_bind_i].length        = &amp;(ndo_tmp_str_len[ndo_bind_i]);
        ndo_bind_i++;

        i++;

        /* we need to finish the query and execute */
        if (i &gt;= ndo_max_object_insert_count || tmp-&gt;next == NULL) {

            memcpy(query + query_len - 1, query_on_update, query_on_update_len);

            mysql_stmt_prepare(ndo_stmt, query, query_len + query_on_update_len);
            mysql_stmt_bind_param(ndo_stmt, ndo_bind);
            mysql_stmt_execute(ndo_stmt);

            /* remove everything after the base query */
            memset(query + query_base_len, 0, MAX_SQL_BUFFER - query_base_len);

            query_len = query_base_len;
            ndo_bind_i = 0;
            i = 0;
        }

        tmp = tmp-&gt;next;
    }

    mysql_query(mysql_connection, "UNLOCK TABLES");
}
</code></pre>

<p>This has been edited for brevity, and to get at least a basic understanding of what's happening here. In reality, there is real error checking happening after each mysql return.</p>

<p>Regardless, even with <code>ndo_max_object_insert_count</code> set to a high number (50, 100, etc.) - this still takes about 50 seconds for 15k hosts and 25k services.</p>

<p>I'm at my wits end trying to make this faster, so if anyone sees some glaring problem that I'm not noticing, or has any advice on how to make this style of string manipulation/bulk insert more performant, I'm all ears.</p>

<p><strong><em>Update 1</em></strong></p>

<p>Since posting this, I've gone through and updated the loop to not continuously rewrite the string, and also to stop re-preparing the statement and re-binding the parameters. Now it only updates the query the first loop through and then on the last loop (depending on the result of <code>number of hosts % max object inserts</code>). This has actually shaved a few seconds off, but nothing substantial.</p>

## Answers
### Answer ID: 57914202
<p>Your code at first glance does not appear to have any issues that would cause a performance problem like this. With this amount of data I would expect the code to run in a few seconds given normal hardware/OS behavior. I would recommend examining two possible pain points:</p>

<ol>
<li>How fast are you generating the data to insert? (Replace the insertion part of the code to a NOOP)</li>
<li>If you determine in step 1 that the data is being generated quickly enough, the problem is with the write performance of the database.</li>
</ol>

<p>Regardless, it is very likely that you have to troubleshoot on the database server level - run SHOW PROCESSLIST to start, then SHOW ENGINE INNODB STATUS if you are using InnoDB, and if all else fails, grab stacktrace shots of mysqld process with gdb. </p>

<p>Likely culprit is something horribly wrong with the I/O subsystem of the server or perhaps some form of synchronous replication is enabled, but it is hard to know for sure without some server-level diagnostic.</p>


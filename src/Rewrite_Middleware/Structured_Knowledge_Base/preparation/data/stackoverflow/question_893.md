# Problems when using Db2 Developer-C Edition from Docker on Mac
[Link to question](https://stackoverflow.com/questions/48473517/problems-when-using-db2-developer-c-edition-from-docker-on-mac)
**Creation Date:** 1517037082
**Score:** 1
**Tags:** docker, db2
## Question Body
<p>(I am rewriting this question from <a href="https://developer.ibm.com/answers/questions/426985/using-db2-developer-c-edition-from-docker-on-mac.html" rel="nofollow noreferrer">another site</a> to get more attention, I hope it is ok.)</p>

<p>I am trying to setup a Db2 developer environment following instruction from <a href="https://store.docker.com/images/db2-developer-c-edition" rel="nofollow noreferrer">https://store.docker.com/images/db2-developer-c-edition</a>.</p>

<p>I am able to create the container, start it and do even some sql queries</p>

<pre><code>mkdir docker_volume
# I use the same env_list as the instructions link above
docker run -h db2server_myDb \
    --name db2server \
    --restart=always  \
    --detach \
    --privileged=true  \
    -p 50000 \
    --env-file .env_list \
    -v docker_volume:/database \
    store/ibmcorp/db2_developer_c:11.1.2.2
docker exec -ti db2server bash -c "su db2inst1"
db2 connect to testdb
db2 "create table t_project ( code varchar(5), name varchar(60) )"
db2 "insert into t_project (code, name) values (57003, 'sample')"
db2 "select * from t_project"
</code></pre>

<p>So far everything seems ok.</p>

<h2>Problems:</h2>

<ol>
<li><p>I am <strong>NOT</strong> able to connect to db from the host. How can I connect to this db from my macos machine? I am trying host: <code>172.17.0.1</code> port: <code>50000</code> Database: <code>testdb</code> username: <code>db2inst1</code> password: <code>password</code></p></li>
<li><p>After stopping the container I am <strong>NOT</strong> able to start it again. What is the correct command to start or stop my db2 container?</p>

<pre><code>$ docker stop db2server
$ docker start -ia db2server
(output)
...
DB2 State : Operable
DB2 has not been started
Starting DB2...
01/26/2018 03:21:38     0   0   SQL1063N  DB2START processing was successful.
SQL1063N  DB2START processing was successful.
mkdir: cannot create directory '/var/log/supervisor': File exists
Unlinking stale socket /var/run/supervisor.sock
(*) All databases are now active. 
(*) Setup has completed.
false

2018-01-26-03.21.38.860516+000 I342573E395           LEVEL: Warning
PID     : 629                  TID : 140077563770752 PROC : db2start
INSTANCE: db2inst1             NODE : 000
HOSTNAME: db2server_myDb
FUNCTION: DB2 UDB, base sys utilities, sqleReleaseStStLockFile, probe:15795
MESSAGE : Released lock on the file:
DATA #1 : String, 50 bytes
/database/config/db2inst1/sqllib/ctrl/db2strst.lck
</code></pre></li>
</ol>

<p>I am stuck here and I need to terminate the process and remove the container and re-do everything again.</p>

<p>Any help is highly appreciated</p>

## Answers
### Answer ID: 48697371
<p>You are using the Docker Store image of DB2 Developer-C.  If you following the instructions for creating the container, you will notice that the instructions specify to use the option <code>-p 50000</code> for <code>docker run</code>. This option specifies that port 50000 in the container will be bound to a <em>dynamic</em> port on the host machine.</p>

<p>You need to check to see what port is attached on the host computer.  You can see this in the output from <code>docker ps</code> or, better, from <code>docker port</code>:</p>

<pre><code>$ docker port db2serverX
50000/tcp -&gt; 0.0.0.0:32777
</code></pre>

<p>This shows that port 50000 in the container is mapped to port 32777 on (all) interfaces on the Docker host.</p>

<p>If you would like to specify the port you connect to on your Docker host, make sure to use the format <code>-p 50000:50000</code>, where you are specifying <code>hostPort:containerPort</code>.</p>


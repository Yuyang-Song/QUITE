# Hibernate Java batch operation deadlock
[Link to question](https://stackoverflow.com/questions/6781138/hibernate-java-batch-operation-deadlock)
**Creation Date:** 1311274208
**Score:** 1
**Tags:** java, oracle-database, hibernate, locking, deadlock
## Question Body
<p>We have J2EE application built using Hibernate and struts. We have RMI registry based implementation for business functionality. </p>

<p>In our application around 250 concurrent users are going to upload batches containing huge data named BATCHDET. These batches are first validated against 30 validation and then they are inserted to tables where we have parent and child relationship. Similar there are other operation which need huge processing. like printing etc. </p>

<p>There is one table containing 10 million record which gets accessed for all types of transactions and every process inserts and updates this table. This table has emerged as bottleneck. We have added all the required indexes as well. </p>

<p>After 30 minutes of run system JVM utilizes all the allocated 6GB of RAM and goes in no response state. When we tried to find out root cause we realized there was lock at database site and all the update queries related to BATCHDET table were in wait state. We tried everything which we could but no luck. </p>

<p>System run smooth when tried with 50 concurrent user but dies with 250 users which are expected. BATCHDET has lot of dependency on almost every module, not in mood to rewrite the implementation, could you please provide quick fix to it.</p>

<p>we have Thread based transaction demarcation at Hibernate implemented with HIbernateUtil.java. Transaction isolation is ReadCommitted. Is there any way where we can define no lock for all search operation. we have oracle 10G RDBMS. </p>

<p>Let me know if you need any other details.</p>

<p>~Amar</p>

## Answers
### Answer ID: 6784043
<p>" Is there any way where we can define no lock for all search operation. we have oracle 10G RDBMS."</p>

<p>Oracle doesn't lock on selects, so in effect this is already in place.</p>

<p>Oracle also locks at a row level, so you need to stop thinking about the table as a whole and start thinking individual rows.</p>

<p>You need to talk with your DBA. There's a whole bunch of stuff to monitor in Oracle at both the system and session level. The DBA will be able to be able to look at v$session and tell you what the individual sessions are waiting on. There might be locks, it might be a disk bottle neck, it may be index contention, or it may be the database is sat there idle and all the inefficiency is in the java layer.</p>


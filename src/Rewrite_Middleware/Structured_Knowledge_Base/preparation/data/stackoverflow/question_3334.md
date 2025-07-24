# How can I optimise a Node.js simulation that writes results to a MySQL database?
[Link to question](https://stackoverflow.com/questions/76581373/how-can-i-optimise-a-node-js-simulation-that-writes-results-to-a-mysql-database)
**Creation Date:** 1688044087
**Score:** 0
**Tags:** mysql, node.js, multithreading, montecarlo, node-worker-threads
## Question Body
<p>I have a monte carlo simulation (essentially a simulation of game involving random numbers that I run millions of times) that I've coded in Node.js. The simulation runs a batch of 100,000 games and then inserts the data from that batch into a local MySQL database. After all batches have run a number of queries are run against the database.</p>
<p>I recently decided to try and rewrite the simulator for multithreading. I now have a main thread that assigns batches one at a time to 7 worker threads. They send their results back to the main thread and this thread inserts them into the database. This is working fine, but I've noticed that it doesn't seem to cut down the total time taken very much at all. I'm assuming this is because the I/O operation takes so much longer than the simulation itself.</p>
<p>I'm wondering if I should have each thread insert it's own results into the database, but I'm not sure if this will speed things up since presumably the MySQL database can only handle one query at a time anyway (and the database server is on the same machine)?</p>
<p>Would this speed things up or not? And is there anything I can do to speed up the INSERTs, perhaps on the server side?</p>


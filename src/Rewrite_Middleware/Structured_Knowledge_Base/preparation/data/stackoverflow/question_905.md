# Parallel job execution with split-and-aggregate in Java
[Link to question](https://stackoverflow.com/questions/49104126/parallel-job-execution-with-split-and-aggregate-in-java)
**Creation Date:** 1520228549
**Score:** 0
**Tags:** java, multithreading, jobs
## Question Body
<p>We are working on rewrite of an existing application, and need support for high number of read/write to database. For this, we are proceeding with sharding on MySQL. Since we are allowing bulk APIs for read/write, this would mean parallel execution of queries on different shards.</p>

<p>Can you suggest frameworks which would support the same in Java, mainly focussing on split-and-aggregate jobs. Basically I will define two interfaces ReadTask and WriteTask, and implementation of these tasks will be jobs and they would be submitted as a list for parallel execution.</p>

<p>I might not have termed this question in the right way, but I hope you got the context from the description. Let me know if there is any info needed for answer.</p>

## Answers
### Answer ID: 49106367
<p>You can use the <a href="https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ThreadPoolExecutor.html" rel="nofollow noreferrer">ThreadPoolExecutor</a> &amp; <a href="https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/Executors.html" rel="nofollow noreferrer">Executors</a>(factory) in Java to create Thread pools to which you can submit your read &amp; write tasks. It allows for Runnable &amp; Callable based on your situation.</p>

### Answer ID: 49104210
<p>BLUF: This sounds like a common processing pattern in <a href="https://akka.io" rel="nofollow noreferrer">Akka</a>.</p>

<p>This sounds like a Scatter-Gather patterned API.</p>

<p>If you have 1 job, you should first answer if that job will touch only one shard or more? If it will touch many shards you may choose to reject it (allowing only single-shard actions) or you may choose to break it up (scatter) it across other workers.</p>

<p>Akka gives you APIs, especially the Streaming API, that talk about this style of work. Akka is best expressed in Scala, but it has a Java API that gives you all the functionality of the Scala one. That you are talking about "mapping" and "reducing" (or "folding") data, these are functional operations and Scala gives you the functional idioms.</p>

<p>If you scatter it across other workers, you'll need to communicate the manifest of jobs to the gather side of the system.</p>

<p>Hope that's helpful.</p>


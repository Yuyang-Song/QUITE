# Asynchronous database/service calls in PHP: Gearman vs. pthreads
[Link to question](https://stackoverflow.com/questions/33219294/asynchronous-database-service-calls-in-php-gearman-vs-pthreads)
**Creation Date:** 1445271529
**Score:** 4
**Tags:** php, mysql, apache, asynchronous, gearman
## Question Body
<p>On our LAMP site, we have a problem with some services having to make several calls to the database to pull data. Usually the way this is done in PHP (at least my experience) is serially; which obviously is inefficient. We can mitigate some of the inefficiencies by using caching and aggregating some queries; but in some cases we need to still need to do multiple db calls.</p>

<p>Ideally, I would just send as many as requests as possible to the db or web services at the same time asynchronously, but PHP doesn't seem to support that pattern out of the box. These are the workarounds I know about to accomplish this.</p>

<p>We currently use Gearman to take care of asynchronous tasks. I could rewrite some our services as Gearman tasks and use that to make async calls to the db and services. However, we've had bad experiences with Gearman eating up a lot of processes and memory; forcing use to restart our production servers on some occasions as they become unresponsive. However, I believe I was able to trace this issue due to some errors in the scripts and believe I have it fixed. But I feel this instability and excessive resource consumption may rear its head again if we use Gearman as a task pool/manager for processing async tasks.</p>

<p>Alternatively, I was looking at pthreads. It seemed like a better alternative as it didn't require having a running Gearman daemon to work, and it accomplished what I wanted. There even seemed to be a decent framework over it, amphp. We decided to configured a test server with pthreads enabled. However, what we didn't know was pthreads required changing our Apache config, specifically going to httpd.worker from httpd(aka prefork). Admittedly, I'm not an experienced Apache admin, so I'm not even sure what the ramifications of making this change will be. Because of this, now I'm hesitant to use it, at least until I have time to research this some more.</p>

<p>So my question is, if I wanted to do asynchronous requests in PHP, should I stick with Gearman knowing I may run into issues, or should I risk it and go with pthreads, even though it seems to require changes to our Apache configuration that I quite frankly don't know how it will affect our site? Or maybe, there is perhaps another option for what I'm trying to do that I just don't know about yet.</p>

<p>Server config:</p>

<ul>
<li>PHP 5.6.1</li>
<li>Apache 2.4.12</li>
<li>Red Hat Enterprise 6.3</li>
<li>MySQL 5.5.28</li>
<li>8GB RAM</li>
</ul>

## Answers
### Answer ID: 33219584
<p>Firstly, there is a deep confusion going on here between asynchronous and parallel concurrency.</p>

<p>Asynchronous execution means that instructions for individual tasks are interleaved, such that the tasks run concurrently <em>with respect to each other</em>.</p>

<p>Parallel execution means that the instructions for individual tasks are executed in parallel, such that they run concurrently <em>with respect to time</em>.</p>

<p>You can find a more complete explanation of asynchronous and parallel concurrency, with pretty pictures <a href="http://blog.krakjoe.ninja/2015/07/the-universe-is-not-aware.html" rel="noreferrer">here</a>.</p>

<p>Gearmans multi-processing model allows parallel execution, as does pthreads.</p>

<p>When you say asynchronous execution is not well supported in PHP, this is wrong.</p>

<p>It's wrong because asynchronous execution is not something that requires language support to achieve. Just interleaving instructions is not that complicated, <a href="https://3v4l.org/gNmQg" rel="noreferrer">here</a> is an example that will work on any version of PHP that we need to care about.</p>

<p>Interleaving instructions like this makes a mess of code, and is really only worth it in the case of non-blocking I/O. In this case, interleaved instructions allow you to eliminate waiting, by executing the instructions for another task when synchronous blocking code would have forced you to wait. This reduces the total execution time.</p>

<p>Modern versions of PHP do have facilities (generators) to make this much nicer, and as you already know, many frameworks exist to abstract away as much difficulty as possible.</p>

<p>Now, we come onto using pthreads in the frontend of your web server. In the latest versions of pthreads, this is disabled by force. There is no good reason, and no good time to create (real, kernel) threads at the frontend of a web application, it will never make sense.</p>

<p>For more detail on that decision, read <a href="http://blog.krakjoe.ninja/2015/09/the-worth-of-advice.html" rel="noreferrer">this</a>.</p>

<p>So, looking forward, your intended usage is out of the question.</p>

<p>Nothing would give me more pleasure than to say <code>pthreads' got this</code>, but it wouldn't be true I don't think. I think you are focusing on the wrong kind of optimizations.</p>

<p>If there is a problem with your database schema or server, then solve that problem. If you need to make multiple requests to external API's then take the simplest route possible; asynchronous non-blocking I/O.</p>

<p>Throwing threads, in the form of gearman or pthreads at any particular task is only guaranteed to do one thing; <strong>make it more complex</strong>.</p>


# How can I make an SQL query thread start, then do other work before getting results?
[Link to question](https://stackoverflow.com/questions/3974746/how-can-i-make-an-sql-query-thread-start-then-do-other-work-before-getting-resu)
**Creation Date:** 1287548681
**Score:** 6
**Tags:** mysql, multithreading, delphi, scheduling
## Question Body
<p>I have a program that does a limited form of multithreading.  It is written in Delphi, and uses libmysql.dll (the C API) to access a MySQL server.  The program must process a long list of records, taking ~0.1s per record.  Think of it as one big loop.  All database access is done by worker threads which either prefetch the next records or write results, so the main thread doesn't have to wait.</p>

<p>At the top of this loop, we first wait for the prefetch thread, get the results, then have the prefetch thread execute the query for the next record.  The idea being that the prefetch thread will send the query immediately, and wait for results while the main thread completes the loop.  </p>

<p>It often does work that way.  But note there's nothing to ensure that the prefetch thread runs right away.  I found that often the query was not sent until the main thread looped around and started waiting for the prefetch.</p>

<p>I sort-of fixed that by calling sleep(0) right after launching the prefetch thread.  This way the main thread surrenders the remainder of it's time slice, hoping that the prefetch thread will now run, sending the query.  Then <em>that</em> thread will sleep while waiting, which allows the main thread to run again.<br>
Of course, there's plenty more threads running in the OS, but this did actually work to some extent.</p>

<p>What I really want to happen is for the main thread to send the query, and then have the worker thread wait for the results.  Using libmysql.dll I call </p>

<pre><code>result := mysql_query(p.SqlCon,pChar(p.query));
</code></pre>

<p>in the worker thread.  Instead, I'd like to have the main thread call something like </p>

<pre><code>mysql_threadedquery(p.SqlCon,pChar(p.query),thread);
</code></pre>

<p>which would hand off the task as soon as the data went out.</p>

<p>Anybody know of anything like that?  </p>

<p>This is really a scheduling problem, so I could try is lauching the prefetch thread at a higher priority, then have it reduce its priority after the query is sent.  But again, I don't have any mysql call that separates sending the query from receiving the results.</p>

<p>Maybe it's in there and I just don't know about it.  Enlighten me, please.</p>

<p>Added Question:</p>

<p>Does anyone think this problem would be solved by running the prefetch thread at a higher priority than the main thread?  The idea is that the prefetch would immediately preempt the main thread and send the query.  Then it would sleep waiting for the server reply.  Meanwhile the main thread would run.</p>

<p>Added: Details of current implementation</p>

<p>This program performs calculations on data contained in a MySQL DB.  There are 33M items with more added every second.  The program runs continuously, processing new items, and sometimes re-analyzing old items.  It gets a list of items to analyze from a table, so at the beginning of a pass (current item) it knows the next item ID it will need.</p>

<p>As each item is independent, this is a perfect target for multiprocessing.  The easiest way to do this is to run multiple instances of the program on multiple machines.  The program is highly optimized via profiling, rewrites, and algorithm redesign.  Still, a single instance utilizes 100% of a CPU core when not data-starved.  I run 4-8 copies on two quad-core workstations.  But at this rate they must spend time waiting on the MySQL server.  (Optimization of the Server/DB schema is another topic.)</p>

<p>I implemented multi-threading in the process solely to avoid blocking on the SQL calls.  That's why I called this "limited multi-threading".  A worker thread has one task: send a command and wait for results.  (OK, two tasks.)</p>

<p>It turns out there are 6 blocking tasks associated with 6 tables.  Two of these read data and the other 4 write results.  These are similar enough to be defined by a common Task structure.  A pointer to this Task is passed to a threadpool manager which assigns a thread to do the work.  The main thread can check the task status through the Task structure.</p>

<p>This makes the main thread code very simple.  When it needs to perform Task1, it waits for Task1 to be not busy, puts the SQL command in Task1 and hands it off.  When Task1 is no longer busy, it contains the results (if any).</p>

<p>The 4 tasks that write results are trivial.  The main thread has a Task write records while it goes on to the next item.  When done with that item it makes sure the previous write finished before starting another.</p>

<p>The 2 reading threads are less trivial.  Nothing would be gained by passing the read to a thread and then waiting for the results.  Instead, these tasks prefetch data for the next item.  So the main thread, coming to this blocking tasks, checks if the prefetch is done; Waits if necessary for the prefetch to finish, then takes the data from the Task.  Finally, it reissues the Task with the NEXT Item ID.  </p>

<p>The idea is for the prefetch task to immediately issue the query and wait for the MySQL server.  Then the main thread can process the current Item and by the time it starts on the next Item the data it needs is in the prefetch Task.</p>

<p>So the threading, a thread pool, the synchronization, data structures, etc. are all done.  And that all works.  What I'm left with is a Scheduling Problem.</p>

<p>The Scheduling Problem is this:  All the speed gain is in processing the current Item while the server is fetching the next Item.  We issue the prefetch task before processing the current item, but how do we guarantee that it starts?  The OS scheduler does not know that it's important for the prefetch task to issue the query right away, and then it will do nothing but wait.</p>

<p>The OS scheduler is trying to be "fair" and allow each task to run for an assigned time slice.  My worst case is this:  The main thread receives its slice and issues a prefetch, then finishes the current item and must wait for the next item.  Waiting releases the rest of its time slice, so the scheduler starts the prefetch thread, which issues the query and then waits.  Now both threads are waiting.  When the server signals the query is done the prefetch thread restarts, and requests the Results (dataset) then sleeps.  When the server provides the results the prefetch thread awakes, marks the Task Done and terminates.  Finally, the main thread restarts and takes the data from the finished Task.</p>

<p>To avoid this worst-case scheduling I need some way to ensure that the prefetch query is issued before the main thread goes on with the current item.  So far I've thought of three ways to do that:</p>

<ol>
<li><p>Right after issuing the prefetch task, the main thread calls Sleep(0).  This should relinquish the rest of its time slice.  I then <em>hope</em> that the scheduler runs the prefetch thread, which will issue the query and then wait.  Then the scheduler should restart the main thread (I hope.)  As bad as it sounds, this actually works better than nothing.</p></li>
<li><p>I could possibly issue the prefetch thread at a higher priority than the main thread.  That should cause the scheduler to run it right away, even if it must preempt the main thread.  It may also have undesirable effects.  It seems unnatural for a background worker thread to get a higher priority.</p></li>
<li><p>I could possibly issue the query asynchronously.  That is, separate sending the query from receiving the results.  That way I could have the main thread send the prefetch using mysql_send_query (non blocking) and go on with the current item.  Then when it needed the next item it would call mysql_read_query, which would block until the data is available.  </p></li>
</ol>

<p>Note that solution 3 does not even use a worker thread.  This looks like the best answer, but requires a rewrite of some low-level code.  I'm currently looking for examples of such asynchronous client-server access.  </p>

<p>I'd also like any experienced opinions on these approaches.  Have I missed anything, or am I doing anything wrong?  Please note that this is all working code.  I'm not asking how to do it, but how to do it better/faster.</p>

## Answers
### Answer ID: 4010736
<p>I'm putting in a second answer, for your second part of the question: your <strong>Scheduling Problem</strong>
This makes it easier to distinguish both answers.</p>
<p>First of all, you should read <a href="https://devblogs.microsoft.com/oldnewthing/2005/10/04" rel="nofollow noreferrer">Consequences of the scheduling algorithm: Sleeping doesn't always help</a> which is part of <a href="https://news.microsoft.com/life/" rel="nofollow noreferrer">Raymond Chen</a>'s blog &quot;<a href="https://devblogs.microsoft.com/oldnewthing/" rel="nofollow noreferrer">The Old New Thing</a>&quot;.<br />
<a href="https://devblogs.microsoft.com/oldnewthing/2009/07/27" rel="nofollow noreferrer">Sleeping versus polling</a> is also good reading.<br />
Basically <a href="http://www.google.com/search?q=sleep+thread+site:blogs.msdn.com/b/oldnewthing" rel="nofollow noreferrer">all these</a> make good reading.</p>
<p>If I understand your Scheduling Problem correctly, you have 3 kinds of threads:</p>
<ol>
<li>Main Thread: makes sure the Fetch Threads always have work to do</li>
<li>Fetch Threads: (database bound) fetch data for the Processing Threads</li>
<li>Processing Threads: (CPU bound) process fetched data</li>
</ol>
<p>The only way to keep 3 running is to have 2 fetch as much data as they can.<br />
The only way to keep 2 fetching, is to have 1 provide them enough entries to fetch.</p>
<p>You can use queues to communicate data between 1 and 2 and between 2 and 3.</p>
<p>Your problem now is two-fold:</p>
<ul>
<li>finding the balance between the number of threads in category 2 and 3</li>
<li>making sure that 2 always have work to do</li>
</ul>
<p>I think you have solved the former.<br />
The latter comes down to making sure the queue between 1 and 2 is never empty.</p>
<p>A few tricks:</p>
<ul>
<li>You can use Sleep(1) (see the blog article) as a simple way to &quot;force&quot; 2 to run</li>
<li>Never let the treads exit their execute: creating and destroying threads is expensive</li>
<li>choose your synchronization objects (often called IPC objects) carefully (<a href="https://web.archive.org/web/20161015002148/http://www.kudzuworld.com:80/bio.en.aspx" rel="nofollow noreferrer">Kudzu</a> has a <a href="https://web.archive.org/web/20160421161631/http://www.kudzuworld.com:80/Articles/AdvancedIPC/index.en.aspx" rel="nofollow noreferrer">nice article</a> on them)</li>
</ul>
<p>--jeroen</p>

### Answer ID: 4012510
<blockquote>
  <p>Still, a single instance utilizes 100% of a CPU core when not data-starved. I run 4-8 copies on two quad-core workstations.</p>
</blockquote>

<p>I have a conceptual problem here. In your situation I would either create a multi-process solution, with each process doing everything in its single thread, or I would create a multi-threaded solution that is limited to a single instance on any particular machine. Once you decide to work with multiple threads and accept the added complexity and probability of hard-to-fix bugs, then you should make maximum use of them. Using a single process with multiple threads allows you to employ varying numbers of threads for reading from and writing to the database and to process your data. The number of threads may even change during the runtime of your program, and the ratio of database and processing threads may too. This kind of dynamic partitioning of the work is only possible if you can control all threads from a single point in the program, which isn't possible with multiple processes.</p>

<blockquote>
  <p>I implemented multi-threading in the process solely to avoid blocking on the SQL calls.</p>
</blockquote>

<p>With multiple processes there wouldn't be a real need to do so. If your processes are I/O-bound some of the time they don't consume CPU resources, so you probably simply need to run more of them than your machine has cores. But then you have the problem to know how many processes to spawn, and that may again change over time if the machine does other work too. A threaded solution in a single process can be made adaptable to a changing environment in a relatively simple way.</p>

<blockquote>
  <p>So the threading, a thread pool, the synchronization, data structures, etc. are all done. And that all works. What I'm left with is a Scheduling Problem.</p>
</blockquote>

<p>Which you should leave to the OS. Simply have a single process with the necessary pooled threads. Something like the following:</p>

<ul>
<li><p>A number of threads reads records from the database and adds them to a producer-consumer queue with an upper bound, which is somewhere between <em>N</em> and <em>2*N</em> where <em>N</em> is the number of processor cores in the system. These threads will block on the full queue, and they can have increased priority, so that they will be scheduled to run as soon as the queue has more room and they become unblocked. Since they will be blocked on I/O most of the time their higher priority shouldn't be a problem.<br>
I don't know what that number of threads is, you would need to measure.</p></li>
<li><p>A number of processing threads, probably one per processor core in the system. They will take work items from the queue mentioned in the previous point, on block on that queue if it's empty. Processed work items should go to another queue.</p></li>
<li><p>A number of threads that take processed work items from the second queue and write data back to the database. There should probably an upper bound for the second queue as well, to make it so that a failure to write processed data back to the database will not cause processed data to pile up and fill all your process memory space.</p></li>
</ul>

<p>The number of threads needs to be determined, but all scheduling will be performed by the OS scheduler. The key is to have enough threads to utilise all CPU cores, and the necessary number of auxiliary threads to keep them busy and deal with their outputs. If these threads come from pools you are free to adjust their numbers at runtime too.</p>

<p>The <a href="http://otl.17slon.com/" rel="nofollow noreferrer">Omni Thread Library</a> has a solution for tasks, task pools, producer consumer queues and everything else you would need to implement this. Otherwise you can write your own queues using mutexes.</p>

<blockquote>
  <p>The Scheduling Problem is this: All the speed gain is in processing the current Item while the server is fetching the next Item. We issue the prefetch task before processing the current item, but how do we guarantee that it starts?</p>
</blockquote>

<p>By giving it a higher priority.</p>

<blockquote>
  <p>The OS scheduler does not know that it's important for the prefetch task to issue the query right away</p>
</blockquote>

<p>It will know if the thread has a higher priority.</p>

<blockquote>
  <p>The OS scheduler is trying to be "fair" and allow each task to run for an assigned time slice.</p>
</blockquote>

<p>Only for threads of the same priority. No lower priority thread will get any slice of CPU while a higher priority thread in the same process is runnable.<br>
<em>[Edit: That's not completely true, more information at the end. However, it is close enough to the truth to ensure that your higher priority network threads send and receive data as soon as possible.]</em></p>

<blockquote>
  <ol>
  <li>Right after issuing the prefetch task, the main thread calls Sleep(0).</li>
  </ol>
</blockquote>

<p>Calling <code>Sleep()</code> is a bad way to force threads to execute in a certain order. Set the thread priority according to the priority of the work they perform, and use OS primitives to block higher priority threads if they should not run.</p>

<blockquote>
  <p>I could possibly issue the prefetch thread at a higher priority than the main thread. That should cause the scheduler to run it right away, even if it must preempt the main thread. It may also have undesirable effects. It seems unnatural for a background worker thread to get a higher priority.</p>
</blockquote>

<p>There is nothing unnatural about this. It is the intended way to use threads. You only must make sure that higher priority threads block sooner or later, and any thread that goes to the OS for I/O (file or network) does block. In the scheme I sketched above the high priority threads will also block on the queues.</p>

<blockquote>
  <p>I could possibly issue the query asynchronously.</p>
</blockquote>

<p>I wouldn't go there. This technique may be necessary when you write a server for many simultaneous connections and a thread per connection is prohibitively expensive, but otherwise blocking network access in a threaded solution should work fine.</p>

<p><strong>Edit:</strong></p>

<p>Thanks to Jeroen Pluimers for the poke to look closer into this. As the information in the links he gave in his comment shows my statement</p>

<blockquote>
  <p>No lower priority thread will get any slice of CPU while a higher priority thread in the same process is runnable.</p>
</blockquote>

<p>is not true. Lower priority threads that haven't been running for a long time get a random priority boost and will indeed sooner or later get a share of CPU, even though higher priority threads are runnable. For more information about this see in particular <a href="http://support.microsoft.com/kb/96418" rel="nofollow noreferrer">"Priority Inversion and Windows NT Scheduler"</a>.</p>

<p>To test this out I created a simple demo with Delphi:</p>

<pre><code>type
  TForm1 = class(TForm)
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Timer1: TTimer;
    procedure FormCreate(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
  private
    fLoopCounters: array[0..5] of LongWord;
    fThreads: array[0..5] of TThread;
  end;

var
  Form1: TForm1;

implementation

{$R *.DFM}

// TTestThread

type
  TTestThread = class(TThread)
  private
    fLoopCounterPtr: PLongWord;
  protected
    procedure Execute; override;
  public
    constructor Create(ALowerPriority: boolean; ALoopCounterPtr: PLongWord);
  end;

constructor TTestThread.Create(ALowerPriority: boolean;
  ALoopCounterPtr: PLongWord);
begin
  inherited Create(True);
  if ALowerPriority then
    Priority := tpLower;
  fLoopCounterPtr := ALoopCounterPtr;
  Resume;
end;

procedure TTestThread.Execute;
begin
  while not Terminated do
    InterlockedIncrement(PInteger(fLoopCounterPtr)^);
end;

// TForm1

procedure TForm1.FormCreate(Sender: TObject);
var
  i: integer;
begin
  for i := Low(fThreads) to High(fThreads) do
//    fThreads[i] := TTestThread.Create(True, @fLoopCounters[i]);
    fThreads[i] := TTestThread.Create(i &gt;= 4, @fLoopCounters[i]);
end;

procedure TForm1.FormDestroy(Sender: TObject);
var
  i: integer;
begin
  for i := Low(fThreads) to High(fThreads) do begin
    if fThreads[i] &lt;&gt; nil then
      fThreads[i].Terminate;
  end;
  for i := Low(fThreads) to High(fThreads) do
    fThreads[i].Free;
end;

procedure TForm1.Timer1Timer(Sender: TObject);
begin
  Label1.Caption := IntToStr(fLoopCounters[0]);
  Label2.Caption := IntToStr(fLoopCounters[1]);
  Label3.Caption := IntToStr(fLoopCounters[2]);
  Label4.Caption := IntToStr(fLoopCounters[3]);
  Label5.Caption := IntToStr(fLoopCounters[4]);
  Label6.Caption := IntToStr(fLoopCounters[5]);
end;
</code></pre>

<p>This creates 6 threads (on my 4 core machine), either all with lower priority, or 4 with normal and 2 with lower priority. In the first case all 6 threads run, but with wildly different shares of CPU time:</p>

<p><img src="https://i.sstatic.net/vCk8X.png" alt="6 threads with lower priority"></p>

<p>In the second case 4 threads run with roughly equal share of CPU time, but the other two threads get a little share of the CPU as well:</p>

<p><img src="https://i.sstatic.net/OvEFj.png" alt="4 threads with normal, 2 threads with lower priority"></p>

<p>But the share of CPU time is very very small, way below a percent of what the other threads receive.</p>

<p>And to get back to your question: A program using multiple threads with custom priority, coupled via producer-consumer queues, should be a viable solution. In the normal case the database threads will block most of the time, either on the network operations or on the queues. And the Windows scheduler will make sure that even a lower priority thread will not completely starve to death.</p>

### Answer ID: 3977337
<p>I don't know any database access layer that permits this.</p>

<p>The reason is that each thread has its own "<a href="http://en.wikipedia.org/wiki/Thread-local_storage" rel="nofollow noreferrer">thread local storage</a>" (The <code>threadvar</code> keyword in Delphi, other languages have equivalents, it is used in a lot of frameworks).<br>
When you start things on one thread, and continue it on another, then you get these local storages mixed up causing all sorts of havoc.</p>

<p>The best you can do is this:</p>

<ol>
<li>pass the query and parameters to the thread that will handle this (use the standard Delphi thread synchronization mechanisms for this)</li>
<li>have the actual query thread perform the query</li>
<li>return the results to the main thread (use the standard Delphi thread synchronization mechanisms for this)</li>
</ol>

<p>The answers to <a href="https://stackoverflow.com/questions/1806339/is-it-better-to-use-tthreads-synchronize-or-use-window-messages-for-ipc-betwee">this question</a> explains thread synchronization in more detail.</p>

<p><strong>Edit:</strong> (on presumed slowness of starting something in an other thread)</p>

<p>"Right away" is a relative term: it depends in how you do your thread synchronization and can be very very fast (i.e. less than a millisecond).<br>
Creating a new thread might take some time.<br>
The solution is to have a threadpool of worker threads that is big enough to service a reasonable amount of requests in an efficient manner.<br>
That way, if the system is not yet too busy, you will have a worker thread ready to start servicing your request almost immediately.  </p>

<p>I have done this (even cross process) in a big audio application that required low latency response, and it works like a charm.<br>
The audio server process runs at high priority waiting for requests. When it is idle, it doesn't consume CPU, but when it receives a request it responds really fast.</p>

<p>The answers to <a href="https://stackoverflow.com/questions/373449/what-simple-changes-made-the-biggest-improvements-to-your-delphi-programs">this question on changes with big improvements</a> and <a href="https://stackoverflow.com/questions/438945/cross-thread-communication-in-delphi">this question on cross thread communication</a> provide some interesting tips on how to get this asynchronous behaviour working.<br>
Look for the words <code>AsyncCalls</code>, <code>OmniThread</code> and <code>thread</code>.</p>

<p>--jeroen</p>

### Answer ID: 3975204
<p>You just have to use the standard Thread synchronization mechanism of the Delphi threading.</p>

<p>Check your IDE help for TEvent class and its associated methods.</p>


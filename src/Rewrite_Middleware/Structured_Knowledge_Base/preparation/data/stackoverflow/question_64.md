# c# parallel programming for several methods
[Link to question](https://stackoverflow.com/questions/11603422/c-parallel-programming-for-several-methods)
**Creation Date:** 1342986070
**Score:** 1
**Tags:** c#
## Question Body
<p>I have a method that looks like this:</p>

<pre><code>public void SomeMethodThatLoadsUserData()
{
   Method1();
   Method2();
   Method3();
   .....
   Method12();
}
</code></pre>

<p>These get executed when the user logs on and each method fetches some data related to the user. I was wondering if making these run in parallel would have any performance benefit because each method ends up calling a query to the same database file. And, if there would be a performance benefit, how would I rewrite this code?</p>

<p>Thanks for your suggestions.</p>

## Answers
### Answer ID: 11604127
<p>The following code demonstrates a parallel test using a list of Thread and Stopwatch objects. I think this is pretty good method to test with because it guarantees a parallel execution attempt (unlike Parallel.Invoke) and it's easier to set up than using the ThreadPool IMO.</p>

<pre><code>public static void SomeMethodThatLoadsUserData()
{
    Stopwatch s = new Stopwatch();
    s.Start();

    List&lt;Thread&gt; threads = new List&lt;Thread&gt; {new Thread(Method1), new Thread(Method2)};

    foreach (Thread thread in threads)
    {
        thread.Start();
    }

    foreach (Thread thread in threads)
    {
        thread.Join();
    }

    s.Stop();
    Console.WriteLine("Total: {0} ms", s.ElapsedMilliseconds);

    Console.ReadKey();
}

private static void Method1()
{
    Stopwatch s = new Stopwatch();
    s.Start();
    // do work
    Thread.Sleep(1000);
    s.Stop();
    Console.WriteLine("Method 1: {0} ms", s.ElapsedMilliseconds);
}

private static void Method2()
{
    Stopwatch s = new Stopwatch();
    s.Start();
    // do work
    Thread.Sleep(1000);
    s.Stop();
    Console.WriteLine("Method 2: {0} ms", s.ElapsedMilliseconds);
}
</code></pre>

<p>Output:</p>

<pre><code>Method 1: 999 ms
Method 2: 999 ms
Total: 1051 ms
</code></pre>

<p>Any time saving will show up when (hopefully) <code>Total</code> is less than the sum of each method.</p>

### Answer ID: 11603468
<p>I don't know if this is the fastest or the best way of doing it but you could spin each method off to a new thread.</p>

<pre><code>Thread t = new Thread(() =&gt; Method1());
t.Start();
</code></pre>


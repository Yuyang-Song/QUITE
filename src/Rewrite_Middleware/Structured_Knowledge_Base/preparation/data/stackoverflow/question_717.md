# Multiprocessing, having issues
[Link to question](https://stackoverflow.com/questions/38654999/multiprocessing-having-issues)
**Creation Date:** 1469783784
**Score:** 1
**Tags:** python, pathos
## Question Body
<p>I'm a fairly novice programmer and I'm putting my hand to multiprocessing for the first time. After running into the usual pickling errors I searched here and found Pathos was likely the best thing to use.</p>

<p>The point of the application in full is it connects to a collection of servers with ssh, pulls data out and stores it into a database. It works great, but it would obviously be beneficial if it ran multiprocessing.</p>

<p>The original function call looks like this:</p>

<pre><code>    devices = sq.sqlOperation("SELECT * from Devices")
    for device in devices:
            pullNewData(device) 
</code></pre>

<p>In short, the SQL query gives me a list of dictionaries, I feed pullNewData() a dictionary for each record, it goes, connects, pulls everything through and updates the database.</p>

<p>I'd rather not rewrite a few thousand lines of code, so I'm hoping adapting it will be easy:
All of the following examples have:</p>

<pre><code>from pathos.multiprocessing import ProcessingPool as Pool
</code></pre>

<p>At the top. I've tried:</p>

<pre><code>    devices = sq.sqlOperation("SELECT * from Devices")
    p = Pool(4)
    p.apipe(pullNewData, devices) 
</code></pre>

<p>Which silently failed, even with a try/except round it</p>

<pre><code>    devices = sq.sqlOperation("SELECT * from Devices")
    p = Pool(4)
    p.map(pullNewData, devices) 
</code></pre>

<p>Same, silent fail:</p>

<p>However:</p>

<pre><code>    devices = sq.sqlOperation("SELECT * from Devices")
    p = Pool(4)
    for data in devices:
        p.apipe(pullNewData(data))
</code></pre>

<p>worked but just went through each one serially.</p>

<p>In my desperation I even tried putting it inside a list comprehension (which, yes, is horribly ugly, but at that point I'd have done anything)</p>

<pre><code>    devices = sq.sqlOperation("SELECT * from Devices")
    p = Pool(4)
    [ p.apipe(pullNewData(data)) for data in devices ]
</code></pre>

<p>So, how Would I do this?
How would I have it fire off a new connection for each record in a parallel fashion?</p>

## Answers
### Answer ID: 38658400
<p>So trying <code>Pool(1)</code> showed me what issues it was having. I was calling other functions within both this file and other files which, due to the function being an entirely new process it had no idea about, so I had to put import statements for both the other modules and issue a</p>

<pre><code>from thisModule import thisFunction
</code></pre>

<p>for other functions in the same file. Then after that I upped the pool and it worked perfectly using:</p>

<pre><code>devices = sq.sqlOperation("SELECT * from Devices")
p = Pool(4)
p.map(pullNewData, devices)
</code></pre>

<p>Thanks, this was extremely helpful and very much a learning experience for me.</p>

<p>It hadn't twigged to me that the new process wouldn't be aware of the import statements in the file that the function lived in, or the other functions. Oh well. Thanks very much to thebjorn for pointing me in the right direction.</p>


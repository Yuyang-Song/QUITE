# Why do a small amount of add/deletes take several seconds in EF4?
[Link to question](https://stackoverflow.com/questions/4522697/why-do-a-small-amount-of-add-deletes-take-several-seconds-in-ef4)
**Creation Date:** 1293140954
**Score:** 0
**Tags:** c#, performance, entity-framework-4, code-first
## Question Body
<p>Using the Entity Framework 4. I have created a Code First database in the past and a piece of code needs to delete and add 16 objects, this takes 6 seconds each. That's 300+ ms for each query!</p>

<p>The deletes/adds occur in a <code>foreach</code> scope and there is a <code>SaveChanges()</code> outside the <code>foreach</code>.</p>

<p><img src="https://i.sstatic.net/o6t1N.png" alt="alt text"></p>

<p>In the above image you see that each takes 6 seconds, which is 34% of the time, for 16 calls.</p>

<p>That doesn't sound normal to me... <strong>Why is this and how can I improve the performance?</strong>  </p>

<p>If there is no solution: Are there any workarounds I can use? It would be a pain to rewrite my project...</p>

## Answers
### Answer ID: 4522779
<p>I'd advise you to try something like <a href="http://efprof.com/" rel="nofollow">EF Profiler</a>. I think there's a free trial, which allows you to try it out. Basically, with it you can see what kind of things are happening internally with your EF app.</p>

<p>Another point to note: Is this by chance a web application? In my own project I found that when I ran the app in Cassini (built-in visual studio webserver) things were pretty slow. Moving over to IIS 7 suddenly made everything a hell of a lot faster. It's not hard to do either, provided you have IIS installed.
Simply go to the properties of your web project, go to the 'Web' tab and toggle 'Use Local IIS Web server'. It will also allow you to create a virtual directory from here, so there's no need for managing IIS directly.</p>

<p>Other than that, I don't think there's much to be said about your problem, as we don't have any sample code. It could be that your 16 objects actually produce a lot of queries, because of related entities or something. EF Profiler will show that though.</p>

<hr>

<p>Addition:
Another thing to be aware of is that EF isn't really meant for bulk actions. IF you need to do a lot of updating/deleting/inserting at once you'd be better off with something else I think.</p>

<p>I know 16 entities is not bulk (yet), but I figured I'd put this little notion in here anyway.</p>


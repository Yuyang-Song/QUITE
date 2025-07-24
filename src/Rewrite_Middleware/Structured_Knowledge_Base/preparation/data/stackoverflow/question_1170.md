# Distinct in LINQ and change result type
[Link to question](https://stackoverflow.com/questions/61802462/distinct-in-linq-and-change-result-type)
**Creation Date:** 1589473643
**Score:** 0
**Tags:** c#, entity-framework, linq, entity-framework-core
## Question Body
<p>I am trying to get a list of distinct items from a database. 
I want the result to be in a list of CarMakes, which has only one property called Make.</p>

<p>I can get the following items to work in LINQPad, but when I try to get it working in C#.  I get the following error </p>

<p>"  <em>.First()' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable()</em>,"</p>

<pre><code>var result = await _context.Cars
              .GroupBy(x =&gt; x.Make)
              .Select(x =&gt;   x.First().Make  )
              .ToListAsync();
</code></pre>

<p>I have tried the following, which can all the makes, but its not distinct.</p>

<pre><code>var result = await _context.Cars
                .Select(x =&gt; new CarMakes() { Assembly =  x.Assembly })
                .ToListAsync();
</code></pre>

<p>The Car table has the following columns,  Id, Colour, Make, Model, Registration </p>

<p>I tried using MORELinq but couldnt get that working to</p>

## Answers
### Answer ID: 61812513
<p>Could you try running the code below:</p>

<pre><code>var result = await _context.Cars
              .GroupBy(x =&gt; x.Make)
              .Select(x =&gt;   x.Key  )
              .ToListAsync();
</code></pre>

<p>Hope it helps! :)</p>

### Answer ID: 61802754
<p>Try this:</p>

<pre><code>var result = await _context.Cars.Select(c =&gt; c.Make).Distinct()
                .Select(m =&gt; new CarMakes { Assembly = m })
                .ToListAsync();
</code></pre>


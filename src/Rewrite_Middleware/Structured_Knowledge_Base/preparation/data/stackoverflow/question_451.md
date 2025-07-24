# Performance of nested for loops vs Array functions in Javascript
[Link to question](https://stackoverflow.com/questions/26811628/performance-of-nested-for-loops-vs-array-functions-in-javascript)
**Creation Date:** 1415402035
**Score:** 3
**Tags:** javascript, node.js, performance, functional-programming
## Question Body
<p>I wrote a small block of code yesterday that uses two for loops to compare objects in two arrays(the arrays are the same though).</p>
<pre><code>var result = []
for (var i = 0; i &lt; res.length; i++) {
    var tempObj = {}
    tempObj.baseName = res[i].name
    tempObj.cnt = res[i].cnt
    tempObj.matches = []
    for (var j = 0; j &lt; compareArr.length; j++) {
        if(natural.LevenshteinDistance(res[i].name, compareArr[j].name) === options.distance) {
            tempObj.matches.push(compareArr[j])
        }
    }
    if (tempObj.matches.length &gt; 0) {
        result.push(tempObj)
    }
}
</code></pre>
<p>However, I have been on a functional programming kick the last few months and decided rewrite the code block using a more functional approach and ended up with this:</p>
<pre><code>var result = res.
    map(function(baseItem) {
        baseItem.matches = compareArr.
            reduce(function(acc, compItem) {
                if(natural.LevenshteinDistance(baseItem.name, compItem.name) === options.distance) {
                    acc.push(compItem)
                }
                return acc
            }, [])
            return baseItem
        }).
        filter(function(item) {
          return item.matches.length &gt; 0
        })
</code></pre>
<p>My route felt like it was responding a bit slower however, the data being iterated over is the result of a database query that may contain 10s of thousands of items and I wanted to make sure I wasn't about to hurt the performance of the server for no reason.  So, I plugged the functions into jsperf, and <a href="http://jsperf.com/forvsfunc" rel="nofollow noreferrer">the results</a> were saddening. The for loops run at about 2,600 ops/sec, while the second block runs at about 500 ops/sec. :(</p>
<p>The question is, is my second block poorly written, can it be improved and brought up to speed?  If not, is this normal?  I see more and more people pushing functional style javascript.</p>
<p>Am I hurting performance in the name of style?  Should I enjoy learning functional languages and just leave it out of my javascript?</p>
<p><a href="http://jhusain.github.io/learnrx/" rel="nofollow noreferrer">http://jhusain.github.io/learnrx/</a></p>
<p><a href="https://github.com/timoxley/functional-javascript-workshop" rel="nofollow noreferrer">https://github.com/timoxley/functional-javascript-workshop</a></p>
<p><a href="https://medium.com/javascript-scene/the-two-pillars-of-javascript-ee6f3281e7f3" rel="nofollow noreferrer">https://medium.com/javascript-scene/the-two-pillars-of-javascript-ee6f3281e7f3</a></p>
<p>John Resig seems to be a fan -&gt; <a href="http://ejohn.org/blog/partial-functions-in-javascript/" rel="nofollow noreferrer">http://ejohn.org/blog/partial-functions-in-javascript/</a></p>
<p><a href="http://shop.oreilly.com/product/0636920028857.do" rel="nofollow noreferrer">http://shop.oreilly.com/product/0636920028857.do</a></p>
<p>I realize this post went from very specific to very general very quickly, I'll edit the scope and make a new post if suggested.</p>
<p>EDIT: Added tests for lodash and underscore to the group.  Lodash comes in second at around 870 ops/sec and underscore at only 475 ops/sec.  Tests <a href="http://jsperf.com/forvsfunc/4" rel="nofollow noreferrer">here</a>.</p>
<p>I found a benchmark of fast.js vs a for loop and a js native function <a href="http://jsperf.com/fast-js-benchmarks" rel="nofollow noreferrer">here</a> and it is similarly blown away by a simple for loop.</p>

## Answers
### Answer ID: 33623605
<p>Array methods are inherently slower than for loops since 1) they have to re-build the function scope on every iteration and 2) some of them (<code>.map</code>, <code>.reduce</code>) have to rebuild a copy of the array (so more memory, more GarbageCollection and generally more operations). So if speed is your concern, stay as low as possible.</p>
<p>Specifically to your algorithm though, there are a few things that you can do to improve the runtime. Your most expensive operation is the <code>LevenshteinDistance</code> so optimizing that would give you considerable speed improvements.</p>
<p>The easiest thing you can do is do a length check of the strings and do an early return: you know that if 2 strings' length differ by more than <code>options.distance</code> their Levenshtein distance will be at least more than that, so you can easily early return:</p>
<pre><code>for (var j = 0; j &lt; compareArr.length; j++) {
    // This check was added
    if (Math.abs(res[i].name.length - compareArr[j].name.length) &gt; options.distance) {
        continue;
    }
    if(natural.LevenshteinDistance(res[i].name, compareArr[j].name) === options.distance) {
        tempObj.matches.push(compareArr[j])
    }
}
</code></pre>
<p>There are also several improvements to the method itself that are better explained in another stackoverflow post: <a href="https://stackoverflow.com/a/3183199/574576">https://stackoverflow.com/a/3183199/574576</a></p>


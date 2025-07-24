# MongoDB: Efficiency of operation pushing to a nested array or updating it when identifier found, using aggregation pipeline
[Link to question](https://stackoverflow.com/questions/75217320/mongodb-efficiency-of-operation-pushing-to-a-nested-array-or-updating-it-when-i)
**Creation Date:** 1674533442
**Score:** 3
**Tags:** javascript, mongodb, aggregation-framework
## Question Body
<p>I have a document that holds lists containing nested objects. The document simplified looks like this:</p>
<pre class="lang-json prettyprint-override"><code>{
    &quot;username&quot;: &quot;user&quot;,
    &quot;listOne&quot;: [
        {
            &quot;name&quot;: &quot;foo&quot;,
            &quot;qnty&quot;: 5
        },
        {
            &quot;name&quot;: &quot;bar&quot;,
            &quot;qnty&quot;: 3
        },

    ],
    &quot;listTwo&quot;: [
        {
            &quot;id&quot;: 1,
            &quot;qnty&quot;: 13
        },
        {
            &quot;id&quot;: 2,
            &quot;qnty&quot;: 9
        },

    ]
}
</code></pre>
<p>And I need to update quantity in lists based on an indentifier. For list one it was easy. I was doing something like this:</p>
<pre class="lang-js prettyprint-override"><code>db.collection.findOneAndUpdate(
    {
        &quot;username&quot;: &quot;user&quot;,
        &quot;listOne.name&quot;: name
    },
    {
        $inc: {
            &quot;listOne.$.qnty&quot;: qntyChange,
        }
    }
)
</code></pre>
<p>Then I would catch whenever find failed because there was no object in the list with that name and nothing was updated, and do a new operation with <code>$push</code>. Since this is a rarer case, it didn't bother me to do two queries in the database collection.</p>
<p>But now I had to also add list two to the document. And since the identifiers are not the same I would have to query them individually. Meaning four searches in the database collection, in the worst case scenario, if using the same strategy I was using before.</p>
<p>So, to avoid this, I wrote an update using an aggregation pipeline. What it does is:</p>
<ol>
<li>Look if there is an object in the list one with the queried identifier.</li>
<li>If true, map through the entire array and:<br />
2.1) Return the same object if the identifier is different.<br />
2.2) Return object with the quantity changed when identifier matches.</li>
<li>If false, push a new object with this identifier to the list.</li>
<li>Repeat for list two</li>
</ol>
<p>This is the pipeline for list one:</p>
<pre class="lang-js prettyprint-override"><code>db.coll1.updateOne(
    {
        &quot;username&quot;: &quot;user&quot;
    },
    [{
        &quot;$set&quot;: {
            &quot;listOne&quot;: {
                &quot;$cond&quot;: {
                    &quot;if&quot;: {
                        &quot;$in&quot;: [
                            name,
                            &quot;$listOne.name&quot;
                        ]
                    },
                    &quot;then&quot;: {
                        &quot;$map&quot;: {
                            &quot;input&quot;: &quot;$listOne&quot;,
                            &quot;as&quot;: &quot;one&quot;,
                            &quot;in&quot;: {
                                &quot;$cond&quot;: {
                                    &quot;if&quot;: {
                                        &quot;$eq&quot;: [
                                            &quot;$$one.name&quot;,
                                            name
                                        ]
                                    },
                                    &quot;then&quot;: {
                                        &quot;$mergeObjects&quot;: [
                                            &quot;$$one&quot;,
                                            {
                                                &quot;qnty&quot;: {
                                                    &quot;$add&quot;: [
                                                        &quot;$$one.qnty&quot;,
                                                        qntyChange
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    &quot;else&quot;: &quot;$$one&quot;
                                }
                            }
                        }
                    },
                    &quot;else&quot;: {
                        &quot;$concatArrays&quot;: [
                            &quot;$listOne&quot;,
                            [
                                {
                                    &quot;name&quot;: name,
                                    &quot;qnty&quot;: qntyChange
                                }
                            ]
                        ]
                    }
                }
            }
        }
    }]
);
</code></pre>
<p>Entire pipeline can be foun on this <a href="https://mongoplayground.net/p/aFs_9UczuUg" rel="nofollow noreferrer">Mongo Playgorund</a>.</p>
<hr />
<p>So my question is about how efficient is this. As I am paying for server time, I would like to use an efficient solution to this problem. Querying the collection four times, or even just twice but at every call, seems like a bad idea, as the collection will have thousands of entries. The two lists, on the other hand, are not that big, and should not exceed a thousand elements each. But the way it's written it looks like it will iterate over each list about two times.</p>
<p>And besides, what worries me the most, is if when I use <code>map</code> to change the list and return the same object, in cases where the identifier does not match, does MongoDB rewrite these elements too? Because not only would that increase my time on the server rewriting the entire list with the same objects, but it would also count towards the bytes size of my write operation, which are also charged by MongoDB.</p>
<p>So if anyone has a better solution to this, I'm all ears.</p>

## Answers
### Answer ID: 75224254
<p>According to <a href="https://stackoverflow.com/questions/11355539/algorithmic-complexity-of-mongodbs-array-operations">this SO answer</a>,</p>
<blockquote>
<p>What you actually do inside of the document (push around an array, add a field) should not have any significant impact on the total cost of the operation</p>
</blockquote>
<p>So, in your case, your array operations should not be causing a heavy impact on the total cost.</p>


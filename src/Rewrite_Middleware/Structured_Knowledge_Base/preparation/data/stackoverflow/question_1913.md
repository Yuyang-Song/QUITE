# VB.NET Sort Order Using CompareTo - Incorrect Results?
[Link to question](https://stackoverflow.com/questions/11961053/vb-net-sort-order-using-compareto-incorrect-results)
**Creation Date:** 1344979865
**Score:** 2
**Tags:** vb.net, string, sorting, compare, compareto
## Question Body
<p>I have a long list of string values I am trying to sort in a grid. Initially, the default sort algorithm was used for the entire grid. However, I ended up having to rewrite the sorting for the grid because a few columns required special sorting and the grid does not allow custom sorting for specific columns. The column in question here did not require special sorting, so I just used CompareTo:</p>

<pre><code>Public Function Compare(ByVal p1 as MyObj, ByVal p2 as MyObj) As Integer
    Return p1.Description.CompareTo(p2.Description)
End Function
</code></pre>

<p>Comparing the default grid sort method and the one I'm now using with CompareTo, I get the exact same results. However, the sort results from a direct database query differ (where the database results are correct according to what I think they should be). </p>

<p>Here are three examples of what I believe are incorrect sort results:</p>

<p><strong>Example 1</strong></p>

<p>Sort Result:</p>

<ol>
<li>TEST- A/A MY TEST</li>
<li>TEST1000 A TEST</li>
<li>TEST1000 TEST</li>
<li>TESTR A TEST</li>
<li>TEST-B/A MY TEST</li>
</ol>

<p>Expected Result:</p>

<ol>
<li>TEST- A/A MY TEST</li>
<li>TEST-B/A MY TEST</li>
<li>TEST1000 A TEST</li>
<li>TEST1000 TEST</li>
<li>TESTR A TEST</li>
</ol>

<p><strong>Example 2</strong></p>

<p>Sort Result:</p>

<ol>
<li>TEST- A TEST</li>
<li>TEST ME</li>
<li>TEST-#1 A</li>
<li>TEST-#1 B</li>
</ol>

<p>Expected Result:</p>

<ol>
<li>TEST ME</li>
<li>TEST- A TEST</li>
<li>TEST-#1 A</li>
<li>TEST-#1 B</li>
</ol>

<p><strong>Example 3</strong></p>

<p>Sort Result:</p>

<ol>
<li>LOUISE TEST 1</li>
<li>LOUISE TEST 2</li>
<li>LOUIS- TEST 1</li>
</ol>

<p>Expected Result:</p>

<ol>
<li>LOUIS- TEST 1</li>
<li>LOUISE TEST 1</li>
<li>LOUISE TEST 2</li>
</ol>

<p>Has anyone run across this before or have any ideas what could be going on here?</p>

## Answers
### Answer ID: 11961814
<p><a href="http://msdn.microsoft.com/en-us/library/35f0x18w.aspx" rel="nofollow">CompareTo</a> does a case-sensitive, culture-sensitive sort, so characters like apostrophes, hyphens, etc. don't show where there would in a strict character encoding sort - which it seems you were expecting.</p>

<p>Consider using an overload of <a href="http://msdn.microsoft.com/en-us/library/e6883c06" rel="nofollow">Compare</a> that lets you specify the <a href="http://msdn.microsoft.com/en-us/library/system.stringcomparison" rel="nofollow">StringComparison</a> as Ordinal</p>


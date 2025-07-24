# XBase Language Rounding Weirdness
[Link to question](https://stackoverflow.com/questions/13653016/xbase-language-rounding-weirdness)
**Creation Date:** 1354308826
**Score:** 0
**Tags:** .net, decimal, rounding, visual-foxpro
## Question Body
<p>I have a requirement to take legacy code in an <a href="http://en.wikipedia.org/wiki/XBase" rel="nofollow">XBase-style</a> language (FoxPro, in this case) and convert it to C#.NET.  I want to get identical output from my rewrite, but rounding discrepancies are driving me nuts.  I tried <strong>Decimal.Round(MidpointRounding)</strong> stuff alone, but found that I also needed to write my own "round up" function for midpoint = 5 situations.</p>

<p>That would be fine, if it worked, but what I'm seeing is that the my "round up" method is needed to agree with FoxPro output in some cases, but actually creates discrepancies in others.  The database query is doing some multiplication and division, and I'm wondering whether math discrepancies between the two systems are accumulating.</p>

<p>Here is an example of what seems to me to be an inconsistency.  The initial value of each pair comes from the output of my LINQ query.  Given these, I want to generate a rounded result that is identical to the FoxPro result shown:</p>

<pre><code>.NET LINQ Query result: 7.0477049103806673503597572093.
FoxPro rounding: 7.0

.NET LINQ: 7.2499596595318807183725770943.
FoxPro rounding: 7.3
</code></pre>

<p>Any suggestions as to how I can exactly duplicate the value from the legacy system without out resorting to a completely kludgey hack?</p>

## Answers
### Answer ID: 13653199
<p>Your problem might have to do with floating point accuracy. Before the FoxPro program round, what type of variable does it store the value in ?  And what type do you use ? </p>

<p>If the FoxPro program uses a floating point number with less accuracy than you do in C# (or vice versa), this might be the reason for the discrepancies you are seeing.</p>


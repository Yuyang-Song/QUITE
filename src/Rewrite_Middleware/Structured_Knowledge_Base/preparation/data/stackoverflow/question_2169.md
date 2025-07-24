# &quot;Strategy Pattern&quot; in Haskell
[Link to question](https://stackoverflow.com/questions/21677201/strategy-pattern-in-haskell)
**Creation Date:** 1392035130
**Score:** 5
**Tags:** haskell, interface, strategy-pattern
## Question Body
<p>In the OO world, I have a class (let's call it "Suggestor") that implement something approaching a "Strategy Pattern" to provide differing implementations of an algorithm at runtime. As an exercise in learning Haskell, I want to rewrite this.</p>

<p>The actual use-case is quite complex, so I'll boil down a simpler example.</p>

<p>Let's say I have a class <code>Suggester</code> that's takes a list of rules, and applies each rule as a filter to a list of database results.</p>

<p>Each rule has three phases "Build Query", "Post Query Filter", and "Scorer". We essentially end up with an interface meeting the following</p>

<pre><code>buildQuery :: Query -&gt; Query
postQueryFilter :: [Record] -&gt; [Record]
scorer :: [Record] -&gt; [(Record, Int)]
</code></pre>

<p>Suggestor needs to take a list of rules that match this interface - dynamically at run time - and then execute them in sequence. buildQuery() must be run across all rules first, followed by postQueryFilter, then scorer. (i.e. I can't just compose the functions for one rule into a single function).</p>

<p>in the scala I simply do</p>

<pre><code>// No state, so a singleton `object` instead of a class is ok
object Rule1 extends Rule {
  def buildQuery ...
  def postQueryFilter ...
  def scorer ...
}

object Rule2 extends Rule { .... }
</code></pre>

<p>And can then initialise the service by passing the relevant rules through (Defined at runtime based on user input). </p>

<pre><code>val suggester = new Suggester( List(Rule1, Rule2, Rule3) );
</code></pre>

<p>If the rules were a single function, this would be simple - just pass a list of functions. However since each rule is actually three functions, I need to group them together somehow, so I have multiple implementations meeting an interface.</p>

<p>My first thought was type classes, however these don't quite seem to meet my needs - they expect a type variable, and enforce that each of my methods must use it - which they don't.</p>

<pre><code>No parameters for class `Rule`
</code></pre>

<p>My second thought was just to place each one in a haskell module, but as modules aren't "First Class" I can't pass them around directly (And they of course don't enforce an interface). </p>

<p>Thirdly I tried creating a record type to encapsulate the functions</p>

<pre><code>data Rule = Rule { buildQuery :: Query -&gt; Query, .... etc }
</code></pre>

<p>And then defined an instance of "Rule" for each. When this is done in each module it encapsulates nicely and works fine, but felt like a hack and I'm not sure if this is an appropriate use of records in haskell?</p>

<p>tl;dr - How do I encapsulate a group of functions together such that I can pass them around as an instance of something matching an interface, but don't actually use a type variable.</p>

<p>Or am I completely coming at this from the wrong mindset?</p>

## Answers
### Answer ID: 21688170
<p>Just generate a single <code>Rule</code> type as you did</p>

<pre><code>data Rule = Rule
  { buildQuery :: Query -&gt; Query
  , postQueryFilter :: [Record] -&gt; [Record]
  , scorer :: [Record] -&gt; [(Record, Int)]
  }
</code></pre>

<p>And build a general application method—I'm assuming such a generic thing exists given that these <code>Rules</code> are designed to operate independently over SQL results</p>

<pre><code>applyRule :: Rule -&gt; Results -&gt; Results
</code></pre>

<p>Finally, you can implement as many rules as you like wherever you want: just import the <code>Rule</code> type and create an appropriate value. There's no a priori reason to give each different rule its own type as you might in an OO setting.</p>

<pre><code>easyRule :: Rule
easyRule = Rule id id (\recs -&gt; zip recs [1..])

upsideDownRule :: Rule
upsideDownRule = Rule reverse reverse (\recs -&gt; zip recs [-1, -2..])
</code></pre>

<p>Then if you have a list of <code>Rule</code>s you can apply them all in order</p>

<pre><code>applyRules :: [Rule] -&gt; Results -&gt; Results
applyRules []     res = res
applyRules (r:rs) res = applyRules rs (applyRule r res)
</code></pre>

<p>which is actually just a <code>foldr</code> in disguise</p>

<pre><code>applyRules rs res = foldr applyRule res rs

foo :: Results -&gt; Results
foo = applyRules [Some.Module.easyRule, Some.Other.Module.upsideDownRule]
</code></pre>

### Answer ID: 21680222
<p>In my opinion your solution isn't the "hack", but the "strategy pattern" in OO languages: It is only needed to work around the limitations of a language, especially in case of missing, unsafe or inconvenient Lambdas/Closures/Function Pointers etc, so you need a kind of "wrapper" for it to make it "digestible" for that language. </p>

<p>A "strategy" <strong>is</strong> basically a function (may be with some additional data attached). But if a function is truly a first class member of the language - as in Haskell, there is no need to hide it in the object closet.</p>


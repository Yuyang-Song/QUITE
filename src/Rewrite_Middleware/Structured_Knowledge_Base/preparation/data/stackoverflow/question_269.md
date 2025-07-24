# Filtering dimensions in MDX inside a SUM
[Link to question](https://stackoverflow.com/questions/18579658/filtering-dimensions-in-mdx-inside-a-sum)
**Creation Date:** 1378150011
**Score:** 2
**Tags:** mdx, olap
## Question Body
<p>I am new to MDX expressions and I am trying to create one that sums the value of a given measure filtered by dimensions.</p>

<p>In my database I have several different dimensions that have the same name: "Answer". To sum them up, I have created the query below:</p>

<pre><code>WITH MEMBER Measures.Total as SUM ({[Activity].[Activity].&amp;[14], [Activity][Activity].&amp;[22]}, 
[Measures].[Activity time])
SELECT NON EMPTY [Measures].[Total] on COLUMNS from  [My Analytics]
</code></pre>

<p>This query works, however I had to use the "&amp;[14]" and "&amp;[22]" statments that correspond to two different "Answer" dimensions.</p>

<p>Since I have more than two dimensions with the same name, is there a way to rewrite the query above in a way that I would select all these dimensions without having to add their unique ID? For example, I would re-write the query as something like this:</p>

<pre><code>WITH MEMBER Measures.Total as SUM ({[Activity].[Activity].&amp;["Answer"]}, 
[Measures].[Activity time])
SELECT NON EMPTY [Measures].[Total] on COLUMNS from  [My Analytics]
</code></pre>

<p>Is this possible?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 18581589
<p>You can use the <a href="http://www.iccube.com/support/documentation/mdx/Filter.html" rel="nofollow">Filter</a> function as following:</p>

<pre><code>with 
  set [my-answers] as 
      Filter( [Activity].[Activity].members, 
              [Activity].[Activity].currentMember.name = 'Answer' 
      )

   member [Measures].[Total] as Sum( [my-answers] )

...
</code></pre>


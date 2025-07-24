# Dlookup/rank next 3 field&#39;s after today&#39;s date
[Link to question](https://stackoverflow.com/questions/55471140/dlookup-rank-next-3-fields-after-todays-date)
**Creation Date:** 1554196828
**Score:** 0
**Tags:** ms-access, expression
## Question Body
<p>Part of my database form that I created will list the newest added event as well as the next upcoming 3 events that we are hosting. However I am unable to figure out how to get the dlookup expression to return the correct values into the form field.</p>

<p>I use the following expression to return the latest event added:</p>

<pre><code>=DLookup("[Event Name]","[Events]","[Event Date] = DMax('[Event Date]','[Events]')")
</code></pre>

<p>Which works perfectly well for that field, moving onto the upcoming events, I was looking for an expression that lists the next 3 events</p>

<p>I use the below to list the next event</p>

<pre><code>=DLookUp("[Event Name]","[Events]","[Event Date] &gt;= now()")
</code></pre>

<p>This again works fine however the problem occurs when trying to list event #2 &amp; #3. I was wondering if possible to use the dlookup expression / rewrite the expression to list the next 2 upcoming events.</p>

<p>I also created a <a href="https://imgur.com/8k4XR5t" rel="nofollow noreferrer">new query</a> to list all events after now() and was thinking of using DCount and referring to that instead with a mod however I can't find the right criteria</p>

<pre><code>=DCount("  [View - Upcoming Events]![Event Name] "," [View - Upcoming Events]","[Event Name] &lt;= &amp; [Event Name]") Mod 2

=DCount("  [View - Upcoming Events]![Event Name] "," [View - Upcoming Events] "," [Event Name] &lt;= " &amp; [Event Name]) Mod 2
</code></pre>

<p>This will always return #Name or #Error depending on how I play around with the coding. And I've misplaced my big list of expressions.</p>

## Answers
### Answer ID: 55471938
<p>In your (secret) query, insert a <strong>TOP 3</strong> statement to select only the <em>three top records</em>, like:</p>

<pre><code>Select TOP 3 [Event Name], [Event Date] 
From [Events]
Where [Event Date] &gt; Date()
Order By [Event Date] Asc
</code></pre>


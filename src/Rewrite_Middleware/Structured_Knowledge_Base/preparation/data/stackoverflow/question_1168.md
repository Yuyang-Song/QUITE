# Getting Errors from Entity Framework Core for a List contains another List
[Link to question](https://stackoverflow.com/questions/61717341/getting-errors-from-entity-framework-core-for-a-list-contains-another-list)
**Creation Date:** 1589137542
**Score:** -1
**Tags:** c#, entity-framework-core, blazor-server-side
## Question Body
<p>I have a List of SkillIDs, and I want to include the records from database that have that list in their skills:</p>

<pre><code>List&lt;int&gt; skillIDs = skills.Where(s =&gt; s.Checked == true)?.Select(s =&gt; s.Id)?.ToList&lt;int&gt;() ?? new List&lt;int&gt;();
if (skillIDs.Count() &gt; 0)
{
    jobSeekers = jobSeekers.Where(js =&gt; js.ProfileJobs
         .Where(pj =&gt; skillIDs.All(s =&gt; pj.ProfileJobSkills.Select(pjs =&gt; pjs.SkillId).Contains(s))).Any());
         //.Where(pj =&gt; pj.ProfileJobSkills.Select(pjs =&gt; pjs.SkillId).Intersect(skillIDs).Count() == skillIDs.Count()).Any());
}
</code></pre>

<p>I either Get "Bug or Limitation" Error from Entity Framework core for the intersect and except or I get "Can't translate and use client evaluation" Error from EF Core, Ofcourse I don't want to use client evaluation since data is large, What do I do?</p>

<p><strong>For the not commented code I get:</strong></p>

<p>selector: (p2) => p2.SkillId), \r\n            item: s)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). </p>

<p><strong>and For the commented code I get:</strong></p>

<p>{"Processing of the LINQ expression 'Intersect(\r\n ...  by 'NavigationExpandingExpressionVisitor' failed. This may indicate either a bug or a limitation in EF Core.</p>

## Answers
### Answer ID: 62115177
<p>You can try something like this:</p>

<pre><code>List&lt;int&gt; skillIDs = skills.Where(s =&gt; s.Checked == true)
     .Select(s =&gt; s.Id)
     .ToList&lt;int&gt;() ?? new List&lt;int&gt;();

if (skillIDs.Count() &gt; 0)
{
    jobSeekers = jobSeekers
      .Where(js =&gt; 
         js.ProfileJobs != null &amp;&amp; 
         js.ProfileJobs.Any(pj =&gt; 
              pj.ProfileJobSkills != null &amp;&amp;
              pj.ProfileJobSkills.Any(pjs =&gt; 
                   skillIds.Contains(pjs.SkillId))
     ); 
 }
</code></pre>

<p>Because you have multiple layers in your table relationships, you can't obtain the cleanest query.  Something like this should work though.</p>


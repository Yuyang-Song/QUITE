# EF Core 7 : Contains method exception: could not be translated. Either rewrite the query in a form that can be translated
[Link to question](https://stackoverflow.com/questions/75720756/ef-core-7-contains-method-exception-could-not-be-translated-either-rewrite-t)
**Creation Date:** 1678703978
**Score:** 0
**Tags:** c#, asp.net, .net, entity-framework-core, ef-core-7.0
## Question Body
<p>I want to write a LINQ query for finding 10 courses with the most intersect tags with a specific course.</p>
<p>I wrote it but I get an exception. I don't want to use <code>ToList</code> or <code>AsEnumerable</code> because I don't want to execute the query to get all the courses before getting 10.</p>
<p>I don't want to use other ORMs.</p>
<p>The code:</p>
<pre><code>var courses = await _dbContext.Courses
                              .AsNoTracking()
                              .Where(c =&gt; c.Id != request.Id)
                              .Select(c =&gt; new
                                      {
                                           Course = c,
                                           IntersectTagsCount = c.Tags.Sum(t =&gt; course.Tags.Contains(t) ? 1 : 0)
                                      })
                              .OrderByDescending(c =&gt; c.IntersectTagsCount)
                              .Take(10)
                              .ToListAsync();
</code></pre>
<p>The error I get is:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 't =&gt; __course_Tags_1 .Contains(t) ? 1 : 0' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>The entity looks like this:</p>
<p><img src="https://i.sstatic.net/Odcof.png" alt="Entity class picture" /></p>
<p>Which is stored in the database like this:</p>
<p><img src="https://i.sstatic.net/3ctf1.png" alt="SQL Server database table picture" /></p>

## Answers
### Answer ID: 75726793
<p>The issue will be trying to inject another entity or DTO into the query expression. (counrse.Tags)</p>
<p>Give this a try.</p>
<pre><code>var tagIds = course.Tags.Select(t =&gt; t.Id).ToList();

var courses = await _dbContext.Courses
    .AsNoTracking()
    .Where(c =&gt; c.Id != request.Id)
    .Select(c =&gt; new
    {
       Course = c,
       IntersectTagsCount = c.Tags.Sum(t =&gt; tagIds.Contains(t.Id) ? 1 : 0)
    })
    .OrderByDescending(c =&gt; c.IntersectTagsCount)
    .Take(10)
    .ToListAsync();
</code></pre>
<p><strong>Edit:</strong> Ok, I missed that you're storing the tags as an array within the entity. Unfortunately you won't be able to translate a Array.Sum where that Tags property likely needs to go through a value converter down to a varchar to build a comma-delimited value to store in the DB.</p>
<p>My recommendation is that if you need to be able to query/consolidate courses by tags, that you normalize the table structure so that Tag references can be related across courses. Something like this would be a standard many-to-many relationship where we create a Tag table (TagId &amp; TagName) then a CourseTags table (CourseId &amp; TagId as a composite PK with FKs back to their respective tables)</p>
<p>THe entity structure changes slightly:</p>
<pre><code>[Table(&quot;Courses&quot;)]
public class Course
{
    [Key, DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; }
    // ...

    public virtual ICollection&lt;Tag&gt; Tags { get; set; } = new List&lt;Tag&gt;();
}

[Table(&quot;Tags&quot;)]
public class Tag
{
    [Key]
    public string Id { get; set; }
    
    public virtual ICollection&lt;Course&gt; Courses { get; set; } = new List&lt;Course&gt;();
}
</code></pre>
<p>EF can manage the CourseTags table completely behind the scenes. In the above example I just used the tag name/string as the ID/PK (I.e. &quot;TestTagName1&quot;) as this option might be less hassle to re-factor to use. If there are expected to be a lot of tags, I would recommend using an identity integer for the ID as it will be easier on the indexing.</p>
<p>Now assuming your client code passes a filtered array of tag IDs to check as course.tags (array of strings) then EF can now build a query across related Tag rows through the CourseTags relationship:</p>
<pre><code>var courses = await _dbContext.Courses
    .AsNoTracking()
    .Where(c =&gt; c.Id != request.Id)
    .Select(c =&gt; new
    {
       Course = c,
       IntersectTagsCount = c.Tags.Sum(t =&gt; course.Tags.Contains(t.Id) ? 1 : 0)
    })
    .OrderByDescending(c =&gt; c.IntersectTagsCount)
    .Take(10)
    .ToListAsync();
</code></pre>
<p>The difference is now that EF has a relational relationship between Courses and Tags, it can build queries around the Linq operations since it knows a Course will be associated to a set of Tag records rather than containing a single column with the tag values appended together.</p>
<p>An alternative option which may work with EF Core 7 would be to store the Tags as a JSON set of values within the Course as I believe EF Core does support querying against JSON data. Unfortunately this isn't something I have spent time tinkering with yet but it might be worth looking into if you decide you really prefer storing the tags in a field rather than a relational table.</p>


# To monitor changes in the properties of a class using reflection in C#
[Link to question](https://stackoverflow.com/questions/63923055/to-monitor-changes-in-the-properties-of-a-class-using-reflection-in-c)
**Creation Date:** 1600269203
**Score:** 0
**Tags:** c#
## Question Body
<p>Let's say I have a class with public properties. Example of a class.</p>
<pre><code>public class Book
{
    public string Title { get; set; }
    public string Author { get; set; }
}
</code></pre>
<p>To optimize queries, only modified fields must be sent to the database.</p>
<p><strong>How can I track changes to the properties of the book class, provided that I can't rewrite the code of the class itself in any way?</strong></p>
<p>The book itself is in the cache for updating, it can be accessed from outside the link.</p>
<p>I've been working on it for a week.</p>
<p><em>I searched through the reference books on reflection, but I didn't find anything. Although you can somehow use reflection to read the set method of the book class, add your own code, and put everything back in the method.</em></p>


# Split content based on content that fits over the same
[Link to question](https://stackoverflow.com/questions/66234888/split-content-based-on-content-that-fits-over-the-same)
**Creation Date:** 1613528604
**Score:** 2
**Tags:** c#
## Question Body
<p>My problem as it is right now. That is, it does not go down to the other table which is courseCategory which is put together with CourseData.</p>
<p>I would therefore like to get hold of courses that have been set up on the single category value.</p>
<p>Let's say that Course did not find anything on any of the others while addressing my category content.</p>
<p>As you can see in the picture here, for example, I just have several right now, but when each course adds a category. and it is not found on any of the others. Well then, search for the single category should take over.</p>
<p>My table from category
<a href="https://i.sstatic.net/8MudC.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/8MudC.png" alt="My table from category" /></a></p>
<p>My database overview
<a href="https://i.sstatic.net/qdDE5.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/qdDE5.png" alt="My database overview" /></a></p>
<p>So my problem to make it clear is that it basically does not address the words from SearchWord. As long as there is one or more words that fit, it must address it.</p>
<pre><code>public List&lt;CourseData&gt; GetCourseList(string text)//Undervisning
    {
        List&lt;CourseData&gt; list = new List&lt;CourseData&gt;();
        var dataContent = _dbContext.CourseDataModul
            .Where(r =&gt; r.Title.Contains(text) 
                        || r.Deck.Contains(text) 
                        || r.CourseDataContent.FirstOrDefault(x =&gt; x.Title.Contains(text)).Title.Contains(text) 
                        || r.CourseDataContent.FirstOrDefault(x =&gt; x.Deck.Contains(text)).Deck.Contains(text)
                        || r.CourseDataContent.FirstOrDefault(x =&gt; x.ContentValue.Contains(text)).ContentValue.Contains(text))
            .ToList();
        
        foreach (var item in dataContent)
        {
            list = _dbContext.CourseData
                .Where(r =&gt; r.Id == item.CourseDataId &amp;&amp; r.OpenNow || r.Title.Contains(text) || r.Deck.Contains(text) ||
                            r.CourseCategori.SearchWord
                                .Split(new [] {&quot;,&quot;, &quot;, &quot;, &quot; &quot;}, StringSplitOptions.None) //online undervisning,undervisning,computer undervisning
                                .Contains(text)).ToList();//undervisning
        }
        return list;
    }
</code></pre>
<p>You can see in the code by split that I have commented on some code which should tell what it looks like in the database and that it should for example just be based on &quot;undervisning&quot; only. As I said, it is welcome to address more.</p>
<p>I have looked at these here link:</p>
<p><a href="https://stackoverflow.com/questions/32071789/how-can-i-check-and-split-strings-which-contains-comma-backslash-and-hyphen/32071948">How can i check and split strings which contains comma,backslash,and(&amp;),hyphen</a></p>
<p><a href="https://stackoverflow.com/questions/52051043/c-sharp-split-string-only-if-delimiter-found/52051082">c# split string only if delimiter found</a></p>
<p><a href="https://stackoverflow.com/questions/2586602/best-way-to-check-for-string-in-comma-delimited-list-with-net">Best way to check for string in comma-delimited list with .NET?</a></p>
<p><strong>Update.</strong></p>
<p>After I have updated my code and done like this. Then there will be an error which can be seen here.</p>
<pre><code>public List&lt;CourseData&gt; GetCourseList(string text)//Undervisning
    {
        List&lt;CourseData&gt; list = new List&lt;CourseData&gt;();
        var dataContent = _dbContext.CourseDataModul
            .Where(r =&gt; r.Title.Contains(text) 
                        || r.Deck.Contains(text) 
                        || r.CourseDataContent.Any(x =&gt; x.Title.Contains(text)) 
                        || r.CourseDataContent.Any(x =&gt; x.Deck.Contains(text))
                        || r.CourseDataContent.Any(x =&gt; x.ContentValue.Contains(text)))
            .ToList();
        if (dataContent.Count &gt; 0)
        {
            foreach (var item in dataContent)
            {
                list = _dbContext.CourseData
                    .Where(r =&gt; r.Id == item.CourseDataId &amp;&amp; 
                                r.OpenNow || 
                                r.Title.Contains(text) ||
                                r.Deck.Contains(text) ||
                                r.CourseCategori.SearchWord
                                    .Split(new[] {&quot;,&quot;, &quot;, &quot;, &quot;/&quot;},
                                        StringSplitOptions
                                            .RemoveEmptyEntries) //online undervisning,undervisning,computer undervisning
                                    .Any(x =&gt; x.Contains(text))).ToList(); //undervisning
            }
        }
        else
        {
            list = _dbContext.CourseData.Where(r =&gt; r.OpenNow &amp;&amp;
                                r.Title.Contains(text) ||
                                r.Deck.Contains(text) ||
                                r.Text.Contains(text) ||
                                r.CourseCategori.SearchWord
                                    .Split(new[] {&quot;,&quot;, &quot;, &quot;, &quot;/&quot;},
                                        StringSplitOptions
                                            .RemoveEmptyEntries) //online undervisning,undervisning,computer undervisning
                                    .Any(x =&gt; x.Contains(text))).ToList();
        }

        return list;
    }
</code></pre>
<p>Error code here:</p>
<blockquote>
<p>The LINQ expression 'DbSet .Join( outer:
DbSet, inner: c =&gt; EF.Property&lt;Nullable&gt;(c,
&quot;CourseCategoriId&quot;), outerKeySelector: c0 =&gt;
EF.Property&lt;Nullable&gt;(c0, &quot;Id&quot;), innerKeySelector: (o, i) =&gt; new
TransparentIdentifier&lt;CourseData, CourseCategori&gt;( Outer = o, Inner =
i )) .Where(c =&gt; c.Outer.OpenNow &amp;&amp; c.Outer.Title.Contains(__text_0)
|| c.Outer.Deck.Contains(__text_0) || c.Outer.Text.Contains(__text_0)
|| c.Inner.SearchWord.Split( separator: string[] { &quot;,&quot;, &quot;, &quot;, &quot;/&quot;, },
options: RemoveEmptyEntries) .Any(x =&gt; x.Contains(__text_0)))' could
not be translated. Either rewrite the query in a form that can be
translated, or switch to client evaluation explicitly by inserting a
call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
more information.</p>
</blockquote>


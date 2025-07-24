# System.InvalidOperationException: The LINQ expression
[Link to question](https://stackoverflow.com/questions/63803864/system-invalidoperationexception-the-linq-expression)
**Creation Date:** 1599617823
**Score:** 0
**Tags:** c#, linq, asp.net-core-webapi
## Question Body
<p>I set up an asynchronous method in webapi(.NET Core 3.1), use linq to search the database and get the number of each category, and return it in the controller. I use Swagger to test but there are always errors. I don't know where the error is. Can i ask for some help?</p>
<p>The service:</p>
<pre><code>public async Task&lt;ClassficationSimpleInfo[]&gt; SearchZulib(string token, string keyWord)  
{  
    var data = zudb.ZuFileinfo.Include(x =&gt; x.Classify).Where(x =&gt; x.IsHiden != 1)  
        .Where(x =&gt; keyWord == &quot;&quot; || x.FamilyName.Contains(keyWord) || x.Description.Contains(keyWord))  
        .GroupBy(x =&gt; x.Classify)  
        .Select(x =&gt; new { classify = x.Key, count = x.Count() })  
        .ToList();  
    var result = data.Select(x =&gt; new ClassficationSimpleInfo(x.classify.Name, x.classify.ClassificationCode)  
    {  
        Count = x.count,  
        Folder = x.classify.Folder,  
        
    }).ToArray();  
    return result;  
}
</code></pre>
<p>The controller:</p>
<pre><code>        [HttpGet]
        [Route(&quot;Controller/SearchZulib&quot;)]
        public async Task&lt;ClassficationSimpleInfo[]&gt; SearchZulib(string token, string keyWord)
        {
            return await service.SearchZulib(token, keyWord);
        }  
</code></pre>
<p>The definition of related Class:</p>
<pre><code>namespace ZulibWebServer.Entities
{
    public class ClassficationSimpleInfo
    {
        public int Id { get; set; }

        public string ClassifyCode { get; set; }

        public string Name { get; set; }

        public int Count { get; set; }

        public string Folder { get; set; }

        public bool Existed { get; set; }

        public ClassficationSimpleInfo(string name, string classifyCode)
        {
            Name = name;
            ClassifyCode = classifyCode;
        }
    }
}
namespace ZulibWebServer.Models
{
    public partial class ZuFileinfo
    {
        public int FileId { get; set; }
        public string FamilyName { get; set; }
        public string FileUrl { get; set; }
        public int ClassifyId { get; set; }
        public string Description { get; set; }
        public byte[] ThumbImage { get; set; }
        public int? MinVer { get; set; }
        public string LargeImage { get; set; }
        public int IsHiden { get; set; }
        public string UploaderName { get; set; }
        public int? UploaderId { get; set; }

        public virtual ZuClassfication Classify { get; set; }
    }
}
public partial class ZuClassfication
    {
        public ZuClassfication()
        {
            ZuFileinfo = new HashSet&lt;ZuFileinfo&gt;();
            ZuMapingrule = new HashSet&lt;ZuMapingrule&gt;();
        }

        public int ClassificationIdid { get; set; }
        public string ClassifyName { get; set; }
        public string ClassificationCode { get; set; }
        public string RelQc { get; set; }
        public string RelCbimcode { get; set; }
        public string RelOminClass { get; set; }
        public string Reluniformat { get; set; }
        public string OtherCode { get; set; }
        public string Name { get; set; }
        public int? ParentCodeId { get; set; }
        public string Folder { get; set; }

        public virtual ICollection&lt;ZuFileinfo&gt; ZuFileinfo { get; set; }
        public virtual ICollection&lt;ZuMapingrule&gt; ZuMapingrule { get; set; }
    }
}
</code></pre>
<p>But the error response is</p>
<p>System.InvalidOperationException: The LINQ expression 'DbSet<br />
.Where(z =&gt; z.IsHiden != 1)
.Where(z =&gt; False || z.FamilyName.Contains(__keyWord_0) || z.Description.Contains(__keyWord_0))<br />
.Join( outer: DbSet, inner: z =&gt; EF.Property&gt;(z, &quot;ClassifyId&quot;), outerKeySelector: z0 =&gt; EF.Property&gt;(z0, &quot;ClassificationIdid&quot;), innerKeySelector: (o, i) =&gt; new TransparentIdentifier( Outer = o, Inner = i ))
.GroupBy( source: z =&gt; z.Inner, keySelector: z =&gt; z.Outer)' could not be translated.<br />
Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>

## Answers
### Answer ID: 63807949
<blockquote>
<p>I tested it again and found the error in GroupBy(x =&gt; x.Classify)</p>
</blockquote>
<p>Yeah, it is invalid to GroupBy a Navigation property.</p>
<p>Also, you can simplify your query by linq like below:</p>
<pre><code>var data = zudb.ZuFileinfo.Include(x =&gt; x.Classify).Where(x =&gt; x.IsHiden != 1)
    .Where(x =&gt; keyWord == &quot;&quot; || x.FamilyName.Contains(keyWord) || x.Description.Contains(keyWord))
    .GroupBy(x =&gt; x.ClassifyId)
    .Select(x =&gt; new { classifyId = x.Key, count = x.Count() })
    .ToList();

var result = (from d in data
            join c in zudb.ZuClassfication on d.classifyId equals c.ClassificationIdid
            select new ClassficationSimpleInfo(c.Name, c.ClassificationCode)
            {
                Count = d.count,
                Folder = c.Folder
            }).ToArray();
</code></pre>

### Answer ID: 63807299
<p>I tested it again and found the error in GroupBy(x =&gt; x.Classify), so i modified the code to query the database twice.</p>
<pre><code>var data =await zudb.ZuFileinfo
    .Where(x =&gt; x.IsHiden != 1)
    .Where(x =&gt; keyWord == &quot;&quot; || x.FamilyName.Contains(keyWord) || x.Description.Contains(keyWord))
    .GroupBy(x =&gt; x.ClassifyId).Select(x =&gt; new { classifyId = x.Key, count = x.Count() })
    .ToListAsync();

var classifies =await zudb.ZuClassfication.ToDictionaryAsync(x =&gt; x.ClassificationIdid);

var result = data.Select(x =&gt;
    {
         if (!classifies.TryGetValue(x.classifyId, out var classify)) return null;
         return new ClassficationSimpleInfo(classify.Name, classify.ClassificationCode)
              {
                  Count = x.count,
                  Folder = classify.Folder,
              };
    }).ToArray();
</code></pre>
<p>Finally, I succeeded.</p>


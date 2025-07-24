# Getting around lack of &#39;Contains&#39; in Linq To Entities
[Link to question](https://stackoverflow.com/questions/11926407/getting-around-lack-of-contains-in-linq-to-entities)
**Creation Date:** 1344811067
**Score:** 2
**Tags:** c#, linq, .net-3.5, linq-to-entities
## Question Body
<p>I have the following function (which is hosted in a WCF service, if that matters):</p>

<pre><code>    public List&lt;IceVsRepositoryFile&gt; GetRepositoryFilesByRepositoryId(int repId)
    {
        var entity = new IceVSEntities();
        var files = from p in entity.Files where p.RepositoryId == repId select p.FileId;
        List&lt;long&gt; iList = files.ToList();
        var repFiles = from p in entity.RepositoryFiles where iList.Contains(p.FileId) select p;

        if (!repFiles.Any())
            return null;

        var retFiles = repFiles.ToList().Select(z =&gt; new IceVsRepositoryFile
            {
                FileId = (int)z.FileId,
                RollbackFileId = (int)z.RollbackFileId,
                UserId = (int)z.UserId,
                FileContents = z.FileContents,
                ChangeDescription = z.ChangeDescription
            }).ToList();

        return retFiles;
    }
</code></pre>

<p>When I run this function I am getting the following an error that says "LINQ to Entities does not recognize the method 'Boolean Contains(Int64)' method and this method cannot be translated into a store expression.</p>

<p>I understand why I am getting the error message. My question is, how can I rewrite my query to make this work as expected? My backend database, if it matters, if SqlLite 3. I am using .NET 3.5.</p>

## Answers
### Answer ID: 11926424
<p>The contains you used is for <code>List</code>, it's not in IEnumerable so it can't be converted to corresponding sql query. Instead you can use <code>Any</code>, ... like:</p>

<pre><code>iList.Any(x=&gt;x == p.FileId) (or use related property)
</code></pre>

<p>Also instead of doing:</p>

<pre><code>List&lt;long&gt; iList = files.ToList();
</code></pre>

<p>use <code>files.Any...</code> in your query to prevent from too many fetching from DB. Actually use IEnumerable functions instead of <code>List</code> functions.</p>

### Answer ID: 11927238
<p>I believe a join can do this:</p>

<pre><code>public List&lt;IceVsRepositoryFile&gt; GetRepositoryFilesByRepositoryId(int repId)
{
  var entity = new IceVSEntities();    

  var repFiles = from file in entity.Files where file.RepositoryId == repId join repFile in entity.RepositoryFiles on repFile.FileId equals file.FileId select repFile;

  var retFiles = // as before

  return retFiles;

}
</code></pre>

### Answer ID: 11926621
<p>Do you have a relationship between Files and RepositoryFiles?  If so, it would be easier to do something like this:</p>

<pre><code>var repFiles = from p in entity.RepositoryFiles where p.File.RepositoryId == repId select p;
</code></pre>

<p>This will avoid the problems with being unable to translate the query to SQL.</p>


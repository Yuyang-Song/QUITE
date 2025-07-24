# Relax C# LINQ String Comparison (Trim, Case Insensitive, ??)
[Link to question](https://stackoverflow.com/questions/33913263/relax-c-linq-string-comparison-trim-case-insensitive)
**Creation Date:** 1448445058
**Score:** 4
**Tags:** c#, string, linq
## Question Body
<h2>Problem</h2>

<blockquote>
  <p>Background Story: I am rewriting all SQL queries of legacy system into LINQ. </p>
</blockquote>

<p>The database is not as clean as I expect. As many of these SQL record contains spaces or different cases which treated as the same.</p>

<pre><code>SELECT * 
FROM fruit 
WHERE name = @fruitname;
</code></pre>

<p>Provided <code>@fruitname</code> is <code>apple</code>, this query will match any record ends with <code>apple</code>, <code>_apple</code>, <code>APPLE_</code> (where <code>_</code> is a whitespace character).</p>

<p>However, This is the expected behavior in my use cases.</p>

<p>On the otherhand, LINQ string comparison is more precise. Which annoys me because such issues keep surfacing to me.</p>

<h2>Setup</h2>

<pre><code>FruitTableAdapter fruitsAdapter = new FruitTableAdapter();
MyGardenDataSet.FruitDataTable fruitsTable = fruitsAdapter.GetData();
</code></pre>

<h2>Approaches</h2>

<pre><code>// Issue 1: Does not match, '_apple' or 'APPLE_'
var fruits1 = fruitsTable.Where(row=&gt;row.name == fruitname);

// Issue 2: String Comparison with case insensitive (does not match 'APPLE')
var fruits2 = fruitsTable.Where(
    row=&gt;row.nameEquals(fruitname, StringComparison.OrdinalIgnoreCase));

// Issue 3: Trailing space with case insensitive
var fruits2 = fruitsTable.Where(
    row=&gt;row.name.Trim().Equals(fruitname.Trim(), 
                                StringComparison.OrdinalIgnoreCase));
</code></pre>

<p>I'm not sure but there could be many issues which SQL query are different from String Comparison.</p>

<p>Is there any SQL aware StringComparison? How can I achieve the same string comparison as SQL in LINQ?</p>

## Answers
### Answer ID: 56498804
<p>Here's a nice String Extension method that builds on the solutions from a similiar question about casing <a href="https://stackoverflow.com/questions/5312585/linq-case-insensitive-without-toupper-or-tolower">StackOverflow</a></p>

<p>Keep in mind, we want to allow for NULL strings in our trim scenarios, so this extension will do a Case Insensitive compare on Trimmed strings after checking for null values</p>

<pre><code>public static class StringExtension
{
    // Trim strings and compare values without casing
    public static bool SqlCompare(this string source, string value)
    {
        // Handle nulls before trimming
        if (!string.IsNullOrEmpty(source))
            source = source.Trim();

        if (!string.IsNullOrEmpty(value))
            value = value.Trim();

        // Compare strings (case insensitive)
        return string.Equals(source, value, StringComparison.CurrentCultureIgnoreCase);
    }
}
</code></pre>

<p>Here's how to use the Extension in your LINQ statement:  </p>

<p>(SysUserDisplayFavorites table is composed of char() fields with space filled results. These will get trimmed and compared (case insensitive) to the user provided values in displayFavorite object)</p>

<pre><code>                    var defaultFavorite = _context.SysUserDisplayFavorites
                    .Where(x =&gt; x.UserId.SqlCompare(displayFavorite.UserId))
                    .Where(x =&gt; x.ModuleCode.SqlCompare(displayFavorite.ModuleCode))
                    .Where(x =&gt; x.ActivityCode.SqlCompare(displayFavorite.ActivityCode))
                    .Where(x =&gt; x.ActivityItemCode.SqlCompare(displayFavorite.ActivityItemCode))
                    .Where(x =&gt; x.IsDefault);
</code></pre>

### Answer ID: 51066489
<p><code>fruitsTable.Where(row =&gt; row.name.Trim().Equals(fruitname, StringComparison.OrdinalIgnoreCase));</code> should do what you need, but I'm confused because you've listed almost the same under Issue 3. Were you not realising it was working because you are reusing <code>fruits2</code>?</p>

<p>This little NUnit test is passing</p>

<pre><code>[Test]
public void FruitTest()
{
    var fruitsTable = new List&lt;string&gt; { " Apple", " APPLE", "Apple", "apple", "apple ", " apple", "APPLE " };
    var fruitname = "apple ".Trim();

    var fruits = fruitsTable.Where(row =&gt; row.Trim().Equals(fruitname, StringComparison.OrdinalIgnoreCase));

    Assert.AreEqual(fruitsTable.Count(), fruits.Count());
}
</code></pre>

### Answer ID: 51065153
<p>This is a very late answer.</p>

<p>You can use <code>Regex</code> to solve your problem
Here's what I have tried, hope it helps </p>

<p>I created a sample class </p>

<pre><code> public class SampleTable
 {
     public string Name { get; set; }

     public SampleTable(string name)
     {
        Name = name;
     }
 }
</code></pre>

<p>Populated sample data </p>

<pre><code>List&lt;SampleTable&gt; sampleTblList = new List&lt;SampleTable&gt;();
sampleTblList.Add(new SampleTable(" Apple"));
sampleTblList.Add(new SampleTable(" APPLE"));
sampleTblList.Add(new SampleTable("Apple"));
sampleTblList.Add(new SampleTable("apple"));
sampleTblList.Add(new SampleTable("apple "));
sampleTblList.Add(new SampleTable("apmangple"));
</code></pre>

<p>Solution:-</p>

<pre><code>string fruitName = "apple";
List&lt;SampleTable&gt; sortedSampleTblList = sampleTblList.Where(x =&gt; 
Regex.IsMatch(fruitName, x.Name, RegexOptions.IgnorePatternWhitespace | RegexOptions.IgnoreCase)).ToList();
</code></pre>

<p>Output:- </p>

<pre><code>string ans = String.Join(",", sortedSampleTblList.Select(x =&gt; x.Name.Replace(" ","_")).ToArray());
Console.Write(ans);
</code></pre>

<blockquote>
  <p><code>_Apple,_APPLE,Apple,apple,apple_</code></p>
</blockquote>


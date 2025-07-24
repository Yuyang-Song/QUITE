# How to efficiently work with Entity Framework Core?
[Link to question](https://stackoverflow.com/questions/36624959/how-to-efficiently-work-with-entity-framework-core)
**Creation Date:** 1460641271
**Score:** 3
**Tags:** c#, entity-framework, entity-framework-core
## Question Body
<p>Let's take a look at simple class examples:</p>

<pre><code>public class Book
{
    [Key]
    public string BookId { get; set; }
    public List&lt;BookPage&gt; Pages { get; set; }
    public string Text { get; set; }
} 

public class BookPage
{
    [Key]
    public string BookPageId { get; set; }
    public PageTitle PageTitle { get; set; }
    public int Number { get; set; }
}

public class PageTitle
{
    [Key]
    public string PageTitleId { get; set; }
    public string Title { get; set; }
}
</code></pre>

<p>So, if I want to get all PageTitiles, if I knew only the BookId, I need to write a few includes, like this:</p>

<pre><code>using (var dbContext = new BookContext())
{
    var bookPages = dbContext
    .Book
    .Include(x =&gt; x.Pages)
    .ThenInclude(x =&gt; x.PageTitle)//.ThenInclude(x =&gt; x.Select(y =&gt; y.PageTitle)) Shouldn't use in EF Core
    .SingleOrDefault(x =&gt; x.BookId == "some example id")
    .Pages
    .Select(x =&gt; x.PageTitle);
}
</code></pre>

<p>And if i want to get PageTitles connected with other book, I need to rewrite this method again, and nothing changed except the BookId! This is very inefficient way to work with database, in this example I have 3 classes, but if I had hundreds of classes, nested to the very deep level, it would be very slow and uncomfortable to work.</p>

<p>How exactly should I organize working with my database, to avoid many Includes, and redundant queries?</p>

## Answers
### Answer ID: 49914195
<p>None of the examples given require any Include statements at all. If you are using a select at the end of your query and you are still operating on an IQueryable such as a DbSet, Entity Framework will perform what is known as a 'projection' and will run the query including all of the required fields for you automatically.</p>

<p>For example, your original code:</p>

<pre><code>using (var dbContext = new BookContext())
{
    var bookPages = dbContext
        .Book
        .Include(x =&gt; x.Pages)
        .ThenInclude(x =&gt; x.PageTitle)//.ThenInclude(x =&gt; x.Select(y =&gt; y.PageTitle)) Shouldn't use in EF Core
        .SingleOrDefault(x =&gt; x.BookId == "some example id")
        .Pages
        .Select(x =&gt; x.PageTitle);
}
</code></pre>

<p>You can rewrite this like so:</p>

<pre><code>using (var dbContext = new BookContext())
{
    var bookPages = dbContext
        .Book
        .Where(x =&gt; x.BookId == "some example id")
        .SelectMany(x =&gt; x.Pages.Select(y =&gt; y.PageTitle))
        .ToList();
}
</code></pre>

<p>Here's what Entity Framework will do to resolve this:</p>

<ol>
<li>We tell Entity Framework that we're going to look at entries from the books table</li>
<li>We then tell Entity Framework that we only want the books with a specific ID (which should just be a single record, of course)</li>
<li>From there, for each book we tell Entity Framework that we want a list of all of that books pages (again, this will just be one book's pages because of the Where statement)</li>
<li>Then we tell Entity Framework that we want just the PageTitle from each Page</li>
<li><strong>Finally, we tell Entity Framework to use all of the information we've just provided to generate a query and execute it</strong></li>
</ol>

<p>The last step is the crucial one if you want to understand how Entity Framework does what it does. In your example when you call <code>SingleOrDefault</code> you are instructing Entity Framework to execute the query, which is why you need the includes. In your example you haven't actually told Entity Framework that you need the pages when you run the query, so you have to manually request them using <code>Include</code>.</p>

<p>In the example I've posted, you can see that by the time you run the query (<code>ToList</code> is what triggers the query execution) Entity Framework knows from your Select expression that it is going to need the pages, and their titles. Even better - this means Entity Framework will not even include unused columns in the <code>SELECT</code> statement that it generates.</p>

<p>I highly recommend investigating projections, they're probably the best way I know of to remove the requirement to continuously manually include stuff.</p>

### Answer ID: 36647683
<p>I would have built the model like this:</p>

<pre><code>    public class Book
    {
        // a property "Id" or ClassName + "Id" is treated as primary key. 
        // No annotation needed.
        public int BookId { get; set; }

        // without [StringLenth(123)] it's created as NVARCHAR(MAX)
        [Required]
        public string Text { get; set; }

        // optionally if you need the pages in the book object:
        // Usually I saw ICollections for this usage.
        // Without lazy loading virtual is probably not necessary.
        public virtual ICollection&lt;BookPage&gt; BookPages { get; set; }
    }

    public class BookPage
    {
        public int BookPageId { get; set; }

        // With the following naming convention EF treats those two property as 
        // on single database column. This automatically corresponds
        // to ICollection&lt;BookPage&gt; BookPages of Books.
        // Required is not neccessary if "BookId" is int. If not required use int?
        // A foreign key relationship is created automatically. 
        // With RC2 also an index is created for all foreign key columns.
        [Required]
        public Book Book { get; set; }
        public int BookId { get; set; }

        [Required]
        public PageTitle PageTitle { get; set; }
        public int PageTitleId { get; set; }

        public int Number { get; set; }
    }

    public class PageTitle
    {
        public int PageTitleId { get; set; }

        // without StringLenth it's created as NVARCHAR(MAX)
        [Required]
        [StringLength(100)]
        public string Title { get; set; }
    }
</code></pre>

<p>As you had a collection of <code>BookPage</code> in <code>Book</code> a foreign key is created in <code>BookPage</code>. In my model I have exposed this explicitly in <code>BookPage</code>. And not only with the object <code>Book</code> but also with the key <code>BookId</code>. The created tables are quite the same but now you can access the <code>BookId</code> without using the <code>Book</code> table.</p>

<pre><code>    using (var dbContext = new BookContext())
    {
        var pageTitles = dbContext.BookPages
            .Include(p =&gt; p.PageTitle)
            .Where(p =&gt; p.BookId == myBookId)
            .Select(p =&gt; p.PageTitle);
    }
</code></pre>

<p>I would recommend to activate logging or to use the profiler to check which SQL statements are actually executed. </p>

<p>Regarding to the comments of @bilpor:
I found out that I did not need many DataAnnotations and almost no fluent API mappings. Primary and foreign keys are created automatically if you use the designated naming conventions. For foreign key relationships I only needed <code>[InverseProperty()]</code> on the collections if I had two foreign key relationships on the same two classes. Currently I only used fluent API mappings for composite primary keys (m:n tables) and to define the discriminator in a TPH structure.</p>

<p>Hint:
Currently there are bugs in EF Core which lead to client side evaluation of constraints.</p>

<pre><code>.Where(p =&gt; p.BookId == myBookId)  // OK 
.Where(p =&gt; p.BookId == myObject.BookId) // client side 
.Where(p =&gt; p.BookId == myBookIdList[0]) // client side 
</code></pre>

<p>Same is true when you use Contains() and you mix nullable and not nullable data types. </p>

<pre><code>.Where(p =&gt; notNullableBookIdList.Contains(p.NullableBookId)) // client side 
</code></pre>

### Answer ID: 36631316
<p><strong>Problem 1:  I have to add a bunch of <code>Includes</code> each time.</strong></p>

<p>Well, there's not a way around that as you have to explicitly included related data in EF, but you can easily create an extension method to make it cleaner:</p>

<pre><code>public static IQueryable&lt;Book&gt; GetBooksAndPages(this BookContext db)
{
    return db.Book.Include(x =&gt; x.Pages);
}

public static IQueryable&lt;Book&gt; GetBooksAndPagesAndTitles(this BookContext db)
{
    return GetBooksAndPages(db).ThenInclude(p =&gt; p.PageTitle)

}
</code></pre>

<p>Then you can just do:</p>

<pre><code>var bookPages = dbContext
    .GetBooksAndPagesAndTitles()
    .SingleOrDefault(x =&gt; x.BookId == "some example id")
    .Pages
    .Select(x =&gt; x.PageTitle);
</code></pre>

<p><strong>Problem 2:  I have to write this query multiple times for different IDs.</strong></p>

<p>Why not just refactor that into a method with a <code>bookId</code> parameter?</p>

<pre><code>public IEnumerable&lt;PageTitle&gt; GetPageTitlesForBook(BookContext dbContext, int bookId)
{
    return dbContext
        .GetBooksAndPagesAndTitles()
        .SingleOrDefault(x =&gt; x.BookId == bookId)
        .Pages
        .Select(x =&gt; x.PageTitle);
}
</code></pre>

<p>Bottom line - if you find yourself writing the same thing many times, that's a perfect opportunity to refactor your code into smaller methods that can be re-used.</p>

### Answer ID: 36626857
<p>I somehow missed this was EF Core (despite the title). Try this instead:</p>

<pre><code>public class BookPage
{
    [Key]
    public string BookPageId { get; set; }
    public int Number { get; set; }
    public PageTitle PageTitle { get; set; }
    public Book Book { get; set; }   // Add FK if desired
}
</code></pre>

<p>Now to get all page titles for a book:</p>

<pre><code>// pass the book you want in as a parameter, viewbag, etc.
using (var dbContext = new BookContext())
{
    var bookPages = dbContext.BookPages
        .Include(p =&gt; p.Book)
        .Include(p =&gt; p.PageTitle)
        .Where(p =&gt; p.Book.BookId == myBookId)
        .Select(p =&gt; new { 
            Bookid = p.Book.BookId,
            Text = p.Book.Text,
            PageNumber = p.Number,
            PageTitle = p.PageTitle.Title
        });
}
</code></pre>


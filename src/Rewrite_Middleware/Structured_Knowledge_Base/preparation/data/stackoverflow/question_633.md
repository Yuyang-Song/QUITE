# Entity Framework - How to convert my specific code to an expression that MySQL can understand
[Link to question](https://stackoverflow.com/questions/34376388/entity-framework-how-to-convert-my-specific-code-to-an-expression-that-mysql-c)
**Creation Date:** 1450566832
**Score:** 0
**Tags:** c#, mysql, regex, entity-framework, linq
## Question Body
<p>I have an ASP.NET MVC Application with Entity Framework and MySQL Database. I would like to enforce my code to do all the logic on MySQL server. Obviously I found many cases with similar problem, but I wasn't able to figure out my specific scenario. Thats why I am asking you guys for help.</p>

<p>I have a method like this, it performs a search against space separated words entered by user, each word should be longer than two characters:</p>

<pre><code>protected List&lt;Book&gt; GetBooks(Search search)
{
    var db = new ProjectDbContext();
    var books = db.Books;

    var listTerms = search.SearchTerm.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries)
        .Where(s =&gt; s.Length &gt;= 3).ToList().ConvertAll(t =&gt; t.ToLower());

    var searchedBooks = books//.SqlQuery("", );
        .AsEnumerable().Where(book =&gt; CheckWhatToSearch(book, search, listTerms));

    var sortedBooks = searchedBooks.OrderBy(search.SortBy + " " + search.SortOrder.ToLower()); // dynamic LINQ query helper

    var pagedBooks = search.HowMuchSkip &gt;= 0 ? 
        sortedBooks.Skip(search.HowMuchSkip).Take(search.HowMuchTake) :
        Enumerable.Empty&lt;Book&gt;().AsQueryable();

    return pagedBooks.ToList(); 
}
</code></pre>

<p>Of course when running this method, I am receiving an error, because EF is unable to convert my custom function to SQL Code</p>

<blockquote>
  <p>Error: LINQ to Entities does not recognize the method 'Boolean CheckWhatToSearch(MVCDemo.Models.Book, MVCDemo.Models.Search, System.Collections.Generic.List`1[System.String])' method, and this method cannot be translated into a store expression.</p>
</blockquote>

<p>CheckWhatToSearch method is defined like this:</p>

<pre><code>private static bool CheckWhatToSearch(Book book, Search search, List&lt;string&gt; listTerms)
{
    var db = new ProjectDbContext();
    var users = db.Users;

    if (book.IsPublic != true)
        return false; // skip all not public books

    if (listTerms.Count &lt;= 0)
        return true; // if user typed nothing, display entire list of books

    var sbWhereToSearch = new StringBuilder();
    var titleValue = book.Title;
    var authorValue = users.Single(u =&gt; u.Id == book.AuthorId).UserName;
    var categoryValue = book.Category;
    var descriptionValue = book.Description;

    if (search.IncludeTitle)
        sbWhereToSearch.Append(titleValue + " ");

    if (search.IncludeAuthor)
        sbWhereToSearch.Append(authorValue + " ");

    if (search.IncludeCategory)
        sbWhereToSearch.Append(categoryValue + " ");

    if (search.IncludeDescription)
        sbWhereToSearch.Append(descriptionValue + " ");

    if (sbWhereToSearch.Length == 0) // default if nothing has been chosen
        sbWhereToSearch.Append(titleValue + " ");

    return listTerms.All(sbWhereToSearch.ToString().ToLower().Contains); // true if all property values concatenated contain all the words typed by user
}
</code></pre>

<p>What exactly do I need to figure out?</p>

<ol>
<li>How to rewrite code from <strong>CheckWhatToSearch</strong> method, so I can remove <strong>AsEnumerable()</strong> and enforce all the logic to be executed on MySQL Server. OR</li>
<li>What SqlQuery could replace the functionality of my <strong>CheckWhatToSearch</strong> method (in this case I could call it directly)</li>
</ol>

<p>In second case I started with sth like this:</p>

<pre><code>DROP PROCEDURE IF EXISTS sp_SearchBooks;
CREATE PROCEDURE sp_SearchBooks(
  IN p_SearchTerms VARCHAR(1000), 
  IN p_IncludeTitle TINYINT, 
  IN p_IncludeAuthor TINYINT, 
  IN p_IncludeCategory TINYINT, 
  IN p_IncludeDescription TINYINT)
BEGIN
  DECLARE v_fieldsToSearch INT DEFAULT "";

  SELECT * FROM tblBooks b
    WHERE 
      LOWER(CONCAT(
        CASE p_IncludeTitle WHEN 1 THEN b.Title ELSE "" END,
        CASE p_IncludeAuthor WHEN 1 THEN (SELECT u.UserName FROM tblUsers u WHERE u.ID = b.AuthorId) ELSE "" END,
        CASE p_IncludeCategory WHEN 1 THEN b.Category ELSE "" END,
        CASE p_IncludeDescription WHEN 1 THEN b.Description ELSE "" END))
      REGEXP REPLACE(p_SearchTerms, " ", "|");
END;

CALL sp_SearchBooks("word1 word2", 1, 1, 0, 0);
</code></pre>

<p>But I don't like my approach and I guess its vulnerable to SQL injection. Besides it matches Any, not All (c# regex is different than MySQL one, there is no (?=...)). (SQL procedure is not finished, I have pasted it to show you my way of thinking, but today I really struggle with MySQL)</p>

<p>I prefer option number 1, with LINQ only.</p>

<p><strong>EDIT (20-12-2015 @ 3:30):</strong></p>

<p>Alright, I created stored procedure like this:</p>

<pre><code>DROP PROCEDURE IF EXISTS sp_SearchBooks;
CREATE PROCEDURE sp_SearchBooks(
  IN p_SearchTerms VARCHAR(1000), 
  IN p_IncludeTitle TINYINT, 
  IN p_IncludeAuthor TINYINT, 
  IN p_IncludeCategory TINYINT, 
  IN p_IncludeDescription TINYINT)
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE v_currTerm VARCHAR(100) DEFAULT "";

  DROP TEMPORARY TABLE IF EXISTS temp_tblSearchMatches;
    CREATE TEMPORARY TABLE temp_tblSearchMatches
  (
    Id VARCHAR(36),
    SearchTerm VARCHAR(100),
    CONSTRAINT ck_temp_searchmatches_id CHECK (Id REGEXP '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')
  );

  WHILE (SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(p_SearchTerms, " end;"), ' ', i), ' ', -1) != "end;") DO
    SET v_currTerm = LOWER(SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(p_SearchTerms, " end;"), ' ', i), ' ', -1));
    INSERT INTO temp_tblSearchMatches (temp_tblSearchMatches.Id, temp_tblSearchMatches.SearchTerm) 
      SELECT b.Id, v_currTerm FROM tblBooks b
        WHERE 
          LOWER(CONCAT(
            CASE p_IncludeTitle WHEN 1 THEN b.Title ELSE "" END, " ",
            CASE p_IncludeAuthor WHEN 1 THEN (SELECT u.UserName FROM tblUsers u WHERE u.ID = b.AuthorId) ELSE "" END, " ",
            CASE p_IncludeCategory WHEN 1 THEN b.Category ELSE "" END, " ",
            CASE p_IncludeDescription WHEN 1 THEN b.Description ELSE "" END)) LIKE CONCAT("%", v_currTerm, "%");
    SET i = i + 1;
  END WHILE;
  COMMIT;
  SELECT b.Id, b.Title, b.Category, b.Description, b.AuthorId, b.Thumbnail, b.AdditionDate, b.IsPublic FROM tblBooks b
    WHERE b.Id IN (
      SELECT sm.Id
        FROM temp_tblSearchMatches sm
        GROUP BY sm.Id
        HAVING COUNT(sm.SearchTerm) = i - 1);
  DROP TEMPORARY TABLE IF EXISTS temp_tblSearchMatches;
END;
</code></pre>

<p>Modified method <strong>GetBooks</strong></p>

<pre><code>protected List&lt;Book&gt; GetBooks(Search search)
{
    var db = new ProjectDbContext();
    var books = db.Books;

    //var listTerms = search.SearchTerm.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries)
    //    .Where(s =&gt; s.Length &gt;= 3).ToList().ConvertAll(t =&gt; t.ToLower().Replace("|", ""));

    var paramSearchTerms = new MySqlParameter { ParameterName = "p_SearchTerms", Value = search.SearchTerm };
    var paramIncludeTitle = new MySqlParameter { ParameterName = "p_IncludeTitle", Value = search.IncludeTitle };
    var paramIncludeAuthor = new MySqlParameter { ParameterName = "p_IncludeAuthor", Value = search.IncludeAuthor };
    var paramIncludeCategory = new MySqlParameter { ParameterName = "p_IncludeCategory", Value = search.IncludeCategory };
    var paramIncludeDescription = new MySqlParameter { ParameterName = "p_IncludeDescription", Value = search.IncludeDescription };

    var searchedBooks = books
        .SqlQuery("CALL sp_SearchBooks(@p_SearchTerms, @p_IncludeTitle, @p_IncludeAuthor, @p_IncludeCategory, @p_IncludeDescription)", paramSearchTerms, paramIncludeTitle, paramIncludeAuthor, paramIncludeCategory, paramIncludeDescription);
        //.AsEnumerable().Where(book =&gt; CheckWhatToSearch(book, search, listTerms));

    var sortedBooks = searchedBooks.OrderBy(search.SortBy + " " + search.SortOrder.ToLower()); // dynamic LINQ query helper

    var pagedBooks = search.HowMuchSkip &gt;= 0 ? 
        sortedBooks.Skip(search.HowMuchSkip).Take(search.HowMuchTake) :
        Enumerable.Empty&lt;Book&gt;().AsQueryable();

    return pagedBooks.ToList(); 
}
</code></pre>

<p>But now, I am randomly getting error:</p>

<blockquote>
  <p>“Context cannot be used while the model is being created”</p>
</blockquote>

<p>during materializing in the last line of the method.or deadlock (it never reaches next line). And I am not entirely sure if I was able to mirror <strong>CheckWhatToSearch</strong> method functionality exactly.</p>

<p><strong>EDIT (24-12-2015)</strong></p>

<p>This is mysql server operation when I am using stored procedure:</p>

<pre><code>151224  0:38:17    44 Init DB   project
           44 Query CALL sp_SearchBooks('wła', 1, 1, 0, 0)
           44 Init DB   project
           44 Query SELECT
`Extent1`.`Id`, 
`Extent1`.`UserName`, 
`Extent1`.`Password`, 
`Extent1`.`Email`, 
`Extent1`.`RegistrationDate`, 
`Extent1`.`RetryAttempts`, 
`Extent1`.`IsLocked`, 
`Extent1`.`LockedDateTime`
FROM `tblUsers` AS `Extent1`
</code></pre>

<p>Why, and where the hell it is calling select to retrieve entire users table - I don't know. And I am still getting deadlocks.</p>

<p>Following your suggestion I have tried to implement it using Dynamic Expression but it has proven to be rather difficult, can you guys help me with this?</p>

<p>I have started with code below but I am stuck and I don't know how to properly write concatenation using Expressions. I am missing the point of this I guess cuz I am not sure when during mirroring my method I should use normal variables and methods, and where I should use Expressions (I guess, listterms and search could be left as they are and only things that are book related should be rewritten):</p>

<pre><code>// Parameter of the main predicate
ParameterExpression pe = Expression.Parameter(typeof(Book), "book");
LabelTarget returnTarget = Expression.Label(typeof(bool));

// if (book.IsPublic != true)
//     return false;
Expression ifBookNotPublic = Expression.IfThen(
    Expression.NotEqual(
        Expression.Property(pe, typeof(Book).GetProperty("IsPublic")),
        Expression.Constant(true)),
    Expression.Return(returnTarget, Expression.Constant(false)));

// if (listTerms.Count &lt;= 0)
//     return true;
Expression paramListTerms = Expression.Constant(listTerms);
Expression ifListTermsCountLessOrEqualThanZero = Expression.IfThen(
    Expression.LessThanOrEqual(
        Expression.Property(paramListTerms, typeof(List&lt;string&gt;).GetProperty("Count")),
        Expression.Constant(0, typeof(int))),
    Expression.Return(returnTarget, Expression.Constant(true)));

// listTerms.All(s =&gt; sbWhereToSearch.ToString().ToLower().Contains(s));
ParameterExpression pTerm = Expression.Parameter(typeof(string), "s");
Expression paramSearch = Expression.Constant(search);

// if (search.IncludeTitle)
//     sbWhereToSearch.Append(titleValue + " ");
Expression ifSearchIncludeTitleThenConcat = Expression.IfThen(
    Expression.Equal(
        Expression.Property(paramSearch, typeof(Search).GetProperty("IncludeTitle")),
        Expression.Constant(true)),
    Expression.WHAT NOW ? );


// ===================================
var exprBlock = Expression.Block(); // Expression Calls here
var searchedBooks = books.AsQueryable().Where(Expression.Lambda&lt;Func&lt;Book, bool&gt;&gt;(exprBlock, pe)); // book such as whole block returns true for it
</code></pre>

<p>I have tried another approach as well, I replaced predicate with anonymous function and it works actually, but for some unknown reason mysql log shows that I am retrieving both tables, despite the fact that Visual Studio shows my data as Queryable and materializes it in the last line only.</p>

## Answers
### Answer ID: 34379674
<p>Starting from the point that for EF + is a canonical function and Contains is a canonical function you could just create an expression tree where you have the sum of all the fields you need to check then apply the contains. You can do this inside C# + EF without using stored procedures.</p>

<p>Here you can find an example from Microsoft on how to build an expression tree on IQueryables</p>

<p><a href="https://msdn.microsoft.com/library/bb882637(v=vs.100).aspx" rel="nofollow">https://msdn.microsoft.com/library/bb882637(v=vs.100).aspx</a></p>

### Answer ID: 34376548
<p>Typically you'd want to write that function as a stored procedure, like you started to do. Which should get recognized by EF and allow you to use it as a method on your context.</p>

<p>However, you might be better off writing the GetBooks method as a stored procedure and just invoking that as the request comes in and returning the procedure results. That way the whole thing would get executed on the DB engine instead of on the web server.</p>

<p>The downside of that would be that you'll have a lot of arguments you'll be passing to the stored procedure which might make it a bit messy.</p>


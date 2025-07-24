# .NET build predicate with custom date format (not using client side). LinqKit
[Link to question](https://stackoverflow.com/questions/78587738/net-build-predicate-with-custom-date-format-not-using-client-side-linqkit)
**Creation Date:** 1717688507
**Score:** 0
**Tags:** c#, datetime, linqkit
## Question Body
<p>I don't know if this is possible.</p>
<p>I've been trying to implement a &quot;global filter&quot; that runs a &quot;like&quot; clause on the database engine and it varies a little bit depending on the column data type. To do so, I've been using <code>LinqKit</code>.</p>
<p>This is my current code. First of all, this is the global filter predicate builder:</p>
<pre><code>/// &lt;summary&gt;
/// Gets a global filter predicate for the specified property name, filter value, and filter data type.
/// &lt;/summary&gt;
/// &lt;typeparam name=&quot;T&quot;&gt;The type of entity.&lt;/typeparam&gt;
/// &lt;param name=&quot;propertyName&quot;&gt;The name of the property to filter on.&lt;/param&gt;
/// &lt;param name=&quot;filterValue&quot;&gt;The value to filter with.&lt;/param&gt;
/// &lt;param name=&quot;filterDataType&quot;&gt;The data type of the filter (text, numeric, date, boolean).&lt;/param&gt;
/// &lt;returns&gt;
/// An expression representing the filter predicate for the specified property and filter value.
/// Returns null if the data type is not supported.
/// &lt;/returns&gt;
/// &lt;exception cref=&quot;ArgumentException&quot;&gt;Thrown when the filterDataType is not supported.&lt;/exception&gt;
private static Expression&lt;Func&lt;T, bool&gt;&gt;? GetGlobalFilterPredicate&lt;T&gt;(string propertyName, string filterValue, string filterDataType) {
    Expression&lt;Func&lt;T, bool&gt;&gt;? predicate = null; // Initialize the predicate as null
    ParameterExpression parameter = Expression.Parameter(typeof(T), &quot;x&quot;); // Create an expression parameter to represent the generic entity T
    MemberExpression property = Expression.Property(parameter, propertyName); // Get the specific property of the entity using the provided property name
    if(filterDataType == &quot;text&quot; || filterDataType == &quot;numeric&quot; || filterDataType == &quot;date&quot;) { // Check the filter data type, if it's text, numeric, or date, call method to create a filter predicate
        predicate = CreateTextFilterPredicate&lt;T&gt;(property, filterValue, &quot;contains&quot;);
    } else if (filterDataType != &quot;boolean&quot;) { // If the filter data type is not text, numeric, date or boolean, throw an exception
        throw new ArgumentException(&quot;Invalid filterDataType value&quot;, nameof(filterDataType));
    }
    return predicate; // Return the predicate (may be null if the data type is not supported)
}
</code></pre>
<p>As you can see from the above code, if my <code>filterDataType</code> is date (the one I'm having issues with), it will call the <code>CreateTextFilterPredicate</code>. The function called is as follows:</p>
<pre><code>private static Expression&lt;Func&lt;T, bool&gt;&gt; CreateTextFilterPredicate&lt;T&gt;(MemberExpression property, string filterValue, string matchMode = &quot;contains&quot;) {
    #region PREPARE THE toStringMethod
    Expression toStringMethod; // Prepare the method to convert the property to a string if necessary
    bool isStringProperty = property.Type == typeof(string) || Nullable.GetUnderlyingType(property.Type) == typeof(string); // Check if the property type is a string or nullable string
    bool isDateTimeProperty = property.Type == typeof(DateTime) || Nullable.GetUnderlyingType(property.Type) == typeof(DateTime); // Check if the property type is DateTime or nullable DateTime
    if(isStringProperty) { // If the property is a string (or nullable string)
        toStringMethod = property; // Get the property as is, its already a string
    } else if(isDateTimeProperty) { // If the property is DateTime (or nullable DateTime)
        toStringMethod = Expression.Call(property, &quot;ToString&quot;, null); // We need to cast ToString
    } else { // The property is not a string
        toStringMethod = Expression.Call(property, &quot;ToString&quot;, null); // We need to cast ToString
    }
    #endregion
    MethodCallExpression toUpperMethod = Expression.Call(toStringMethod, &quot;ToUpper&quot;, null); // Convert property string to uppercase (for case insensitive search)
    filterValue = filterValue.ToUpper(); // Convert filter value to uppercase (for case insensitive search)
    dynamic matchModeCheck = matchMode switch { // Create the predicate based on the match mode
        &quot;startsWith&quot; =&gt; Expression.Call(toUpperMethod, &quot;StartsWith&quot;, null, Expression.Constant(filterValue)),
        &quot;contains&quot; =&gt; Expression.Call(toUpperMethod, &quot;Contains&quot;, null, Expression.Constant(filterValue)),
        &quot;notContains&quot; =&gt; Expression.Not(Expression.Call(toUpperMethod, &quot;Contains&quot;, null, Expression.Constant(filterValue))),
        &quot;endsWith&quot; =&gt; Expression.Call(toUpperMethod, &quot;EndsWith&quot;, null, Expression.Constant(filterValue)),
        &quot;equals&quot; =&gt; Expression.Equal(toUpperMethod, Expression.Constant(filterValue)),
        &quot;notEquals&quot; =&gt; Expression.NotEqual(toUpperMethod, Expression.Constant(filterValue)),
        _ =&gt; throw new ArgumentException(&quot;Invalid filtering option value for text predicate&quot;, nameof(matchMode)),
    };
    #region PREPARE THE predicateBody
    dynamic predicateBody; // Prepare the predicate body
    if(isStringProperty) { // If filterDataType is text
        BinaryExpression nullCheck = Expression.NotEqual(property, Expression.Constant(null)); // Prepare binary expression to check for null values
        predicateBody = Expression.AndAlso(nullCheck, matchModeCheck); // Combine null check and string matching conditions using AndAlso
    } else {// If filterDataType is not text
        predicateBody = matchModeCheck; // Just use the matching conditions
    }
    #endregion
    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(predicateBody, property.Expression as ParameterExpression); // Create and return the lambda expression
}
</code></pre>
<p>My current code works if I want to search a string in the format <code>yyyy-mm-dd hh:mm:ss</code>. What I'm stuck with is trying to specify a custom date conversion that takes into account the culture. For example, I would like to specify that the date format for comparison should be <code>dd-mmm-yyyy hh:mm:ss</code> in the en-us culture.</p>
<p>I've tried, for example, this at the beginning in the case of <code>if(isDateTimeProperty)</code> (still not implementing the culture, but just to test the date conversion):</p>
<pre><code>var dateTimeFormat = Expression.Constant(&quot;dd-MMM-yyyy HH:mm:ss&quot;); // Specify the desired date format
toStringMethod = Expression.Call(property, &quot;ToString&quot;, null, dateTimeFormat);
</code></pre>
<p>However if gives me the following error:</p>
<blockquote>
<p>&quot;An unexpected error occurred: The LINQ expression 'DbSet()\r\n    .OrderBy(t =&gt; t.LocationDesignation)\r\n    .Where(t =&gt; t.LocationDesignation != null &amp;&amp; t.LocationDesignation.ToUpper().Contains(&quot;0&quot;) || t.DateCreated.ToString(&quot;dd-MMM-yyyy HH:mm:ss&quot;).ToUpper().Contains(&quot;0&quot;))' could not be translated. Additional information: Translation of method 'System.DateTime.ToString' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information.\r\nTranslation of method 'System.DateTime.ToString' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;</p>
</blockquote>
<p>Is there a way to achieve what I want without doing a client side evaluation?</p>
<p><strong>Example of the use case</strong></p>
<p>Its a table were the user in the frontend the user sees the date with a mask. The global filter should search in the date column taking into account that date mask.
<a href="https://i.sstatic.net/MB3jrb8p.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/MB3jrb8p.png" alt="enter image description here" /></a></p>
<p>Thanks in advance!</p>


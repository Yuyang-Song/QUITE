# LINQ query optimization for slow grouping
[Link to question](https://stackoverflow.com/questions/26926526/linq-query-optimization-for-slow-grouping)
**Creation Date:** 1415956584
**Score:** 3
**Tags:** c#, linq, entity-framework, repository-pattern
## Question Body
<p>I have a LINQ query that gets data via Entity Framework Code First from an SQL database. This works, but it works very very slow. </p>

<p>This is the original query:</p>

<pre><code>      var tmpResult = from mdv in allMetaDataValues
                  where mdv.Metadata.InputType == MetadataInputType.String &amp;&amp; mdv.Metadata.ShowInFilter &amp;&amp; !mdv.Metadata.IsHidden &amp;&amp; !string.IsNullOrEmpty(mdv.ValueString)
                  group mdv by new
                  {
                    mdv.ValueString,
                    mdv.Metadata
                  } into g
                  let first = g.FirstOrDefault()
                  select new
                  {
                    MetadataTitle = g.Key.Metadata.Title,
                    MetadataID = g.Key.Metadata.ID,
                    CollectionColor = g.Key.Metadata.Collection.Color,
                    CollectionID = g.Key.Metadata.Collection.ID,

                    MetadataValueCount = 0,
                    MetadataValueTitle = g.Key.ValueString,
                    MetadataValueID = first.ID
                  };
</code></pre>

<p>This is the generated SQL from the original query:</p>

<pre><code>{SELECT 
0 AS [C1], 
[Project4].[Title] AS [Title], 
[Project4].[ID] AS [ID], 
[Extent9].[Color] AS [Color], 
[Project4].[Collection_ID] AS [Collection_ID], 
[Project4].[ValueString] AS [ValueString], 
[Project4].[C1] AS [C2]
FROM   (SELECT 
    [Project2].[ValueString] AS [ValueString], 
    [Project2].[ID] AS [ID], 
    [Project2].[Title] AS [Title], 
    [Project2].[Collection_ID] AS [Collection_ID], 
    (SELECT TOP (1) 
        [Filter4].[ID1] AS [ID]
        FROM ( SELECT [Extent6].[ID] AS [ID1], [Extent6].[ValueString] AS [ValueString], [Extent7].[Collection_ID] AS [Collection_ID1], [Extent8].[ID] AS [ID2], [Extent8].[InputType] AS [InputType], [Extent8].[ShowInFilter] AS [ShowInFilter], [Extent8].[IsHidden] AS [IsHidden1]
            FROM   [dbo].[MetadataValue] AS [Extent6]
            LEFT OUTER JOIN [dbo].[Media] AS [Extent7] ON [Extent6].[Media_ID] = [Extent7].[ID]
            INNER JOIN [dbo].[Metadata] AS [Extent8] ON [Extent6].[Metadata_ID] = [Extent8].[ID]
            WHERE ( NOT (([Extent6].[ValueString] IS NULL) OR (( CAST(LEN([Extent6].[ValueString]) AS int)) = 0))) AND ([Extent7].[IsHidden] &lt;&gt; cast(1 as bit))
        )  AS [Filter4]
        WHERE (2 =  CAST( [Filter4].[InputType] AS int)) AND ([Filter4].[ShowInFilter] = 1) AND ([Filter4].[IsHidden1] &lt;&gt; cast(1 as bit)) AND ([Filter4].[Collection_ID1] = @p__linq__0) AND (([Project2].[ValueString] = [Filter4].[ValueString]) OR (([Project2].[ValueString] IS NULL) AND ([Filter4].[ValueString] IS NULL))) AND (([Project2].[ID] = [Filter4].[ID2]) OR (1 = 0))) AS [C1]
    FROM ( SELECT 
        [Distinct1].[ValueString] AS [ValueString], 
        [Distinct1].[ID] AS [ID], 
        [Distinct1].[Title] AS [Title], 
        [Distinct1].[Collection_ID] AS [Collection_ID]
        FROM ( SELECT DISTINCT 
            [Filter2].[ValueString] AS [ValueString], 
            [Filter2].[ID3] AS [ID], 
            [Filter2].[InputType1] AS [InputType], 
            [Filter2].[Title1] AS [Title], 
            [Filter2].[ShowInFilter1] AS [ShowInFilter], 
            [Filter2].[IsHidden2] AS [IsHidden], 
            [Filter2].[Collection_ID2] AS [Collection_ID]
            FROM ( SELECT [Filter1].[ValueString], [Filter1].[Collection_ID3], [Filter1].[IsHidden3], [Filter1].[ID3], [Filter1].[InputType1], [Filter1].[Title1], [Filter1].[ShowInFilter1], [Filter1].[IsHidden2], [Filter1].[Collection_ID2]
                FROM ( SELECT [Extent1].[ValueString] AS [ValueString], [Extent2].[Collection_ID] AS [Collection_ID3], [Extent4].[IsHidden] AS [IsHidden3], [Extent5].[ID] AS [ID3], [Extent5].[InputType] AS [InputType1], [Extent5].[Title] AS [Title1], [Extent5].[ShowInFilter] AS [ShowInFilter1], [Extent5].[IsHidden] AS [IsHidden2], [Extent5].[Collection_ID] AS [Collection_ID2]
                    FROM     [dbo].[MetadataValue] AS [Extent1]
                    LEFT OUTER JOIN [dbo].[Media] AS [Extent2] ON [Extent1].[Media_ID] = [Extent2].[ID]
                    INNER JOIN [dbo].[Metadata] AS [Extent3] ON [Extent1].[Metadata_ID] = [Extent3].[ID]
                    LEFT OUTER JOIN [dbo].[Metadata] AS [Extent4] ON [Extent1].[Metadata_ID] = [Extent4].[ID]
                    LEFT OUTER JOIN [dbo].[Metadata] AS [Extent5] ON [Extent1].[Metadata_ID] = [Extent5].[ID]
                    WHERE ( NOT (([Extent1].[ValueString] IS NULL) OR (( CAST(LEN([Extent1].[ValueString]) AS int)) = 0))) AND ([Extent2].[IsHidden] &lt;&gt; cast(1 as bit)) AND (2 =  CAST( [Extent3].[InputType] AS int)) AND ([Extent3].[ShowInFilter] = 1)
                )  AS [Filter1]
                WHERE [Filter1].[IsHidden3] &lt;&gt; cast(1 as bit)
            )  AS [Filter2]
            WHERE [Filter2].[Collection_ID3] = @p__linq__0
        )  AS [Distinct1]
    )  AS [Project2] ) AS [Project4]
LEFT OUTER JOIN [dbo].[Collection] AS [Extent9] ON [Project4].[Collection_ID] = [Extent9].[ID]}
</code></pre>

<p>If we remove the "<strong>let first = g.FirstOrDefault()</strong>" and change "<strong>MetadataValueID = first.ID</strong>" to "<strong>MetadataValueID = 0</strong>" so that we just have a fixed ID = 0 for testing purposes, then the data loads very fast and the generated query itself is half the size compared to the original
So it seems that this part is making the query very slow:</p>

<pre><code>let first = g.FirstOrDefault()
...
  MetadataValueID = first.ID
};
</code></pre>

<p>How can this be rewritten? 
If I try to rewrite the code, it is still slow:</p>

<pre><code>MetadataValueID = g.Select(x =&gt; x.ID).FirstOrDefault()
</code></pre>

<p>or</p>

<pre><code>let first = g.Select(x =&gt; x.ID).FirstOrDefault()
...
  MetadataValueID = first
};
</code></pre>

<p>Any suggestions?</p>

## Answers
### Answer ID: 26927229
<p>Using EF I have allways felt that it has problems efficiently translating stuff like <code>g.Key.Metadata.Collection</code>, so I try to join more explicitly and to include only fields, that are neccessary for your result. You can use <code>include</code> instead of join using repository pattern.</p>

<p>Then your query would look like this:</p>

<pre><code>   from mdv in allMetaDataValues.Include("Metadata").Include("Metadata.Collection")
   where mdv.Metadata.InputType == MetadataInputType.String &amp;&amp; 
         mdv.Metadata.ShowInFilter &amp;&amp; 
         !mdv.Metadata.IsHidden &amp;&amp; 
         !string.IsNullOrEmpty(mdv.ValueString)
   group mdv by new
   {
     MetadataID = mdv.Metadata.ID,
     CollectionID = mdv.Metadata.Collection.ID,
     mdv.Metadata.Title,
     mdv.Metadata.Collection.Color,
     mdv.ValueString
   } into g
   let first = g.FirstOrDefault().ID
   select new
   {
     MetadataTitle = g.Key.Title,
     MetadataID = g.Key.MetadataID,
     CollectionColor = g.Key.Color,
     CollectionID = g.Key.CollectionID,
     MetadataValueCount = 0,
     MetadataValueTitle = g.Key.ValueString,
     MetadataValueID = first
   }
</code></pre>

<p>Good tool for playing with linq is <a href="http://www.linqpad.net" rel="nofollow noreferrer">LinqPad</a>. </p>

<p>The problem is also that: </p>

<pre><code>  let first = g.FirstOrDefault().ID
</code></pre>

<p>cannot be easily translated to SQL see <a href="https://stackoverflow.com/questions/3800551/select-first-row-in-each-group-by-group">this answer</a>. But this rewrite simplifies the underlying query for it at least. It remains to me unclear, why you need first ID from a set without using <code>orderby</code>.</p>

<p>It could be rewriten like this:</p>

<pre><code>let first =  (from f in allMetaDataValues
              where f.Metadata.ID == g.Key.MetadataID &amp;&amp; 
                    f.ValuesString == g.Key.ValuesString select f.ID)
             .FirstOrDefault()
</code></pre>

<p>This way you do not let EF write the query for you and you can specify exactly how to do the select.
To speed up the query you can also consider adding indexes to database according to the generated query - namely index using both colums used in where clause of this <code>let first</code> query.</p>

### Answer ID: 26928134
<p>Try the following solution.<br>
 Replace <code>FirstOrDefault()</code> with <code>.Take(1)</code>.       <code>FirstOrDefault()</code> is not lazy loaded. </p>

<pre><code>var tmpResult = from mdv in allMetaDataValues
                  where mdv.Metadata.InputType == MetadataInputType.String &amp;&amp; mdv.Metadata.ShowInFilter &amp;&amp; !mdv.Metadata.IsHidden &amp;&amp; !string.IsNullOrEmpty(mdv.ValueString)
                  group mdv by new
                  {
                    mdv.ValueString,
                    mdv.Metadata
                  } into g
                  let first = g.Take(1)
                  select new
                  {
                    MetadataTitle = g.Key.Metadata.Title,
                    MetadataID = g.Key.Metadata.ID,
                    CollectionColor = g.Key.Metadata.Collection.Color,
                    CollectionID = g.Key.Metadata.Collection.ID,

                    MetadataValueCount = 0,
                    MetadataValueTitle = g.Key.ValueString,
                    MetadataValueID = first.ID
                  };
</code></pre>


# XQuery - Search within XML Column in Table
[Link to question](https://stackoverflow.com/questions/8577975/xquery-search-within-xml-column-in-table)
**Creation Date:** 1324395653
**Score:** 0
**Tags:** sql, xml, sql-server-2008, xquery
## Question Body
<p>Please find the following query that is being used to search for keyword in a database xml column</p>

<p>The shown query is being used to search for Name,word or brief from an xml column in SQL Server. The CMS in use is Umbraco.</p>

<p>The query was designed initially when the data was limited.</p>

<p>Now the database has millions of  records and the query times out unable to fetch data.
The query also prioritizes the order in which the search results are retrieved as 
in if the Name field data search result is returned the CASE 1 is returned else 
depending on the search data is returned</p>

<pre><code>     SELECT Name,word,brief,              */Selecting Values */
     CASE
       WHEN Name  like '%' THEN 1       */Prioritizing Order in which data to be seen */
     WHEN word  like '%' THEN 2
     WHEN brief like '%' THEN 3
     END AS Search
  from
      (select                                 
            A.xml.value('(//@node)[1]','nvarchar(20)') as Name,   /* XQuery */    
          A.xml.value('(//word)[1]','nvarchar(225)') as word,
          A.xml.value('(//brief)[1]','nvarchar(max)')as brief
  from 
         (Select Convert(xml, xml) AS XML 
          from [dbo].[cmsContentXml]) AS B
          Cross Apply xml.nodes('//items/item') AS A(xml)) D  
        where  ((Name like '%')                                   /*Condition */
               OR(word like '%')   
               OR(brief like '%'))
          group by word,Name,brief
      order by 3 ASC
</code></pre>

<p>Please help with a solution on optimizing or rewriting this query to search for data in the xml column. Also apart from retrieving data from the column.</p>

<p>When in the front end the search button is clicked without entering any keyword the click operation has to retrieve all the items from the database.</p>

<p>Thanks in advance</p>

## Answers
### Answer ID: 8594027
<p>First, don't allow a search with no keyword, direct the user to a browse mechanism instead. There's no point in having the overhead of a search query if there's nothing to search for.</p>

<p>Second, Select Convert(xml, xml) is unnecessary overhead, your database column should be xml if it's storing xml. Having the column with an xml type also allows you to put xml indexes on it which will help speed things up. See <a href="http://msdn.microsoft.com/en-us/library/ms191497.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/ms191497.aspx</a> for more information on XML Indexes. Also, without the conversion you no longer need to keep that as a subquery.</p>

<p>Third don't use the ORDER BY 3 syntax, use the column name. ORDER BY 3 is not ANSI standard and also can cause maintainability problems.</p>

<p>Fourth, your xml sample data appears to be invalid xml (an unclosed data tag for brief, no closing element for id, no opening element for block). Please check your data, if it's actually broken like that in the real database, it will need to be fixed as bad xml does slow down the node searches.</p>

<p>Fifth, avoid single letter aliases, it's another maintainability issue.</p>


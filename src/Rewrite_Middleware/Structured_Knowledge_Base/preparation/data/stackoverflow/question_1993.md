# Oracle query using Entity Framework is ridiculously slow
[Link to question](https://stackoverflow.com/questions/14886120/oracle-query-using-entity-framework-is-ridiculously-slow)
**Creation Date:** 1360885590
**Score:** 7
**Tags:** c#, linq, oracle-database, entity-framework
## Question Body
<p>Here is my setup:</p>

<ul>
<li>Compiling at .NET 4.0 (I can't go any higher than this)</li>
<li>Using EntityFramework against Oracle 11gR2 database</li>
<li>Using ODP.NET 11.2.0.3.20</li>
<li>Using Visual Studio 2012 Ultimate and <a href="http://www.oracle.com/technetwork/developer-tools/visual-studio/overview/index.html" rel="noreferrer">Oracle Developer Tools for Visual Studio</a> 11.2.0.3.20</li>
<li>Performing queries using LINQ to Entity</li>
</ul>

<p>So here's my problem: I have some entities that I've created with Oracle Developer Tools for Visual Studio (11.2.0.3.20). Some of the entities return results fairly quickly. However, with others that are querying against a view/table that contains more than 20 million records, it is consistently taking <strong>10 minutes to return results</strong> (I've verified this time via unit tests) for this simple query:</p>

<pre><code>var member = (from m in context.Members
              where m.MemberID.Equals(memberId, StringComparison.OrdinalIgnoreCase)
              select m).FirstOrDefault();
</code></pre>

<p>I used to be using <a href="http://www.devart.com/dotconnect/oracle/" rel="noreferrer">Devart dotConnect for Oracle</a> which worked really well...but my company isn't renewing their license for this product and have told me to use the new Oracle Developer Tools for Visual Studio to accomplish things.</p>

<p>As a work around, I've made a direct connection to the database using <code>OracleCommand</code> provided by ODP.NET (Oracle.DataAccess.dll) and I get results back in less than a second. Same with doing other queries directly against the database using a management client.</p>

<p>My best guess as to why this is happening would be that perhaps Entity is loading the entire database into memory and then running my queries on it...which would be horrible, but I really don't believe that is what is happening.</p>

<p><strong>Can someone please explain why this is happening and how I can fix it using Entity so that I don't have to manually rewrite all of my DB queries?</strong>
<br/>
<br/>
<br/>
<strong>UPDATE:</strong>
<br/>
So I found the reason that my queries were taking 10 minutes to complete. I (with my very little experience with databases) had put this in my EDMX file:</p>

<pre><code>...
&lt;EntityContainer Name="MyStoreContainer"&gt;
  &lt;EntitySet Name="MY_TABLE" EntityType="MyDB.Store.MY_TABLE" store:Type="Views" store:Schema="MYUSERNAME" store:Name="MY_TABLE"&gt;
    &lt;DefiningQuery&gt;
      SELECT
      "MY_TABLE"."COL1" AS "COL1",
      "MY_TABLE"."COL2" AS "COL2",
      "MY_TABLE"."COL3" AS "COL3",
      "MY_TABLE"."COL4" AS "COL4",
      "MY_TABLE"."COL5" AS "COL5",
      "MY_TABLE"."COL6" AS "COL6",
      "MY_TABLE"."MEMBERSHIP_ID" AS "MEMBERSHIP_ID",
      "MEMBERS"."EXTRA_INFO1" AS "EXTRA_INFO1",
      "MEMBERS"."EXTRA_INFO2" AS "EXTRA_INFO2"
      FROM "MYUSERNAME"."MY_TABLE" "MY_TABLE"
      LEFT JOIN "MYUSERNAME"."MEMBERS" ON "MY_TABLE"."MEMBERSHIP_ID" = "MEMBERS"."MEMBER_ID"
    &lt;/DefiningQuery&gt;
  &lt;/EntitySet&gt;
...
</code></pre>

<p>Turns out that the <code>LEFT JOIN</code> takes about 10 minutes when directly querying with a management client as well. So I took the <code>LEFT JOIN</code> out...and now I see an increase in speed. Here's the catch, this EntitySet was NOT the EntitySet that I was querying against when I was getting really slow responses. I still get a response about 4-5 times faster if I manually write the code with <code>OracleCommand</code>.
<br/>
<strong>Can anyone explain why Entity is slowing things down so much and when I am not even accessing this left join query?</strong></p>

## Answers
### Answer ID: 41988066
<p>We had a similar performance issue. Thanks @CameronP for the suggestion to use the EntityFunctions.AsNonUnicode, which fixed the performance issue.  Our project uses EF6 with Oracle 12.1* Managed Data Access. Instead of making the change to every EF query parameter, we used the TypeName attribute on the Entity Model and it worked !</p>

<pre><code>Public Class Table1
    &lt;Column("COLUMN_1", TypeName:="VARCHAR2")&gt;
    Public Property Column1 As String
End Class 
</code></pre>

### Answer ID: 41040473
<p>An other solution is to update your oracle provider!
Odac 12c fix this problem : <a href="https://community.oracle.com/message/11065799#11065799" rel="nofollow noreferrer">https://community.oracle.com/message/11065799#11065799</a></p>

<p>It will prevent you from changing all your query with EntityFunctions.AsNonUnicode()</p>

### Answer ID: 36727321
<p>Another trick is to disable Lazy Loading.</p>

<p>If you can disable, do it.</p>

<p>Example when you can't disable Lazy Loading:</p>

<p>When you have a table called Customers. Then, when you call something like this:</p>

<pre><code>var obj = myCustomerList.FirstOrDefault().ORDERS.ToList()
</code></pre>

<p>If you have code that access childrens, you can't disable the Lazy Loading</p>

### Answer ID: 25922164
<p>Wrap your input parameter with <code>EntityFunctions.AsNonUnicode(memberId)</code>.</p>

<pre><code>var member = (from m in context.Members
          where m.MemberID.Equals(EntityFunctions.AsNonUnicode(memberId), StringComparison.OrdinalIgnoreCase)
          select m).FirstOrDefault();
</code></pre>

<p>See <a href="https://community.oracle.com/message/10725648">https://community.oracle.com/message/10725648</a></p>


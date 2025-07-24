# Match int column on two different numbers
[Link to question](https://stackoverflow.com/questions/43627846/match-int-column-on-two-different-numbers)
**Creation Date:** 1493192274
**Score:** 0
**Tags:** sql, sql-server, azure-sql-database
## Question Body
<p>I have an tag table in my MS SQL database where i have specified a "TagType" column that are a smallint, it can have the values 0,1,2,3 and all of them have different meanings and there can obviously only be one since there is only one column. Now i have a requirement that stuff should be able to have two TagTypes at once.</p>

<p>So for example an item should be able to have both 2 and 3 at the same time. And since i only have one column it's of course not possible. It's not that hard for me to introduce new type likes "4" and make that mean 2 OR 3. But i really do not want to rewrite all my queries that are dependent on checking if something is 2 or 3 I just want them to match.</p>

<p>What i want is to be able to do is to have a query that says "WHERE TagType = 3" and if the value in the column is for example "4" or "23" it would match that, i'm not sure how but maybe there is some smart feature somewhere that can do this?</p>

## Answers
### Answer ID: 43627955
<p>The natural representation of multiple values of the same type in SQL is to continue to use one column but to use <em>multiple rows</em>. If you're changing the multiplicity of a column, you would frequently discover that you need to create a new table that then allows you to have a many-to-one relationship back to the original table.</p>

<p>This will require schema changes and some updates to existing code, but anything else will be a fudge.</p>

<p>So, we go from:</p>

<pre><code>CREATE TABLE T1 (
  ID int not null primary key,
  Col1 varchar(19) not null,
  TagType smallint
)
</code></pre>

<p>to:</p>

<pre><code>CREATE TABLE T1 (
  ID int not null primary key,
  Col1 varchar(19) not null
)

CREATE TABLE T1Tags (
  T1ID int not null,
  TagType smallint not null,
  constraint PK_T1Tags PRIMARY KEY (T1ID,TagType),
  constraint FK_T1Tags_T1 FOREIGN KEY (T1ID)
     references T1(ID)
)
</code></pre>


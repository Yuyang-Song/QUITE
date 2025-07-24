# SQLiteDatabase select with dynamic number of conditions
[Link to question](https://stackoverflow.com/questions/17316640/sqlitedatabase-select-with-dynamic-number-of-conditions)
**Creation Date:** 1372239756
**Score:** 1
**Tags:** sql, sqlite, select, join
## Question Body
<p>I am new to databases, so it might be it is very easy.
I have the following database structure:
<strong>Table products</strong></p>

<p><strong>Table filters</strong> (could contain something like)</p>

<ul>
<li>Color blue </li>
<li>Color black </li>
<li>Color red </li>
<li>Size small </li>
<li>Brand X</li>
</ul>

<p><strong>Table relation</strong> (has only product id and filter id)</p>

<p>Lets say I want to obtain all products that are black or red and are small, I wrote the following query: </p>

<pre><code>SELECT products.name FROM products 
JOIN pfrelation ON
    ((pfrelation.filter_id=18) AND (pfrelation.filter_id=11 OR pfrelation.filter_id=13) AND products.id=pfrelation.product_id) 
</code></pre>

<p>In the the example above 11 and 13 represent black and red, while 18 is the id for small. As you might suspect the above query has no results (the id can not be both 18 and 11/13). How can I write the select in order to dynamically add any combination of filters? How can I rewrite the query in the example above?</p>

<p>Thank you</p>

## Answers
### Answer ID: 17319326
<p>I build the query dynamically this way:</p>

<pre><code>public ArrayList&lt;Products&gt; getFilteredOnlinePictures( Hashtable&lt;String, List&lt;String&gt;&gt; filters,..)
{
    SQLiteDatabase db = getWritableDatabase();
    // create query conditions
    StringBuffer filtersQuery = new StringBuffer();
    for (String key: Collections.list(filters.keys()))
    {
        List&lt;String&gt; filtersValues = filters.get(key);
        if (filtersQuery.length() &gt; 0)
            filtersQuery.append(" INTERSECT ");
        filtersQuery.append("SELECT " + TABLE_PFRELATIONS + "." + COLUMN_PRODUCT_ID
            + " FROM " + TABLE_PFRELATIONS + " WHERE " + TABLE_PFRELATIONS + "."
            + COLUMN_FILTER_ID + " IN (");
        for (String value: filtersValues)
        {
            long filterID = getIDForFilter(db, key, value);
            filtersQuery.append(filterID);
            if (filtersValues.indexOf(value) == (filtersValues.size() - 1))
            {
                // this is the last value
                filtersQuery.append(")");
            }
            else
            {
                // there are more values
                filtersQuery.append(",");
            }

        }
    }
    if (filtersQuery.length() &gt; 0)
    {
        filtersQuery.append(")");
        filtersQuery.insert(0, " WHERE " + TABLE_PRODUCTS + ".id" + " IN (");
    }
    String sql = "SELECT " + TABLE_PRODUCTS + "." + COLUMN_NAME + " FROM " + TABLE_PRODUCTS + filtersQuery.toString();
    Cursor c = db.rawQuery(sql, null); ...
</code></pre>

<p>The query given as an example will be:</p>

<pre><code>SELECT products.name FROM products
WHERE products.id IN (
    SELECT pfrelation.product_id FROM pfrelation WHERE pfrelation.filter_id IN (18) 
    INTERSECT 
    SELECT pfrelation.product_id FROM pfrelation WHERE pfrelation.filter_id IN (11,13)
    ) 
</code></pre>

<p>This way I could have any filter with any number of values.</p>

### Answer ID: 17319062
<p>you can achieve this with Dynamic Query.
I don't much know about PostgreSql, but I know SQL Server, so I am giving a example to do same.</p>

<p><a href="http://sqlfiddle.com/#!3/692bb/3" rel="nofollow">Here is SQLFiddel Demo</a></p>

<pre><code>Create table Product(pid int,name varchar(10),color varchar(10),brand varchar(10),size varchar(10));
insert into product values(1,'ABC','red','X','small');
create table pfrelation(pid int,fid int,relation varchar(100));
insert into pfrelation values(1,10,'Color=''blue''');
insert into pfrelation values(1,11,'Color=''black''');
insert into pfrelation values(1,13,'Color=''red''');
insert into pfrelation values(1,18,'size=''small''');
insert into pfrelation values(1,20,'brand=''X''');

Declare @sql varchar(200)

select @sql = ((select 'pr.' + relation from pfrelation where fid = 18) 
   + ' and (' + 
(select 'pr.' + relation from pfrelation where fid = 11) 
   + ' or '   + 
(select 'pr.' + relation from pfrelation where fid = 13) 
   + ') and pr.pid=pf.pid' ) 
select @sql
print('select * from Product pr,pfrelation pf where '+@sql)
exec('select * from Product pr,pfrelation pf where '+@sql)
</code></pre>


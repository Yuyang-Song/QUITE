# How to prevent duplicate records being inserted with SqlBulkCopy when there is no primary key
[Link to question](https://stackoverflow.com/questions/2593689/how-to-prevent-duplicate-records-being-inserted-with-sqlbulkcopy-when-there-is-n)
**Creation Date:** 1270653747
**Score:** 19
**Tags:** c#, sql, sql-server, sql-server-2008, sqlbulkcopy
## Question Body
<p>I receive a daily XML file that contains thousands of records, each being a business transaction that I need to store in an internal database for use in reporting and billing.
I was under the impression that each day's file contained only unique records, but have discovered that my definition of unique is not exactly the same as the provider's. </p>

<p>The current application that imports this data is a C#.Net 3.5 console application, it does so using SqlBulkCopy into a MS SQL Server 2008 database table where the columns exactly match the structure of the XML records. Each record has just over 100 fields, and there is no natural key in the data, or rather the fields I can come up with making sense as a composite key end up also having to allow nulls. Currently the table has several indexes, but no primary key.</p>

<p>Basically the entire row needs to be unique. If one field is different, it is valid enough to be inserted. I looked at creating an MD5 hash of the entire row, inserting that into the database and using a constraint to prevent SqlBulkCopy from inserting the row,but I don't see how to get the MD5 Hash into the BulkCopy operation and I'm not sure if the whole operation would fail and roll back if any one record failed, or if it would continue.</p>

<p>The file contains a very large number of records, going row by row in the XML, querying the database for a record that matches all fields, and then deciding to insert is really the only way I can see being able to do this. I was just hoping not to have to rewrite the application entirely, and the bulk copy operation is so much faster.</p>

<p>Does anyone know of a way to use SqlBulkCopy while preventing duplicate rows, without a primary key? Or any suggestion for a different way to do this?</p>

## Answers
### Answer ID: 13997080
<p>Why not simply use, instead of a <strong>Primary Key</strong>, create an <strong>Index</strong> and set</p>

<pre><code>Ignore Duplicate Keys: YES
</code></pre>

<p>This will <a href="http://msdn.microsoft.com/en-us/library/ms186869.aspx" rel="noreferrer">prevent any duplicate key to fire an error</a>, and it will not be created (as it exists already).</p>

<p><img src="https://i.sstatic.net/eRMkG.png" alt="enter image description here"></p>

<p>I use this method to insert around 120.000 rows per day and works flawlessly.</p>

### Answer ID: 4471392
<p>I think this is a lot cleaner.             </p>

<pre><code>var dtcolumns = new string[] { "Col1", "Col2", "Col3"};

var dtDistinct = dt.DefaultView.ToTable(true, dtcolumns);

using (SqlConnection cn = new SqlConnection(cn) 
{
                copy.ColumnMappings.Add(0, 0);
                copy.ColumnMappings.Add(1, 1);
                copy.ColumnMappings.Add(2, 2);
                copy.DestinationTableName = "TableNameToMapTo";
                copy.WriteToServer(dtDistinct );

}
</code></pre>

<p>This way only need one database table and can keep Bussiness Logic in code.</p>

### Answer ID: 2597536
<p>Given that you're using SQL 2008, you have two options to solve the problem easily without needing to change your application much (if at all).</p>

<p>The first possible solution is create a second table like the first one but with a surrogate identity key and a uniqueness constraint added using the ignore_dup_key option which will do all the heavy lifting of eliminating the duplicates for you.</p>

<p>Here's an example you can run in SSMS to see what's happening:</p>

<pre><code>if object_id( 'tempdb..#test1' ) is not null drop table #test1;
if object_id( 'tempdb..#test2' ) is not null drop table #test2;
go


-- example heap table with duplicate record

create table #test1
(
     col1 int
    ,col2 varchar(50)
    ,col3 char(3)
);
insert #test1( col1, col2, col3 )
values
     ( 250, 'Joe''s IT Consulting and Bait Shop', null )
    ,( 120, 'Mary''s Dry Cleaning and Taxidermy', 'ACK' )
    ,( 250, 'Joe''s IT Consulting and Bait Shop', null )    -- dup record
    ,( 666, 'The Honest Politician', 'LIE' )
    ,( 100, 'My Invisible Friend', 'WHO' )
;
go


-- secondary table for removing duplicates

create table #test2
(
     sk int not null identity primary key
    ,col1 int
    ,col2 varchar(50)
    ,col3 char(3)

    -- add a uniqueness constraint to filter dups
    ,constraint UQ_test2 unique ( col1, col2, col3 ) with ( ignore_dup_key = on )
);
go


-- insert all records from original table
-- this should generate a warning if duplicate records were ignored

insert #test2( col1, col2, col3 )
select col1, col2, col3
from #test1;
go
</code></pre>

<p>Alternatively, you can also remove the duplicates in-place without a second table, but the performance may be too slow for your needs. Here's the code for that example, also runnable in SSMS:</p>

<pre><code>if object_id( 'tempdb..#test1' ) is not null drop table #test1;
go


-- example heap table with duplicate record

create table #test1
(
     col1 int
    ,col2 varchar(50)
    ,col3 char(3)
);
insert #test1( col1, col2, col3 )
values
     ( 250, 'Joe''s IT Consulting and Bait Shop', null )
    ,( 120, 'Mary''s Dry Cleaning and Taxidermy', 'ACK' )
    ,( 250, 'Joe''s IT Consulting and Bait Shop', null )    -- dup record
    ,( 666, 'The Honest Politician', 'LIE' )
    ,( 100, 'My Invisible Friend', 'WHO' )
;
go


-- add temporary PK and index

alter table #test1 add sk int not null identity constraint PK_test1 primary key clustered;
create index IX_test1 on #test1( col1, col2, col3 );
go


-- note: rebuilding the indexes may or may not provide a performance benefit

alter index PK_test1 on #test1 rebuild;
alter index IX_test1 on #test1 rebuild;
go


-- remove duplicates

with ranks as
(
    select
         sk
        ,ordinal = row_number() over 
         ( 
            -- put all the columns composing uniqueness into the partition
            partition by col1, col2, col3
            order by sk
         )
    from #test1
)
delete 
from ranks
where ordinal &gt; 1;
go


-- remove added columns

drop index IX_test1 on #test1;
alter table #test1 drop constraint PK_test1;
alter table #test1 drop column sk;
go
</code></pre>

### Answer ID: 2594454
<p>And fix that table. No table ever should be without a unique index, preferably as a PK. Even if you add a surrogate key because there is no natural key, you need to be able to specifically identify a particular record. Otherwise how will you get rid of the duplicates you already have?</p>

### Answer ID: 2593740
<p>What is the data volume? You have 2 options that I can see:</p>

<p>1: filter it at source, by implementing your own <code>IDataReader</code> and using some hash over the data, and simply skipping any duplicates so that they never get passed into the TDS.</p>

<p>2: filter it in the DB; at the simplest level, I guess you could have multiple stages of import - the raw, unsanitised data - and then copy the <code>DISTINCT</code> data into your <em>actual</em> tables, perhaps using an intermediate table if you want to. You <em>might</em> want to use <code>CHECKSUM</code> for some of this, but it depends.</p>

### Answer ID: 2593716
<p>I'd upload the data into a staging table then deal with duplicates afterwards on copy to the final table.</p>

<p>For example, you can create a (non-unique) index on the staging table to deal with the "key"</p>

### Answer ID: 2593708
<p>I would bulk copy into a temporary table and then push the data from that into the actual destination table. In this way, you can use SQL to check for and handle duplicates.</p>


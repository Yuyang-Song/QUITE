# MS-Access: TableAdapter UpdateCommand for table without primary key
[Link to question](https://stackoverflow.com/questions/2449829/ms-access-tableadapter-updatecommand-for-table-without-primary-key)
**Creation Date:** 1268681030
**Score:** 1
**Tags:** sql, vb.net, ms-access, dataset, strongly-typed-dataset
## Question Body
<p>What's the syntax for an Update query for a table without a primary key?</p>
<p><strong>Disclaimer:</strong> Frustratingly, adding a primary key is not an option.  My program is a small program in a much larger system with poor data management.  My development time does not include rewriting the other software.</p>
<p><strong>Note:</strong> The database is Microsoft Access.</p>
<p><strong>Note:</strong> Similar to: <a href="https://stackoverflow.com/questions/2450491/excel-tableadapter-updatecommand-for-table-without-primary-key">Excel: TableAdapter UpdateCommand for table without primary key</a></p>
<p><strong>UPDATE:</strong> Am I correct in saying, &quot;If the table in the database has no explicit primary key, then there can be no valid TableAdapter UpdateCommand?&quot;</p>

## Answers
### Answer ID: 2449949
<p>If there isn't an explicit primary key, there should at least be an implicit primary key (even if it's <em>every column</em>).  Without any sort of key, you won't be able to <em>safely</em> update the table.</p>

<p>If you go through the wizard when creating the dataset, you should get an update query that includes an update statement similar to this:</p>

<pre>
update TableA
set Column1 = @Column1, Column2 = @Column2 ...
where Column1 = @PreviousColumn1 and Column2 = @PreviousColumn2 ...
</pre>

<p><strong>EDIT</strong><br>
You won't be able to use the wizard for update or delete commands without a PK on the table.  You can, however, make a copy of the Access file put a PK on the table (if you can't derive a short implicit key, you may have to use every column) and use that to create the commands via the wizard.</p>

<p>If you don't want to go through that step, then you'll have to create a query similar to the one above.  The <code>@PreviousColumnX</code> parameters would have their <code>SourceVersion</code> values set to <code>Original</code>.</p>

<pre><code>update TableA
set Column1 = @Column1, Column2 = @Column2 ...
where (Column1 = @PreviousColumn1 or @PreviousColumn1 is null)
    and Column2 = @PreviousColumn2 ...
</code></pre>

### Answer ID: 2449860
<p>It's no different than if you have a primary key. However, you will have to set some sort of where clause that will allow you to uniquely identify a row.</p>

### Answer ID: 2449862
<p>Which DBMS are you using ? On Oracle (and probably others, but I have more experience with Oracle), there is a ROWID pseudo-column that you can use as a unique row identifier, even when there's no primary key</p>


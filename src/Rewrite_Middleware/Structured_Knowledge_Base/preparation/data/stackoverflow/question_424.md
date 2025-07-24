# APPEND FROM excel sheet gives strange error
[Link to question](https://stackoverflow.com/questions/25571077/append-from-excel-sheet-gives-strange-error)
**Creation Date:** 1409324749
**Score:** 0
**Tags:** excel, visual-foxpro
## Question Body
<p>I have a problem with the APPEND FROM statement in Visual FoxPro. I cannot do an APPEND FROM an excel sheet without getting this error:</p>

<blockquote>
  <p>Function name is missing (</p>
</blockquote>

<p>I'm working on processing some legacy data stored in a FoxPro database. I'm reading it, processing it in .NET, and then writing it back to a new FoxPro database. However, the writing part is not working. Unfortunately using another database is not an option. And yes, I am a FoxPro newbie.</p>

<p>I do get INSERT statements to work, but it would be useful if I could get APPEND FROM an external file to work as well, AND also be able to hydrate memo fields. Afaik you can't do that with CSV files in FoxPro, only Excel and some other formats - but not CSV.</p>

<p>To demonstrate the problem I'm using the Address Book sample database that comes with Visual Foxpro.</p>

<p>I run this query in the query window in V.FP: </p>

<pre><code>USE "ADDRESS BOOK!ADDRESSES"
APPEND FROM D:\tmp\excel_data2.xls FIELDS (addressid, firstname) DELIMITED XLS
</code></pre>

<p>The .xls file is a Excel 97-2003 workbook and looks like this: </p>

<pre><code>A   | B
------------------------
23  | Sample 1
------------------------
24  | Sample 2 
</code></pre>

<p>I think the syntax should be correct according to this doc: <a href="http://msdn.microsoft.com/en-us/library/aa977271(v=vs.71).aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/aa977271(v=vs.71).aspx</a></p>

<p>However, running this query just gives me the error about "Function name is missing (" . I've tried all sorts of rewrites and variations of this query that I could think of, but I just can't figure out what the problem is. Any help would be appreciated, thanks.</p>

## Answers
### Answer ID: 25601026
<p>Not to steal the show, but this is how I got it working: </p>

<p>Ensure the XLS file is stored in the Excel 5.0/95 format (basically an ancient Excel format, but more than sufficient for data entry).</p>

<p>Close the Excel file, otherwise you will get an error about the file being locked/open in another app.</p>

<p>I used the following amended APPEND FROM statement and it worked: </p>

<pre><code>USE "ADDRESS BOOK!ADDRESSES"
APPEND FROM D:\tmp\excel_data2.xls FIELDS addressid, firstname XLS
</code></pre>

### Answer ID: 25592247
<p>LAK was correct, but I will clarify for your app and possible future encounters with Excel imports.  If your table does not match the columns order in Excel, you could run into problems.  Typically I import into a cursor that I know the order and format of the fields.  Then I'll append from.  Once in a cursor version of a table, I can then append to any other table, cycle through it, do data cleansing, etc.</p>

<p>Say your address table had it's structure of ID, LastName, FirstName, Address... but your Excel file had ID, FirstName+LastName as a single field, Address and you know you will need to parse it into proper first/last fields.  This would be a good example of using the interim cursor.  If the cursor has more columns than Excel, they will just come along for the ride and be blank, but there to work with as you need.</p>

<pre><code>create cursor C_TmpFromExcel;
   ( IDCol     int,;
     FullName  c(40),;
     Address   c(35),;
     FirstName c(20),;
     LastName  c(20) )

append from D:\tmp\excel_data2.xls type xls

*/ VERY BASIC example to split the name
replace all lastname with left( fullname, at("," , FullName ) -1 )
replace all firstname with substr( fullname, at( ",", FullName ) +1 )

select LiveAddressTable
append from C_TmpFromExcel
</code></pre>

<p>When appending one table (or cursor) together with another, VFP will handle match by same column names and disregard those where the column(s) are otherwise extra and not needed (such as the sample "FullName" column -- vs the FirstName extracted as extra ).</p>


# JavaScript function to query a MS Access DB using Recordsets with multiple parameters
[Link to question](https://stackoverflow.com/questions/35956927/javascript-function-to-query-a-ms-access-db-using-recordsets-with-multiple-param)
**Creation Date:** 1457781289
**Score:** 0
**Tags:** javascript, sql, database, select, adodb
## Question Body
<p>I have a front-end HTML page which is querying an MS Access Database. </p>

<p>HTML:</p>

<pre><code>&lt;input class="textbox" id="searchValue" maxlength="100" name="KeywordSearch" onclick="this.value='';" size="50" type="text" value="Enter Your Keyword Here" /&gt;

&lt;input class="textbox" id="ForCLNo" name="CLNum"  type="text" onclick="this.value='';" size="25" type="text" value="CL Number"/&gt; 

&lt;input class="button" name="Search" onclick="searchEngineSearch();" type="button" value="Search" /&gt;&lt;/p&gt;
</code></pre>

<p>Want to execute this query:</p>

<pre><code>SELECT * FROM MasterTable where CLNo = test1 AND Query = test2;
</code></pre>

<p>For the query, <code>SELECT * FROM MasterTable where Query LIKE test2</code>, I have created the ADODB object as follows:</p>

<pre><code>var adVarWChar = 202;
var adParamInput = 1;
var pad = "C:\\Users\\Rik\\Desktop\\Project\\MyTable.accdb";
var cn = new ActiveXObject("ADODB.Connection");
var strConn = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + pad;
cn.Open(strConn);
var cm = new ActiveXObject("ADODB.Command");
cm.ActiveConnection = cn;

cm.CommandText = "SELECT * FROM MasterTable where Query LIKE test2";

cm.Parameters.Append(cm.CreateParameter(
        "test2",
        adVarWChar,
        adParamInput,
        255,
        "%" + document.getElementById("searchValue").value + "%"));
var rs = cm.Execute();
</code></pre>

<p>and the correct result is obtained.</p>

<p>Not sure how to rewrite the cm.Parameters.Append(cm.CreateParameter()) function to incorporate more than one WHERE condition in an SQL query [<code>SELECT * FROM MasterTable where CLNo = test1 AND Query = test2;</code>]. </p>

<p>Please Help :)</p>

## Answers
### Answer ID: 35970067
<p>You're creating one parameter within the Parameters collection already... you just need to create one more:</p>

<pre><code>cm.CommandText = "SELECT * FROM MasterTable where Query LIKE test1 OR Query LIKE Test2";

cm.Parameters.Append(cm.CreateParameter(
    "test1",
    adVarWChar,
    adParamInput,
    255,
    "%" + document.getElementById("searchValue").value + "%"));


cm.Parameters.Append(cm.CreateParameter(
    "test2",
    adVarWChar,
    adParamInput,
    255,
    "%" + document.getElementById("searchValue").value + "%"));

var rs = cm.Execute();
</code></pre>

<p><code>cm.Parameters</code> is a collection, meaning it's capable of holding any reasonable number of its item type.  For each piece of parameter code above, you append a newly created parameter into the collection. The entire collection is then used to resolve the SQL statement.</p>


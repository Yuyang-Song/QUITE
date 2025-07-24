# How to run parameterized query from VBA. Parameters sourced from recordset
[Link to question](https://stackoverflow.com/questions/31059553/how-to-run-parameterized-query-from-vba-parameters-sourced-from-recordset)
**Creation Date:** 1435261911
**Score:** 1
**Tags:** vba, ms-access, parameterized-query
## Question Body
<p>I have a form where a user selects a vendor's name from a combobox, whose catalog file is to be imported.  The combobox selection then drives a query to create a one-record recordset (rsProfile) containing several profile variables queried from a table of all vendor profiles. These variables are then used in a series of different queries to reformat, translate and normalize the vendor's uniquely structured files to a standardized format that can be imported into our system.</p>

<p>I am frustrated that I can't figure out how to build my stored queries that will use one or more parameters that are automatically populated from the profile recordset.</p>

<p>Here is my rsProfile harvesting code. It works. Note that <em>intVdrProfileID</em> is a global variable set and used in other places.</p>

<pre><code>Private Sub btn_Process_Click()

Dim ws As Workspace
Dim db, dbBkp As DAO.Database
Dim qdf As DAO.QueryDef
Dim rsProfile, rsSubscrip As Recordset
Dim strSQL As String
Dim strBkpDBName As String
Dim strBkpDBFullName As String

strBkpDBName = Left(strVdrImportFileName, InStr(strVdrImportFileName, ".") - 1) &amp; "BkpDB.mdb"
strBkpDBFullName = strBkpFilePath &amp; "\" &amp; strBkpDBName

Set db = CurrentDb
Set ws = DBEngine.Workspaces(0)

MsgBox ("Vendor Profile ID = " &amp; intVdrProfileID &amp; vbCrLf &amp; vbCrLf &amp; "Backup file path: " &amp; strBkpFilePath)

' Harvest Vendor Profile fields used in this sub
strSQL = "SELECT VendorID, Div, VPNPrefix, ImportTemplate, " &amp; _
                 "VenSrcID, VenClaID, ProTyp, ProSeq, ProOrdPkg, ProOrdPkgTyp, JdeSRP4Code, " &amp; _
                 "PriceMeth, " &amp; _
                 "ProCost1Frml, ProCost2Frml, " &amp; _
                 "ProAmt1Frml, ProAmt2Frml, ProAmt3Frml, ProAmt4Frml, ProAmt5Frml " &amp; _
         "FROM tZ100_VendorProfiles " &amp; _
         "WHERE VendorID = " &amp; intVdrProfileID &amp; ";"

Set qdf = db.QueryDefs("qZ140_GetProfileProcessParms")
qdf.SQL = strSQL
Set rsProfile = qdf.OpenRecordset(dbOpenSnapshot)
DoCmd.OpenQuery "qZ140_GetProfileProcessParms"
' MsgBox (qdf.SQL)
</code></pre>

<p>I have used QueryDefs to rewrite stored queries at runtime, and although it works, it is quite cumbersome and does not work for everything.</p>

<p>I was hoping for something like the sample below as a stored query using DLookups. I can get this to work in VBA, but I can't get anything to work with stored queries. I am open to other suggestions.</p>

<p>Stored Query "qP0060c_DirectImportTape":</p>

<pre><code>SELECT 
    DLookUp("[VPNPrefix]","rsProfile","[VendorID]=" &amp; intVdrProfileID) &amp; [PartNo] AS VenPrtId,
    Description AS Des,
    DLookup("[Jobber]","rsProfile",[VendorID=" &amp; intVdrProfileID) AS Amt1,
INTO tP006_DirectImportTape
FROM tJ000_VendorFileIn;
</code></pre>

<p>ADDENDUM: 
Let me adjust the problem to make it a bit more complex. I have a collection of about 40 queries each of which use a different collection of parameters (or none). I also have a table containing the particular set of queries that each vendor 'subscribes' to. The goal is to have a database where a non-coding user can add new vendor profiles and create/modify the particular set of queries which would be run against that vendor file. I have almost 100 vendors so far, so coding every vendor seperately is not practical. Each vendor file will be subjected to an average of 14 different update queries.</p>

<p>Simplified Example:
Vendor1 file needs to be processed with queries 1, 2 and 5. Vendor2 file might need only update queries 2 and 4. The parameters for these queries might be as follows:</p>

<p>query1 (parm1)
query2 (parm1, parm4, parm8, parm11)
query4 (parm5, parm6, parm7, parm8, parm9, parm10, parm11)
query5 () -no parms required</p>

<p>This is the core query processing that loops through only the queries relevant to the current vendor file. <strong>rsSubscrip</strong> is the recordset (queried from a master table) containing this filtered list of queries.</p>

<pre><code>' Run all subscribed queries
MsgBox "Ready to process query subscription list."
With rsSubscrip
    Do While Not .EOF
        db.Execute !QueryName, dbFailOnError
        .MoveNext
    Loop
    .Close
End With
</code></pre>

## Answers
### Answer ID: 31068105
<p>You can set the parameters of a predefined query using the syntax;</p>

<pre><code>Set qdf = CurrentDB.QueryDefs(QueryName)
qdf.Parameters(ParameterName) = MyValue
</code></pre>

<p>To add parameters to the query, add the following before the SELECT statement in the sql</p>

<pre><code>PARAMETERS [ParameterOne] DataType, [ParameterTwo] DataType;
SELECT * FROM tblTest;
</code></pre>


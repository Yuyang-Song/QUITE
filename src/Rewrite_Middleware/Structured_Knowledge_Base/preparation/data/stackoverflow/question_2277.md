# Handling Unicode string pulled from SOQL In Python
[Link to question](https://stackoverflow.com/questions/27151373/handling-unicode-string-pulled-from-soql-in-python)
**Creation Date:** 1417011375
**Score:** 0
**Tags:** python, unicode, ascii, soql
## Question Body
<p>The purpose of the code is to use SOQL to query the SalesForce API, then to format the data and do some stuff before putting putting it into an oracle database. My code successfully handles the first and third part but the second part keeps breaking. </p>

<p>The code is using Python 2.7 with the standard C python compiler on Windows 7. </p>

<p>The SOQL is </p>

<pre><code>SELECT  ID, Name, Type, Description, StartDate, EndDate, Status
FROM        CAMPAIGN
ORDER BY    ID
</code></pre>

<p>This query pulls back a few hundred results in a JSON Dict.
I have to pull each record (Record contains ID, Name, Type, Description, StartDate, EndDate, and Status) one at a time and pass them to a function that generates the proper SQL to put the data in the proper Oracle Database. All of the results of the query come back as Unicode strings. </p>

<p>After I query the data and try to pass it to the function to generate the SQL to insert it into the Oracle database is where the trouble shows up. </p>

<p>Here is the section of code where the error occurs.</p>

<pre><code>keys = ['attributes', 'Id', 'Name', 'Type', 'Description', 'StartDate', 'EndDate', 'Status']
for record in SrcData['records']:  #Data cleaning in this loop. 
    processedRecs = []
    if record['Description'] is not None:                
        record['Description'] = encodeStr(record['Description'])
        record['Description'] = record['Description'][0:253]

    for key in keys:
        if key == 'attributes':
            continue
        elif key == 'StartDate' and record[key] is not None:
            record[key] = datetime.datetime.strptime(record[key], "%Y-%m-%d")
        elif key == 'EndDate' and record[key] is not None:
            record[key] = datetime.datetime.strptime(record[key], "%Y-%m-%d")
        else:
            pass

        processedRecs.append(record[key])

    sqlFile.seek(0)
    Query = RetrieveSQL(sqlFile, processedRecs)
</code></pre>

<p>The key list is because there was issues with looping on SrcData.keys().
the encodeStr function is:</p>

<pre><code>def encodeStr(strToEncode):
    if strToEncode == None:
        return ""
    else:
        try:
            tmpstr = strToEncode.encode('ascii', 'ignore')
            tmpstr = ' '.join(tmpstr.split())
            return tmpstr 
        except:
            return str(strToEncode)
</code></pre>

<p>The error message I get is:</p>

<pre><code>Traceback (most recent call last): File "XXX", line 106, in Query = ASPythonLib.RetrieveSQL(sqlFile, processedRecs), UnicodeEncodeError: ascii codec cant encode character u\u2026 in position 31: ordinal not in range(128)
</code></pre>

<p>the XXXX is just a file path to where this code is in our file system. Boss said I must remove the path.</p>

<p>I have also tried multiple variation of:</p>

<pre><code>record['Description'] = record['Description'].encode('ascii', 'ignore').decode(encoding='ascii',errors='strict')
</code></pre>

<p>I have tried swapping the order of the encode and decode functions. I have tried different codecs and different error handling schemes. </p>

<p>****Edit**** This code works correct in like 20 other cycles so it's safe to assume the error is not in the RetrieveSQL().
Here is the code for RetrieveSQL:</p>

<pre><code>def RetrieveSQL(SQLFile, VarList, Log = None):
    SQLQuery = SQLFile.readline()

    FileArgs = [""]

    NumArgValues = len(VarList)

    if( "{}" in SQLQuery ):
        # NumFileArgs == 0
        if (NumArgValues != 0):
            print "Number of File Arguments is zero for File " + str(SQLFile) + " is NOT equal to the number of values provided per argument (" + str(NumArgValues) + ")."
        return SQLFile.read()
    elif( SQLQuery[0] != "{" ):
        print "File " + str(SQLFile) + " is not an SQL source file."
        return -1

    elif( SQLQuery.startswith("{") ):
        FileArgs = SQLQuery.replace("{", "").replace("}", "").split(", ")
        for Arg in xrange(0, len(FileArgs)):
            FileArgs[Arg] = "&amp;" + FileArgs[Arg].replace("\n", "").replace("\t", "") + "&amp;" # Add &amp;'s for replacing

    NumFileArgs  = len(FileArgs)

    if (NumFileArgs != NumArgValues):
        if (NumArgValues == 0):
            print "No values were supplied to RetrieveSQL() for File " + str(SQLFile) + " when there were supposed to be " + str(NumFileArgs) + " values."
            return -1
        elif (NumArgValues &gt; 0):
            "Number of File Arguments (" + str(NumFileArgs) + ") for File " + str(SQLFile) + " is NOT equal to the number of values provided per argument (" + str(NumArgValues) + ")."
            return -1

    SQLQuery = SQLFile.read()
    VarList = list(VarList)
    for Arg in xrange(0, len(FileArgs)):
            if (VarList[Arg] == None):
                SQLQuery = SQLQuery.replace(FileArgs[Arg], "NULL")
            elif ("'" in str(VarList[Arg])):
                SQLQuery = SQLQuery.replace(FileArgs[Arg], "'" + VarList[Arg].replace("'", "''") + "'")
            elif ("&amp;" in str(VarList[Arg])):
                SQLQuery = SQLQuery.replace(FileArgs[Arg], "'" + VarList[Arg].replace("&amp;", "&amp;'||'") + "'")
            elif (isinstance(VarList[Arg], basestring) == True):
                VarList[Arg] = VarList[Arg].replace("'", "''")
                SQLQuery = SQLQuery.replace(FileArgs[Arg], "'" + VarList[Arg] + "'")
            else:
                SQLQuery = SQLQuery.replace(FileArgs[Arg], str(VarList[Arg]))
    SQLFile.seek(0)

    return SQLQuery
</code></pre>

<p>****Edit #2 ****
Tried finding a complete traceback in logging files but the logging system for this script is terrible and never logs more than 'Cycle success' or 'Cycle Fail'. Ahh the fun of rewriting code written by people who don't know how to code. </p>


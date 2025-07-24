# ASP Experts - Need help converting this PHP code to ASP
[Link to question](https://stackoverflow.com/questions/1146658/asp-experts-need-help-converting-this-php-code-to-asp)
**Creation Date:** 1247888653
**Score:** 0
**Tags:** php, sql, asp-classic
## Question Body
<p>I am facing some problems converting the PHP SQL insertion code below to ASP, I want to use the same concept in ASP, because it is more flexible, not tied to ASP owned keywords.</p>

<p>Wonder if anyone can help ASP newbie here.</p>

<pre><code>$table = 'tbluser';
$array = array (
        'name' =&gt; $name,
        'email' =&gt; $email,
        'ip' =&gt; $remoteIP
        );
$newid = insert_query ($table, $array); 



  function insert_query ($table, $array)
  {
    global $mysql_errors;
    $query = 'INSERT INTO ' . $table . ' ';
    foreach ($array as $key =&gt; $value)
    {

      $fieldnamelist .= '' . '`' . $key . '`,';
      if ($value == 'now()')
      {
        $fieldvaluelist .= 'now(),';
        continue;
      }
      else
      {
        $fieldvaluelist .= '\'' . $value . '\',';
        continue;
      }
    }

    $fieldnamelist = substr ($fieldnamelist, 0, 0 - 1);
    $fieldvaluelist = substr ($fieldvaluelist, 0, 0 - 1);
    $query .= '' . '(' . $fieldnamelist . ') VALUES (' . $fieldvaluelist . ')';
    $result = mysql_query ($query);
    if (!$result)
    {
      $message = 'Invalid query: ' . mysql_error () . '&lt;br&gt;';
      $message .= 'Whole query: ' . $query;
    }

    $id = mysql_insert_id ();
    return $id;
  }
</code></pre>

<p>it's classic ASP. No choice, company still need to maintain this for a specific project.</p>

<p>The main reason I want this specific code style in ASP is because I don't want to tie to the ASP style of querying database (using cmd and etc...)</p>

<p>By creating array collection with key(table fieldname) and value, then convert into a full sql string, I only need to run .execute(sql) , it means in future I can more easier convert the project to other framework, without needing to rewrite the way to insert/update data into DB.</p>

## Answers
### Answer ID: 1180502
<p>Not exactly the same, but here are some functions I've used in ASP classic sites.<br>
I think it should be a good starting point for learning.</p>

<pre><code>Function AddUser(Name, Email, IP )
    dim sqlstmt
    sqlstmt = "INSERT INTO tbluser (Name, Email, IP )"
    sqlstmt = sqlstmt &amp; " values (?, ?, ?)"
    call RunSQL( sqlstmt, array( _
        mp("@Name", adVarChar, 100, Name), _
        mp("@Email", adVarChar, 100, Email), _
        mp("@IP", adVarChar, 100, IP)))
end Function

Function RunSQL(strSqlStmt , params())
    On Error resume next

    ''// Create the ADO objects
    Dim cmd
    Set cmd = server.createobject("ADODB.Command")

    ''// Init the ADO objects &amp; the stored proc parameters
    cmd.ActiveConnection = GetConnectionString()
    cmd.CommandText = strSqlStmt
    cmd.CommandType = adCmdText
    collectParams cmd, params

    ''// Execute the query without returning a recordset
    cmd.Execute , , adExecuteNoRecords
    If err.number &gt; 0 then
        BuildErrorMessage()
        exit function
    end if

    ''// Cleanup
    Set cmd.ActiveConnection = Nothing
    Set cmd = Nothing

    Exit Function

End Function


Private Sub collectParams(cmd , argparams())
    Dim params , v
    Dim i , l , u

    params = argparams


    For i = LBound(params) To UBound(params)
        l = LBound(params(i))
        u = UBound(params(i))

        ''// Check for nulls.
        If u - l = 3 Then
            If VarType(params(i)(3)) = vbString Then
                If params(i)(3) = "" then
                                    v = null
                else
                    v = params(i)(3)
                end if
            Else
                v = params(i)(3)
            End If

        If params(i)(1) = adLongVarChar Then
                Dim p ''// As New Parameter
                Set p = cmd.CreateParameter(params(i)(0), params(i)(1), adParamInput)
                p.Attributes = adParamLong + adParamSigned
                If Not IsNull(v) Then
                    p.AppendChunk v
                    p.Size = Len(v)
                Else
                    p.Value = v
                    p.Size = 10000
                End If
                cmd.Parameters.Append p
            Else
                cmd.Parameters.Append cmd.CreateParameter(params(i)(0), params(i)(1), adParamInput, params(i)(2), v)
            End If
        Else
            RaiseError m_modName, "collectParams(...): incorrect # of parameters"
        End If
    Next
End Sub
</code></pre>

### Answer ID: 1151687
<p>I guess a simple rewrite would not help you that much as you need to establish a DB connection, handle errors, etc.</p>

<p>I would recommend you have a look at <a href="http://www.ajaxed.org" rel="nofollow noreferrer">ajaxed library</a> which offers you a <a href="http://ajaxed.org/api/#method_IDAFVF1" rel="nofollow noreferrer">db.insert()</a> method .. which I believe does the same as the method you require.</p>


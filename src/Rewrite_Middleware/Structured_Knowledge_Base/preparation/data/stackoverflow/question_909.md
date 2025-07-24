# How to query Firebird SQL Dialect
[Link to question](https://stackoverflow.com/questions/49404046/how-to-query-firebird-sql-dialect)
**Creation Date:** 1521628624
**Score:** 4
**Tags:** delphi, firebird, firedac, delphi-10.2-tokyo
## Question Body
<p>I'm trying to query the SQL dialect of a Firebird database (using the embedded driver):</p>

<pre><code>procedure TFrmFireDACEmbed.BtnGetDBDialectClick(Sender: TObject);
var
   lFDConnection : TFDConnection;
   lDriverLink   : TFDPhysFBDriverLink;
   l             : Integer;
begin
   if not DlgOpen.Execute then Exit;

   lDriverLink   := TFDPhysFBDriverLink.Create(nil);
   lFDConnection := TFDConnection.Create(nil);
   try
      lDriverLink.DriverID := 'FBEmbedded';
      lDriverLink.VendorLib := 'fbembed.dll';  // 32-bits embedded
      lFDConnection.DriverName := S_FD_FBId;
      lFDConnection.Params.Database := DlgOpen.FileName;
      lFDConnection.Params.Add('Server=127.0.0.1');
      lFDConnection.Params.UserName := 'SYSDBA';
      lFDConnection.Params.Password := 'masterkey';
      lFDConnection.LoginPrompt := False;
      lFDConnection.Open;
      l := lFDConnection.Params.IndexOf('SQLDialect');
      if l &lt;&gt; -1 then
         ShowMessage(lFDConnection.Params[l])
      else
         ShowMessage('SQLDialect not found');
   finally
      lFDConnection.Close;
      lFDConnection.Free;
      lDriverLink.Free;
   end;
end;
</code></pre>

<p>But the <code>lFDConnection.Params</code> only contains <code>DriverID</code>, <code>Database</code>, <code>Server</code>, <code>User_Name</code>, <code>Password</code>.</p>

<p>The inspector shows:</p>

<pre><code>(nil, $2F22820, #$D#$A, nil, 0, ',', '"', '=', [soWriteBOM,soTrailingLineBreak,soUseLocale], (('DriverID=FB', nil), ('Database=D:\Temp\KLANTEN.GDB', nil), ('Server=127.0.0.1', nil), ('User_Name=SYSDBA', nil), ('Password=masterkey', nil), ('', nil), ('', nil), ('', nil)), 5, 8, False, dupIgnore, False, (FireDAC.Stan.Def.TFDDefinition.ParamsChanged,$2F5C4F0), (FireDAC.Stan.Def.TFDDefinition.ParamsChanging,$2F5C4F0), False, TFDConnectionDef($2F5C534) as IFDStanDefinition)
</code></pre>

<p>And <code>lFDConnection.Params.SQLDialect</code> is not recognized by the compiler.</p>

<p>Digging though the system tables I found that for a dialect 3 db the query</p>

<pre><code>select mon$sql_dialect from mon$database
</code></pre>

<p>will return 3, but for an older version <code>mon$database</code> does not exist.</p>

<p>How can I retrieve the SQL dialect for any dialect?</p>

<p>The intention is to rewrite old code that used 'under the hood' functions like <code>isc_attach_database</code>, <code>isc_database_info</code> (which had to be dynamically linked, <code>GetProcAddress</code>, etc).</p>

## Answers
### Answer ID: 49409670
<p>I'm not familiar with Delphi, so my answer is from a generic Firebird perspective.</p>

<p>The <code>MON$DATABASE</code> table exists both in dialect 1 and dialect 3 databases, provided that database is at least ODS 11.1 (Firebird 2.1, which introduced the monitoring pseudo-tables). If you don't have a <code>MON$DATABASE</code> table then the database is ODS 10.0 (InterBase 6/Firebird 1.x) or ODS 11.0 (Firebird 2.0).</p>

<p>In other words, if you don't have a <code>MON$DATABASE</code>, you could backup and restore the database to upgrade it and then check <code>MON$DATABASE</code>.</p>

<p>Otherwise, there is a trick you can use to determine if a database is dialect 1 or dialect 3. The trick is to execute the following query:</p>

<pre><code>select 1/2 from rdb$database
</code></pre>

<p>If the result is <code>0</code> (integer), then your database is dialect 3, if the result is <code>0.500000</code> (double precision), the database is dialect 1. In theory preparing the query should be enough, the value would be described as <code>DOUBLE PRECISION</code> in dialect 1 and as <code>BIGINT</code> (or <code>DECIMAL(18,0)</code>) in dialect 3.</p>

<p>This is because this is one of the differences between dialect 1 and dialect 3: integer division in dialect 1 is done as floating point division.</p>

<p>Be aware: it is possible to explicitly set a connection dialect and override the default of using the database dialect. This should produce a warning on connect, but not all drivers/components communicate that warning.</p>

<p>Alternatively, you could query for <code>isc_info_db_sql_dialect</code> using <code>isc_database_info</code> (or check if your component has something that does this for you, see the <a href="https://stackoverflow.com/a/49408649/466862">answer by Victoria</a>), or use <code>gstat -h</code> to check the database header page directly.</p>

### Answer ID: 49408649
<h2>How to get SQL dialect of the connected Firebird database?</h2>

<p>You can replace your legacy code by something like this:</p>

<pre><code>uses
  FireDAC.Phys.IBWrapper;

procedure TForm1.Button1Click(Sender: TObject);
var
  SQLDialect: Integer;
  IBDatabase: TIBDatabase;
begin
  IBDatabase := TObject(FDConnection1.CliObj) as TIBDatabase;
  SQLDialect := IBDatabase.db_sql_dialect;
end;
</code></pre>

<h2>How to specify SQL dialect for Firebird database connection at runtime?</h2>

<p>You can specify connection definition parameter for SQL dialect by:</p>

<pre><code>FDConnection1.Params.Add('SQLDialect=1');
</code></pre>

<p>Or by typecasting to specific Firebird DBMS connection definition class like this:</p>

<pre><code>TFDPhysFBConnectionDefParams(FDConnection1.Params).SQLDialect := 1;
</code></pre>


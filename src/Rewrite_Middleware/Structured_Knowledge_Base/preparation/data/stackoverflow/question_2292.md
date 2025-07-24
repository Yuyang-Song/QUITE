# Native connections in SQLWindows, is there a way to send NULL instead of blank spaces in SQL without extra variable?
[Link to question](https://stackoverflow.com/questions/27903196/native-connections-in-sqlwindows-is-there-a-way-to-send-null-instead-of-blank-s)
**Creation Date:** 1421069640
**Score:** 2
**Tags:** odbc, guptateamdeveloper, centura
## Question Body
<p>Due to many inconveniences caused by the ODBC driver, regardless the database management system (SQL Server 2000 in my case), I want to change my application connection type from ODBC to native.</p>

<p>SQLWindows offers this feature, but with a huge gap. Using ODBC driver, when a field in the form is blank, it sends NULL to be recorded in the database. Thanks to the configuration parameter <strong>setzerolengthstringstonull=on</strong>, in the <strong>sql.ini</strong> file. However, using native connections, it sends a blank string <strong>' '</strong> instead, and that, of course, causes a variety of inconsistencies and errors depending on which table or foreign keys the column is related. I don't know how to reproduce the parameter <strong>setzerolengthstringstonull</strong> in a <strong>UDL file</strong> or change it internally.</p>

<p>Is there a way to configure that correctly in the application, or even intercept the SQL command before running (in a generic way, not before each SQL) so I can manually change blank values to NULLs?</p>

<p>I know that SQLWindows documentation suggests me don't send fields directly in SQLs, but create extra variables, check if those fields are blank or not, set the variables to either the values in the fields or <strong>STRING_Null</strong>, and send the variables in SQL. That is impossible in my situation due to the immense corporative size of my application. That would require simply rewrite almost everything.</p>

<hr>

<p>I wrote two minimal examples of how things are different between them:</p>

<p>This works in OBDC, it inserts an user in table <em>tblUser</em>, supposing that column <em>UsrEmail</em> looks for emails in a <em>tblEmail</em>. And <em>dfUsr[something]</em> are controls in <em>MyForm</em>.</p>

<pre><code>INSERT INTO tblUser (
    UsrName,
    UsrEmail
)
SELECT
    :MyForm.dfUsrName,
    :MyForm.dfUsrEmail
</code></pre>

<p>To do the same in native connections, I have to create a String variable named <em>sUsrEmail</em> (or whatever), and execute the following code before the specific SQL below</p>

<pre><code>if SalIsNull(MyForm.dfUsrEmail)
    sUsrEmail = STRING_Null
else
    sUsrEmail = MyForm.dfUsrEmail
</code></pre>

<p>Even the query is different:</p>

<pre><code>INSERT INTO tblUser (
    UsrName,
    UsrEmail
)
SELECT
    :MyForm.dfUsrName,
    :sUsrEmail
</code></pre>

## Answers
### Answer ID: 41444211
<p>In Sql.ini you can use the <code>substitute=</code> setting.
This setting is used by the native connection driver provided by Gupta for every DB-Client communication.</p>

<p>The setting must be placed within the appropriate section in sql.ini.
I.e. when using an Oracle DBMS, the setting has to be inside [oragtwy] 
The setting has been made for substituting DBMS specific commands.</p>

<p>Example:</p>

<p><code>
[oragtwy]
substitute=@UPPER,UPPER</code></p>

<p>In the example, mentioned above the setting is being considered by the native connector when connected to an oracle DBMS and every time it finds a Statement having "@UPPER" inside (which is SqlBase specific), it substitutes that string with UPPER (which is used in oracle)</p>

<p>So in your case, the setting should look like this:</p>

<p><code>substitute='',</code></p>

<p>I am using it constantly when working with oracle databases.</p>

### Answer ID: 27917411
<p>I dont know how to change global, 
but in instruction you can use:</p>

<pre><code>INSERT INTO tblUser (
    UsrName,
    UsrEmail
)
SELECT
    :MyForm.dfUsrName,
    NULLIF(:MyForm.dfUsrEmail, '')
</code></pre>


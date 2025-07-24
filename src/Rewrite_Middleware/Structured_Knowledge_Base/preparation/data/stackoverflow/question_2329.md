# Trouble installing SQL Developer OE (Order Entry) sample database
[Link to question](https://stackoverflow.com/questions/29724009/trouble-installing-sql-developer-oe-order-entry-sample-database)
**Creation Date:** 1429399201
**Score:** 0
**Tags:** oracle-database
## Question Body
<p>I've been at this for literally hours. I've followed the instructions here - <a href="http://docs.oracle.com/database/121/COMSC/installation.htm#COMSC109" rel="nofollow">http://docs.oracle.com/database/121/COMSC/installation.htm#COMSC109</a> - but I get the following when arriving at the 'Installing Schema OE and Subschema OC' section and doing as it says, running oe_main.sql;</p>

<pre><code>specify password for OE as parameter 1:
old:DEFINE pass     = &amp;1
new:DEFINE pass     = oe

specify default tablespeace for OE as parameter 2:
old:DEFINE tbs      = &amp;2
new:DEFINE tbs      = OE

specify temporary tablespace for OE as parameter 3:
old:DEFINE ttbs     = &amp;3
new:DEFINE ttbs     = temp

specify password for HR as parameter 4:
old:DEFINE passhr   = &amp;4
new:DEFINE passhr   = hr

specify password for SYS as parameter 5:
old:DEFINE pass_sys = &amp;5
new:DEFINE pass_sys = manager

specify directory path for the data files as parameter 6:
old:DEFINE data_path = &amp;6
new:DEFINE data_path = C:\

writeable directory path for the log files as parameter 7:
old:DEFINE log_path = &amp;7
new:DEFINE log_path = C:\

specify version as parameter 8:
old:DEFINE vrs = &amp;8
new:DEFINE vrs = 5

old:DEFINE spool_file = &amp;log_path.oe_oc_&amp;vrs..log
new:DEFINE spool_file = C:\oe_oc_5.log
old:SPOOL &amp;spool_file
new:SPOOL C:\oe_oc_5.log

Error starting at line : 75 in command -
DROP USER oe CASCADE
Error report -
SQL Error: ORA-01918: user 'OE' does not exist
01918. 00000 -  "user '%s' does not exist"
*Cause:    User does not exist in the system.
*Action:   Verify the user name is correct.
old:CREATE USER oe IDENTIFIED BY &amp;pass
new:CREATE USER oe IDENTIFIED BY oe

Error starting at line : 86 in command -
CREATE USER oe IDENTIFIED BY oe
Error at Command Line : 86 Column : 30
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges
old:ALTER USER oe DEFAULT TABLESPACE &amp;tbs QUOTA UNLIMITED ON &amp;tbs
new:ALTER USER oe DEFAULT TABLESPACE temp QUOTA UNLIMITED ON temp

Error starting at line : 88 in command -
ALTER USER oe DEFAULT TABLESPACE &amp;tbs QUOTA UNLIMITED ON &amp;tbs
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges
old:ALTER USER oe TEMPORARY TABLESPACE &amp;ttbs
new:ALTER USER oe TEMPORARY TABLESPACE temp

Error starting at line : 90 in command -
ALTER USER oe TEMPORARY TABLESPACE &amp;ttbs
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges

Error starting at line : 92 in command -
GRANT CREATE SESSION, CREATE SYNONYM, CREATE VIEW TO oe
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges
Error starting at line : 93 in command -
GRANT CREATE DATABASE LINK, ALTER SESSION TO oe
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges

Error starting at line : 94 in command -
GRANT RESOURCE TO oe
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges

Error starting at line : 95 in command -
GRANT CREATE MATERIALIZED VIEW  TO oe
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges

Error starting at line : 96 in command -
GRANT QUERY REWRITE             TO oe
Error report -
SQL Error: ORA-01031: insufficient privileges
01031. 00000 -  "insufficient privileges"
*Cause:    An attempt was made to perform a database operation without
           the necessary privileges.
*Action:   Ask your database administrator or designated security
           administrator to grant you the necessary privileges
old:CONNECT sys/&amp;pass_sys AS SYSDBA
new:CONNECT sys/manager AS SYSDBA
Connected

Error starting at line : 103 in command -
GRANT execute ON sys.dbms_stats TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.
old:CONNECT hr/&amp;passhr
new:CONNECT hr/hr
Connected

Error starting at line : 110 in command -
GRANT REFERENCES, SELECT ON employees TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.

Error starting at line : 111 in command -
GRANT REFERENCES, SELECT ON countries TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.

Error starting at line : 112 in command -
GRANT REFERENCES, SELECT ON locations TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.

Error starting at line : 113 in command -
GRANT SELECT ON jobs TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.
Error starting at line : 114 in command -
GRANT SELECT ON job_history TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.

Error starting at line : 115 in command -
GRANT SELECT ON departments TO oe
Error report -
SQL Error: ORA-01917: user or role 'OE' does not exist
01917. 00000 -  "user or role '%s' does not exist"
*Cause:    There is not a user or role by that name.
*Action:   Re-specify the name.
old:CONNECT oe/&amp;pass
new:CONNECT oe/oe

Error starting at line : 122 in command -
CONNECT oe/&amp;pass
Error report -
Connection Failed
Commit
</code></pre>

<p>The problems start with 'User 'OE' doesn't exist'. Any Oracle DBA available for some guidance?</p>

<p>Running this in Oracle SQL Developer, and tried the same in SQLPlus - same results.</p>

<p>EDIT:</p>

<p>Now seeing this;</p>

<pre><code>specify password for OE as parameter 1:
old:DEFINE pass     = &amp;1
new:DEFINE pass     = oe

specify default tablespeace for OE as parameter 2:
old:DEFINE tbs      = &amp;2
new:DEFINE tbs      = OE

specify temporary tablespace for OE as parameter 3:
old:DEFINE ttbs     = &amp;3
new:DEFINE ttbs     = temp

specify password for HR as parameter 4:
old:DEFINE passhr   = &amp;4
new:DEFINE passhr   = hr

specify password for SYS as parameter 5:
old:DEFINE pass_sys = &amp;5
new:DEFINE pass_sys = password

specify directory path for the data files as parameter 6:
old:DEFINE data_path = &amp;6
new:DEFINE data_path = C:\

writeable directory path for the log files as parameter 7:
old:DEFINE log_path = &amp;7
new:DEFINE log_path = C:\log

specify version as parameter 8:
old:DEFINE vrs = &amp;8
new:DEFINE vrs = v3

old:DEFINE spool_file = &amp;log_path.oe_oc_&amp;vrs..log
new:DEFINE spool_file = C:\logoe_oc_v3.log
old:SPOOL &amp;spool_file
new:SPOOL C:\logoe_oc_v3.log
user OE dropped.
old:CREATE USER oe IDENTIFIED BY &amp;pass
new:CREATE USER oe IDENTIFIED BY oe
user OE created.
old:ALTER USER oe DEFAULT TABLESPACE &amp;tbs QUOTA UNLIMITED ON &amp;tbs
new:ALTER USER oe DEFAULT TABLESPACE OE QUOTA UNLIMITED ON OE
Error starting at line : 96 in command -
ALTER USER oe DEFAULT TABLESPACE &amp;tbs QUOTA UNLIMITED ON &amp;tbs
Error report -
SQL Error: ORA-00959: tablespace 'OE' does not exist
00959. 00000 -  "tablespace '%s' does not exist"
*Cause:    
*Action:
old:ALTER USER oe TEMPORARY TABLESPACE &amp;ttbs
new:ALTER USER oe TEMPORARY TABLESPACE temp
user OE altered.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
old:CONNECT sys/&amp;pass_sys AS SYSDBA
new:CONNECT sys/password AS SYSDBA
Connected
GRANT succeeded.
old:CONNECT hr/&amp;passhr
new:CONNECT hr/hr
Connected
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
old:CONNECT oe/&amp;pass
new:CONNECT oe/oe
Connected
session SET altered.
session SET altered.
old:DEFINE vscript = ?/demo/schema/order_entry/coe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/coe_v3
old:@&amp;vscript &amp;vrs &amp;pass &amp;pass_sys
new:@?/demo/schema/order_entry/coe_v3 v3 oe password

Error starting at line : 139 in command -
@&amp;vscript &amp;vrs &amp;pass &amp;pass_sys
Error report -
Unable to open file: "?/demo/schema/order_entry/coe_v3.sql"
old:DEFINE vscript = ?/demo/schema/order_entry/loe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/loe_v3
old:@&amp;vscript &amp;vrs &amp;data_path &amp;log_path &amp;pass
new:@?/demo/schema/order_entry/loe_v3 v3 C:\ C:\log oe

Error starting at line : 146 in command -
@&amp;vscript &amp;vrs &amp;data_path &amp;log_path &amp;pass
Error report -
Unable to open file: "?/demo/schema/order_entry/loe_v3.sql"
old:DEFINE vscript = ?/demo/schema/order_entry/poe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/poe_v3
old:@&amp;vscript &amp;vrs
new:@?/demo/schema/order_entry/poe_v3 v3

Error starting at line : 153 in command -
@&amp;vscript &amp;vrs 
Error report -
Unable to open file: "?/demo/schema/order_entry/poe_v3.sql"

Error starting at line : 159 in command -
@?/demo/schema/order_entry/oc_main
Error report -
Unable to open file: "?/demo/schema/order_entry/oc_main.sql"

Error starting at line : 165 in command -
@?/demo/schema/order_entry/oe_analz
Error report -
Unable to open file: "?/demo/schema/order_entry/oe_analz.sql"
Connection created by CONNECT script command disconnected
</code></pre>

<p>The first error is 'tablespace 'OE' does not exist' - surely the whole point is to create it? And then line above appears to be trying to do that.</p>

<p>There's also errors retrieving the data (Unable to open file) - is that because I specified only C:\ (incidentally when I have this working I'll change that, I just got fed up with copying and pasting the complete path every time)? I've tried specifying C:\app\Hamish\product\11.2.0\dbhome_1\demo\schema\order_entry which is where the data is but I get the same result as above.</p>

<p>EDIT 2:</p>

<p>Now I'm seeing this;</p>

<p>As per my comments to the guys who gave feedback below - am I supposed to put the /demo/... somewhere in the SQL Developer directory so it can automatically find the files?</p>

<pre><code>specify password for OE as parameter 1:
old:DEFINE pass     = &amp;1
new:DEFINE pass     = oe

specify default tablespeace for OE as parameter 2:
old:DEFINE tbs      = &amp;2
new:DEFINE tbs      = users

specify temporary tablespace for OE as parameter 3:
old:DEFINE ttbs     = &amp;3
new:DEFINE ttbs     = temp

specify password for HR as parameter 4:
old:DEFINE passhr   = &amp;4
new:DEFINE passhr   = hr

specify password for SYS as parameter 5:
old:DEFINE pass_sys = &amp;5
new:DEFINE pass_sys = password

specify directory path for the data files as parameter 6:
old:DEFINE data_path = &amp;6
new:DEFINE data_path = C:/

writeable directory path for the log files as parameter 7:
old:DEFINE log_path = &amp;7
new:DEFINE log_path = C:/log

specify version as parameter 8:
old:DEFINE vrs = &amp;8
new:DEFINE vrs = v3

old:DEFINE spool_file = &amp;log_path.oe_oc_&amp;vrs..log
new:DEFINE spool_file = C:/logoe_oc_v3.log
old:SPOOL &amp;spool_file
new:SPOOL C:/logoe_oc_v3.log
user OE dropped.
old:CREATE USER oe IDENTIFIED BY &amp;pass
new:CREATE USER oe IDENTIFIED BY oe
user OE created.
old:ALTER USER oe DEFAULT TABLESPACE &amp;tbs QUOTA UNLIMITED ON &amp;tbs
new:ALTER USER oe DEFAULT TABLESPACE users QUOTA UNLIMITED ON users
user OE altered.
old:ALTER USER oe TEMPORARY TABLESPACE &amp;ttbs
new:ALTER USER oe TEMPORARY TABLESPACE temp
user OE altered.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
old:CONNECT sys/&amp;pass_sys AS SYSDBA
new:CONNECT sys/password AS SYSDBA
Connected
GRANT succeeded.
old:CONNECT hr/&amp;passhr
new:CONNECT hr/hr
Connected
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
GRANT succeeded.
old:CONNECT oe/&amp;pass
new:CONNECT oe/oe
Connected
session SET altered.
session SET altered.
old:DEFINE vscript = ?/demo/schema/order_entry/coe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/coe_v3
old:@&amp;vscript &amp;vrs &amp;pass &amp;pass_sys
new:@?/demo/schema/order_entry/coe_v3 v3 oe password

Error starting at line : 131 in command -
@&amp;vscript &amp;vrs &amp;pass &amp;pass_sys
Error report -
Unable to open file: "?/demo/schema/order_entry/coe_v3.sql"
old:DEFINE vscript = ?/demo/schema/order_entry/loe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/loe_v3
old:@&amp;vscript &amp;vrs &amp;data_path &amp;log_path &amp;pass
new:@?/demo/schema/order_entry/loe_v3 v3 C:/ C:/log oe

Error starting at line : 138 in command -
@&amp;vscript &amp;vrs &amp;data_path &amp;log_path &amp;pass
Error report -
Unable to open file: "?/demo/schema/order_entry/loe_v3.sql"
old:DEFINE vscript = ?/demo/schema/order_entry/poe_&amp;vrs
new:DEFINE vscript = ?/demo/schema/order_entry/poe_v3
old:@&amp;vscript &amp;vrs
new:@?/demo/schema/order_entry/poe_v3 v3

Error starting at line : 145 in command -
@&amp;vscript &amp;vrs 
Error report -
Unable to open file: "?/demo/schema/order_entry/poe_v3.sql"

Error starting at line : 151 in command -
@?/demo/schema/order_entry/oc_main
Error report -
Unable to open file: "?/demo/schema/order_entry/oc_main.sql"

Error starting at line : 157 in command -
@?/demo/schema/order_entry/oe_analz
Error report -
Unable to open file: "?/demo/schema/order_entry/oe_analz.sql"
Connection created by CONNECT script command disconnected
</code></pre>

<p>EDIT 3: I went into each file and manually changed the @? for @C:/[path to..]/demo/schema ... etc. Once it could find the files the process completed but it was painful amending every single @? - if there's an easier way to do this I'd like to hear it.</p>

<p>FYI for anyone struggling with this process going forward (evidently that's not many people as there's very little on the internet about this):</p>

<ol>
<li><p>Make sure you're logged in as sys/[sys password]. You can change this via SQLPlus if you're not sure by using sqlplus / as sysdba and then use an ALTER statement to change the password.</p></li>
<li><p>Specify for the input: default OE tablespace "users".</p></li>
<li><p>Update all the @? to the directory your files are stored.</p></li>
</ol>

## Answers
### Answer ID: 39168375
<p>Although this is installation is for <code>12c</code>, I have found that it does not reckon with that this must be performed against a pluggable database, and not against the container database. It seems it is built for <code>12C</code> databases that do not use <code>cdb/pdb</code>. To make this work for a <code>pdb</code> you have to:</p>

<ol>
<li>beforehand connect with <code>sys</code> to the <code>pdb</code> where you want the <code>HR</code> and <code>OE schemas</code>.</li>
<li>Edit the <code>hr_main.sql</code> and <code>oe_main</code> sql lines that do a <code>CONNECT</code> and add <code>@[pdbname]</code> to it. This has to be done for <code>CONNECT</code> with <code>hr</code>, <code>oe</code> and <code>sys</code></li>
</ol>

<p>Example: <code>CONNECT oe/&amp;pass</code> has to be changed to <code>CONNECT oe/&amp;pass@[pdb name]</code></p>

### Answer ID: 29730568
<p>The output shows a series of <code>ORA-01031: insufficient privileges</code> for activities like CREATE USER.  Clearly you are not running this script whilst connected as SYSDBA account.  </p>

<p>The <a href="https://github.com/oracle/db-sample-schemas/blob/master/order_entry/oe_main.sql" rel="nofollow">script itself</a> states:  </p>

<pre><code>rem NOTES
rem   Run as SYS or SYSTEM
</code></pre>

<p>Note that you need to connect <code>AS SYSDBA</code>. It's better to use an OS account that's part of the DBA group.  Check your connection properties in SQL Developer. <a href="http://www.asktheoracle.net/problem-connecting-to-oracle-as-sysdba-from-oracle-sql-developer.html" rel="nofollow">See this</a>. Or in SQL*Plus you do something like this:</p>

<pre><code>SQL&gt; show user
USER is "APC"
SQL&gt; connect / as sysdba
Connected.
SQL&gt; show user
USER is "SYS"
SQL&gt; 
</code></pre>

<hr>

<p>By the way, it's very bad practice to specify the root directory for everything <code>DEFINE data_path = C:\</code>.  I hope that's not what you're really doing.  Finding files will be an absolute nightmare.</p>


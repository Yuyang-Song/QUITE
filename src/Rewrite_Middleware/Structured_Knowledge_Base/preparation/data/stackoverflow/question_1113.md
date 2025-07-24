# Problem in installing SH scheme in Oracle Database
[Link to question](https://stackoverflow.com/questions/59661357/problem-in-installing-sh-scheme-in-oracle-database)
**Creation Date:** 1578563764
**Score:** -1
**Tags:** sql, plsql, oracle12c, oracle18c, oracle19c
## Question Body
<p>on executing sh_main.sql everything works fine. It even creates the schema but during the execution it gives the error </p>

<pre><code>ERROR at line 1:
ORA-29913: error in executing ODCIEXTTABLEOPEN callout
ORA-29400: data cartridge error
KUP-04027: file name check failed: ext_1v3.log
</code></pre>

<p>I am getting this error when sh_main.sql populates the table. While populating the table it uses lsh_v3.sql. In this script it creates an external table. </p>

<p>Till the creation  of external table everything is good but when it is having problem while populating using the external table sale1vs.dat.</p>

<p>Here is the content of the log file </p>

<pre><code>Session altered.

DROP USER sh CASCADE
          *
ERROR at line 1:
ORA-01918: user 'SH' does not exist



User created.


User altered.


User altered.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.

Connected.

Grant succeeded.


Directory created.


Directory created.


Grant succeeded.


Grant succeeded.


Grant succeeded.


Grant succeeded.

Connected.

Session altered.


Session altered.


Table created.


Table created.


Table created.


Table created.


Table created.


Table created.


Table created.


Table created.


Table created.


Creating constraints ...

Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


specify password for SH as parameter 1:

specify path for data files as parameter 2:

specify path for log files as parameter 3:

specify version as parameter 4:

specify connect string as parameter 5:

Looking for indexes that could slow down load ...

no rows selected


loading TIMES using:
C:/App/db_home/demo/schema/sales_history/time_v3.ctl
C:/App/db_home/demo/schema/sales_history/time_v3.dat
%ORACLE_HOME%/demo/schema/logtime_v3.log


loading COUNTRIES using:
C:/App/db_home/demo/schema/sales_history/coun_v3.ctl
C:/App/db_home/demo/schema/sales_history/coun_v3.dat
%ORACLE_HOME%/demo/schema/logcoun_v3.log


loading CUSTOMERS using:
C:/App/db_home/demo/schema/sales_history/cust_v3.ctl
C:/App/db_home/demo/schema/sales_history/cust1v3.dat
%ORACLE_HOME%/demo/schema/logcust1v3.log


loading PRODUCTS  using:
C:/App/db_home/demo/schema/sales_history/prod_v3.ctl
C:/App/db_home/demo/schema/sales_history/prod1v3.dat
%ORACLE_HOME%/demo/schema/logprod1v3.log


loading PROMOTIONS  using:
C:/App/db_home/demo/schema/sales_history/prom_v3.ctl
C:/App/db_home/demo/schema/sales_history/prom1v3.dat
%ORACLE_HOME%/demo/schema/logprom1v3.log


loading CHANNELS using:
C:/App/db_home/demo/schema/sales_history/chan_v3.ctl
C:/App/db_home/demo/schema/sales_history/chan_v3.dat
%ORACLE_HOME%/demo/schema/logchan_v3.log


loading SALES  using:
C:/App/db_home/demo/schema/sales_history/sale_v3.ctl
C:/App/db_home/demo/schema/sales_history/sale1v3.dat
%ORACLE_HOME%/demo/schema/logsale1v3.log


loading COSTS using external table


Table created.

INSERT /*+ append */ INTO costs
*
***ERROR at line 1:
ORA-29913: error in executing ODCIEXTTABLEOPEN callout
ORA-29400: data cartridge error
KUP-04027: file name check failed: ext_1v3.log***



loading additonal SALES using:
C:/App/db_home/demo/schema/sales_history/dmsal_v3.ctl
C:/App/db_home/demo/schema/sales_history/dmsal_v3.dat
%ORACLE_HOME%/demo/schema/logdmsal_v3.log


loading SUPPLEMENTARY DEMOGRAPHICS using:
C:/App/db_home/demo/schema/sales_history/dem_v3.ctl
C:/App/db_home/demo/schema/sales_history/dem1v3.dat
%ORACLE_HOME%/demo/schema/logdem1v3.log


Commit complete.


Enabling constraints ...

Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Table altered.


Creating additional indexes ...

Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Index created.


Create dimensions ...

Dimension created.


Commit complete.


Dimension created.


Dimension created.


Dimension created.


Dimension created.

Creating MVs as tables ...


View created.


Table created.


Table created.


Index created.


Index created.


Index created.


Index created.

Creating materialized views ...


Materialized view created.


Materialized view created.


Creating comments ...

Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


Comment created.


gathering statistics ...
BEGIN dbms_stats.gather_table_stats(          ownname          =&gt; 'SH'                     ,          tabname          =&gt; 'SALES_TRANSACTIONS_EXT' ,          partname         =&gt; NULL                     ,          estimate_percent =&gt; NULL                     ,          block_sample     =&gt; TRUE                     ,          method_opt       =&gt; 'FOR ALL COLUMNS SIZE 1' ,          degree           =&gt; NULL                     ,          granularity      =&gt; 'ALL'                    ,          cascade          =&gt; TRUE                     ,          stattab          =&gt; NULL                     ,          statid           =&gt; NULL                     ,          statown          =&gt; NULL                     ); END;

*
ERROR at line 1:
ORA-29913: error in executing ODCIEXTTABLEOPEN callout
ORA-06512: at "SYS.DBMS_STATS", line 40751
ORA-06512: at "SYS.DBMS_STATS", line 40035
ORA-06512: at "SYS.DBMS_STATS", line 38912
ORA-06512: at "SYS.DBMS_STATS", line 37089
ORA-06512: at "SYS.DBMS_STATS", line 30296
ORA-29400: data cartridge error
KUP-04027: file name check failed: ext_1v3.log
ORA-06512: at "SYS.DBMS_SQL", line 1735
ORA-06512: at "SYS.DBMS_STATS", line 30213
ORA-06512: at "SYS.DBMS_STATS", line 36821
ORA-06512: at "SYS.DBMS_STATS", line 38738
ORA-06512: at "SYS.DBMS_STATS", line 39738
ORA-06512: at "SYS.DBMS_STATS", line 40183
ORA-06512: at "SYS.DBMS_STATS", line 40732
ORA-06512: at line 1



PL/SQL procedure successfully completed.
</code></pre>

<p>I am using Oracle 19c. HR schema is already unlocked</p>

<hr>

<p>Here are the scripts which I am executing using the SYS user with proper pluggable container </p>

<p><strong>SH_MAIN.SQL</strong></p>

<pre><code>SET ECHO OFF

PROMPT
PROMPT specify password for SH as parameter 1:
DEFINE pass     = &amp;1
PROMPT
PROMPT specify default tablespace for SH as parameter 2:
DEFINE tbs      = &amp;2
PROMPT
PROMPT specify temporary tablespace for SH as parameter 3:
DEFINE ttbs     = &amp;3
PROMPT
PROMPT specify password for SYS as parameter 4:
DEFINE pass_sys = &amp;4
PROMPT
PROMPT specify directory path for the data files as parameter 5:
DEFINE data_dir = &amp;5
PROMPT
PROMPT writeable directory path for the log files as parameter 6:
DEFINE log_dir = &amp;6
PROMPT
PROMPT specify version as parameter 7:
DEFINE vrs = &amp;7
PROMPT
PROMPT specify connect string as parameter 8:
DEFINE connect_string     = &amp;8
PROMPT

DEFINE spool_file = &amp;log_dir.sh_&amp;vrs..log
SPOOL &amp;spool_file

ALTER SESSION SET NLS_LANGUAGE='American';

--
-- Dropping the user with all its objects
--

DROP USER sh CASCADE;

REM =======================================================
REM create user
REM THIS WILL ONLY WORK IF APPROPRIATE TS ARE PRESENT
REM =======================================================

CREATE USER sh IDENTIFIED BY &amp;pass;

ALTER USER sh DEFAULT TABLESPACE &amp;tbs
 QUOTA UNLIMITED ON &amp;tbs;
ALTER USER sh TEMPORARY TABLESPACE &amp;ttbs;

GRANT CREATE DIMENSION         TO sh;
GRANT QUERY REWRITE            TO sh;
GRANT CREATE MATERIALIZED VIEW TO sh;


GRANT CREATE SESSION           TO sh;
GRANT CREATE SYNONYM           TO sh;
GRANT CREATE TABLE             TO sh;
GRANT CREATE VIEW              TO sh;
GRANT CREATE SEQUENCE          TO sh;
GRANT CREATE CLUSTER           TO sh;
GRANT CREATE DATABASE LINK     TO sh;
GRANT ALTER SESSION            TO sh;


GRANT RESOURCE , UNLIMITED TABLESPACE              TO sh;
GRANT select_catalog_role   TO sh;

rem   ALTER USER sh GRANT CONNECT THROUGH olapsvr;

REM =======================================================
REM grants for sys schema
REM =======================================================

CONNECT sys/&amp;pass_sys@&amp;connect_string AS SYSDBA;
GRANT execute ON sys.dbms_stats TO sh;

REM =======================================================
REM DIRECTORY objects are always owned by SYS
REM    for security reasons, SH does not have
REM    CREATE ANY DIRECTORY system privilege
REM =======================================================

CREATE OR REPLACE DIRECTORY data_file_dir AS '&amp;data_dir';
CREATE OR REPLACE DIRECTORY log_file_dir AS '&amp;log_dir';

GRANT READ ON DIRECTORY data_file_dir TO sh;
GRANT READ ON DIRECTORY log_file_dir  TO sh;
GRANT WRITE ON DIRECTORY log_file_dir TO sh;
GRANT WRITE ON DIRECTORY data_file_dir TO sh;
REM =======================================================
REM create sh schema objects (sales history - star schema)
REM =======================================================

CONNECT sh/&amp;pass@&amp;connect_string

ALTER SESSION SET NLS_LANGUAGE=American;
ALTER SESSION SET NLS_TERRITORY=America;

REM =======================================================
REM Create tables
REM =======================================================

REM CONNECT sh/&amp;pass  reconnecting undoes the prior NLS settings

DEFINE vscript = C:/App/db_home/demo/schema/sales_history/csh_&amp;vrs
@&amp;vscript

REM =======================================================
REM Populate tables
REM =======================================================

DEFINE vscript = C:/App/db_home/demo/schema/sales_history/lsh_&amp;vrs
@&amp;vscript &amp;pass &amp;data_dir &amp;log_dir &amp;vrs &amp;connect_string

REM =======================================================
REM Post load operations
REM =======================================================

DEFINE vscript = C:/App/db_home/demo/schema/sales_history/psh_&amp;vrs
@&amp;vscript


spool off
</code></pre>

<p><strong>lsh_v3.sql</strong>
This main script is calling another script "lsh_v3.sql" for populating the tables. Here is that script</p>

<pre><code>SET FEEDBACK 1
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL ON
SET TAB OFF
SET PAGESIZE 100
SET VERIFY OFF
SET CONCAT '.'

PROMPT
PROMPT specify password for SH as parameter 1:
DEFINE sh_pass     = &amp;1
PROMPT
PROMPT specify path for data files as parameter 2:
DEFINE data_path = &amp;2
PROMPT
PROMPT specify path for log files as parameter 3:
DEFINE log_path = &amp;3
PROMPT
PROMPT specify version as parameter 4:
DEFINE vrs = &amp;4
PROMPT
PROMPT specify connect string as parameter 5:
DEFINE connect_string     = &amp;5
PROMPT

SET PAGESIZE 0

COLUMN index_name FORMAT A20

PROMPT Looking for indexes that could slow down load ...

SELECT index_name FROM user_indexes;

--
-- TIMES
--

DEFINE ctl_file = &amp;data_path.time_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.time_&amp;vrs..dat
DEFINE log_file = &amp;log_path.time_&amp;vrs..log

PROMPT
PROMPT loading TIMES using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=1000

--
-- COUNTRIES
--

DEFINE ctl_file = &amp;data_path.coun_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.coun_&amp;vrs..dat
DEFINE log_file = &amp;log_path.coun_&amp;vrs..log

PROMPT
PROMPT loading COUNTRIES using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=1000

--
-- CUSTOMERS
--

DEFINE ctl_file = &amp;data_path.cust_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.cust1&amp;vrs..dat
DEFINE log_file = &amp;log_path.cust1&amp;vrs..log

PROMPT
PROMPT loading CUSTOMERS using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=10000



--
-- PRODUCTS
--

DEFINE ctl_file = &amp;data_path.prod_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.prod1&amp;vrs..dat
DEFINE log_file = &amp;log_path.prod1&amp;vrs..log

PROMPT
PROMPT loading PRODUCTS  using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=10000


--
-- PROMOTIONS
--

DEFINE ctl_file = &amp;data_path.prom_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.prom1&amp;vrs..dat
DEFINE log_file = &amp;log_path.prom1&amp;vrs..log

PROMPT
PROMPT loading PROMOTIONS  using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=10


--
-- CHANNELS
--

DEFINE ctl_file = &amp;data_path.chan_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.chan_&amp;vrs..dat
DEFINE log_file = &amp;log_path.chan_&amp;vrs..log

PROMPT
PROMPT loading CHANNELS using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=10



--
-- SALES
--

DEFINE ctl_file = &amp;data_path.sale_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.sale1&amp;vrs..dat
DEFINE log_file = &amp;log_path.sale1&amp;vrs..log

PROMPT
PROMPT loading SALES  using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=100000


--
-- COSTS
--

PROMPT
PROMPT loading COSTS using external table
PROMPT

CREATE TABLE sales_transactions_ext
( PROD_ID           NUMBER,
  CUST_ID       NUMBER,
  TIME_ID       DATE,
  CHANNEL_ID    NUMBER,
  PROMO_ID      NUMBER,
  QUANTITY_SOLD   NUMBER,
  AMOUNT_SOLD   NUMBER(10,2),
  UNIT_COST     NUMBER(10,2),
  UNIT_PRICE    NUMBER(10,2)
)
ORGANIZATION external
(
  TYPE oracle_loader
  DEFAULT DIRECTORY data_file_dir
  ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE CHARACTERSET US7ASCII
    TERRITORY AMERICA
    BADFILE log_file_dir:'ext_1v3.bad'
    LOGFILE log_file_dir:'ext_1v3.log'
    FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '^' LDRTRIM
    MISSING FIELD VALUES ARE NULL
    ( PROD_ID         ,
      CUST_ID         ,
      TIME_ID         DATE(10) "YYYY-MM-DD",
      CHANNEL_ID      ,
      PROMO_ID        ,
      QUANTITY_SOLD   ,
      AMOUNT_SOLD     ,
      UNIT_COST       ,
      UNIT_PRICE
    )
 )
 LOCATION
 ('sale1v3.dat')
)
REJECT LIMIT UNLIMITED;
--REJECT LIMIT 100;

INSERT /*+ append */ INTO costs
( prod_id,
  time_id,
  channel_id,
  promo_id,
  unit_cost,
  unit_price )
SELECT
  prod_id,
  time_id,
  channel_id,
  promo_id,
  AVG(unit_cost),
  AVG(amount_sold/quantity_sold)
FROM
  sales_transactions_ext
GROUP BY
  prod_id,
  time_id,
  channel_id,
  promo_id;


--
-- ODM additional SALES rows
--

DEFINE ctl_file = &amp;data_path.dmsal_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.dmsal_&amp;vrs..dat
DEFINE log_file = &amp;log_path.dmsal_&amp;vrs..log

PROMPT
PROMPT loading additonal SALES using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file


HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=100


--
-- SUPPLEMENTARY DEMOGRAPHICS
--

DEFINE ctl_file = &amp;data_path.dem_&amp;vrs..ctl
DEFINE dat_file = &amp;data_path.dem1&amp;vrs..dat
DEFINE log_file = &amp;log_path.dem1&amp;vrs..log

PROMPT
PROMPT loading SUPPLEMENTARY DEMOGRAPHICS using:
PROMPT   &amp;ctl_file
PROMPT   &amp;dat_file
PROMPT   &amp;log_file

HOST sqlldr sh/&amp;sh_pass@&amp;connect_string  -
 control=&amp;ctl_file data=&amp;dat_file log=&amp;log_file -
 direct=yes -
 rows=10

COMMIT;
</code></pre>

<hr>

<p>The portion of lsh_v3.sql script which I think is causing the error is this --</p>

<pre><code>PROMPT
PROMPT loading COSTS using external table
PROMPT

CREATE TABLE sales_transactions_ext
( PROD_ID           NUMBER,
  CUST_ID       NUMBER,
  TIME_ID       DATE,
  CHANNEL_ID    NUMBER,
  PROMO_ID      NUMBER,
  QUANTITY_SOLD   NUMBER,
  AMOUNT_SOLD   NUMBER(10,2),
  UNIT_COST     NUMBER(10,2),
  UNIT_PRICE    NUMBER(10,2)
)
ORGANIZATION external
(
  TYPE oracle_loader
  DEFAULT DIRECTORY data_file_dir
  ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE CHARACTERSET US7ASCII
    TERRITORY AMERICA
    BADFILE log_file_dir:'ext_1v3.bad'
    LOGFILE log_file_dir:'ext_1v3.log'
    FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '^' LDRTRIM
    MISSING FIELD VALUES ARE NULL
    ( PROD_ID         ,
      CUST_ID         ,
      TIME_ID         DATE(10) "YYYY-MM-DD",
      CHANNEL_ID      ,
      PROMO_ID        ,
      QUANTITY_SOLD   ,
      AMOUNT_SOLD     ,
      UNIT_COST       ,
      UNIT_PRICE
    )
 )
 LOCATION
 ('sale1v3.dat')
)
REJECT LIMIT UNLIMITED;
--REJECT LIMIT 100;

INSERT /*+ append */ INTO costs
( prod_id,
  time_id,
  channel_id,
  promo_id,
  unit_cost,
  unit_price )
SELECT
  prod_id,
  time_id,
  channel_id,
  promo_id,
  AVG(unit_cost),
  AVG(amount_sold/quantity_sold)
FROM
  sales_transactions_ext
GROUP BY
  prod_id,
  time_id,
  channel_id,
  promo_id;
</code></pre>

<p>Things till table creation are working fine but the <code>insert into</code> statement is causing the error.</p>

## Answers
### Answer ID: 59869628
<p>Just went through your post again.Most probably script failed with creating table also your log_dir is pointing to non existing directory.Recreate log_dir again without %ORACLE HOME%. Here is standalone script to test relevant parts and iron out errors.</p>

<pre><code>SQL&gt; CREATE OR REPLACE directory ext_data as 'D:\test'; -- execute as sysdba

Directory created.

SQL&gt; ho type l_costs.sql
----------------------------------------------------------------------------------------
--------file nanme l_costs.sql----------------------------------------------------------
--------Description:stand alone script to load costs table-------------------------------
--------Date:01/22/2020-----------------------------------------------------------------
SET FEEDBACK 1
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL ON
SET TAB OFF
--SET PAGESIZE 100
SET VERIFY OFF
SET CONCAT '.'

SET PAGESIZE 0
--
-- COSTS
--
PROMPT creating costs100 dummy table for testing
CREATE TABLE sh.costs100
AS
SELECT * FROM sh.costs
WHERE 1&gt;0;

PROMPT
PROMPT DROPPING TABLE sales_transactions_ext100
 -- you can omit this step once desc or select works on the external table

DROP TABLE sh.sales_transactions_ext100;
 PROMPT CREATING TABLE sales_transactions_ext100
PROMPT
/*
CREATE TABLE sales_transactions_ext
( PROD_ID         NUMBER,
  CUST_ID                 NUMBER,
  TIME_ID                 DATE,
  CHANNEL_ID      NUMBER,
  PROMO_ID                NUMBER,
  QUANTITY_SOLD   NUMBER,
  AMOUNT_SOLD     NUMBER(10,2),
  UNIT_COST       NUMBER(10,2),
  UNIT_PRICE      NUMBER(10,2)
)
ORGANIZATION external
(
  TYPE oracle_loader
 DEFAULT DIRECTORY data_file_dir
  ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE CHARACTERSET US7ASCII TERRITORY AMERICA
        BADFILE 'C:\sql\db-sample-schemas-Windows\sales_history\ext_lv3.bad'
        LOGFILE 'C:\sql\db-sample-schemas-Windows\sales_history\ext_lv3.log'
    FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '^' LDRTRIM
    ( PROD_ID         ,
      CUST_ID         ,
      TIME_ID         DATE(10) "YYYY-MM-DD",
      CHANNEL_ID      ,
      PROMO_ID        ,
      QUANTITY_SOLD   ,
      AMOUNT_SOLD     ,
      UNIT_COST       ,
      UNIT_PRICE
    )
)
LOCATION
 ('sale1v3.dat')

*/

CREATE TABLE sh.sales_transactions_ext100
( PROD_ID         NUMBER,
  CUST_ID                 NUMBER,
  TIME_ID                 DATE,
  CHANNEL_ID      NUMBER,
  PROMO_ID                NUMBER,
  QUANTITY_SOLD   NUMBER,
  AMOUNT_SOLD     NUMBER(10,2),
  UNIT_COST       NUMBER(10,2),
  UNIT_PRICE      NUMBER(10,2)
)
ORGANIZATION external
(
  TYPE oracle_loader
  DEFAULT DIRECTORY EXT_DATA
   ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE CHARACTERSET US7ASCII TERRITORY AMERICA
        BADFILE 'ext_lv3.bad'
        LOGFILE 'ext_lv3.log'
    FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '^' LDRTRIM
    ( PROD_ID         ,
      CUST_ID         ,
      TIME_ID         DATE(10) "YYYY-MM-DD",
      CHANNEL_ID      ,
      PROMO_ID        ,
      QUANTITY_SOLD   ,
      AMOUNT_SOLD     ,
      UNIT_COST       ,
      UNIT_PRICE
    )
  )
  LOCATION ('sale1v3.dat')
)
REJECT LIMIT 100;

PROMPT Verify external table created without any error
PROMPT
DESC sh.sales_transactions_ext100
PROMPT
PROMPT count the rows in sales_transactions_ext100
PROMPT
select count(*) from sh.sales_transactions_ext100;
PROMPT
PROMPT loading COSTS using external table
PROMPT


INSERT /*+ append */ INTO sh.costs100
( prod_id,
  time_id,
  channel_id,
  promo_id,
  unit_cost,
  unit_price )
SELECT
  prod_id,
  time_id,
  channel_id,
  promo_id,
  AVG(unit_cost),
  AVG(amount_sold/quantity_sold)
FROM
  sh.sales_transactions_ext100
GROUP BY
  prod_id,
  time_id,
  channel_id,
  promo_id;
commit;
PROMPT
PROMPT verify costs100 table loaded
PROMPT
PROMPT Total rows in sh.costs100
select count(*) from sh.costs100;

PROMPT Truncate table costs100 for next run
PROMPT
TRUNCATE TABLE sh.costs100;
PROMPT
PROMPT Verify table is empty
PROMPT
select count(*) from sh.costs100;
.


SQL&gt; @l_costs
creating costs100 dummy table for testing
CREATE TABLE sh.costs100
                *
ERROR at line 1:
ORA-00955: name is already used by an existing object



DROPPING TABLE sales_transactions_ext100

Table dropped.

CREATING TABLE sales_transactions_ext


Table created.

Verify external table created without any error

           Name                            Null?    Type
           ------------------------------- -------- ----------------------------
    1      PROD_ID                                  NUMBER
    2      CUST_ID                                  NUMBER
    3      TIME_ID                                  DATE
    4      CHANNEL_ID                               NUMBER
    5      PROMO_ID                                 NUMBER
    6      QUANTITY_SOLD                            NUMBER
    7      AMOUNT_SOLD                              NUMBER(10,2)
    8      UNIT_COST                                NUMBER(10,2)
    9      UNIT_PRICE                               NUMBER(10,2)


count the rows in sales_transactions_ext100

    916039

1 row selected.


loading COSTS using external table


82112 rows created.


Commit complete.


verify costs100 table loaded

Total rows in sh.costs100
     82112

1 row selected.

Truncate table costs100 for next run


Table truncated.


Verify table is empty

         0

1 row selected.

SQL&gt;
</code></pre>

<p>P.S:-Ran another test with fresh copy from github.Most probably LF problem with datafile.Download <a href="https://sourceforge.net/projects/dos2unix/" rel="nofollow noreferrer">unix2dos/dos2unix</a> utility which is open source run unix2dos and you're good to go</p>

### Answer ID: 59661964
<p>Basically, there are two errors which look the same:</p>

<pre><code>***ERROR at line 1:
ORA-29913: error in executing ODCIEXTTABLEOPEN callout
ORA-29400: data cartridge error
KUP-04027: file name check failed: ext_1v3.log***

ORA-29400: data cartridge error
KUP-04027: file name check failed: ext_1v3.log
</code></pre>

<p>The error suggests that fiel <code>ext_1v3.log</code> doesn't exist in a (physical, operating system) directory which is pointed to by a (logical, Oracle object) <em>directory</em>.</p>

<p>Check (connected as a privileged user, such as SYS) the result of</p>

<pre><code>select * from dba_directories
</code></pre>

<p>Then edit that <em>installation script</em>, find line(s) that raised those errors and see which directories were used there - obviously, should be some listed in the <code>dba_directories</code>.</p>

<p>Though, that's somewhat strange as you use an installation script which should take care about that ... Did you, perhaps, edit it?</p>


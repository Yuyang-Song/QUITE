# creating insert, update rules in postgresql tables
[Link to question](https://stackoverflow.com/questions/13094365/creating-insert-update-rules-in-postgresql-tables)
**Creation Date:** 1351285315
**Score:** 0
**Tags:** sql, postgresql
## Question Body
<p>I am trying to create a postgresql table with insert and update rules  that can make it possible for the users to automatically insert information or update the the existing information on the database table. When i try to run the SQL query within the database inorder to create the table, i keep getting this error. I tried to follow the documentaion steps in PostgreSQL 9.1. It keeps giving me error on the expression for one of my primary keys stating that i need to be re-write it . Please can somebody look at this script and help me out. Thanks for your most valued contributions!</p>

<blockquote>
  <p>Here is my SQL script</p>
</blockquote>

<pre><code> CREATE TABLE fieldtally1
  (fieldtally1_id serial NOT NULL,
  pipeno character varying,
  wthick real,
  heatno1 character varying(32),
  pipeno2 character varying(32),
  heatno2 character varying(32),
  Djointno character varying(32),
  ContractorNo character varying(32),
  measuredlength double precision,
  serialno character varying(32),
  CoatingType character varying(32),
  coatingno character varying(32),
  mnfcno character varying(32),
  FactoryLength double precision,
  pipeod_in numeric,
  pipeod_mm numeric,
  pipeweight double precision,
  pipegrade numeric,
  loadtally numeric,
  dateweilded date,
  datereceived date,
  dataenteredby character varying(50),
  deliveryno character varying(50),
  manufacturer character varying(50),
  Remarks character varying(100),
  ManualUser character varying(100),
  log_when timestamp,
  CONSTRAINT fieldtally1_pkey PRIMARY KEY (fieldtally1_id, pipeno)
  );
  Create rule fieldtally1_ins as on INSERT to fieldtally1
  Do Instead
  Insert into fieldtally1 values (
                New.pipeno,
                New.wthick,
                New.heatno1,
                New.pipeno2,
                New.heatno2,
                New.Djointno,
                New.ContractorNo,
                New.measuredlength,
                New.serialno,
                New.coatingtype,
                New.coatingno,
                New.mnfcno,
                New.factorylength,
                New.pipeod_in,
                New.pipeod_mm,
                New.pipeweight,
                New.pipegrade,
                New.ManualUser, 
                current_timestamp
                );

CREATE RULE fieldtally1_upd AS ON UPDATE TO fieldtally1
    DO INSTEAD
    UPDATE fieldtally1
    SET PIPENO = New.pipeno,
    wthick = New.wthick,
    heatno1 = New.heatno1,
    pipeno2 = New.pipeno2,
    heatno2 = New.heatno2,
    Djointno = New.Djointno,
    ContractorNo = New.ContractorNo,
    measuredlength = New.measuredlength,
    New.serialno = New.serialno,
    coatingtype = New.coatingtype,
    coatingno = New.coatingno,
    mnfcno = New.mnfcno,
    factorylength = New.factorylength,
    pipeod_in = New.pipeod_in,
    pipeod_mm = New.pipeod_mm,
    pipeweight = New.pipeweight,
    pipegrade =  New.pipegrade,
    ManualUser = New.ManualUser 
    WHERE pipeno = OLD.pipeno;      

CREATE RULE fieldtally1_del AS ON DELETE TO fieldtally1
    DO INSTEAD
    DELETE FROM fieldtally1
     WHERE pipeno = OLD.pipeno;
</code></pre>

<blockquote>
  <p>Here is the error i get when i run the script</p>
  
  <blockquote>
    <p>NOTICE:  CREATE TABLE will create implicit sequence "fieldtally1_fieldtally1_id_seq" for serial column
    "fieldtally1.fieldtally1_id" NOTICE:  CREATE TABLE / PRIMARY KEY will
    create implicit index "fieldtally1_pkey" for table "fieldtally1"
    ERROR:  column "fieldtally1_id" is of type integer but expression is
    of type character varying LINE 34:     New.pipeno,
                 ^ HINT:  You will need to rewrite or cast the expression.</p>
  </blockquote>
  
  <p><em><strong></em>***<em></strong> Error <strong></em>**<em>*</em></strong></p>
  
  <p>ERROR: column "fieldtally1_id" is of type integer but expression is of
  type character varying SQL state: 42804 Hint: You will need to rewrite
  or cast the expression. Character: 1024</p>
</blockquote>

## Answers
### Answer ID: 13094529
<p>If your insert doesn't match the column exactly, you need to specify them. Your update includes a "new." on the left hand side of serialno: This works in <a href="http://sqlfiddle.com/#!1/c9ef3/1/0" rel="nofollow">http://sqlfiddle.com/#!1/c9ef3/1/0</a></p>

<pre><code>CREATE TABLE fieldtally
(fieldtally_id serial NOT NULL primary key,
  pipeno character varying,
  wthick real,
  heatno1 character varying(32),
  pipeno2 character varying(32),
  heatno2 character varying(32),
  Djointno character varying(32),
  ContractorNo character varying(32),
  measuredlength double precision,
  serialno character varying(32),
  CoatingType character varying(32),
  coatingno character varying(32),
  mnfcno character varying(32),
  FactoryLength double precision,
  pipeod_in numeric,
  pipeod_mm numeric,
  pipeweight double precision,
  pipegrade numeric,
  loadtally numeric,
  dateweilded date,
  datereceived date,
  dataenteredby character varying(50),
  deliveryno character varying(50),
  manufacturer character varying(50),
  Remarks character varying(100),
  ManualUser text,
  log_when timestamp
  );
  Create rule fieldtally_ins as on INSERT to fieldtally
  Do Instead
  Insert into fieldtally (pipeno, wthick, heatno1, pipeno2, heatno2, djointno, contractorno, measuredlength, serialno, coatingtype, coatingno,
                         mnfcno, factorylength, pipeod_in, pipeod_mm, pipeweight, pipegrade, manualuser, log_when) values (
                New.pipeno,
                New.wthick,
                New.heatno1,
                New.pipeno2,
                New.heatno2,
                New.Djointno,
                New.ContractorNo,
                New.measuredlength,
                New.serialno,
                New.coatingtype,
                New.coatingno,
                New.mnfcno,
                New.factorylength,
                New.pipeod_in,
                New.pipeod_mm,
                New.pipeweight,
                New.pipegrade,
                New.ManualUser, 
                current_timestamp
                );

CREATE RULE fieldtally_upd AS ON UPDATE TO fieldtally
    DO INSTEAD
    UPDATE fieldtally
    SET PIPENO = New.pipeno,
    wthick = New.wthick,
    heatno1 = New.heatno1,
    pipeno2 = New.pipeno2,
    heatno2 = New.heatno2,
    Djointno = New.Djointno,
    ContractorNo = New.ContractorNo,
    measuredlength = New.measuredlength,
    serialno = New.serialno,
    coatingtype = New.coatingtype,
    coatingno = New.coatingno,
    mnfcno = New.mnfcno,
    factorylength = New.factorylength,
    pipeod_in = New.pipeod_in,
    pipeod_mm = New.pipeod_mm,
    pipeweight = New.pipeweight,
    pipegrade =  New.pipegrade,
    ManualUser = New.ManualUser 
    WHERE pipeno = OLD.pipeno;      

CREATE RULE fieldtally_del AS ON DELETE TO fieldtally
    DO INSTEAD
    DELETE FROM fieldtally
     WHERE pipeno = OLD.pipeno;
</code></pre>

### Answer ID: 13094488
<p>user GO - so sql will not check the valitation before the last go</p>

<pre><code>CREATE TABLE fieldtally
    (fieldtally_id serial NOT NULL primary key,
      pipeno character varying,
      wthick real,
      heatno1 character varying(32),
      pipeno2 character varying(32),
      heatno2 character varying(32),
      Djointno character varying(32),
      ContractorNo character varying(32),
      measuredlength double precision,
      serialno character varying(32),
      CoatingType character varying(32),
      coatingno character varying(32),
      mnfcno character varying(32),
      FactoryLength double precision,
      pipeod_in numeric,
      pipeod_mm numeric,
      pipeweight double precision,
      pipegrade numeric,
      loadtally numeric,
      dateweilded date,
      datereceived date,
      dataenteredby character varying(50),
      deliveryno character varying(50),
      manufacturer character varying(50),
      Remarks character varying(100),
      ManualUser text,
      log_when timestamp
      );
GO
      Create rule fieldtally_ins as on INSERT to fieldtally
      Do Instead
      Insert into fieldtally values (
                    New.pipeno,
                    New.wthick,
                    New.heatno1,
                    New.pipeno2,
                    New.heatno2,
                    New.Djointno,
                    New.ContractorNo,
                    New.measuredlength,
                    New.serialno,
                    New.coatingtype,
                    New.coatingno,
                    New.mnfcno,
                    New.factorylength,
                    New.pipeod_in,
                    New.pipeod_mm,
                    New.pipeweight,
                    New.pipegrade,
                    New.ManualUser, 
                    current_timestamp
                    );
GO
        CREATE RULE fieldtally_upd AS ON UPDATE TO fieldtally
            DO INSTEAD
            UPDATE fieldtally
            SET PIPENO = New.pipeno,
            wthick = New.wthick,
            heatno1 = New.heatno1,
            pipeno2 = New.pipeno2,
            heatno2 = New.heatno2,
            Djointno = New.Djointno,
            ContractorNo = New.ContractorNo,
            measuredlength = New.measuredlength,
            New.serialno = New.serialno,
            coatingtype = New.coatingtype,
            coatingno = New.coatingno,
            mnfcno = New.mnfcno,
            factorylength = New.factorylength,
            pipeod_in = New.pipeod_in,
            pipeod_mm = New.pipeod_mm,
            pipeweight = New.pipeweight,
            pipegrade =  New.pipegrade,
            ManualUser = New.ManualUser 
            WHERE pipeno = OLD.pipeno;      
    GO
        CREATE RULE fieldtally_del AS ON DELETE TO fieldtally
            DO INSTEAD
            DELETE FROM fieldtally
             WHERE pipeno = OLD.pipeno;
</code></pre>


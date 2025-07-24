# How to execute sql query in different database
[Link to question](https://stackoverflow.com/questions/25133916/how-to-execute-sql-query-in-different-database)
**Creation Date:** 1407225963
**Score:** 1
**Tags:** c#, sql, nhibernate, enterprise-architect
## Question Body
<p>I'm writing addin to EA and I want to create new table in repository but I don't want to write query to every database type and also I don't know how to write one query, because eq. <code>AUTO_INCREMENT</code> exist in MySQL but in PostgreSQL doesn't. So what do you suggest? Should I use nHibernate or something else?</p>

<p>This is query in PostgreSQL I need to rewrite to other database:</p>

<pre><code>CREATE OR REPLACE FUNCTION create_history ()
  RETURNS void AS
$_$
BEGIN

IF EXISTS (
    SELECT *
    FROM   pg_catalog.pg_tables 
    WHERE  schemaname = 'public'
    AND    tablename  = 't_history'
    ) THEN
   RAISE NOTICE ' ';
ELSE
   CREATE TABLE t_history
(
  id integer NOT NULL DEFAULT nextval(('"object_id_seq"'::text)::regclass),
  object_id integer NOT NULL,
  object_type character varying(255),
  diagram_id integer DEFAULT 0,
  name character varying(255),
  alias character varying(255),
  author character varying(255),
  ch_author character varying(255),
  version character varying(50) DEFAULT '1.0'::character varying,
  note text,
  package_id integer DEFAULT 0,
  stereotype character varying(255),
  ntype integer DEFAULT 0,
  createddate timestamp without time zone DEFAULT now(),
  status character varying(50),
  abstract character(1),
  tagged integer DEFAULT 0,
  pdata1 character varying(255),
  pdata2 text,
  pdata3 text,
  pdata4 text,
  pdata5 character varying(255),
  concurrency character varying(50),
  visibility character varying(50),
  persistence character varying(50),
  cardinality character varying(50),
  gentype character varying(50),
  genfile character varying(255),
  header1 text,
  header2 text,
  phase character varying(50),
  scope character varying(25),
  genoption text,
  genlinks text,
  classifier integer,
  ea_guid character varying(40),
  parentid integer,
  runstate text,
  classifier_guid character varying(40),
  tpos integer,
  isroot integer DEFAULT 0,
  isleaf integer DEFAULT 0,
  isspec integer DEFAULT 0,
  isactive integer DEFAULT 0,
  stateflags character varying(255),
  packageflags character varying(255),
  multiplicity character varying(50),
  styleex text,
  actionflags character varying(255),
  eventflags character varying(255),
  CONSTRAINT t_history_pkey PRIMARY KEY (id)
);
END IF;

END;
$_$ LANGUAGE plpgsql;

SELECT create_history();
</code></pre>

<p><strong>EDIT</strong></p>

<p>Changed query</p>

<p><strong>MySQL</strong></p>

<pre><code>CREATE TABLE IF NOT EXISTS t_history
(
  id integer NOT NULL AUTO_INCREMENT,
  object_id integer NOT NULL,
  name character varying(255),
  author character varying(255),
  ch_author character varying(255),
  version character varying(50) DEFAULT '1.0',
  note text,
  package_id integer DEFAULT 0,
  stereotype character varying(255),
  createddate timestamp DEFAULT now(),
  pdata1 character varying(255),
  pdata2 text,
  pdata3 text,
  pdata4 text,
  phase character varying(50),
  CONSTRAINT t_history_pkey PRIMARY KEY (id)
);
</code></pre>

<p><strong>MSSQL</strong></p>

<pre><code>if not exists (select * from sys.tables where name = 't_history' and type = 'U')
CREATE TABLE t_history
(
  id integer NOT NULL IDENTITY PRIMARY KEY,
  object_id integer NOT NULL,
  name character varying(255),
  author character varying(255),
  ch_author character varying(255),
  version character varying(50) DEFAULT '1.0',
  note text,
  package_id integer DEFAULT 0,
  stereotype character varying(255),
  createddate datetime DEFAULT getdate(),
  pdata1 character varying(255),
  pdata2 text,
  pdata3 text,
  pdata4 text,
  phase character varying(50)
);
</code></pre>

## Answers
### Answer ID: 25134576
<p>Given the small size of your script it would probably be the best approach to just manually "translate" it to Oracle / MySQL / whatever database systems you need. It shouldn't take more than a few minutes and you can make good use of find/replace functionalities.</p>

<p>e.g. like this:</p>

<pre><code>Find: character varying
Replace with: VARCHAR2 

Find: text
Replace with: CLOB
</code></pre>

<p>This is unless you already have a big C# application anyway. In that case you could just use nHibernate (I assume it is like Hibernate for Java) and implement appropriate classes, functions and annotations/configs. This approach would also make sense if you are planning to use further SQL scripts in the future.</p>

<p>If this is the only script that you will ever make use of, Hibernate is pretty overkill though. It will create a huge overhead and take a lot more time to set up than simply "translating" the script into various other SQL dialects. It only really makes sense if you are going to have a lot of transactions with databases.</p>


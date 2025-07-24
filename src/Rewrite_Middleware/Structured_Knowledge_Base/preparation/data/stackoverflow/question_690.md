# Rewrite Select SQL query for PostgreSQL
[Link to question](https://stackoverflow.com/questions/37225114/rewrite-select-sql-query-for-postgresql)
**Creation Date:** 1463219070
**Score:** 0
**Tags:** sql, postgresql, postgresql-9.1, postgresql-9.3
## Question Body
<p>I created these tables in PostgreSQL based on this topic :</p>

<p><a href="https://stackoverflow.com/questions/10204902/database-design-for-user-settings">Database design for user settings</a></p>

<pre><code>-- TABLE SETTING

CREATE TABLE SETTING(
 ID INTEGER NOT NULL,
 DESCRIPTION TEXT,
 CONSTRAINED TEXT,
 DATA_TYPE TEXT,
 MIN_VALUE TEXT,
 MAX_VALUE TEXT
)
;

-- ADD KEYS FOR TABLE SETTING

ALTER TABLE SETTING ADD CONSTRAINT KEY34 PRIMARY KEY (ID)
;

-- TABLE ALLOWED_SETTING_VALUE

CREATE TABLE ALLOWED_SETTING_VALUE(
 ID INTEGER NOT NULL,
 SETTING_ID INTEGER,
 ITEM_VALUE TEXT,
 CAPTION TEXT
)
;

-- CREATE INDEXES FOR TABLE ALLOWED_SETTING_VALUE

CREATE INDEX IX_RELATIONSHIP16 ON ALLOWED_SETTING_VALUE (SETTING_ID)
;

-- ADD KEYS FOR TABLE ALLOWED_SETTING_VALUE

ALTER TABLE ALLOWED_SETTING_VALUE ADD CONSTRAINT KEY35 PRIMARY KEY (ID)
;

-- TABLE USER_SETTING

CREATE TABLE USER_SETTING(
 ID INTEGER NOT NULL,
 USER_ID INTEGER,
 SETTING_ID INTEGER,
 ALLOWED_SETTING_VALUE_ID INTEGER,
 UNCONSTRAINED_VALUE TEXT
)
;

-- CREATE INDEXES FOR TABLE USER_SETTING

CREATE INDEX IX_RELATIONSHIP15 ON USER_SETTING (SETTING_ID)
;

CREATE INDEX IX_RELATIONSHIP17 ON USER_SETTING (ALLOWED_SETTING_VALUE_ID)
;

-- ADD KEYS FOR TABLE USER_SETTING

ALTER TABLE USER_SETTING ADD CONSTRAINT KEY36 PRIMARY KEY (ID)
;
</code></pre>

<p>But when I run Select SQL query I get error because it's for MySQL:</p>

<pre><code>-- Show settings for a given user
select
  US.user_id 
, S1.description 
, S1.data_type 
, case when S1.constrained = 'true'
  then AV.item_value
  else US.unconstrained_value
  end value
, AV.caption
from USER_SETTING US
  inner join SETTING S1
    on US.setting_id = S1.id 
  left outer join ALLOWED_SETTING_VALUE AV
    on US.allowed_setting_value_id = AV.id
where US.user_id = 234
</code></pre>

<p><strong><em>result</em></strong></p>

<pre><code>ERROR:  syntax error at or near "value"
LINE 8:   end value
</code></pre>

<p>Howe I can rewrite this SQL query for PostgreSQL?</p>

## Answers
### Answer ID: 37226148
<p><code>value</code> is a reserved keyword, you need to quote it in SQL:</p>

<pre><code>case when S1.constrained = 'true'
    then AV.item_value
    else US.unconstrained_value
end "value"
</code></pre>

<p>Adding the <code>as</code> keyword works, because this remove the ambiguity what <code>value</code> might be. But it's still better to quote it - even when using the <code>as</code> keyword (or find a different name).</p>

<p><a href="http://www.postgresql.org/docs/current/static/queries-select-lists.html#QUERIES-COLUMN-LABELS" rel="nofollow">This behaviour is documented</a> and the manual explicitly mentions the keyword <code>value</code></p>

<blockquote>
  <p>The AS keyword is optional, but only if the new column name does not match any PostgreSQL keyword (see Appendix C). To avoid an accidental match to a keyword, you can double-quote the column name. For example, VALUE is a keyword, so this does not work:</p>
  
  <p><code>SELECT a value, b + c AS sum FROM ...</code></p>
  
  <p>but this does:</p>
  
  <p>SELECT a "value", b + c AS sum FROM ...</p>
  
  <p>For protection against possible future keyword additions, it is recommended that you always either write AS or double-quote the output column name.</p>
</blockquote>

<hr>

<p>Unrelated, but:</p>

<p>You shouldn't store boolean values (<code>true</code>, <code>false</code>)  in a <code>text</code> column. Postgres has a native <code>boolean</code> data type for this. </p>


# Identically formatted queries with different parameters have radically different execution times in MySQL 8.0
[Link to question](https://stackoverflow.com/questions/49623554/identically-formatted-queries-with-different-parameters-have-radically-different)
**Creation Date:** 1522736795
**Score:** 2
**Tags:** mysql, sql, query-optimization, mysql-8.0, query-planner
## Question Body
<p>EDIT: I have now solved this problem. Thank you Rick James for your help! Also: it wasn't part of the solution, but you were 100% right about prefix indexes. Performance actually went up slightly when I took them out.</p>

<p>.
.
.</p>

<p>I am having a strange database issue that I cannot make head nor tail of and I am hoping that this wise hive mind can help me. Put simply, I am finding that despite being formatted identically, some queries to my database are incredibly slow while others are nearly instant. For instance, this query:</p>

<pre><code>SELECT SQL_NO_CACHE DISTINCT pr.Master_Person_ID
FROM liverpool.person_record pr 
JOIN liverpool.person_property_view ppv1 ON (pr.Master_Person_ID = ppv1.Master_Person_ID)
JOIN liverpool.property_type_class ptc1 ON (ptc1.Property_ID = ppv1.Property_ID)
JOIN liverpool.person_property_view ppv2 ON (pr.Master_Person_ID = ppv2.Master_Person_ID)
JOIN liverpool.property_type_class ptc2 ON (ptc2.Property_ID = ppv2.Property_ID)
WHERE ptc1.Property_Class_ID = 2
AND ppv1.Property_Value = 'Ruth'
AND ptc2.Property_Class_ID = 6
AND ppv2.Property_Value = 'Davies'
ORDER BY pr.Year_From_Origin_Record, pr.Recorded_Date
LIMIT 100000;
</code></pre>

<p>Returns results in 0.06 seconds. More than fast enough for my needs. But <em>this</em> query:</p>

<pre><code>SELECT SQL_NO_CACHE DISTINCT pr.Master_Person_ID
FROM liverpool.person_record pr
JOIN liverpool.person_property_view ppv1 ON (pr.Master_Person_ID = ppv1.Master_Person_ID)
JOIN liverpool.property_type_class ptc1 ON (ptc1.Property_ID = ppv1.Property_ID)
JOIN liverpool.person_property_view ppv2 ON (pr.Master_Person_ID = ppv2.Master_Person_ID)
JOIN liverpool.property_type_class ptc2 ON (ptc2.Property_ID = ppv2.Property_ID)
WHERE ptc1.Property_Class_ID = 2
AND ppv1.Property_Value = 'Edward'
AND ptc2.Property_Class_ID = 6
AND ppv2.Property_Value = 'Abbott'
ORDER BY pr.Year_From_Origin_Record, pr.Recorded_Date
LIMIT 100000;
</code></pre>

<p>The only difference here are in the search parameters. But this second query takes more than <em>9 minutes</em> to execute. Longer still if using "LIKE" instead of "=". Certainly there are more 'Edward's' in my database than 'Ruth's,' but surely that alone couldn't account for why the second query is several <em>orders of magnitude</em> slower than the first? The query, as you can probably see, uses self-joins. I appreciate these might not be the most efficient way to do this, but they're fine for what I need and make my front end code MUCH simpler. And most of the time, they work fine. </p>

<p>Here is the EXPLAIN for the first (fast) query:</p>

<pre><code>id,select_type,table,partitions,type,possible_keys,key,key_len,ref,rows,filtered,Extra
1,SIMPLE,ptc1,NULL,ref,"PRIMARY,Property_ID_IDX,Property_Class_ID_IDX",Property_Class_ID_IDX,4,const,2,100.00,"Using index; Using temporary; Using filesort"
1,SIMPLE,pt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.ptc1.Property_ID,1,100.00,NULL
1,SIMPLE,rlt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.pt.Record_Link_Type_ID,1,100.00,"Using where; Using index"
1,SIMPLE,prp,NULL,ref,"PRIMARY,Property_Value_IDX,Person_Record_ID_IDX",Property_Value_IDX,23,"const,liverpool.ptc1.Property_ID",13,100.00,"Using where"
1,SIMPLE,pr,NULL,eq_ref,"PRIMARY,Master_Person_ID_IDX,Person_Record_ID_IDX",PRIMARY,4,liverpool.prp.Person_Record_ID,1,100.00,"Using where"
1,SIMPLE,rt,NULL,eq_ref,"PRIMARY,Record_Type_ID",PRIMARY,4,liverpool.pr.Record_Type_ID,1,100.00,"Using index"
1,SIMPLE,pr,NULL,ref,Master_Person_ID_IDX,Master_Person_ID_IDX,17,liverpool.pr.Master_Person_ID,1,100.00,NULL
1,SIMPLE,pr,NULL,ref,"PRIMARY,Master_Person_ID_IDX,Person_Record_ID_IDX",Master_Person_ID_IDX,17,liverpool.pr.Master_Person_ID,1,100.00,Distinct
1,SIMPLE,rt,NULL,eq_ref,"PRIMARY,Record_Type_ID",PRIMARY,4,liverpool.pr.Record_Type_ID,1,100.00,"Using index; Distinct"
1,SIMPLE,ptc2,NULL,ref,"PRIMARY,Property_ID_IDX,Property_Class_ID_IDX",Property_Class_ID_IDX,4,const,5,100.00,"Using index; Distinct"
1,SIMPLE,pt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.ptc2.Property_ID,1,100.00,Distinct
1,SIMPLE,rlt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.pt.Record_Link_Type_ID,1,100.00,"Using where; Using index; Distinct"
1,SIMPLE,prp,NULL,eq_ref,"PRIMARY,Property_Value_IDX,Person_Record_ID_IDX",PRIMARY,8,"liverpool.ptc2.Property_ID,liverpool.pr.Person_Record_ID",1,5.00,"Using where; Distinct"
</code></pre>

<p>And here is the EXPLAIN for the second (slow) query:</p>

<pre><code>id,select_type,table,partitions,type,possible_keys,key,key_len,ref,rows,filtered,Extra
1,SIMPLE,ptc1,NULL,ref,"PRIMARY,Property_ID_IDX,Property_Class_ID_IDX",Property_Class_ID_IDX,4,const,2,100.00,"Using index; Using temporary; Using filesort"
1,SIMPLE,pt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.ptc1.Property_ID,1,100.00,NULL
1,SIMPLE,rlt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.pt.Record_Link_Type_ID,1,100.00,"Using where; Using index"
1,SIMPLE,prp,NULL,ref,"PRIMARY,Property_Value_IDX,Person_Record_ID_IDX",Property_Value_IDX,23,"const,liverpool.ptc1.Property_ID",13,100.00,"Using where"
1,SIMPLE,pr,NULL,eq_ref,"PRIMARY,Master_Person_ID_IDX,Person_Record_ID_IDX",PRIMARY,4,liverpool.prp.Person_Record_ID,1,100.00,"Using where"
1,SIMPLE,rt,NULL,eq_ref,"PRIMARY,Record_Type_ID",PRIMARY,4,liverpool.pr.Record_Type_ID,1,100.00,"Using index"
1,SIMPLE,pr,NULL,ref,Master_Person_ID_IDX,Master_Person_ID_IDX,17,liverpool.pr.Master_Person_ID,1,100.00,NULL
1,SIMPLE,pr,NULL,ref,"PRIMARY,Master_Person_ID_IDX,Person_Record_ID_IDX",Master_Person_ID_IDX,17,liverpool.pr.Master_Person_ID,1,100.00,Distinct
1,SIMPLE,rt,NULL,eq_ref,"PRIMARY,Record_Type_ID",PRIMARY,4,liverpool.pr.Record_Type_ID,1,100.00,"Using index; Distinct"
1,SIMPLE,ptc2,NULL,ref,"PRIMARY,Property_ID_IDX,Property_Class_ID_IDX",Property_Class_ID_IDX,4,const,5,100.00,"Using index; Distinct"
1,SIMPLE,pt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.ptc2.Property_ID,1,100.00,Distinct
1,SIMPLE,rlt,NULL,eq_ref,PRIMARY,PRIMARY,4,liverpool.pt.Record_Link_Type_ID,1,100.00,"Using where; Using index; Distinct"
1,SIMPLE,prp,NULL,eq_ref,"PRIMARY,Property_Value_IDX,Person_Record_ID_IDX",PRIMARY,8,"liverpool.ptc2.Property_ID,liverpool.pr.Person_Record_ID",1,5.00,"Using where; Distinct"
</code></pre>

<p>I know that's almost impossible to read, but I can't for the life of me figure out how to paste/import anything in tabulated layout into this site...</p>

<p>The important part is that, as far as I can see, these two EXPLAINs show a functionally identical query plan! Yet one is <em>much</em> faster than the other. Is there something in how the planner is ordering these statements perhaps? I am fairly capable with SQL, but this query planner/indexing stuff is delving into the Dark Arts a little too far for me. Can anyone out there help?</p>

<p>I've tried adding and removing indexes. I've tried rewriting the queries using FORCE INDEX, but that only made them slower. I am at my wit's end here. </p>

<p>The only thing I can think of is that perhaps, if the two sides of the self-join are both sufficiently large (i.e., searching for a very common first name AND a very common last name), the combination of the two are overflowing some in-memory buffer somewhere and are instead being handled on disk. That seems like the only thing that would produce such a drastic slowdown in only <em>some</em> cases. So here's some indicative relevant numbers from the main (i.e., biggest) table being searched.</p>

<p>In the main data table (aliased as prp in the EXPLAIN), there are 24,771 records with a Property_Class corresponding to 'First_Name' and a Property_Value of 'Edward' and 567 records with a Property_Class corresponding to 'Last_Name' and with a Property_Value of 'Abbott.' The query that searches for these parameters takes many minutes to execute and usually times out the web server before it finishes.</p>

<p>Conversely, there are 916 records with a Property_Class corresponding to 'First_Name' and a Property_Value of 'Ruth' and 15,054 records with a Property_Class corresponding to 'Last_Name' and with a Property_Value of 'Davies.' The query that searches for these parameters takes 0.6 seconds to execute.</p>

<p>As you can see, both queries would likely involve a similar number of cross-matches (~14,000,000). Yet one is glacial and the other is not. </p>

<p>Anyway, I've tried increasing any likely sounding buffer type variables in my.ini to see if that helps, but I'm a little reluctant to experiment too hard in that respect given that I really don't know what I'm doing. I'm more a coder than a database server admin!</p>

<p>So if anyone out there has some insight for me, I'd be delighted to hear it!</p>

<p>Thank you for your time.</p>

<p>EDIT: The VIEW being used to stitch together the Property_Type, Person and Property_Value into a coherent entry is as follows:</p>

<pre><code>CREATE VIEW liverpool.person_property_view AS
SELECT 
prp.Person_Record_ID, 
pr.Record_Of_Origin_ID,
pr.Relationship_To_Origin_Record, 
pr.Recorded_Date,
pr.Year_From_Origin_Record,
pr.Master_Person_ID,
pr.Composite_Record_ID,
pr.Has_Been_Matched,
pr.First_Name,
pr.Other_Names,
pr.Last_Name,
pt.Property_ID,
pt.Property_Type_Name,
pt.Property_Type_Display_Name,
pt.Show_Property,
prp.Property_Value,
prp.Property_Display_Value,
prp.Property_Date_Value,
pt.Is_Downloadable,
pt.Is_Person_Record_Link,
pt.Is_Record_Link,
pt.Display_Only_Once,
pt.Property_Display_Order,
rt.Record_Type_Description,
rt.Record_Type_Sort_Order,
rt.Record_Type_Precedence,
rlt.Record_Link_Type_Code
FROM liverpool.person_record_property_value prp 
JOIN liverpool.person_record pr ON prp.Person_Record_ID = pr.Person_Record_ID
JOIN liverpool.property_type pt ON prp.Property_ID = pt.Property_ID
LEFT OUTER JOIN liverpool.record_link_type rlt ON pt.Record_Link_Type_ID = rlt.Record_Link_Type_ID
LEFT OUTER JOIN liverpool.record_type rt ON rt.Record_Type_ID = pr.Record_Type_ID;
</code></pre>

<p>And Here are the CREATE TABLE statements for what I think are the relevant tables here: </p>

<pre><code>CREATE TABLE liverpool.property_type (
  Property_ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  Property_Type_Name VARCHAR(255) DEFAULT NULL,
  Property_Type_Display_Name VARCHAR(255) DEFAULT NULL,
  Show_Property CHAR(1) DEFAULT 'Y',
  Is_Downloadable CHAR(1) DEFAULT 'Y',
  Is_Person_Record_Link CHAR(1) DEFAULT 'N',
  Is_Record_Link CHAR(1) DEFAULT 'N',
  Record_Link_Type_ID INT(11) DEFAULT NULL,
  Property_Display_Order INT(11) UNSIGNED DEFAULT 99,
  Display_Only_Once CHAR(1) DEFAULT 'N',
  PRIMARY KEY ( Property_ID ),
  INDEX Property_Type_Name_IDX ( Property_Type_Name(16) ASC )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE liverpool.person_record_property_value (
  Property_ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  Property_Value VARCHAR(2048) DEFAULT NULL,
  Property_Display_Value VARCHAR(2048) DEFAULT NULL,
  Property_Date_Value DATE DEFAULT NULL,
  Person_Record_ID INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY ( Property_ID, Person_Record_ID ),
  INDEX Property_Display_Value_IDX ( Property_Display_Value(16) ASC ),
  INDEX Property_Value_IDX ( Property_Value(16) ASC ),
  INDEX Property_Date_Value_IDX ( Property_Date_Value ASC )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
</code></pre>

<p>..</p>

<pre><code>CREATE TABLE liverpool.person_record (
   Person_Record_ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
   Composite_Record_ID VARCHAR(14) NULL,
   Record_Type_ID INT(11) UNSIGNED DEFAULT NULL,
   Record_Of_Origin_ID VARCHAR(255) NOT NULL,
   Relationship_To_Origin_Record VARCHAR(255) NOT NULL,
   Year_From_Origin_Record VARCHAR(45),
   Recorded_Date DATE DEFAULT NULL, 
   Master_Person_ID VARCHAR(14) NULL,
   Has_Been_Matched CHAR(1) DEFAULT 'N',
   PRIMARY KEY ( Person_Record_ID )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE liverpool.record_type (
  Record_Type_ID INT(11) UNSIGNED NOT NULL UNIQUE,
  Record_Type_Name VARCHAR(45) NOT NULL,
  Record_Of_Origin_Prefix VARCHAR(255) NOT NULL,
  Relationship_To_Origin_Record VARCHAR(255) NOT NULL,
  Record_Type_Description VARCHAR(255) NOT NULL,
  Record_Type_Sort_Order INT(11) UNSIGNED,
  Record_Type_Precedence INT(11) UNSIGNED,
  PRIMARY KEY ( Record_Type_ID ),
  INDEX Record_Type_Name_IDX ( Record_Type_Name(8) ASC )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE liverpool.record_link_type (
  Record_Type_ID INT(11) UNSIGNED NOT NULL,
  Record_Link_Type_ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  Record_Link_Type_Name VARCHAR(255) DEFAULT NULL,
  Record_Link_Type_Code VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY ( Record_Link_Type_ID ),
  INDEX Record_Link_Type_Name_IDX ( Record_Link_Type_Name(8) ASC )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
</code></pre>

<p>EDIT: oops... you're right, Rick James... these table defs were in a separate SQL script so I forgot them. Apologies.</p>

<pre><code>CREATE TABLE liverpool.property_class (
  Property_Class_ID INT(11) UNSIGNED NOT NULL,
  Property_Class_Name VARCHAR(255),
  Property_Class_Display_Name VARCHAR(255),
  Is_Searchable CHAR(1) DEFAULT 'Y',
  Metaphone_Level CHAR(16) DEFAULT '',
  Is_Number CHAR(1) DEFAULT 'N',
  Is_Date CHAR(1) DEFAULT 'N',
  Is_Link CHAR(1) DEFAULT 'N',
  Is_Ranged CHAR(8) DEFAULT '',
  Display_Order INT(11),
  PRIMARY KEY ( Property_Class_ID ),
  INDEX Property_Class_Name_IDX ( Property_Class_Name )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE liverpool.property_type_class (
  Property_Class_ID INT(11) UNSIGNED NOT NULL,
  Property_ID INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY ( Property_Class_ID, Property_ID ),
  INDEX Property_ID_IDX ( Property_ID ASC ),
  INDEX Property_Class_ID_IDX ( Property_Class_ID ASC )
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
</code></pre>

## Answers
### Answer ID: 49713956
<p>It's "over-normalized".</p>

<p>It's "EAV".</p>

<p>Put those two together and you get a lot of <code>JOINs</code> that cannot be optimized.  The processing must go back and forth a lot.</p>

<p>(No, I don't know why one query is significantly slower than the other.)</p>

<p>For more help, please provide <code>SHOW CREATE TABLE</code> and <code>SHOW CREATE VIEW</code>.</p>

<p>(After looking at <code>CREATE TABLEs</code>)</p>

<pre><code> INDEX Property_Type_Name_IDX ( Property_Type_Name(16) ASC )
</code></pre>

<p>"Prefix indexing" is virtually useless.  Remove the <code>(16)</code> since the column is not too big.  (It may not help the problem at hand.)  There are two other indexes like that, but they may need to stay as is unless you can shrink the declared size below 2048.</p>

<p>There are still more table definitions needed.</p>


# Talend 8.0.1 - Insert POINT data type into postgresql from csv file
[Link to question](https://stackoverflow.com/questions/78692681/talend-8-0-1-insert-point-data-type-into-postgresql-from-csv-file)
**Creation Date:** 1719842799
**Score:** 0
**Tags:** postgresql, talend
## Question Body
<p>I'm using Talend Open Studio 8.0.1 and I'm trying to import data from a csv file into a postgresql database.</p>
<p>I'll provide a simplified example of my specific issue :
My test.csv file is as below :</p>
<p>id,lon_lat</p>
<p>1,&quot;(450360.648, 122484.406)&quot;</p>
<p>2,&quot;(450384.431, 122363.579)&quot;</p>
<p>I'm trying to just insert this into a postgresql table with the same columns :
CREATE TABLE ntw.nodes (
id int8 NOT NULL,
lon_lat point NULL,
CONSTRAINT nodes_pk PRIMARY KEY (id)
);</p>
<p>My issue is with the lon_lat field, as I parse is as String in talend (talend does not have a point type), and when trying to insert it into my database with tPostgresqlOutput component, I get this error message :
ERROR: column &quot;lon_lat&quot; is of type point but expression is of type character varying
Hint: You will need to rewrite or cast the expression.</p>
<p>I do not know how to deal with this.
Additional info :</p>
<ol>
<li>I would prefer not to use tPostgresqlRow component as it does not offer batch insert</li>
<li>I have tried with different data type on talend without success</li>
<li>The query in this error message work if I just execute it (for example using dbeaver)</li>
<li>I think the way to do it is to use the Additional columns to replace lon_lat with an SQL expression that would cat the value of lon_lat as a point but I was not able to get the syntax right, nor did I find instruction that helped on the net</li>
</ol>
<p>EDIT : question has been answered by Zegarek. Apply the same method as in the post he links but with &quot;?::point&quot;</p>


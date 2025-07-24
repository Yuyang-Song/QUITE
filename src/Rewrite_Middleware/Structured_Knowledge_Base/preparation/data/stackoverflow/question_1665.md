# Is this a common database design / OO Mapping technique?
[Link to question](https://stackoverflow.com/questions/3211665/is-this-a-common-database-design-oo-mapping-technique)
**Creation Date:** 1278670670
**Score:** 2
**Tags:** schema, orm, relational-database
## Question Body
<p>I've recently been asked to rewrite a booking system that was not performing as well as a client would like.  I've found the database schema / object mapping technique used to be quite unusual and was wondering if anyone else has come across anything similar. </p>

<p>The old system used about 25 classes for things like customers, appointments and orders etc, each of which has a unique property called 'class_id'.</p>

<p>When looking at the database, each class had a corresponding table, however none of them contained any foreign key fields although they had to be linked in some way as the application allowed the client to carry out various levels of reporting.  </p>

<p>After further investigation, I noticed that the database contained another table called 'application_hierarchy'.</p>

<p>This table contained 4 columns which mapped out the relations between different records:</p>

<ol>
<li>class_id - Which identified the record type</li>
<li>object_id - Which referenced the id of the record within its corresponding table</li>
<li>parent_class_id - Which identified the record type of the related record</li>
<li>parent_object_id - Which referenced the id of the parent record within its corresponding table</li>
</ol>

<p>For example, if customer 5 has three different orders with id numbers 10, 11 and 12:</p>

<p>The Customer class was ID 4
The Order class was ID 7
So:</p>

<pre><code>class_id | object_id | parent_class_id | parent_object_id
7          10          4                 5
7          11          4                 5 
7          12          4                 5
</code></pre>

<p>There would be a large number of rows in this table for every single object record in the application and these would be combined with a large join query to create the reports.</p>

<p>Trying to import this data into the new schema has been an absolute nightmare, mainly because the original author has neglected to document which class is identified by which id number!  </p>

<p>Is this a commonly used technique or was the original developer just being a PITA?</p>

<p>Any advice / comments appreciated.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 3211913
<p>You might find you answer here : <a href="http://www.infoq.com/presentations/Generic-Specific-Tradeoffs-Stefan-Tilkov" rel="nofollow noreferrer">Stefan Tilkov: Thoughts on the Generic vs. Specific Tradeoff.</a> </p>


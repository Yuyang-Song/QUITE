# Anyone know of a method / tool to compare ad hoc SQL queries?
[Link to question](https://stackoverflow.com/questions/3987294/anyone-know-of-a-method-tool-to-compare-ad-hoc-sql-queries)
**Creation Date:** 1287663351
**Score:** 1
**Tags:** sql, comparison, diff, adhoc-queries
## Question Body
<p>I have to convert a lot of legacy SQL queries to stored procs (rewriting and tidying) and I'm looking for an efficient way to compare the results one by one to ensure I haven't modified the behaviour.  I currently use SQLDelta but it requires me to pipe the results of each query into tables and transfer one to a separate server using SSIS.  This is because SQL Delta is geared around comparing databases / tables rather than data sets.  It won't compare tables in the same DB.</p>

<p>Really what I want to know is does anyone have a method / tool to compare ad hoc query results in a SQLDelta manner (that is, matching up matching rows on PK, highlighting differences, spacing results to show additional / missing rows in each set).  Ideally I'd paste the before and after SQL in and generate the results.  Results sets can be ~10 to 200k rows and ~50 columns.</p>

<p>Can't believe I can't find something along these lines via google.  Any help appreciated.</p>

<p>Thanks</p>

## Answers
### Answer ID: 3987367
<p>One low tech way would be to output the results of each to a file, (SQL Manager has a 'Results to file' button) and use a diff tool like <a href="http://tortoisesvn.tigris.org/TortoiseMerge.html" rel="nofollow">tortoise merge</a>.</p>

<p>Edit</p>

<hr>

<p>If you have never pulled results from sql Manager as text it comes out in a tabular format.</p>

<pre><code>PrimaryLocation_FacilityLongName                                                                     SecondaryLocation_FacilityLongName                                                                   HasPublicComment HasPublicAttachment CMRID                                CustomerIDNumber
---------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------- ---------------- ------------------- ------------------------------------ ------------------------------
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 NULL             NULL                95FA6986-DB86-4E6F-8C48-05948AA94A30 1145
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 NULL             NULL                0E40FF65-804E-47F7-9BCC-112185196162 1146
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 NULL             NULL                908C5ADB-333C-42D0-9CDD-2FF196696B00 103
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 NULL             NULL                BA8239B2-BF53-451F-A6B2-44432D8B7BC7 1241
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 0                NULL                3B873A2C-4E1C-4E26-A3F7-6FDB0EE61EF2 1244
BCCH-Ambulatory Care Center                                                                          NULL                                                                                                 NULL             NULL                417242E8-E656-4AA3-A4B7-989E5740C84B 1239
</code></pre>

<p>As long as the queries are ordered.  All you have to do is open Tortoise merge and look for red spots in the files.  If there aren't any you are good to go.</p>


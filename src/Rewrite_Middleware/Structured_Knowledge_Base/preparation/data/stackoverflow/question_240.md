# Replacing Crystal Report data source with store procedure
[Link to question](https://stackoverflow.com/questions/17679917/replacing-crystal-report-data-source-with-store-procedure)
**Creation Date:** 1373986288
**Score:** 0
**Tags:** crystal-reports
## Question Body
<p>I used to create crystal reports by going into database expert, selecting tables and specifying the link manually. As I get a bit more comfortable with CR, there is a need for me to put the underlying SQL query into a store procedure to provide data to the report. But doing so will require me to rewrite the whole report which is time consuming. </p>

<p>So, my question is if there are any guru in the community that could and/or have tried to replace the underlying SQL (created by manually add table and links) with a store procedure or cmd without having to rewrite the whole report? I would love to get some hint of how to do that as I have a couple dozen of reports that need "adjustments" and time does not permit me to rewrite them all.</p>

<p>My Crystal Report versions are CR 2008 and CR 2012.</p>

<p>Thank you in advance. </p>

## Answers
### Answer ID: 17684885
<p>Crystal does an absolutely horrible job of migrating from many tables to a single DB object, be it a Command or stored procedure.</p>

<p>You might be able to <code>Database | Set datasource location...</code> to map your SP to one of the many tables in the report (choose the one that has the most fields in use); I've never been able to get this feature to work trying to map a Command to a table.</p>

<p>'Best practice' for a really-poor 'feature' set:</p>

<ul>
<li>create a formula field for each field that will be on the canvas, but isn't grouped (these fields won't be removed when you change datasources)</li>
<li>add the Command to the report; link tables if desired</li>
<li>manually switch grouping, record-selection formula, sorting, etc.</li>
</ul>

### Answer ID: 17680597
<p>In case you can use an existing software : this feature is available in a free Crystal reports viewer. Here is the documentation, which explains the use :
<a href="http://www.r-tag.com/Documents/RTag%20DataSource.pdf" rel="nofollow">http://www.r-tag.com/Documents/RTag%20DataSource.pdf</a>
 ... and here is where you can get your free license:
<a href="http://www.r-tag.com/Pages/FreeCrystalReportsViewer.aspx" rel="nofollow">http://www.r-tag.com/Pages/FreeCrystalReportsViewer.aspx</a></p>


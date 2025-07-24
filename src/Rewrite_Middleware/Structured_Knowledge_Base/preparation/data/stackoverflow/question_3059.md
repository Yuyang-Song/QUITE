# MS Access Report Group Totals
[Link to question](https://stackoverflow.com/questions/64363606/ms-access-report-group-totals)
**Creation Date:** 1602725171
**Score:** 0
**Tags:** ms-access, ms-access-2016
## Question Body
<p>Database set up to track neighborhood community membership.  For context: Neighborhood is divided into ten zones, with each zone further subdivided to the street level.  Each subzone has one or more streets, either partial or total.  Any one street can span mulitple subzones.  Addresses are fixed, but families move in and our.  Membership is optional.  Several tables set up to track all this.  Am having trouble getting one particular report set up.
Due to Access' not-quite-drag-and-drop queries when it comes to conditionals on left-joins (&quot;A left join B left join C where C.this_column is null&quot; uncooperative), I wasn't able to get the report done with a single query.  Thus, the basic structure is:</p>
<ul>
<li>Report query used to get street names, addresses, and identifiers for zone/subzone</li>
<li>subquery used to query resident, if there is one, and membership status for the past five years</li>
<li>Two group levels defined - subzone (one per page) and street (one or more per page)</li>
<li>Checkboxes reflect membership status for each year, and are pulled from the subquery, with the requisite &quot;=IIF(iserror(...&quot; to accommodate vacant addresses.</li>
<li>subzone footer contains textboxes for total memberships by year (sub of boxes checked)</li>
</ul>
<p>Problem: I can't get the subzone footers to &quot;add&quot;.  The prior report written for this entire project (one table, about 60 columns, with new columns each year) was able to do &quot;=Sum([checkbox-element-name])&quot; for this.  When I try to do same, and run the report, I get a pop-up box, prompting me for a value for .</p>
<p>Out of sheer frustration and brute force, the ultimate, hideous, solution I came up with was:</p>
<ul>
<li>Set checkbox from the subquery</li>
<li>Set hidden textboxes to store the value of each checkbox, with &quot;Running Sum = Over Group&quot;</li>
<li>In the street footer, hidden textboxes set to the checkbox element name (displays running total).  These are also set to &quot;Running Sum = Over Group&quot;.  Note, omitting this step meant subzones spanning multiple streets would only propagate the last street to the subzone footer</li>
<li>In the subzone footer, textboxes set to subzone footer textbox names - these are properly showing the totals over all streets within the subzone.</li>
</ul>
<p>Now that it's working, I hate leaving it in this state.  Using the Expression Builder at each step of the way, it recognized each element when I tried to use &quot;=Sum[element-name]&quot;, but still issued a pop-up prompt.  Any ideas what's going on here, and how I can successfully clean this up?  This is Office Professional 2016, running on Windows 10 Home.</p>
<p><strong>Edit, for clarity:</strong>  This is a complete rewrite of an older database.  It is the older one that was a &quot;one table, 60 column, adding columns per year&quot;.  The new database has been normalized to prevent such need in the future.  I only mention the old because the summations worked there.  They are not working in the new design.</p>
<p><strong>Edit 2: query detail</strong>  If I were to replace this all with a single query in mysql, this is what it would look like.  Please note, this is typed up cold, and not actually run.  If I could port this to MS Access, my whole problem will be solved.  It has worked...until I introduced the requirement on &quot;end_date is null&quot; - that indicates the current resident.  Deals with the scenario where a house has changed hands within the past five years.  We only want the address listed once, with the current resident.</p>
<pre><code>-- house: id, number, address, area, subarea
-- family: id, family_name
-- house_family: house_id, family_id, start_date, end_date (when family moved in/out)
-- membership: house_id, family_id, year (family was a member in this house, for this year)

SELECT h.area, h.subarea, h.street, h.number, f.family_name,
       IF(m4.year IS NULL, 'Y', 'N') 'Year-4',
       IF(m3.year IS NULL, 'Y', 'N') 'Year-3',
       IF(m2.year IS NULL, 'Y', 'N') 'Year-2',
       IF(m1.year IS NULL, 'Y', 'N') 'Year-1',
       IF(m0.year IS NULL, 'Y', 'N') 'Year-0',
FROM house h
     LEFT JOIN house_family hf ON h.id = hf.house_id
     LEFT JOIN family f ON hf.family_id = f.id
     LEFT JOIN membership m4 ON m4.house_id = h.id AND m4.family_id = f.id AND m4.year = YEAR(DATE_SUM(CURDATE(), INTERVAL 4 YEAR))
     LEFT JOIN membership m3 ON m3.house_id = h.id AND m3.family_id = f.id AND m3.year = YEAR(DATE_SUM(CURDATE(), INTERVAL 3 YEAR))
     LEFT JOIN membership m2 ON m2.house_id = h.id AND m2.family_id = f.id AND m2.year = YEAR(DATE_SUM(CURDATE(), INTERVAL 2 YEAR))
     LEFT JOIN membership m1 ON m1.house_id = h.id AND m1.family_id = f.id AND m1.year = YEAR(DATE_SUM(CURDATE(), INTERVAL 1 YEAR))
     LEFT JOIN membership m0 ON m0.house_id = h.id AND m0.family_id = f.id AND m0.year = YEAR(CURDATE())
WHERE hf.end_date IS NULL
GROUP BY h.id
</code></pre>


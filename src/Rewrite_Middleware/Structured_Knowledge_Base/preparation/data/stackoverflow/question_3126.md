# MS Access query criteria based on specific field in another query
[Link to question](https://stackoverflow.com/questions/67708734/ms-access-query-criteria-based-on-specific-field-in-another-query)
**Creation Date:** 1622045264
**Score:** 0
**Tags:** ms-access
## Question Body
<p>I have a MS Access Database that identifies all the members in MemberTable. These members are assigned supervisors in that table.</p>
<p>I also have a ManagerTable that identifies managers of sections.</p>
<p>For use in tables I have all individuals referenced to the AutoNum in the MemberTable so updates can be made easily.</p>
<p>I have QueryA that pulls all the information relating to the &quot;Member&quot;, including their &quot;Supervisor&quot;, to generate a report.</p>
<p>I have QueryB that pulls the &quot;Section&quot; they work in, a &quot;LeadManagerA&quot;, and a &quot;LeadManagerB&quot;.</p>
<p>These Lead Managers are also the supervisors of some individuals.</p>
<p>I am attempting to create a query that uses the criteria for &quot;Supervisor&quot; to only display the members whose supervisor is &quot;LeadManagerA&quot; of a specific &quot;Section&quot;.</p>
<p>Essentially my issue is, I don't want to use the specific name or Autonumber for &quot;LeadManagerA&quot; because that can change. And I can't figure out how to call a specific field from a specific row in QueryB for use in criteria.</p>
<p>MemberTable:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>AutoNum</th>
<th>Member</th>
<th>Supervisor</th>
<th>Item1</th>
<th>Item2</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Bob</td>
<td>2</td>
<td>Green</td>
<td>West</td>
</tr>
<tr>
<td>2</td>
<td>Susan</td>
<td></td>
<td>Blue</td>
<td>North</td>
</tr>
<tr>
<td>3</td>
<td>Tim</td>
<td>1</td>
<td>Blue</td>
<td>South</td>
</tr>
<tr>
<td>4</td>
<td>Jane</td>
<td>1</td>
<td>Red</td>
<td>North</td>
</tr>
<tr>
<td>5</td>
<td>Sam</td>
<td>3</td>
<td>Red</td>
<td>West</td>
</tr>
</tbody>
</table>
</div>
<p>ManagerTable:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Section</th>
<th>LeadManagerA</th>
<th>LeadManagerB</th>
</tr>
</thead>
<tbody>
<tr>
<td>TeamA</td>
<td>1</td>
<td>2</td>
</tr>
</tbody>
</table>
</div>
<p>QueryA:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Member</th>
<th>Supervisor</th>
</tr>
</thead>
<tbody>
<tr>
<td>Bob</td>
<td>Susan</td>
</tr>
<tr>
<td>Susan</td>
<td></td>
</tr>
<tr>
<td>Tim</td>
<td>Bob</td>
</tr>
<tr>
<td>Jane</td>
<td>Bob</td>
</tr>
<tr>
<td>Sam</td>
<td>Tim</td>
</tr>
</tbody>
</table>
</div>
<p>QueryB:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Section</th>
<th>LeadManagerA</th>
<th>LeadManagerB</th>
</tr>
</thead>
<tbody>
<tr>
<td>TeamA</td>
<td>Bob</td>
<td>Susan</td>
</tr>
</tbody>
</table>
</div>
<p>QueryICantFigureOut: (Criteria calling members whose Supervisor is TeamA LeadManagerA without using “Bob” as that individual can change and I would have to rewrite the criteria everytime it changed.)</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Member</th>
<th>Supervisor</th>
<th>Item1</th>
<th>Item2</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tim</td>
<td>Bob</td>
<td>Blue</td>
<td>South</td>
</tr>
<tr>
<td>Jane</td>
<td>Bob</td>
<td>Red</td>
<td>North</td>
</tr>
</tbody>
</table>
</div>
## Answers
### Answer ID: 67711217
<p>I figured it out. I was attempting to generate a query using multiple sources that access originally wouldn't allow. I had to make a query and create a join relationship with LeadManagerA and Supervisor.</p>


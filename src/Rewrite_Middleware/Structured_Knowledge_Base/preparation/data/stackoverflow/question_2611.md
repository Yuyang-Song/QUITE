# Incorrect rows returned from user query
[Link to question](https://stackoverflow.com/questions/42714308/incorrect-rows-returned-from-user-query)
**Creation Date:** 1489136711
**Score:** 2
**Tags:** sql, sql-server, database, join, stored-procedures
## Question Body
<p>I'm a newbie when it comes to SQLs and I require some help on this one, this is a little bit too complex to me to digest and make it work. What I have here is a stored procedure that will display a report for my clients when they input search parameters.</p>

<p>The tables I have are:</p>

<ol>
<li><p>TXN_RMReport - RMRID(pk), rmrPlant (fk, from FO_Property), rmrCID (fk, from     RM_Category), rmrBusinessArea, rmrCostCenter, rmrWCCode, rmrReportedBy</p></li>
<li><p>FO_Property - PID(pk), pCode, pMappingCode (contains RM_BusinessArea's             baBusinessArea)</p></li>
<li><p>RM_Category - CID(pk)</p></li>
<li><p>RM_BusinessArea - BAID(pk), baBusinessArea(code, not fk), baDescription</p></li>
<li><p>RM_CostCentre - CCID(pk), ccCostCenter, ccCompCode(code, based on FO_Property's pMappingCode, not fk) ccBusinessArea(code, based on baBusinessArea, not fk), ccDescription.</p></li>
<li><p>SEC_User - UID(pk), uName, uReportedBy</p></li>
</ol>

<p>The frankenstein problem here is that RM_CostCentre's CCID is not used for anything. In order for CostCentre's data to be uniquely identifiable for the report, it needs to refer to ccCompCode, ccCostCenter and ccBusinessArea.</p>

<p>For example, I have two pCode values called "RWB" and "RWMS", ccCostCenter "200" and "201", both are mapped to ccBusinessArea "FB" but has different descriptions "FOOD FACTORY" and "COFFEE TERRACE" respectively for "200" and "TASTE OF INDIA" and "HAINAN EXPRESS" for "201", for a total of 4 unique combinations.</p>

<p>The user can data pick from the database to fill in their forms. They can then insert the report into TXN_RMReport. The problem arises when they want to query their existing entry with empty parameters on Property, resulting in incorrect and duplicate rows that were never added in the first place, due to "200" or any other number being mapped to 2 different codes "RWB" and "RWMS".</p>

<pre><code> SET @SELECT_BASE =
' FROM TXN_RMReport
  INNER JOIN RM_BusinessArea (nolock) on rmrBusinessArea = baBusinessArea
  INNER JOIN RM_CostCentre (nolock) on rmrCostCenter = ccCostCenter
  LEFT JOIN SEC_User (nolock) on rmrRequestedBy = SEC_User.suUserID
  LEFT JOIN (Select WCID,wcCode,wclDesc from RM_WorkCentre (nolock) inner join RM_WorkCentre_Locale (nolock) on WCID = wclWCID) as A on rmrWCCode=A.wcCode
' + CASE WHEN @WithTypeOfWorks = 1 THEN '
  INNER JOIN TXN_RMDetail ON rmdRMRID = RMRID' ELSE '' END + '
  WHERE 0 = 0' + CASE WHEN @RMRID IS NOT NULL THEN
' AND RMRID = @RMRID' ELSE '' END + CASE WHEN @rmrSTAYID IS NOT NULL THEN
' AND rmrSTAYID = @rmrSTAYID' ELSE '' END + CASE WHEN @PID IS NOT NULL THEN
' AND rmrPID = @PID' ELSE '' END + CASE WHEN @rmrCID IS NOT NULL THEN
' AND rmrCID = @rmrCID' ELSE '' END + CASE WHEN @rmrStatusSTID IS NOT NULL THEN
' AND rmrStatusSTID = @rmrStatusSTID' ELSE '' END + CASE WHEN @rmrJobTicketNo IS NOT NULL THEN
' AND rmrJobTicketNo LIKE REPLACE(@rmrJobTicketNo,''*'',''%'')' ELSE '' END + CASE WHEN @rmrContactNo IS NOT NULL THEN
' AND rmrContactNo LIKE REPLACE(@rmrContactNo,''*'',''%'')' ELSE '' END + CASE WHEN @rmrAppointmentDate IS NOT NULL THEN
' AND rmrAppointmentDate = @rmrAppointmentDate' ELSE '' END + CASE WHEN @AppointmentDateFrom IS NOT NULL THEN
' AND rmrAppointmentDate &gt;= @AppointmentDateFrom' ELSE '' END + CASE WHEN @AppointmentDateTo IS NOT NULL THEN
' AND rmrAppointmentDate &lt;= @AppointmentDateTo' ELSE '' END 
</code></pre>

<p><a href="https://i.sstatic.net/e1imO.png" rel="nofollow noreferrer">Unintended Duplicate Rows</a></p>

<p>(The other tables are unrelated in this case and do not affect the search criteria) Here, the second rows should not exist for "1000" or "RWB", as the Cost Center column is mapped to "1001" instead, which should belong to "RWMS". The same is true likewise.</p>

<p>Even with the search criteria on however, the duplicate rows will still happen, which I have to "cheat" with these two lines:</p>

<pre><code>+ CASE @PID WHEN 39 THEN ' AND RM_CostCentre.ccCompCode = ''RWB''' ELSE '' END
+ CASE @PID WHEN 40 THEN ' AND RM_CostCentre.ccCompCode = ''RWMS''' ELSE '' END
</code></pre>

<p>How do I rewrite this so that I won't get the incorrect rows?</p>

<p>Incorrect table:</p>

<pre><code>+------+------+---------+-------------+------------+--------------+-------------+
| Code | Area | CCenter | DESCRIPTION | ReportedBy |   Remarks    | CreatedDate |
+------+------+---------+-------------+------------+--------------+-------------+
| RWB  | FB   |     200 | CTERRACE    | TANTAN     | NO CAKE      | 20/01/2017  |
| RWB  | FB   |     200 | FAVENUE     | TANTAN     | NO CAKE      | 20/01/2017  |
| RWMS | CS   |     501 | BACCARAT    | JIM        | SCRATCHED    | 20/01/2017  |
| RWB  | ADMC |     700 | CAFETERIA   | JIM        | BROKEN TILES | 21/01/2017  |
| RWB  | ADMC |     700 | HRESOURCE   | JIM        | BROKEN TILES | 21/01/2017  |
| RWMS | FB   |     200 | CTERRACE    | ELSA       | LEAKING PIPE | 20/01/2017  |
| RWMS | FB   |     200 | FAVENUE     | ELSA       | LEAKING PIPE | 20/01/2017  |
+------+------+---------+-------------+------------+--------------+-------------+
</code></pre>

<p>Expected Result:</p>

<pre><code>+------+------+---------+-------------+------------+--------------+-------------+
| Code | Area | CCenter | DESCRIPTION | ReportedBy |   Remarks    | CreatedDate |
+------+------+---------+-------------+------------+--------------+-------------+
| RWB  | FB   |     200 | CTERRACE    | TANTAN     | NO CAKE      | 20/01/2017  |
| RWMS | CS   |     501 | BACCARAT    | JIM        | SCRATCHED    | 20/01/2017  |
| RWB  | ADMC |     700 | CAFETERIA   | JIM        | BROKEN TILES | 21/01/2017  |
| RWMS | FB   |     200 | FAVENUE     | ELSA       | LEAKING PIPE | 20/01/2017  |
+------+------+---------+-------------+------------+--------------+-------------+
</code></pre>


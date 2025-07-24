# Access Table updating another Access Table based on variable fields
[Link to question](https://stackoverflow.com/questions/25731875/access-table-updating-another-access-table-based-on-variable-fields)
**Creation Date:** 1410205206
**Score:** 0
**Tags:** ms-access, vba, dao
## Question Body
<p>I think my first submission might have been a bit confusing so I decided to rewrite it to better explain what I am attempting to do.</p>

<p>I have an Access database.  In it there are two combo boxes, one containing all possible forms of annuity (that I'm dealing with) and the other combo box is the ones the user populates that apply to that particular client.  This master list is fed from a table (tblPickAnnuityForms).  This table has 3 fields, Name, VarName (these values match to another table), and Deleted (is a 1 or a 0 depending on if the user selected it).  I also have a second table called tblPlanSpecs.  This table, among other fields, has the fields that match up to the VarName field in the first table.</p>

<p>What I need to do, since tblPickAnnuityForms is basically a temporary table and it changes as you move between records (clients), is to repopulate it when you go to that record based on the values in tblPlanSpecs.  Once tblPickAnnuityForms is populated based on the previous elections for this record (client), the two combo boxes are re-queried to display the proper values (ie the left box shows the remaining, unused annuity forms and the right box shows the forms that apply to this client.  </p>

<p>Below is my attempt at doing this.  </p>

<pre><code>Dim db As DAO.Database
Dim rsList As DAO.Recordset
Dim rsData As DAO.Recordset
Dim CurrForm As String
Dim FormVal As Integer
Dim Plan As String

Set db = CurrentDb
Set rsList = db.OpenRecordset("tblPickAnnuityForms", dbOpenSnapshot)    

Plan = [Forms]![FrmHome]![PlanNameCalc].Value

Set rsData = db.OpenRecordset("SELECT tblPlanSpecs.LifeAnnuity, tblPlanSpecs.FiveCC, tblPlanSpecs.TenCC, " _
    &amp; "tblPlanSpecs.FifteenCC, tblPlanSpecs.TwentyCC, tblPlanSpecs.FiveCertain, tblPlanSpecs.TenCertain, " _
    &amp; "tblPlanSpecs.FifteenCertain, tblPlanSpecs.TwentyCertain, tblPlanSpecs.FiftyJS, tblPlanSpecs.SixtySixJS, " _
    &amp; "tblPlanSpecs.SeventyFiveJS, tblPlanSpecs.HundredJS, tblPlanSpecs.MCR FROM tblPlanSpecs " _
    &amp; "WHERE tblPlanSpecs.PlanName='" &amp; Plan &amp; "'")

Do

    CurrForm = rsList.Fields("VarName")
    FormVal = rsData.Fields(CurrForm)

    DoCmd.RunSQL ("UPDATE tblPickAnnuityForms " _
        &amp; "SET tblPickAnnuityForms.Deleted=" &amp; rsData! &amp; FormVal &amp; " " _
        &amp; "WHERE (((tblPickAnnuityForms.VarName)='" &amp; CurrForm &amp; "'))")

    MsgBox (CurrForm &amp; "changed to " &amp; FormVal)

    rsList.MoveNext

Loop Until rsList.EOF

If Not rsList Is Nothing Then
    rsList.CLOSE
    Set rsList = Nothing
End If
</code></pre>

<p>If there is a better solution, perhaps I can go in a different direction.  Currently this is bombing out in the loop where it says rsData! &amp; FormVal   It does not like using a variable to call a field.  Ideally I would like to avoid specifically calling every variable by name in code when populating rsData.  In other words, I want this to work no matter how many other options I add to my master list for the combo box, without going back in to add more items to select query.</p>

<p>Please let me know if I am unclear in my intended direction or methods.  I could really use the help figuring out what is wrong.</p>

## Answers
### Answer ID: 25752111
<p>Well, it seems I solved my own problem.  I had so many ideas running through my head, I half-implemented one and forgot.  The variable FormVal was already pulling the value I needed from rsData.  I then tried to pull the value again using FormVal as the field variable.  Anyway, below was the simple solution and everything works now.</p>

<pre><code>DoCmd.RunSQL ("UPDATE tblPickAnnuityForms " _
    &amp; "SET tblPickAnnuityForms.Deleted=" &amp; FormVal &amp; " " _
    &amp; "WHERE (((tblPickAnnuityForms.VarName)='" &amp; CurrForm &amp; "'))")
</code></pre>

<p>In other words, I didn't need to do rsData![ &amp; FormVal &amp; ] (which I am sure is improper syntax) I just needed to use FormVal by itself.</p>


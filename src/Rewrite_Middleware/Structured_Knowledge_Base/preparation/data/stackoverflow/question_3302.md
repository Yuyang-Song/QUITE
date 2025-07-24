# doCmd OpenQuery and RunMacro failed after moving database to New Folder
[Link to question](https://stackoverflow.com/questions/75460930/docmd-openquery-and-runmacro-failed-after-moving-database-to-new-folder)
**Creation Date:** 1676469595
**Score:** 1
**Tags:** vba, ms-access, dao, ado
## Question Body
<p>I have a database ready to be deployed with front end using excel. I'm using a combination of ADO and DAO to connect to access db. ADO is mainly for retrieving, updating and view data while DAO is mainly use for running access query or macros using openquery and runmacro method.</p>
<p>The issue start when i have move the database to new folder. My ADO connection is working fine after changing database path which i store in a variable string. However when it come to running access query and macro using DAO connection, it fail to run both query and macros. I have set progress bar to monitor the progress and i can see DAO successfully open connection to database but as soon as it reach to the .docmd.openquery or .docmd.runmacro it failed to run. The only error given is <strong>&quot;The OpenQuery action was cancelled&quot;</strong> or The <strong>&quot;RunMacro action was cancelled&quot;</strong></p>
<p>Below are my full code. I'm changing from path <strong>&quot;Y:\1_Year_2018\2_Admin_Main_Files\0_Database\2023\Database.accdb&quot;</strong> to path <strong>&quot;P:\Database.accdb&quot;</strong></p>
<p>Nothing is changing both in Access DB and Excel VBA. Only the location of the accdb been moved to P drive.</p>
<p>Is there some hidden link that i'm not aware of.</p>
<pre><code>Dim AC As Object
    Set AC = CreateObject(&quot;Access.Application&quot;)
    Dim strDatabasePath As String
    strDatabasePath = &quot;P:\Database.accdb&quot;

'    strDatabasePath = ThisWorkbook.Path &amp; &quot;\Database.accdb&quot;

    Call ProgressBar.Progress(5)
    Application.Wait (Now + TimeValue(&quot;0:00:01&quot;))

    With AC
        .OpenCurrentDatabase (strDatabasePath)

    Call ProgressBar.Progress(30)
    Application.Wait (Now + TimeValue(&quot;0:00:01&quot;))

        Dim db As Object

    Call ProgressBar.Progress(50)
    Application.Wait (Now + TimeValue(&quot;0:00:01&quot;))

        Set db = .CurrentDb

    Call ProgressBar.Progress(70)
    Application.Wait (Now + TimeValue(&quot;0:00:01&quot;))

        .DoCmd.SetWarnings False
        .DoCmd.OpenQuery &quot;qryUpdateInternalInvListing1&quot;
        .DoCmd.OpenQuery &quot;qryUpdate_ItnlNo_toCarrierInvSummary1&quot;
      
        .DoCmd.SetWarnings True
        .Quit
    End With
    ActiveWorkbook.RefreshAll
    
     Call ProgressBar.Progress(90)
    Application.Wait (Now + TimeValue(&quot;0:00:01&quot;))
    Call ProgressBar.Progress(100, False)
    ProgressBar.Hide
    
Application.ScreenUpdating = True

</code></pre>
<p>I have tried remove library reference and re-reference again. Rewriting the code from scratch again and tried to re-create the query in accdb and name it differently, but still nothing works. When i move the database back to old path, everything works 100%.</p>


# Pass-through query is empty when opened through VBA, but not when opened manually
[Link to question](https://stackoverflow.com/questions/75727975/pass-through-query-is-empty-when-opened-through-vba-but-not-when-opened-manuall)
**Creation Date:** 1678752275
**Score:** 1
**Tags:** sql-server, vba, ms-access-2016, pass-through
## Question Body
<p>I have an Access 2016 database connected to a local SQL Server (2019 Developer) instance.</p>
<p>For context, MyDbConn and MyADOParamDefinition below are custom classes which I created ages ago to simplify ADO calls. They're not really relevant, as this part of the code works. Also, dbo.UserVariablesInt is a table to save temporary int variables for the user, so that I can display pass-through queries without having to rewrite the query code each time.</p>
<p>Also just for context, [impexp].[udp_ImportSpreadsheet_PersonActionsAndEvents] is a stored procedure which runs an SSIS package. The SSIS package imports a local copy of a spreadsheet, does a few data transformations, finds people based on cell phone in the spreadsheet, and loads into another table. It also loads any rows with cell phones it did not find into a separate table, impexp.udp_ImportSpreadsheet_PersonActionsAndEvents. Since all of this works, I won't clutter stuff up here.</p>
<p>For the most part, all of this code works, except for one line (towards the bottom of the VBA code, indicated with &quot;!!!!!!!&quot;).</p>
<p>VBA code:</p>
<pre class="lang-vb prettyprint-override"><code>Private Sub SetUserVariable(ByRef dbconn As MyDbConn, iVariableTypeID As Integer, vIntValue As Variant, vVarcharValue As Variant, vDatetimeValue As Variant, vDecimalValue As Variant)
On Error GoTo Err_SetUserVariable

   Dim parm(5) As New MyADOParamDefinition, cmd As ADODB.Command, i As Integer
   Const sCommandText = &quot;[allusr].[udp_AddUpdateUserVariable]&quot;
   Const vCommandType = adCmdStoredProc
   
    If GetCurrentStaffID &gt; 0 Then
        Call parm(0).MakeParamDef(&quot;@StaffID&quot;, adInteger, iCurrentStaffID)
    Else
        Call parm(0).MakeParamDef(&quot;@StaffID&quot;, adInteger, Null) 'pass null to have the procedure fill in the User id of the current user
    End If
   
    Call parm(1).MakeParamDef(&quot;@VariableTypeID&quot;, adInteger, iVariableTypeID)
    Call parm(2).MakeParamDef(&quot;@VariableIntValue&quot;, adInteger, vIntValue)
    Call parm(3).MakeParamDef(&quot;@VariableVarcharValue&quot;, adVarChar, vVarcharValue, , -1)
    Call parm(4).MakeParamDef(&quot;@VariableDatetimeValue&quot;, adDate, vDatetimeValue)
    Call parm(5).MakeParamDef(&quot;@VariableDecimalValue&quot;, adDecimal, vDecimalValue, , , 18, 5)
   
    Set cmd = dbconn.RunProcedureWithParams(sCommandText, vCommandType, parm)
   
Exit_SetUserVariable:
    For i = LBound(parm) To UBound(parm)
        Set parm(i) = Nothing
    Next i
    Erase parm
    Set cmd = Nothing
    Exit Sub
   
Err_SetUserVariable:
    ShowErrorMessage Err, &quot;SetUserVariable&quot;
    Resume Exit_SetUserVariable
End Sub

Public Sub SetUserVariableInt(ByRef dbconn As MyDbConn, iVariableTypeID As Integer, vValue As Variant)
    Call SetUserVariable(dbconn, iVariableTypeID, vValue, Null, Null, Null)
End Sub


Private Sub ImportFromSpreadsheet(sFileLoc As String)
On Error GoTo Err_ImportFromSpreadsheet

    Dim dbcnn As New MyDbConn, bolSuccess As Boolean
    Dim parm(1 To 2) As New MyADOParamDefinition, i As Integer, cmd As ADODB.Command
   
    SetUserVariableInt dbcnn, 27, Me.txtActionID.Value
   
    Call parm(1).MakeParamDef(&quot;@ActionID&quot;, adInteger, Me.txtActionID.Value)
    Call parm(2).MakeParamDef(&quot;@FileName&quot;, adVarWChar, sFileLoc, , 250)
    Set cmd = dbcnn.RunProcedureWithParams(&quot;[impexp].[udp_ImportSpreadsheet_PersonActionsAndEvents]&quot;, adCmdStoredProc, parm)
   
    LoadPeopleList dbcnn
   
Exit_ImportFromSpreadsheet:
    For i = 1 To 2
        Set parm(i) = Nothing
    Next i
    Erase parm
    Set cmd = Nothing
    Set dbcnn = Nothing
    Exit Sub
   
Err_ImportFromSpreadsheet:
    ShowErrorMessage Err, &quot;ImportFromSpreadsheet&quot;
    Resume Exit_ImportFromSpreadsheet
End Sub

Private Sub cmdImportFromSpreadsheet_Click()
On Error GoTo Err_cmdImportFromSpreadsheet_Click

    Dim dbcnn As New MyDbConn
    Dim sServerDir As String, sLocalDir As String
    Const sFileName = &quot;EventImport.xlsx&quot;
   
    sServerDir = sDownloadsTopDir &amp; &quot;ZZ misc\Event Imports\\&quot; 'The double-slashes are actually single slashes in the code; I added the extra one for StackOverflow to fix the formatting.
   
    sLocalDir = sLocalImportExportDir &amp; GetCurrentStaffID() &amp; &quot;\\&quot;
    If CheckForStaffRole(dbcnn, GetCurrentStaffIDWithConn(dbcnn), ude_StaffRole.ImportExportOperator) = False Then
        MsgBox &quot;Cannot load from a spreadsheet. You do not have the appropriate permissions. Please contact a user admin to request 'Non-download Imports and Exports Operator' permissions.&quot;
       GoTo Exit_cmdImportFromSpreadsheet_Click
   End If

    If IsNull(Me.txtActionID.Value) Then
        MsgBox &quot;There's no ActionID yet. Please save this action and try again.&quot;
    ElseIf CopyFileToLocalComputer(sServerDir, sFileName) = True Then
        ImportFromSpreadsheet sLocalDir &amp; sFileName

        ' !!!!!!!This line (below) is where it gets weird!!!!!!!
         DoCmd.OpenQuery &quot;qryImpExpResults_PersonActions_CellNotFound&quot;
    Else
        MsgBox &quot;There was an issue copying the file from the file server to the 'local' (i.e. the machine SQL Server is running on) for import. Import cancelled.&quot;
    End If
   
Exit_cmdImportFromSpreadsheet_Click:
    Set dbcnn = Nothing
    Exit Sub
   
Err_cmdImportFromSpreadsheet_Click:
    ShowErrorMessage Err, &quot;cmdImportFromSpreadsheet_Click&quot;
    Resume Exit_cmdImportFromSpreadsheet_Click
End Sub
</code></pre>
<p>The above code runs, but when it opens the &quot;qryImpExpResults_PersonActions_CellNotFound&quot; pass-through query, it is empty, even though there should be one cell not found in my test case.<br />
When I open it manually, it has one record in it (as it should).</p>
<p>SQL for the pass-through query:</p>
<pre><code>SELECT FirstName, LastName, CellPhone 
        FROM [impexp].[PersonActionsAndEventsImport_CellNoMatch] 
        WHERE ActionID = allusr.udf_GetUserVariableInt(27,allusr.udf_CurrentStaffID())
ORDER BY LastName, FirstName
</code></pre>
<p>Here are the possibly-relevant supporting functions and procedures:</p>
<pre><code>CREATE PROCEDURE [allusr].[udp_AddUpdateUserVariable] 
    -- Add the parameters for the stored procedure here
    @StaffID int=null,
    @VariableTypeID int,
    @VariableIntValue int=null,
    @VariableVarcharValue varchar(max)=null,
    @VariableDatetimeValue datetime=null,
    @VariableDecimalValue decimal=null
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    -- Insert statements for procedure here
BEGIN TRY  
    DECLARE @PrintOutput varchar(150)
    -- SET @PrintOutput = '@StaffID = ' + CASE WHEN @StaffID IS NULL THEN 'Null' ELSE CONVERT(varchar(20), @StaffID) END
    -- RAISERROR (@PrintOutput, 10, 1) WITH NOWAIT

    IF (@StaffID IS NULL)   -- If the staffid of the current user was not supplied, find it in the Staff table
    BEGIN
        DECLARE @CurrentUser nvarchar(255) = SUSER_SNAME()
        SELECT @StaffID = [allusr].[udf_CurrentStaffID]()
        -- SET @PrintOutput = '@StaffID = ' + CASE WHEN @StaffID IS NULL THEN 'Null' ELSE CONVERT(varchar(20), @StaffID) END
        -- RAISERROR (@PrintOutput, 10, 1) WITH NOWAIT
        IF @StaffID IS NULL -- raise error if staffid wasn't found
        BEGIN
            DECLARE @msg NVARCHAR(2048) = FORMATMESSAGE(50001, @CurrentUser);
            THROW 50001, @msg, 1;
        END
    END

    -- Get the variable data type (used to determine where the variable is stored)
    DECLARE @VarDataTypeDesc varchar(20)
    DECLARE @StaffVarID int

    SELECT @VarDataTypeDesc = dt.[StaffVariableDataType] 
    FROM [list].[DataTypes] dt INNER JOIN [list].[UserVariableTypes] svt ON dt.DataTypeID = svt.DataTypeID 
    WHERE svt.VariableTypeID = @VariableTypeID

    -- update or add the staff variable (which table depends on the data type)
    IF @VarDataTypeDesc = 'int'
    BEGIN
        IF EXISTS (SELECT 1 FROM [dbo].[UserVariablesInt] WHERE StaffID = @StaffID AND [VariableTypeID] = @VariableTypeID) -- update
        BEGIN
            UPDATE [dbo].[UserVariablesInt] SET VariableIntValue = @VariableIntValue, DateLastModified = SYSDATETIME()  WHERE StaffID = @StaffID AND VariableTypeID = @VariableTypeID
        END
        ELSE -- insert
        BEGIN
            INSERT INTO [dbo].[UserVariablesInt] (StaffID, VariableTypeID, VariableIntValue) 
            VALUES (@StaffID, @VariableTypeID, @VariableIntValue)
        END
    END

    IF @VarDataTypeDesc = 'datetime'
     --N/A - snipping code

    IF @VarDataTypeDesc = 'decimal'
     --N/A - snipping code

    IF @VarDataTypeDesc = 'varchar'
     --N/A - snipping code


END TRY  
BEGIN CATCH  
    THROW;
END CATCH;  
END
GO

CREATE FUNCTION [allusr].[udf_GetUserVariableInt]
(
    -- Add the parameters for the function here
    @VariableTypeID int
    ,@StaffID int=null
)
RETURNS int
AS
BEGIN
    -- Declare the return variable here
    DECLARE @ResultVar int

    -- Add the T-SQL statements to compute the return value here
    SELECT @ResultVar = VariableIntValue
        FROM [dbo].[UserVariablesInt] v
        WHERE (StaffID = COALESCE(@StaffID, [allusr].[udf_CurrentStaffID]())) AND VariableTypeID = @VariableTypeID

    -- Return the result of the function
    RETURN @ResultVar

END

CREATE FUNCTION [allusr].[udf_CurrentStaffID]()
RETURNS int
AS
BEGIN
    -- Declare the return variable here
    DECLARE @ResultVar int

    -- Add the T-SQL statements to compute the return value here
    SELECT @ResultVar = s.StaffID 
    FROM [dbo].[Staff] s
    INNER JOIN [dbo].[StaffUsernames] su ON s.StaffID = su.StaffID
    WHERE su.UserName = SUSER_SNAME() AND s.IsActive = 1

    -- Return the result of the function
    RETURN @ResultVar

END
</code></pre>
<p>Why would opening the pass-through query with docmd.openquery shows it as empty?</p>
<hr />
<p>QL Profiler revealed that, apparently, the query didn't run when I ran it through VBA, but it did run when I ran it manually. It does run properly when I use a separate button to run the query.</p>


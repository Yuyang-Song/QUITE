# VB.NET - SQL UpdateCommand for table without primary key in Gridview
[Link to question](https://stackoverflow.com/questions/4934497/vb-net-sql-updatecommand-for-table-without-primary-key-in-gridview)
**Creation Date:** 1297176662
**Score:** 0
**Tags:** sql, vb.net, gridview, updatecommand
## Question Body
<p>1) What's the syntax for a Update query for a table without a primary key in vb.net for a gridview with a checkbox?</p>

<p>Disclaimer: Frustratingly, adding a primary key is not an option. My program is a small program in a much larger system with poor data management. My development time does not include rewriting the other software.</p>

<p>Here are the Columns for the table Where AgentLeads is the database and MktDtaLeads_Scrubbed is the table:   </p>

<pre><code>FROM [AgentLeads].[dbo].[MktDtaLeads_Scrubbed] - [Last Name] ,[First Name],
     [Middle Name] ,[Suffix] ,[Address Line 1] ,[Address Line 2] ,[City] ,[ST],
     [ZipCode] ,[Email Address] ,[Phone Nbr] ,[Toll Free Nbr] ,[InsertDate] ,
     [SentDate] ,[DoNotMail] 
</code></pre>

<p>The code I have right now doesn't display any errors but doesn't update the DoNotMail field when you check the checkbox even though it does display the text "The DoNotMail value has been changed in the database for the selected field".</p>

<p>For the default.aspx.vb code behind I added: </p>

<pre><code>Public Sub gridview1_RowCommand(ByVal sender As Object, ByVal e As GridViewCommandEventArgs)


     If e.CommandName = "UpdateDoNotMail" Then

        With Me.SqlDataSource1
           Dim box As CheckBox = DirectCast(sender, CheckBox)


           If box.Checked = True Then

               donotmail.SelectedValue = 1


               .ConnectionString = ConfigurationManager.AppSettings("AgentLeadsConnectionString").ToString

               .UpdateCommand = "UPDATE MktDataLeads_scrubbed set donotmail=@donotmail 
               WHERE [last name]=@lastname.selectedrow AND [first name]=@firstname.selectedrow AND [Address Line 1]=@Address Line 1.selectedrow" 

           Else
               donotmail.SelectedValue = 0


               .ConnectionString = ConfigurationManager.AppSettings("AgentLeadsConnectionString").ToString


               .UpdateCommand = "UPDATE MktDataLeads_scrubbed set donotmail=@donotmail
               WHERE [last name]=@lastname.selectedrow AND [first name]=@firstname.selectedrow AND [Address Line 1]=@Address Line 1.selectedrow"

           End If
       End With

    End If
End Sub
</code></pre>

<p>Here's the code for the GridView on default.aspx:</p>

<pre><code>        &lt;asp:GridView ID="GridView2" runat="server" CellPadding="2" 
            DataSourceID="SqlDataSource1" ForeColor="#333333" GridLines="None" 
            AutoGenerateColumns="False"&gt;
            &lt;Columns&gt;
                &lt;asp:BoundField DataField="Last Name" HeaderText="Last Name" 
                    SortExpression="Last Name" /&gt;
                &lt;asp:BoundField DataField="First Name" HeaderText="First Name" 
                    SortExpression="First Name" /&gt;
                &lt;asp:BoundField DataField="Address Line 1" HeaderText="Addr 1" 
                    SortExpression="Address Line 1" /&gt;
                &lt;asp:BoundField DataField="Address Line 2" HeaderText="Addr 2" 
                    SortExpression="Address Line 2" /&gt;
                &lt;asp:BoundField DataField="City" HeaderText="City" SortExpression="City" /&gt;
                &lt;asp:BoundField DataField="ST" HeaderText="ST" SortExpression="ST" /&gt;
                &lt;asp:BoundField DataField="ZipCode" HeaderText="ZipCode" 
                    SortExpression="ZipCode" /&gt;
                &lt;asp:BoundField DataField="Email Address" HeaderText="Email Addr" 
                    SortExpression="Email Address" /&gt;
                &lt;asp:BoundField DataField="Phone Nbr" HeaderText="Phone Nbr" 
                    SortExpression="Phone Nbr" /&gt;

         &lt;asp:TemplateField HeaderText="DoNotMail" SortExpression="DoNotMail"&gt;     
         &lt;ItemTemplate&gt;         
         &lt;asp:CheckBox ID="CheckBox1" runat="server" AutoPostBack="true" CommandName="UpdateDoNotMail" Checked='&lt;%# Bind("DoNotMail") %&gt;'
                       Enabled="true" /&gt;     
         &lt;/ItemTemplate&gt;     

         &lt;EditItemTemplate&gt;         
         &lt;asp:CheckBox ID="CheckBox1" runat="server" AutoPostBack="true" CommandName="UpdateDoNotMail" Checked='&lt;%# Bind("DoNotMail") %&gt;' /&gt;     
         &lt;/EditItemTemplate&gt;       
         &lt;/asp:TemplateField&gt; 

            &lt;/Columns&gt;
</code></pre>

<p>2) is it possible to do a two way sync on the entire gridview when the user hits a button so you don't have to do an update every time a row is changed? because the user might check the box and then check another box then uncheck a box and it would be a lot of updates... </p>

## Answers
### Answer ID: 4938602
<p>Here's the code for the GridView on default.aspx:</p>

<p>I used a variation of the code detailed on this page and got it to work! <a href="https://stackoverflow.com/questions/4239394/vb-net-sql-query-works-in-sql-server-but-not-when-called-from-checkbox">vb.net SQL query works in SQL server but not when called from checkbox</a>    </p>

<p>For the default.aspx.vb code behind I added: </p>

<pre><code>    Public Sub checkbox_CheckedChanged(ByVal sender As Object, ByVal e As EventArgs) 'Handles checkbox.CheckedChanged
    Dim connectionString As String = ConfigurationManager.ConnectionStrings("AgentLeadsConnectionString").ConnectionString


    Dim box As CheckBox = DirectCast(sender, CheckBox)
    Dim tblcell As TableCell = CType(box.Parent, TableCell)
    Dim dgRow As GridViewRow = CType(tblcell.Parent, GridViewRow)

    Dim lastname As String = [last name].Rows(dgRow.DataItemIndex).Cells(0).Text
    Dim firstname As String = [first name].Rows(dgRow.DataItemIndex).Cells(0).Text
    Dim address As String = [Address Line1].Rows(dgRow.DataItemIndex).Cells(0).Text

    Dim insertSQL As String

    If box.Checked = True Then
        insertSQL = "UPDATE MktDataLeads_scrubbed "
        insertSQL &amp;= "SET donotmail=1 "
        insertSQL &amp;= "WHERE [last name]= @lastname AND [first name]=@firstname AND [Address Line1]=@address "
    Else
        insertSQL = "UPDATE MktDataLeads_scrubbed "
        insertSQL &amp;= "SET donotmail=0 "
        insertSQL &amp;= "WHERE [last name]= @lastname AND [first name]=@firstname AND [Address Line1]=@address "
    End If

    Using con As New SqlConnection(connectionString)
        Dim cmd As New SqlCommand(insertSQL, con)
        cmd.Parameters.AddWithValue("@donotmail", donotmail)
        Try
            con.Open()
            cmd.ExecuteNonQuery()
        Catch Err As SqlException
            MsgBox("Error", 65584, "Insertion Error")
        End Try
        con.Close()
    End Using

End Sub
</code></pre>

<p>For the gridview I used the same code: </p>

<pre><code>             &lt;asp:TemplateField HeaderText="DoNotMail" SortExpression="DoNotMail"&gt;     
             &lt;ItemTemplate&gt;         
             &lt;asp:CheckBox ID="CheckBox" runat="server" AutoPostBack="true" OnCheckedChanged="checkbox_CheckedChanged" Checked='&lt;%# Bind("DoNotMail") %&gt;'
                           Enabled="true" /&gt;     
             &lt;/ItemTemplate&gt;     
             &lt;EditItemTemplate&gt;         
             &lt;asp:CheckBox ID="CheckBox" runat="server" AutoPostBack="true" OnCheckedChanged="checkbox_CheckedChanged" Checked='&lt;%# Bind("DoNotMail") %&gt;' /&gt;     
             &lt;/EditItemTemplate&gt;       
             &lt;/asp:TemplateField&gt;
</code></pre>

### Answer ID: 4935153
<p>This is a tough situation to be in because you can't distinguish between records that are identical without a unique primary key.</p>

<p>What you can do, however, is to make use of <a href="http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.gridviewupdatedeventargs.oldvalues.aspx" rel="nofollow">GridView's OldValues property</a>. This isn't how developers usually handle GridViews but I think it may just be your savior here.</p>

<p>For example, to figure out which row to update, you'd set your <code>where</code> clause to all the OldValues of every property, and update accordingly. Because of your sticky situation, you may just end up updating more than one row - but that's the price you pay for no primary key. </p>


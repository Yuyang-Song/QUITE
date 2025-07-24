# Creating an ASP.NET Treeview with multiple levels
[Link to question](https://stackoverflow.com/questions/9786720/creating-an-asp-net-treeview-with-multiple-levels)
**Creation Date:** 1332246384
**Score:** 1
**Tags:** asp.net, sql, xml, vb.net, treeview
## Question Body
<p>I have a requirement to create a multi level treeview in ASP.Net (with VB) but I am completely stuck on how to start this. Currently my treeview is a fixed 2 level approach but now I need to rewrite this to be more dynamic and support extra levels being added into our database tables.</p>

<p>So this treeview needs to support as many levels as needed without having to rewrite any code each time we want to add new level, Ideally we will just insert the data at the database level.</p>

<p>I think I have the database part designed correctly, I created 2 tables <code>Menu</code> and <code>MenuItems</code></p>

<p><code>Menu</code> has 2 columns <code>ItemID</code> and <code>ChildID</code></p>

<p><code>MenuItems</code> has 2 columns <code>ItemID</code> and <code>Description</code> </p>

<p>Doing this query:</p>

<pre><code>SELECT 
    menu.Item_ID, 
    menu.Child_ID , 
    parent.ID,
    parent.Description,
    child.ID,
    child.Description 
FROM 
    tblSupportTicketMenu menu
JOIN 
    tblSupportTicketMenuItems parent
ON
    parent.ID = menu.Item_ID
JOIN
    tblSupportTicketMenuItems child
ON
    child.ID = menu.Child_ID 
</code></pre>

<p>Will return this data:</p>

<pre><code>Item_ID     Child_ID    ID          Description                                                                                          ID          Description
----------- ----------- ----------- ---------------------------------------------------------------------------------------------------- ----------- ----------------------------------------------------------------------------------------------------
32          33          32          Level 1                                                                                              33          Level 2
33          34          33          Level 2                                                                                              34          Level 3
35          36          35          Item 2 Level 1                                                                                       36          Item 2 Level 2
36          37          36          Item 2 Level 2                                                                                       37          Item 2 Level 3
</code></pre>

<p>From here I am unsure where to go, I read that the asp Treeview can take XML as its datasource and this seems to be a good idea, but how could I select the data into a format which would support multiple levels etc?</p>

<p>If anyone knows how to do this or could link me to a guide I would be very appreciative, also if doing this as XML is a bad idea I am open to other suggestions, I'm still learning ASP.Net so I would like to do this properly.</p>

<p>To be thorough this is the code I am currently replacing which generates the treeview for me.</p>

<pre><code>   Dim ds As New DataTable

      Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("Blueprint").ToString())

      Dim cmd As New SqlCommand
      cmd.CommandType = CommandType.StoredProcedure
      cmd.CommandText = "spGetMenuItemsForTickets"

      cmd.Connection = conn

      Using da As New SqlDataAdapter(cmd)
         conn.Open()
         da.Fill(ds)
         conn.Close()
      End Using

      Dim ParentIds As List(Of Integer) = New List(Of Integer)

      For Each row As DataRow In ds.Rows

         If ParentIds.Contains(row("ParentID")) Then
            '' Do Nothing 
         Else
            ParentIds.Add(row("ParentID"))
         End If
      Next

      For Each Parent As Integer In ParentIds
         Dim parentNode As New System.Web.UI.WebControls.TreeNode

         For Each child In ds.Rows
            If (child("ParentID") = Parent) Then

               Dim childNode As New System.Web.UI.WebControls.TreeNode

               parentNode.Text = child("ParentDescription")
               parentNode.Value = child("ParentID")
               parentNode.Expanded = False

               childNode.Text = child("ChildDescription")
               childNode.Value = child("ChildID")


               parentNode.SelectAction = TreeNodeSelectAction.None
               parentNode.ChildNodes.Add(childNode)
            End If
         Next
         trvItem.Nodes.Add(parentNode)
      Next

      trvItem.Nodes(0).Text += String.Empty
</code></pre>

## Answers
### Answer ID: 9789469
<p>The database structure you have created seems ok however rename itemid to parentid and childid to itemid would be more understandable to me ( I like to see parentid for the current item)</p>

<p>You can go step by step by reading following link , they tried to make it simple to understand. I hope this will help.</p>

<p><a href="http://aspalliance.com/732_Display_Hierarchical_Data_with_TreeView_in_ASPNET_20" rel="nofollow">http://aspalliance.com/732_Display_Hierarchical_Data_with_TreeView_in_ASPNET_20</a></p>


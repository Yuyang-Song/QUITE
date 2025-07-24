# How to store user&#39;s information for future use from MySQL
[Link to question](https://stackoverflow.com/questions/55767661/how-to-store-users-information-for-future-use-from-mysql)
**Creation Date:** 1555706708
**Score:** 1
**Tags:** mysql, .net, vb.net
## Question Body
<p>I have a very simple application where a user will login and be redirected to the dashboard. I got the login part working, however, my next goal is to be able to store the users information for later use on other forms. </p>

<p>Example: User "admin" logs in successfully. I need to be able to store every column in the table for <strong><code>admin</code></strong> so that we can call the user's information for welcome messages, user information form, etc without having to query the database everytime.</p>

<p>I believe this can be accomplished with a class, however, I'm unsure how to rewrite my login script to save all details into a class.</p>

<p>I've tried creating a class, and adding <code>Public Shared</code> properties for each column but I'm not sure how to get every column into the class rather than just the username.</p>



<pre class="lang-vb prettyprint-override"><code>Imports MySql.Data.MySqlClient

Public Class frmLogin
    'count is number of invalid login attempts
    Dim count As Integer
    Private Sub btnLogin_Click(sender As Object, e As EventArgs) Handles btnLogin.Click
        count = count + 1
        Dim x As New MySqlConnection
        Dim admin As New MySqlCommand
        Dim dr1 As MySqlDataReader
        ConnectDatabase()
        admin.Connection = conn
        admin.CommandText = "SELECT user.username, user.password FROM user WHERE user.username = '" &amp; txtUsername.Text &amp; "' and user.password = '" &amp; txtPassword.Text &amp; "'"
        dr1 = admin.ExecuteReader

        If dr1.HasRows Then
            'Read the data
            dr1.Read()

            Me.Hide()
            frmDashboard.Show()
        Else
            MsgBox("Invalid Username or Password! " &amp; vbCrLf &amp; count &amp; " out of 3 attempts remaining.")

            If count &gt;= 3 Then
                MsgBox("You have exceeded the maximum number of attempts to login. Account has been disabled. Please contact OJFS helpdesk at extension 100.", MsgBoxStyle.Critical)
                txtUsername.Enabled = False
                txtPassword.Enabled = False
            End If
        End If
        Connect.conn.Close()
    End Sub
    Dim Assistance As Boolean = False
    Private Sub linkLoginHelp_LinkClicked(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles linkLoginHelp.LinkClicked
        If Assistance = True Then
            Me.Height = 284
            Me.CenterToScreen()
            Assistance = False
            txtUsername.Select()
        Else
            Me.Height = 463
            Me.CenterToScreen()
            Assistance = True
            txtUsername.Select()
        End If
    End Sub

    Private Sub btnExit_Click(sender As Object, e As EventArgs) Handles btnExit.Click
        Application.Exit()
    End Sub
End Class
</code></pre>

## Answers
### Answer ID: 55769511
<p>The <code>Using...End Using</code> blocks ensure that your database objects are closed and disposed even if there is an error.</p>

<p>Of course in a real application you would NEVER store passwords as plain text.</p>

<p>Comments in line.</p>



<pre class="lang-vb prettyprint-override"><code>'Your class might look something like this
Public Class User
    Public Shared ID As Integer
    Public Shared Name As String
    Public Shared Department As String
    Public Shared Address As String
End Class

Private count As Integer
Private Sub btnLogin_Click(sender As Object, e As EventArgs) Handles btnLogin.Click
    count = count + 1
    'keep connections local for better control
    'pass the connection strings directly to the constructor of the connection
    Using cn As New MySqlConnection("Your connection string")
        'pass the query and the connection directly to the constructor of the commmand
        Using cmd As New MySqlCommand("SELECT * FROM user WHERE user.username = @User and user.password = @Password;", cn)
            'Always use parameters to avoid SQL injection
            cmd.Parameters.Add("@User", MySqlDbType.VarChar).Value = txtUsername.Text
            cmd.Parameters.Add("@Password", MySqlDbType.VarChar).Value = txtPassword.Text
            'Open the Connection at the last possible minute.
            cn.Open()
            Using dr1 = cmd.ExecuteReader
                If dr1.HasRows Then
                    dr1.Read()
                    'The indexes of the data reader depent on th order of the fields in the database
                    User.ID = CInt(dr1(0))
                    User.Name = dr1(1).ToString
                    User.Department = dr1(2).ToString
                    User.Address = dr1(3).ToString
                    Me.Hide()
                    frmDashboard.Show()
                    Return 'a successful login will end here
                End If
            End Using 'closes and disposed the reader
        End Using 'close and disposes the command
    End Using 'closes and dipose the connection
    MsgBox("Invalid Username or Password! " &amp; vbCrLf &amp; count &amp; " out of 3 attempts remaining.")
    If count &gt;= 3 Then
        MsgBox("You have exceeded the maximum number of attempts to login. Account has been disabled. Please contact OJFS helpdesk at extension 100.", MsgBoxStyle.Critical)
        btnLogin.Enabled = False 'Instead of the text boxes disable the button.
        'If you just disable the text boxes they can keep clicking the button and opening connections.
    End If
End Sub
</code></pre>


# Combobox default value not showing after changing row source
[Link to question](https://stackoverflow.com/questions/65314612/combobox-default-value-not-showing-after-changing-row-source)
**Creation Date:** 1608071347
**Score:** 1
**Tags:** vba, combobox, onfocus, onload-event
## Question Body
<p><strong>Here's the short version:</strong> Need help figuring out why a combobox on a form is misbehaving. The combobox loads with a rowsource query, and the form load event procedure writes a default text in the combobox as a sort of user input prompt that isn't in the query list but seems to show up just fine when the form loads. When I change the rowsource query through code in another event procedure I can no longer write the same default text into the combobox. If this is because the default value isn't part of the new rowsource query list (which is the same query but with a WHERE clause to filter some of the options), then why can I do this before changing the rowsource even though it also doesn't match any records among the combobox's default rowsource?</p>
<p><strong>Here's the long version:</strong>
I'm working on a construction cost database and modeling tool, and the form in question is an intake form for new conceptual projects with a few textbox and combobox fields for user input.</p>
<p>For aesthetic reasons I want to show default values for each input field in grey as a sort of user instruction prompt, and then change these to black as the fields are completed. There's code in the Form_Load() event procedure which writes the default value in all the controls, and also changes the text color to grey. The GotFocus() event procedure for control then changes the color to black and writes the value to vbNullString so the user doesn't have to delete the previously written default value. Then after the user moves on to another field the LostFocus() event procedure tests if a change has been made, either by typing into the text box in question or selecting from the list if it's a combo box, and will reset the default value as well as change color back to grey if no change has been made (or leave as is in black color if a change was made). This much of the code seems to be working fine.</p>
<p>Here's the issue:
One of the comboboxes asks for 'Space Type' and another one for 'Space Subtype'. When the user selects a particular space type for the project, I want to filter the space subtype list options to show only those related to that space type. I've done this by rewriting the cmbSpaceSubtype.RowSource query within the cmbSpaceType_Change() event procedure, and this also seems to be working fine. The problem is after the row source query is changed through this event procedure, it seems I can no longer rewrite the cmbSpaceSubtype text to the default value that I'd like to show until the user makes a selection for that field. I would think this is obviously because the default value I'm using is not an option on the query list that the row source now points to. But if that's the case then why can I use an identical line of code to write in the same default value through the Form_Load() event procedure, even though the default value also not an option on the row source for that combobox when the form is loading?</p>
<p><strong>Here's a link to the Access file:</strong> [https://app.e-builder.net/public/publicLanding.aspx?QS=b3a5c010645942a9881b361dae7433ae][1]</p>
<p><strong>Here's an excerpt of the vba code:</strong></p>
<pre><code>Option Compare Database
Private Const sListDefault As String = &quot;Select from list&quot;

Private Sub Form_Load()
With Me
    Let .cmbSpaceSubtype = sListDefault
    Let .cmbSpaceType = sListDefault
End With
End Sub

Private Sub cmbSpaceSubtype_GotFocus()
With Me.cmbSpaceSubtype
    If .Text = sListDefault Then
        Let .Value = vbNullString
        Let .ForeColor = vbBlack
    End If
End With
End Sub

Private Sub cmbSpaceSubtype_LostFocus()
With Me.cmbSpaceSubtype
    If .Text = vbNullString Or IsNull(Me.cmbSpaceSubtype) Then
        Let Me.cmbSpaceSubtype = sListDefault
        Let .ForeColor = vbTextLight
    End If
End With
End Sub

Private Sub cmbSpaceType_Change()
With Me.cmbSpaceSubtype

    If Me.cmbSpaceType.Text = sListDefault Then
        Let .RowSource = &quot;SELECT [ID], [Space Subtype] FROM tblSpaceSubtypes ORDER BY [Space Subtype];&quot;
    Else
        Let .RowSource = &quot;SELECT [ID], [Space Subtype] &quot; _
            &amp; &quot;FROM tblSpaceSubtypes WHERE [Space Type]=&quot; &amp; Me.cmbSpaceType.Value &amp; &quot; ORDER BY [Space Subtype];&quot;
    End If

    Let Me.cmbSpaceSubtype = sListDefault
    Call .SetFocus
    Let .ForeColor = vbTextLight
    
End With
End Sub

Private Sub cmbSpaceType_GotFocus()
With Me.cmbSpaceType
    If .Text = sListDefault Then
        Let .Value = vbNullString
        Let .ForeColor = vbBlack
    End If
End With
End Sub

Private Sub cmbSpaceType_LostFocus()
With Me.cmbSpaceType
    If .Text = vbNullString Or IsNull(Me.cmbSpaceType) Then
        Let .Value = sListDefault
        Let .ForeColor = vbTextLight
    End If
End With
End Sub
</code></pre>

## Answers
### Answer ID: 65400141
<p>Finally figured it out ... resetting the combo box to a default value after changing the rowsource did execute properly but I wasn't seeing the default value on the form because it's a multicolumn row source and the bound column was width 0, so the value was hidden.</p>


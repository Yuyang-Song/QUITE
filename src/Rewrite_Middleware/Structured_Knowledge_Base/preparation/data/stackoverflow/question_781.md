# AdoDB filter on merged columns
[Link to question](https://stackoverflow.com/questions/41931948/adodb-filter-on-merged-columns)
**Creation Date:** 1485766530
**Score:** 2
**Tags:** delphi, ms-access, ado, tadotable
## Question Body
<p>So I have an AdoTable connected to database (mdb) and DataSource using it. This DataSource is used by DBGrid...</p>

<p>I tried to filter AdoTable based on user input. There are 3 important columns: name, surname and ID. I came up with something like this as a temporary solution: </p>

<pre><code>AdoTable.filter:='surname like ' +
      QuotedStr('%'+edit1.text+'%')+' or name like ' +
      QuotedStr('%'+edit1.text+'%')+' or ID like ' +
      QuotedStr('%'+edit1.text+'%');
AdoTable.filtered:=true;
</code></pre>

<p>It does work but it doesn't do exactly what I would want it to do... (when searching for name AND surename it won't find anything as it looks in one column only).
So later I modified my code into this:</p>

<pre><code>AdoTable.filter:='surname &amp; " " &amp; name like ' +
      QuotedStr('%'+edit1.text+'%')+' or name &amp; " " &amp; surname like ' +
      QuotedStr('%'+edit1.text+'%')+' or ID like ' +
      QuotedStr('%'+edit1.text+'%');
AdoTable.filtered:=true;
</code></pre>

<p>Now this would do exacly what I want it to do, but it raises exception (EOleException: Arguments are of the wrong type, are out of acceptable range, or are in conflict with one another).
That quite suprises me as I thought that it should behave as where clause in sql command (and it works perfectly as a command).</p>

<p>I tried replacing '&amp;' with '+'.
I could split an input text, but I don't want to do that (it would work poorly if you would have names like Robin van Persie, Ahmad ibn Hanbal, etc..)</p>

<p>Alternatively I could rewrite whole program to use queries instead of tables but I don't really want to do that (that would also mean that I would be getting new recordSet EVERYTIME user would change edit1.text instead of just filtering).</p>

<p>Any ideas?</p>

<p>edit:
so command that works looks like this</p>

<pre><code>select * from person where surname &amp; " " &amp; name like '%John Smith%' or name &amp; " " &amp; surname like '%John Smith%' or ID like '%John Smith%'
</code></pre>

<p>filter looks like this (and it triggers an exception)</p>

<pre><code>surname &amp; " " &amp; name like '%John Smith%' or name &amp; " " &amp; surname like '%John Smith%' or ID like '%John Smith%'
</code></pre>

<p>Note that there could be 'hn Smith' instead of 'John Smith' so it would find also 'Kahn Smithers' etc.</p>

## Answers
### Answer ID: 41936036
<p>The code below works fine with an AdoTable which accesses the <code>employee</code> table in the Delphi <code>dbdemos.mdb</code> database.  My AdoConnection is using the <code>Microsoft Jet 4.0 OLE DB</code> driver.</p>

<pre><code>procedure TForm1.Button1Click(Sender: TObject);
var
  FilterExpr : String;
begin
  AdoTable1.Filtered := not AdoTable1.Filtered;
  if AdoTable1.Filtered then begin
    FilterExpr := 'FirstName like ' + QuotedStr('%' + Edit1.Text + '%') + ' or LastName like ' + QuotedStr('%' + Edit1.Text + '%');
    AdoTable1.Filter := FilterExpr;
  end;
end;
</code></pre>

<p>I think your mistake probably is using that Access-specific syntax you mentioned.  You're accessing the table through the ADO layer, and that AFAIK expects the same syntax as you would use, e.g. for a Sql Server back-end.</p>

<p>From your comment, it seems as if you want to cover the case where the user type into your Edit1.Text a fragment of a first name followed by a space followed by a fragment or a surname.  The following will do that:</p>

<pre><code>procedure TForm1.Button1Click(Sender: TObject);
var
  FilterExpr : String;
  P : Integer;
  S1,
  S2 : String;
begin
  AdoTable1.Filtered := not AdoTable1.Filtered;
  if AdoTable1.Filtered then begin
    P := Pos(' ', Trim(Edit1.Text));
    if P &gt; 0 then begin
      S1 := Copy(Trim(Edit1.Text), 1, P - 1);
      S2 := Copy(Trim(Edit1.Text), P + 1, MaxInt);
      FilterExpr := '(FirstName like ' + QuotedStr('%' + S1 + '%') + ')';
      FilterExpr := FilterExpr + ' or (LastName like ' + QuotedStr('%' + S2 + '%') + ')';
    end
    else
      FilterExpr := 'FirstName like ' + QuotedStr('%' + Edit1.Text + '%') + ' or LastName like ' + QuotedStr('%' + Edit1.Text + '%');
    AdoTable1.Filter := FilterExpr;
  end;
end;
</code></pre>

<p><strong>Update:</strong> If you want to allow the user to enter something like</p>

<p>hn Smith</p>

<p>then you could use a FilterRecord event like this instead of the code above.</p>

<pre><code>procedure TForm1.ADOTable1FilterRecord(DataSet: TDataSet; var Accept: Boolean);
var
  S : String;
begin
  S := LowerCase(DataSet.FieldByName('FirstName').AsString + ' ' + DataSet.FieldByName('LastName').AsString);
  Accept := Pos(LowerCase(Edit1.Text), S) &gt; 0; 
end;
</code></pre>

<p>The conversion to LowerCase, obviously, is to disregard any capitalisation the user might have used.</p>

### Answer ID: 41937982
<p>I found this: <a href="https://stackoverflow.com/questions/11594724/using-like-statement-for-filtering">Using LIKE statement for filtering</a> and used the accepted answer and it works just fine. (Couldn't find it sooner as question quite differs)</p>

<p>On table filter:</p>

<pre><code>procedure TDataModule1.ADOTableFilterRecord(DataSet: TDataSet;
  var Accept: Boolean);
var
  nameSurname :string;
  surnameName :string;
begin
  nameSurname:= DataSet.FieldByName('name').AsString+' '+DataSet.FieldByName('surname').AsString;
  surnameName:= DataSet.FieldByName('surname').AsString+' '+DataSet.FieldByName('name').AsString;

  if assigned(MainForm) then
    Accept := (Pos(MainForm.edit1.Text, nameSurname) &gt; 0)
  or (Pos(MainForm.edit1.Text, surnameName) &gt; 0)
  or (Pos(MainForm.edit1.Text, DataSet.FieldByName('ID').AsString) &gt; 0);
end;
</code></pre>

<p>on edit change:</p>

<pre><code>procedure TMainForm.edit1Change(Sender: TObject);
begin
    DataModule1.AdoTable.Filtered:=false;
    if edit1.Text&lt;&gt;'' then
      DataModule1.AdoTable.Filtered:=True;
end;
</code></pre>

<p>Thank you for your time... I'll leave it here.. I think eventually someone could need it</p>


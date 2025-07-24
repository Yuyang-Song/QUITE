# Why do I get &quot;type mismatch&quot; when I put a date value in SQL?
[Link to question](https://stackoverflow.com/questions/14604210/why-do-i-get-type-mismatch-when-i-put-a-date-value-in-sql)
**Creation Date:** 1359549505
**Score:** 2
**Tags:** sql, delphi, paradox
## Question Body
<p>I am working on a search query function in Delphi 7 (working with a Paradox database) and I keep getting a type mismatch error when selecting between two dates. If I use the date type I get</p>

<blockquote>
  <p>Project Project1.Exe raised exception class EDBEngineError with message 'Type mismatch in expression.'. Process stoped.'</p>
</blockquote>

<p>If i use a dateTime type I get</p>

<blockquote>
  <p>Project Project1.Exe raised exception class EDBEngineError with message 'Invalid use of keyword. Token : 13? AND Line Number: 8'. Process stoped.'</p>
</blockquote>

<p>where 13 is the first digit of the time.</p>

<p>Here's my code:</p>

<pre class="lang-pas prettyprint-override"><code>procedure TForm1.Button1Click(Sender: TObject);
var
  Search1 :string;
  Search2 :string;
  outputveld : string;
  datum : TDateTime;
  datumZoek: TdateTime;
  countmails : integer;
  outfile: textfile;
  Zoek6MaandenTerug: Double;
begin
  Zoek6MaandenTerug := 182.621099;
  datum := tdate(now);
  datumZoek := datum - Zoek6MaandenTerug;
  ShowMessage(DateTimeToStr(Datum));
  ShowMessage(DateTimeToStr(datumZoek));
  Memo1.Lines.Add(DateTimeToStr(Datum));
  //datum := datum- StrToDate('21-4-2004');
  {radio button date controll}

  {//radio button date controll}
  Search1 := Edit1.Text;
  Search2 := Edit2.Text;

  assignfile(outfile,'text\Emails.txt');
  rewrite(outfile);
  outputveld := '';
  countmails := 0;

  {sets up  and executesSQL query(Query1)}
  Query1.close;
  Query1.SQL.Clear;
  memo1.Clear;
  if Search1 &lt;&gt; EmptyStr then
  begin
    //Query1.SQL.add('SELECT * FROM Verkoop');
    Query1.SQL.add('SELECT DISTINCT Verkoophandelingen.Klantnr, Verkoophandelingen.Type, verkoop.Klantnr, Verkoop.Artikelnr, Artikels.Nummer, Artikels.artikelgroep, Verkoophandelingen.Datum, Klanten.Email');
    Query1.SQL.add('FROM Verkoop');
    Query1.SQL.add('full Join Artikels ON Verkoop.Artikelnr = Artikels.Nummer');
    Query1.SQL.add('full Join Klanten ON Verkoop.Klantnr = Klanten.Nummer');
    Query1.SQL.add('full Join Verkoophandelingen ON Verkoop.verkoophandelingnr = Verkoophandelingen.nummer');
    Query1.SQL.add('WHERE Verkoophandelingen.Type = "Bestelling" ');
    Query1.SQL.add('AND Verkoop.Artikelnr = '+Search1+'');
    //Query1.SQL.add('AND Verkoophandelingen.Datum = '+ DateToStr(Date1) +'');
    Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN '+DateTimeToStr(datum)+'');
    Query1.SQL.Add('AND '+DateToStr(datumzoek)+'');
    Query1.SQL.add('ORDER BY Datum');

    Query1.RequestLive := true;
    Query1.open;
  end
  else if Search2 &lt;&gt; EmptyStr then
  begin
    Query1.SQL.add('SELECT DISTINCT Verkoophandelingen.Klantnr, Verkoophandelingen.Type, verkoop.Klantnr, Verkoop.Artikelnr, Artikels.Nummer, Artikels.artikelgroep, Verkoophandelingen.Datum, Klanten.Email');
    Query1.SQL.add('FROM Verkoop');
    Query1.SQL.add('full Join Artikels ON Verkoop.Artikelnr = Artikels.Nummer');
    Query1.SQL.add('full Join Klanten ON Verkoop.Klantnr = Klanten.Nummer');
    Query1.SQL.add('full Join Verkoophandelingen ON Verkoop.verkoophandelingnr = Verkoophandelingen.nummer');
    Query1.SQL.add('WHERE Verkoophandelingen.Type = "Bestelling" ');
    Query1.SQL.add('AND Artikels.ArtikelGroep = '+Search2+'');
    Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN '+DateToStr(datum)+'');
    Query1.SQL.Add('AND '+DateToStr(datumZoek)+'');
    Query1.SQL.add('ORDER BY Datum');
    Query1.RequestLive := true;
    Query1.open;
  end;

  while not Query1.Eof do
  begin
    if Query1.FieldByName('Email').AsString &lt;&gt;  EmptyStr then
    begin
      memo1.Lines.Add(Query1.FieldByName('Email').AsString + ';');
      writeln(outfile, Query1.FieldByName('Email').AsString+ ';');
      Query1.next;
      inc(countmails);
    end
    else
    begin
      Query1.next;
    end;
  end;

  if Query1.Eof then
  begin
    CloseFile(outfile);
    memo1.lines.add('totaal aantal valid email adressen = ' + IntToStr(countmails));
  end;
end;
</code></pre>

<hr>

<p>I hope im posting in the right place.
This is my code after adding parameters for my query still getting
'Type mismatch in expression.'.  </p>

<pre><code>unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Grids, DBGrids, DB, DBTables, DBCtrls;

type
  TForm1 = class(TForm)
    DataSource1: TDataSource;
    Query1: TQuery;
    DBGrid1: TDBGrid;
    Button1: TButton;
    ComboBox1: TComboBox;
    Memo1: TMemo;
    Edit1: TEdit;
    Edit2: TEdit;
    Label1: TLabel;
    Label2: TLabel;
    Button2: TButton;
    RadioButton1: TRadioButton;
    RadioButton2: TRadioButton;
    RadioButton3: TRadioButton;
    procedure Button1Click(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure ComboBox1Change(Sender:TObject);
    procedure Edit1Change(Sender: TObject);
    procedure Edit2Change(Sender: TObject);

  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

uses ComObj;

{$R *.dfm}




procedure TForm1.FormActivate(Sender: TObject);

 var
i : integer;
mystringlist : tstringlist;
 datum: TDateTime;
   Zoek6MaandenTerug : Double;
begin
        Zoek6MaandenTerug := 182.621099;
        datum := tdate(now);
        datum := datum - Zoek6MaandenTerug;
        ShowMessage(DateToStr(datum));
        Memo1.Lines.Add(DateTimeToStr(Datum));
        Memo1.Lines.Add(DateToStr(datum));
        //datum := datum- StrToDate('21-4-2004');

   MyStringList := TStringList.Create;
    {
    memo1.Clear;
    Edit1.Clear;
    Edit2.Clear;
    }

  try
    Session.GetAliasNames(MyStringList);
    { fill a list box with alias names for the user to select from }
    for I := 0 to MyStringList.Count - 1 do begin
      combobox1.Items.Add(MyStringList[I]);
    end
    finally
    MyStringList.Free;
    end;

   end;

   procedure TForm1.ComboBox1Change(Sender: TObject);
begin

try
      Query1.SQL.Clear;
            Query1.Databasename := string(combobox1.items[combobox1.ItemIndex]);

        except
        with Application do
        begin
            NormalizeTopMosts;
            MessageBox(' wrong database ', 'fout..', MB_OK);
            RestoreTopMosts;
            combobox1.SetFocus;
        Exit;
        end;

end;
 end;



procedure TForm1.Button1Click(Sender: TObject);
var

  Search1 :String;
  Search2 :String;
  outputveld : string;
  datum : TDateTime;
  datumZoek: TDateTime;
  countmails : integer;
  outfile: textfile;
  Zoek6MaandenTerug: Double;

begin

        Zoek6MaandenTerug := 182.621099;
        datum := tdate(now);
        datumZoek := datum - Zoek6MaandenTerug;
        ShowMessage(DateTimeToStr(Datum));
        ShowMessage(DateTimeToStr(datumZoek));
        Memo1.Lines.Add(DateToStr(datum));
        Memo1.Lines.Add(DateToStr(datumZoek));

        //datum := datum- StrToDate('21-4-2004');



{//radio button date controll}
      Search1 := Edit1.Text;
      Search2 := Edit2.Text;


      assignfile(outfile,'text\Emails.txt');
      rewrite(outfile);
      outputveld := '';
      countmails := 0;


        {sets up  and executesSQL query(Query1)}
            Query1.close;
      Query1.SQL.Clear;
      memo1.Clear;
       if Search1 &lt;&gt; EmptyStr then
          begin


             //Query1.SQL.add('SELECT * FROM Verkoop');
            Query1.SQL.add('SELECT DISTINCT Verkoophandelingen.Klantnr, Verkoophandelingen.Type, verkoop.Klantnr, Verkoop.Artikelnr, Artikels.Nummer, Artikels.artikelgroep, Verkoophandelingen.Datum, Klanten.Email');
            Query1.SQL.add('FROM Verkoop');
            Query1.SQL.add('full Join Artikels ON Verkoop.Artikelnr = Artikels.Nummer');
            Query1.SQL.add('full Join Klanten ON Verkoop.Klantnr = Klanten.Nummer');
            Query1.SQL.add('full Join Verkoophandelingen ON Verkoop.verkoophandelingnr = Verkoophandelingen.nummer');
            Query1.SQL.add('WHERE Verkoophandelingen.Type = "Bestelling" ');
            Query1.SQL.add('AND Verkoop.Artikelnr = :Search1');
            //Query1.SQL.add('AND Verkoophandelingen.Datum = '+ DateToStr(Date1) +'');
           Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN :datum AND :datumzoek');


            Query1.SQL.add('ORDER BY Datum');


            Query1.ParamByName('datumzoek').Value := datumzoek;
            Query1.ParamByName('datum').Value := datum;
            Query1.ParamByName('Search1').Value := Search1;

                Query1.RequestLive := true;
                  Query1.open;

          end
          else if Search2 &lt;&gt; EmptyStr then
          begin

            Query1.SQL.add('SELECT DISTINCT Verkoophandelingen.Klantnr, Verkoophandelingen.Type, verkoop.Klantnr, Verkoop.Artikelnr, Artikels.Nummer, Artikels.artikelgroep, Verkoophandelingen.Datum, Klanten.Email');
            Query1.SQL.add('FROM Verkoop');
            Query1.SQL.add('full Join Artikels ON Verkoop.Artikelnr = Artikels.Nummer');
            Query1.SQL.add('full Join Klanten ON Verkoop.Klantnr = Klanten.Nummer');
            Query1.SQL.add('full Join Verkoophandelingen ON Verkoop.verkoophandelingnr = Verkoophandelingen.nummer');
            Query1.SQL.add('WHERE Verkoophandelingen.Type = "Bestelling" ');
            Query1.SQL.add('AND Artikels.ArtikelGroep = :Search2');
            //Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN '+DateToStr(datum)+'');
            //Query1.SQL.Add('AND '+DateToStr(datumZoek)+'');

            Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN :datum AND :datumzoek');

            Query1.SQL.add('ORDER BY Datum');

            Query1.ParamByName('datumzoek').Value := datumzoek;
            Query1.ParamByName('datum').Value := datum;
            Query1.ParamByName('Search2').Value := Search2;

            Query1.RequestLive := true;
                  Query1.open;

        end;




      while not Query1.Eof do
 begin
      if Query1.FieldByName('Email').AsString &lt;&gt;  EmptyStr then
        begin
          memo1.Lines.Add(Query1.FieldByName('Email').AsString + ';');
          writeln(outfile, Query1.FieldByName('Email').AsString+ ';');
          Query1.next;
          inc(countmails);
        end

        else
          begin
            Query1.next;
          end;
 end;

  if Query1.Eof then
 begin
  CloseFile(outfile);
  memo1.lines.add('totaal aantal valid email adressen = ' + IntToStr(countmails));

 end;

end;





procedure TForm1.Edit1Change(Sender: TObject);
begin
Edit2.Text := '';
end;

procedure TForm1.Edit2Change(Sender: TObject);
begin
Edit1.Text := '';
end;


 end.
</code></pre>

<hr>

<p>after adding this </p>

<pre><code>        ... 
        Query1.ParamByName('datumzoek').DataType := ftDate;
        Query1.ParamByName('datum').DataType := ftDate;
        Query1.ParamByName('Search1').DataType := ftInteger;

        Query1.ParamByName('datumzoek').Value := datumzoek;
        Query1.ParamByName('datum').Value := datum;
        Query1.ParamByName('Search1').Value := Search1;
        ...
</code></pre>

<p>the query gets run but with no results, after showing the query,text it seems the parameters have a "?" value ?</p>

<pre><code>...
SELECT DISTINCT    Verkoophandelingen.Klantnr, Verkoophandelingen.Type, verkoop.Klantnr, Verkoop.Artikelnr, Artikels.Nummer, Artikels.artikelgroep, Verkoophandelingen.Datum, Klanten.Email
FROM Verkoop
full Join Artikels ON Verkoop.Artikelnr = Artikels.Nummer
full Join Klanten ON Verkoop.Klantnr = Klanten.Nummer
full Join Verkoophandelingen ON Verkoop.verkoophandelingnr = Verkoophandelingen.nummer
WHERE Verkoophandelingen.Type = "Bestelling"
AND Verkoop.Artikelnr = ?
AND Verkoophandelingen.Datum BETWEEN ? AND ?
ORDER BY Datum
...
</code></pre>

## Answers
### Answer ID: 14604501
<p>Perhaps these lines cause the issue:</p>

<pre><code>Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN '+DateTimeToStr(datum)+'');
Query1.SQL.Add('AND '+DateToStr(datumzoek)+'');
</code></pre>

<p>Here you are inserting dates as returned by <code>DateTimeToStr</code> and <code>DateToStr</code>, but you are not delimiting the inserted values in any way, and so the resulting query will look something like this:</p>

<pre><code>...
AND Verkoophandelingen.Datum BETWEEN 21-04-2004
AND 22-04-2004
...
</code></pre>

<p>I'm not sure what delimiter Paradox uses for date constants, but I'm almost sure it does use some. Perhaps, it should be <code>'</code>:</p>

<pre><code>...
AND Verkoophandelingen.Datum BETWEEN '21-04-2004'
AND '22-04-2004'
...
</code></pre>

<p>Check with the manual for the correct one and fix your code accordingly.</p>

<p>On the other hand, it would be a much better idea to use <em>parametrised</em> queries, as @Rob Kennedy has correctly suggested. In a parametrised query, you use placeholders like <code>:name</code> where argument values should go. So, in your case it might look like this:</p>

<pre><code>...
Query1.SQL.add('WHERE Verkoophandelingen.Type = "Bestelling" ');
Query1.SQL.add('AND Verkoop.Artikelnr = :Search');
Query1.SQL.add('AND Verkoophandelingen.Datum BETWEEN :date1');
Query1.SQL.Add('AND :date2');
...
</code></pre>

<p>Before running the query, you'll need to set up the parameters using the <code>TQuery.Params</code> property, something like this:</p>

<pre><code>Query1.Params.CreateParam(ftInteger, 'Search', ptInput).AsInteger := StrToInt(Search1);
Query1.Params.CreateParam(ftDateTime, 'date1', ptInput).AsDateTime := datum;
Query1.Params.CreateParam(ftDateTime, 'date2', ptInput).AsDateTime := datumzoek;
</code></pre>

<p>Or, if the Query component auto-fills the <code>Params</code> collection when assigning the SQL statement:</p>

<pre><code>Query1.Params.ParamByName('Search').AsInteger := StrToInt(Search1);
Query1.Params.ParamByName('date1').AsDateTime := datum;
Query1.Params.ParamByName('date2').AsDateTime := datumzoek;
</code></pre>

<p>That way you won't need to worry about delimiting values: the component will take care of that.</p>


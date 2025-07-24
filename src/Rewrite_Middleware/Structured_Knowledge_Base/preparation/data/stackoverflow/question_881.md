# Removing time from datetime and insert into db table using Python
[Link to question](https://stackoverflow.com/questions/48101607/removing-time-from-datetime-and-insert-into-db-table-using-python)
**Creation Date:** 1515091284
**Score:** 0
**Tags:** python-3.x, datetime, postgresql-9.1, xlrd, python-datetime
## Question Body
<p>Prior to asking a question I tried different ways and none worked.</p>

<p>I tried using datetime.strptime and dateutil, neither worked or I am doing it incorrectly.
I even tried splitting date into y, m, d variables and change to ints and then tried adding all 3 variables together for a full date variable.</p>

<p>How do I need to update the coding for the date portion, so I can read and insert values from the second/third/etc. columns with no errors?</p>

<p>I am having issues with Excel date and changing to postgres date. (The date field in the Excel has date and time. I only need the date portion.) I am reading a date column with xlrd and changing the date to what I need and insert, but once I add another column to read and insert, I receive code issues.</p>

<pre><code>import psycopg2
import xlrd
import datetime
#Tried from datetime import datetime


try:
    conn = psycopg2.connect(user = '', password = '', host =’’, database =’’, port = 0000)
    mycursor = conn.cursor()
    print('DB connection open')
    print('Running SQL query')

    #Open the excel
    book = xlrd.open_workbook('name.xlsx')

    #Open the workbook sheet
    sheet = book.sheet_by_name('Date')

    query = """INSERT INTO table_name(
    date,
    second_column
    )

    VALUES(
    %s,
    %s)"""

    for r in range(1, sheet.nrows):
        db_date = year_date = []
        date = sheet.cell(r, 0).value

        #Changing Excel date from m/d/y to y-m-d
        date_mode = datetime.datetime(*xlrd.xldate_as_tuple(review_date, book.datemode))
        start_date_full = date_mode
        split_start_date_full = str(start_date_full)

        #Splitting date to remove the time portion
        split_start_date_full = split_start_date_full.split(" ")

        #Adding the date to a list
        year_date = split_start_date_full[0]
        db_date.append((year_date))
        #Assign values to each row
        values = (
            db_date,
            second_column
            )
        mycursor.execute(query, values)


    #Commit to the DB. Close the mycursor and conn.
    mycursor.close()
    conn.commit()
    conn.close()
    print('''All done!''')

except Exception as e:
    #making sure cursor and conn is closed if I hit the except
    mycursor.close()
    conn.close()
    print(e)
</code></pre>

<p>Errors/results:
Inserts no problem if I only call the date column
<em>the second date value is only a date column in postgres db table that inserts a date based on when rows were inserted.</em></p>

<pre><code>&gt;&gt;&gt;
================================ RESTART ================================
&gt;&gt;&gt;
DB connection open
Running SQL query
(9616, datetime.date(2017, 12, 6), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, datetime.date(2018, 1, 4))
All done!

I receive text error when I call a second/third/etc. columns
&gt;&gt;&gt;
================================ RESTART ================================
&gt;&gt;&gt;
DB connection open
Running SQL query
column "review_date" is of type date but expression is of type text[]
LINE 6:     ARRAY['2017-12-06'],
            ^
HINT:  You will need to rewrite or cast the expression.
&gt;&gt;&gt; 
</code></pre>

## Answers
### Answer ID: 48116615
<p>Steps I took:</p>

<ol>
<li><p>I split year_date and put into year_date_full variable.</p></li>
<li><p>I created a variable for year, month, and day and turned into int's full_date</p></li>
<li><p>Then I combined year+-+month+-+day into its own variable and called that variable as the value that needs to be inserted into the db table.</p></li>
</ol>

<hr>

<pre><code>for r in range(1, sheet.nrows):
    db_date = year_date = []
    #Date Column A
    date = sheet.cell(r, 0).value
    date_mode = datetime.datetime(*xlrd.xldate_as_tuple(review_date, book.datemode))
    start_date_full = date_mode
    split_start_date_full = str(start_date_full)
    split_start_date_full = split_start_date_full.split(" ")
    year_date = split_start_date_full[0]
    time_date = split_start_date_full[1]
    #Split year_date '-' and put each section into its own variable
    year_date_full = year_date.split('-')
    start_year = year_date_full[0]
    start_month = year_date_full[1]
    start_day = year_date_full[2]
    #Turn str to a int for year, month, day
    full_date = (int(start_year),int(start_month),int(start_day))
    #created a new variable to hold the full year and '-'
    full_date_new = (start_year+'-'+start_month+'-'+start_day)
    #Second Column - Column B
    second_column = sheet.cell(r, 1).value
</code></pre>

<p>Insert results:</p>

<pre><code>&gt;&gt;&gt; ================================ RESTART ================================
&gt;&gt;&gt; 
DB connection open
Running SQL query
(12621, **datetime.date(2017, 12, 6)**, None, None, None, None, None, None, None, None, None, None, None, None, **False**, None, None, datetime.date(2018, 1, 5))
All done!
&gt;&gt;&gt;
</code></pre>


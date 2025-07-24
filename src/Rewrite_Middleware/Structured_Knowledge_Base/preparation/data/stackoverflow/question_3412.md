# How can I get TSQL from easy MS Access SQL with little to no handiwork?
[Link to question](https://stackoverflow.com/questions/78942252/how-can-i-get-tsql-from-easy-ms-access-sql-with-little-to-no-handiwork)
**Creation Date:** 1725319928
**Score:** 0
**Tags:** python, excel, t-sql, ms-access
## Question Body
<p>I have 500+ queries in a bunch of MS Access databases. The queries are rather easy.</p>
<ul>
<li>(1.) I read them out with VBA into an Excel file as columns <code>A</code> to <code>H</code>, with the columns &quot;ID, Datenbank, Objektname, LastUpdated, Objekttyp, Objektart, SourceTableName, Abfrage_SQL&quot;, with the last column being the query,</li>
<li>(2.) split the query with Regex into columns <code>I</code> to <code>P</code> as the split SQL blocks &quot;Select, Into, From, Where, Group_By, Having, Order_By&quot;,</li>
<li>(3.) shortened the code with aliases into two new columns <code>Q</code> (<code>New SQL Codes</code>) and <code>R</code> (<code>Mapping</code>),</li>
<li>and my aim is to make (4.) a column <code>S</code> (<code>TSQL</code>) as the TSQL that I can take to feed an SSIS data flow.</li>
</ul>
<p>For (3.), see <a href="https://stackoverflow.com/questions/78940118/in-a-standard-ms-access-sql-query-output-that-does-not-have-any-aliases-how-do">In a standard MS Access SQL query output that does not have any aliases, how do I replace the full names by their &quot;first-letters&quot; aliases?</a>, and there are also the links (1.)+(2.).</p>
<p>I need to change the MS Access VBA that is embedded in MS Access SQL, like <code>Format()</code> functions and special formats like <code>#my_date#</code>, and I do not want to Regex-replace the code dozens of times by hand in some Regex-Search-Replace menu. Instead, I want to loop over the replacements with Python, taking the <code>output_file.xlsx</code> from (3.) as the input and renaming the new output to <code>output_file_tsql.xlsx</code>. The output of the new TSQL code shall be put in a new column <code>S</code> (<code>TSQL</code>).</p>
<p>Which kind of Regex replacements might help as patterns for anyone to begin with? I am sure that the patterns in my 500+ queries are only a small share of what you can run into, but on the other hand, they should be a good sample for a cold start. You will have other patterns as well so that you cannot rely only on the examples. But then just answer and share what you found.</p>
<p>Is there a better way to get the TSQL from MS Access SQL than by Regex replacements? Any tool or trick can be an answer to this question.</p>
<p>How can I get TSQL from easy MS Access SQL with little to no handiwork?</p>
<p><em>(Old question was: &quot;Which Regex replacements help when rewriting MS Access SQL queries as mere TSQL queries? How can these be looped over with Excel as input and output?&quot;)</em></p>

## Answers
### Answer ID: 78942253
<p>This code is mainly about Regex replacements in a loop, which will give you TSQL-only code from &quot;MS Access SQL(VBA)&quot; queries for the given 500+ queries set. As said above, you will surely run into other patterns as well, this is just to help how the frame and the patterns can look like.</p>
<pre class="lang-py prettyprint-override"><code>import pandas as pd
import re

# Function to convert Access SQL to T-SQL
def convert_access_to_tsql(sql_string):
    if pd.isnull(sql_string) or sql_string.strip() == &quot;&quot;:
        return &quot;&quot;  # Skip empty cells

    # Replace commas in the SELECT clause with a newline before each comma
    def replace_commas_in_select(match):
        select_clause = match.group(1)  # Captures the SELECT line
        other_part = match.group(2)  # Captures the rest (INTO, FROM, WHERE)

        # Replace commas in the select_clause with newline before each comma unless inside parantheses so that functions are skipped
        select_clause = re.sub(r',\s*(?![^(]*\))', r'\r\n,', select_clause)
        
        return f&quot;{select_clause} {other_part}&quot;
        
    select_pattern = r'^(SELECT.*?)(INTO|FROM|WHERE|$)'
    sql_string = re.sub(select_pattern, replace_commas_in_select, sql_string, flags=re.MULTILINE)

    # List of regex patterns and replacements
    replacements = [
        (r'Format\(\[?(\w+)?\]?!\[?(\w+)\]?,\s*&quot;&quot;(.+?)&quot;&quot;\)', r'convert(varchar(10), \1.\2, &lt;Format function for \3&gt;)'),
        (r'\[?(\w+)\]!?\[?(\w+)\]?', r'\1.\2'),
        (r'AS \[(\w+)\]', r'AS \1'),
        (r'\bJOIN\s+\[?(\w+)?\]?!\[?(\w+)\]\s+ON', r'JOIN \1.\2 ON'),
        (r'\bIs\b', r'IS'),
        (r'\bNull\b', r'NULL'),
        (r'\bOr\b', r'OR'),
        (r'convert\(varchar\(\d+\), \[?(\w+)\]?!\?(\w+)\?\)', r'convert(datetime, \1.\2)'),
        (r'Like &quot;(\w+)\*&quot;', r&quot;LIKE '\1%'&quot;),  # Convert asterisks at the end to T-SQL form
        (r'Like &quot;\*(\w+)&quot;', r&quot;LIKE '%\1'&quot;),  # Convert asterisks at the beginning to T-SQL form
        (r'Like &quot;\*(\w+)\*&quot;', r&quot;LIKE '%\1%'&quot;),  # Convert asterisks at both ends to T-SQL form
        (r'#(\d{1,2})/(\d{1,2})/(\d{4})#', r&quot;'\3-\1-\2'&quot;),  # Correctly convert date format
        (r'Format\(\[?([\w|\.]+)\]?,\s*\&quot;dd/mm/yyyy\&quot;\)', r'convert(varchar(10), \1, 120)'),  # 115 would be dd/mm/yyyy Japanese, but my queries needed 120
        (r'Format\(\[?([\w|\.]+)\]?,\s*\&quot;yyyy-mm-dd\&quot;\)', r'convert(varchar(10), \1, 120)'),  # yyyy-mm-dd ODBC canonical
        (r'Format\(\[?([\w|\.]+)\]?,\&quot;yyyy\&quot;', r'convert(varchar(4), \1, 112)'),  # yyyy (from yyyymmdd)
        (r'Format\(\[?([\w|\.]+)\]?,\&quot;dd\&quot;', r'convert(varchar(2), \1, 104)'),  # dd
        (r'Date\(\)', r'CAST(GETDATE() AS Date)'),  # Replace VBA function
        (r'CInt\(', r'convert(int, '),  # Replace VBA function
        (r'&quot;\s*([^&quot;]*)\s*&quot;', r&quot;'\1'&quot;),  # Replace &quot;Text&quot; with 'Text'
        (r'!(?!\[)', '.'),  # Replace ! with . except after [
        (r'\s*(INTO|AND|ON)', r'\r\n\1'),  # Replace INTO, AND, ON with line breaks
        (r'\s*AND', r'\r\n    AND'),  # Four spaces in front of AND
        (r'\s*ON', r'\r\n    ON'),  # Four spaces in front of ON      
        (r'\s*(JOIN\s+\w*|\w+\s+JOIN\s+\w*)', r'\r\n\1'),  # All types of JOIN with line breaks
        (r'(?&lt;!\w)\(\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\)', r'\1'), # Remove parentheses (unless from a function) for simple dot notation (Step 1)
        (r'(?&lt;!#)(\(\s*[^()]*![^()]*\))', r'1 = 1 --\1\n'),  # Comment out formular fields with exclamation marks, line break (Step 2)
        (r'\n\s*\n', r'\n'), # Drop empty line break (Step 3)
        (r'\bINTO\b', '--INTO'), # INTO blocks for nested queries in MS Access only
    ]

    # Loop through the replacements
    for pattern, replacement in replacements:
        try:
            sql_string = re.sub(pattern, replacement, sql_string, flags=re.MULTILINE)
        except re.error as e:
            print(f&quot;Regex error: {e} in pattern: {pattern} for string: {sql_string}&quot;)
            raise 

    # Post-processing conversion of date strings to 'YYYY-MM-DD' format
    sql_string = re.sub(
        r&quot;'(\d{1,4})-(\d{1,2})-(\d{1,2})'&quot;,
        lambda m: f&quot;'{int(m.group(1)):04}-{int(m.group(2)):02}-{int(m.group(3)):02}'&quot;,
        sql_string
    )

    return sql_string

# Load the Excel file and read the 'New SQL Codes' column
input_file = 'output_file.xlsx'
output_file = 'output_file_tsql.xlsx'

# Read the data
df = pd.read_excel(input_file)

# Ensure that the 'New SQL Codes' column exists
if 'New SQL Codes' not in df.columns:
    print(&quot;The column 'New SQL Codes' does not exist in the Excel file.&quot;)
else:
    # Process each cell in the 'New SQL Codes' column and write the result to column 'TSQL'
    df['TSQL'] = df['New SQL Codes'].apply(convert_access_to_tsql)

    # Save the modified DataFrame as a new Excel file
    df.to_excel(output_file, index=False)

print(f&quot;The file has been successfully saved as {output_file}.&quot;)
</code></pre>
<p>The output is the column <code>S</code> filled with 500+ TSQL queries without any MS Access functions and formats and with line breaks before each column and before some SQL keywords, <code>AND</code> and <code>ON</code> four spaces indented.</p>
<p>With its output at hand, you can also sort it by the levels of dependencies with the help of <a href="https://stackoverflow.com/questions/78965913/how-do-i-sort-piles-of-select-into-queries-that-are-built-on-top-of-each-other/">How do I sort &quot;SELECT INTO&quot; queries that are built on top of each other by their &quot;INTO&quot; / &quot;FROM&quot; table links?</a>.</p>


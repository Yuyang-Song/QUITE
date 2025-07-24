# Using sprintf with mysql_query
[Link to question](https://stackoverflow.com/questions/18423576/using-sprintf-with-mysql-query)
**Creation Date:** 1377381833
**Score:** -1
**Tags:** mysql, sql, c, c89
## Question Body
<p>I'm using a mysql snippet that connects to my mysql database (locally) in ANSI C. Everything is working perfectly, but I've been trying to create a function that connects to my database and inserts a new record based on some variables. I'm using sprintf to snag those variables and piece them together to form my SQL query. </p>

<h1>Problem</h1>

<p>Once I have my variables and my SQL ready, I send it over to mysql_query. Unfortunately, this does not work as expected, the program crashes and reports a buffer overflow.</p>

<p>Here are pieces of the overall function that may help explain the problem.</p>

<pre><code>#include &lt;mysql.h&gt;
#include &lt;string.h&gt;
#include &lt;stdio.h&gt;

char *table = "test_table"; // table is called test_table
char *column = "value"; // column is called value
char *value = "working"; // what value we are inserting
char *query; // what we are sending to mysql_query

sprintf(query, "INSERT INTO %s (%s) VALUES ('%s')", table, column, value);

if (mysql_query(conn, query)) {
  fprintf(stderr, "%s\n", mysql_error(conn));
  return;
}
</code></pre>

<h1>Purpose</h1>

<p>The purpose of the overall function is so I don't have to keep rewriting SQL insert or update statements in my program. I want to call to one function and pass a few parameters that identify the table, columns and the values of said columns.</p>

<p>Any help would be most appreciated. I'm a bit rusty in C these days.</p>

<h1>Question</h1>

<p>Why is mysql_query not able to send the string?</p>

<h1>Changes</h1>

<p>This worked based on the comments. </p>

<pre><code>const char *query[MAX_STRING_LENGTH];

sprintf((char *)query, "INSERT INTO %s (%s) VALUES ('%s')", table, column, value);

if (mysql_query(conn, (const char *)query)) {
</code></pre>

## Answers
### Answer ID: 18423617
<p>You have no backing storage for <code>query</code>.</p>

<p>It's either set to NULL or some indeterminate value, depending on its storage duration, neither of which will end well :-)</p>

<p>Quick fix is to change it to</p>

<pre><code>char query[1000];
</code></pre>

<p>though any coder worth their salary would also check to ensure buffer overflow didn't occur.</p>


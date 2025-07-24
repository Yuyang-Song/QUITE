# Converting std::wstring to SQLWCHAR *
[Link to question](https://stackoverflow.com/questions/11275225/converting-stdwstring-to-sqlwchar)
**Creation Date:** 1341069324
**Score:** 2
**Tags:** c++, sql, odbc, wstring
## Question Body
<p>I have a C++ program that is dynamically creating a query string which will then be passed to a <code>SQLExecDirect</code> call to connect to a database using ODBC. I'm having trouble passing the variable from one function to another, so I think I must be missing something basic?</p>

<p>In the <code>ConstructQuery</code> function (which returns type <code>SQLWCHAR *</code>), I have:</p>

<pre><code>std::wstring test = L"test string"; //This test string will actually be several concatenated strings
SQLWCHAR *statement = (SQLWCHAR *)test.c_str();
std::wcout &lt;&lt; statement;
return statement;
</code></pre>

<p>This prints the statement variable as expected. But when I pass the variable to my main function like this:</p>

<pre><code>SQLStatement = ConstructQuery(SQLStatement);
std::wcout &lt;&lt; SQLStatement;
</code></pre>

<p>I get no output. </p>

<p>If, instead of <code>statement = (SQLWCHAR *)test.c_str()</code>;</p>

<p>I use: <code>statement = L"test string"</code>;</p>

<p>The variable passes fine, but then I am not able to dynamically create the "test string" query in the earlier part of the function.</p>

<p>I was having a hard time finding out much about <code>SQLWCHAR</code>. I'm guessing that I may be converting <code>std::wstring</code> to <code>SQLWCHAR *</code> incorrectly? Another option would be to rewrite the function so that all of the <code>wstring</code> are <code>SQLWCHAR *</code> and do the concatenation that way - but I'm not sure that's possible and even if it was I don't think it's preferred?</p>

## Answers
### Answer ID: 11276005
<p>You are returning a pointer to a local variable that goes out of scope at the end of the function ConstructQuery. It might be easiest to return a <code>std::wstring</code> by value and then work from there.</p>


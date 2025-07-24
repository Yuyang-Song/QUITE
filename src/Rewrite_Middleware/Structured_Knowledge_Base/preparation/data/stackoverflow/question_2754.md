# Replace String with Regexp for a value fetched from MySQL Query in Robot framework
[Link to question](https://stackoverflow.com/questions/51043714/replace-string-with-regexp-for-a-value-fetched-from-mysql-query-in-robot-framewo)
**Creation Date:** 1530018490
**Score:** 0
**Tags:** mysql, regex, selenium, robotframework, robotframework-sshlibrary
## Question Body
<p>I am Working in Robot Framework with My SQL Database. I am struck up at a point where I need to Run a Query that returns only one value and use it in UI application. </p>

<pre><code>Connect To Database    pymysql    Schema     Username    Password     localhost      portnumber
${result}=    DatabaseLibrary.Query     query
Disconnect From Database
</code></pre>

<p>In the Report I can see the variable <code>${result}= ((11111111,),)</code></p>

<p>I need that <code>11111111</code> and input in the UI application. I Have tried using <code>Get Substring</code>, <code>Replace String with RegExp</code> but it failing either it returns <code>((11111111,),)</code> or string buffer error or typo error. </p>

<p>How can I rewrite to fetch the numeric value to reuse in my code?.  </p>

## Answers
### Answer ID: 51047120
<p>The response from DB queries is list of tuples (that comes from the underlying python implementation) - a list member is a row in the response, the tuple members are the columns in it.</p>

<p>Thus, to get the value of the first column in the first response row, you could do this:</p>

<pre><code>${value}=    Set Variable    ${result[0][0]}
</code></pre>

<p>The indices are 0-based, so if you want the 3rd column from the 2nd row, that would be</p>

<pre><code>${value}=    Set Variable    ${result[1][2]}
</code></pre>


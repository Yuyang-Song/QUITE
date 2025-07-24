# Can I call a stored MySQL function from PHP if SELECT is not allowed?
[Link to question](https://stackoverflow.com/questions/33856035/can-i-call-a-stored-mysql-function-from-php-if-select-is-not-allowed)
**Creation Date:** 1448203487
**Score:** 2
**Tags:** php, mysql, stored-procedures
## Question Body
<p>I've created a stored function in MySQL, and it works fine with the query:</p>

<blockquote>
  <p>SELECT my_function(param);</p>
</blockquote>

<p>Now I'd like to call it from PHP. But SELECT is forbidden to PHP "user" of my database. Should I rewrite the function as a procedure, or is there a way to call it without "SELECT"? </p>


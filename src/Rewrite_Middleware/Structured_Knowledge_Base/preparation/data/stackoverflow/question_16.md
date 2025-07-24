# LINQ to Entities: All method not yielding the expected result
[Link to question](https://stackoverflow.com/questions/10314107/linq-to-entities-all-method-not-yielding-the-expected-result)
**Creation Date:** 1335350945
**Score:** 4
**Tags:** c#, entity-framework, entity-framework-4, linq-to-entities
## Question Body
<p>I have a pretty simple helper method to generate a unique code. To ensure that codes are unique I execute a LINQ to Entities query to verify that it isn't already in use.</p>

<p>My first attempt at writing this method worked perfectly:</p>

<pre><code>public string GenerateUniqueSignUpCode()
{
    while( true )
    {
        var code = Path.GetRandomFileName().Substring( 0, 6 ).ToUpper();
        if( !Context.Users.Any(e =&gt; e.SignUpCode.ToUpper() == code) )
            return code;
    }
}
</code></pre>

<p>However, R# suggested that the LINQ expression could be simplified, which resulted in this method:</p>

<pre><code>public string GenerateUniqueSignUpCode()
{
    while( true )
    {
        var code = Path.GetRandomFileName().Substring( 0, 6 ).ToUpper();
        if( Context.Users.All(e =&gt; e.SignUpCode.ToUpper() != code) )
            return code;
    }
}
</code></pre>

<p>This rewrite causes an infinite loop. The database does not contain any 6-character codes when the code is run so it should exit the loop on the first attempt (as does the first method shown).</p>

<p>Is All broken in EF 4.3.1 or what's going on?</p>

## Answers
### Answer ID: 10314731
<p><code>Context.Users.All(e =&gt; e.SignUpCode.ToUpper() != code</code>
should throw null reference exception if SignUpCode is null.</p>

<p>I guess expression is all fine. Data behind should have the problem</p>

### Answer ID: 10314169
<p>My guess is that this will happen if <code>SignupCode</code> is null for any entry. The comparison using <code>!=</code> won't give a "true" result, so <code>All</code> will return false.</p>

<p>Just a guess, but it's the kind of thing I've seen before. You could try:</p>

<pre><code>if (Context.Users.All(e =&gt; e.SignUpCode == null ||
                           e.SignUpCode.ToUpper() != code))
</code></pre>


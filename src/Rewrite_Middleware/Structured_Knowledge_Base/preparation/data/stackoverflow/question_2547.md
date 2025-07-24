# C# change Dapper dynamic to complain if the property doesn&#39;t exist
[Link to question](https://stackoverflow.com/questions/39467199/c-change-dapper-dynamic-to-complain-if-the-property-doesnt-exist)
**Creation Date:** 1473760707
**Score:** 0
**Tags:** c#, dynamic, dapper
## Question Body
<p>We're using Dapper to fetch data from our SQL database, which returns our data as a collection of 'dynamic'. I understand the power of dynamic types, and the flexibility of "duck typing", basically "if it quacks like a duck, then it is a duck - I don't need to declare that it's a duck".</p>

<p>However, I don't understand why if I try to get a property from a dynamic object that it <em>doesn't</em> have, why doesn't it complain? For example, if I had something that <strong>wasn't</strong> a duck and I called "Quack" on it, I would have thought it reasonable to expect it to complain. EDIT: see comments, this seems to be something about the dynamic which Dapper is giving me because a standard dynamic object gives a runtime error if the property doesn't exist.</p>

<p>Is there a way I can make it complain?</p>

<p>The code that I have is a sequence of lines taking properties from the 'dynamic' and assigning them to the corresponding property in the strongly-typed object. The property names don't always tie-up (due to legacy database naming standards). At the moment, if a field name is misspelled on the dynamic, then it will just fail silently. I want it to complain. I don't want to have to rewrite each single line of code into 5 lines of "does [hard-coded name] property exist on the dynamic"/"if not complain"/"get the value and put it in the right place".</p>

<p>EDIT: Here is the specific code, in case that helps... the field name that is incorrect is "result.DecisionLevel", and I don't get a runtime error, it just assigns null into the target property</p>

<pre><code>        var results = _connection.Query("usp_sel_Solution", new { IdCase = caseId }, commandType: CommandType.StoredProcedure);
        return results.Select(result =&gt; new Solution
        {
            IsDeleted = result.IsDeleted,
            FriendlyName = result.FriendlyName,
            DecisionLevel = (DecisionLevel?)result.DecisionLevel,
        }).ToList();
</code></pre>

<p>SOLUTION: The accepted answer to <a href="https://stackoverflow.com/questions/26659819/dapper-dynamic-return-types">this</a>, combined with Sergey's answer got me to this solution:</p>

<pre><code>internal class SafeDynamic : DynamicObject
{
    private readonly IDictionary&lt;string, object&gt; _source;

    public SafeDynamic(dynamic source)
    {
        _source = source as IDictionary&lt;string, object&gt;;
    }

    public override bool TryGetMember(GetMemberBinder binder, out object result)
    {
        if (_source.TryGetValue(binder.Name, out result) == false)
        {
            throw new NotSupportedException(binder.Name);
        }

        return true;
    }

    // I'll refactor this later, probably to an extension method...
    public static IEnumerable&lt;dynamic&gt; Create(IEnumerable&lt;dynamic&gt; rows)
    {
        return rows.Select(x =&gt; new SafeDynamic(x));
    }
}
</code></pre>

<p>The only change to the sample code is to wrap the call to Dapper's Query method:</p>

<pre><code>        var results = SafeDynamic.Create(_connection.Query("usp_sel_Solution", new { IdCase = caseId }, commandType: CommandType.StoredProcedure));
</code></pre>

<p>Thanks.</p>

<p>For posterity, I'm adding the link to the solution I've provided for <a href="https://stackoverflow.com/questions/28678442/how-can-i-make-dapper-net-throw-when-result-set-has-unmapped-columns">how to do the same thing for Query&lt;T&gt;</a> and note the Edit 25/1/17 "Improvements to avoid threading issues on the static dictionary", which also applies to the solution shown here.</p>

## Answers
### Answer ID: 39468320
<p>You can add wrapping to source objects you have and implement the desired behavior in it (throwing or not trowing an exception, providing a default value or fixing the property names). Something like this:</p>

<p>public class WrapperDynamic : DynamicObject
{
    private dynamic _source;
    public WrapperDynamic(dynamic source)
    {
        _source = source;
    }</p>

<pre><code>public override bool TryGetMember(GetMemberBinder binder, out object result)
{                        
    if (_source.CheckTheProperyExist(binder))
    {
        result = _source.GetProperty(binder);
        return true;
    }
    return false;
}
</code></pre>

<p>}</p>

<p>You should implement CheckTheProperyExist and GetProperty depending on what kind of source objects.</p>

<p>They you should add covering to you selects</p>

<pre><code>return results.Select(x=&gt;new WrapperDynamic(x))
.Select(result =&gt; new Solution
        {
            IsDeleted = result.IsDeleted,
            FriendlyName = result.FriendlyName,
            DecisionLevel = (DecisionLevel?)result.DecisionLevel,
        }).ToList();
</code></pre>

<p>You can add name conversion for legacy names in this wrapper.</p>

### Answer ID: 39467344
<p>The whole expected behavior may differ depending on the dynamic object being built. </p>

<p>It's not a requirement to throw an exception if a dynamic member isn't part of a dynamic object.</p>

<p>For example:</p>

<pre><code>public class MyDynamic : DynamicObject
{
    public override bool TryGetMember(GetMemberBinder binder, out object result)
    {
           // I always set the result to null and I return true to tell
           // the runtime that I could get the value but I'm lying it!
           result = null;
           return true;
    }
}


dynamic myDynamic = new MyDynamic();
string text = myDynamic.text; // This won't throw a runtime exception!
</code></pre>

<p>Probably and for example Dapper tries to get the dynamic member and it doesn't complain if no member is found, and this might be by design. </p>

<p><code>ExpandoObject</code> is a dynamic object which implements <code>IDictionary&lt;string, object&gt;</code> so you can effectively check if a member exists in the dynamic object using <code>ContainsKey</code>:</p>

<pre><code>dynamic expando = new ExpandoObject();
expando.text = "hello world";

if((IDictionary&lt;string, object&gt;)expando).ContainsKey("text")) 
{
    // True
}
</code></pre>

<p>BTW, if a third-party library (or even first-party one) has implemented a dynamic object which doesn't hurt when you access an non existent member, you won't be able to force the opposite. You'll need to live with it, because it's a design decision.</p>

<p>Since <em>duck typing</em> heavily relies on documentation, if you know that a dynamic object works that way, you'll know what a property wasn't set if it receives property type's default value:</p>

<pre><code>dynamic dyn = ...;

// x should be null once it's set and you'll know that
// dyn had no x member...
string x = dyn.x;
</code></pre>


# Find equivalent nested object inside database using Entity Framework 6
[Link to question](https://stackoverflow.com/questions/49712969/find-equivalent-nested-object-inside-database-using-entity-framework-6)
**Creation Date:** 1523143732
**Score:** 1
**Tags:** c#, database, entity-framework, nested, entity-framework-6
## Question Body
<p>I have <code>Patient</code> and <code>Institution</code> tables which I access using EF6</p>

<pre><code>public class Patient
{
    [Key]
    public int PatientId { get; set; }
    public string PatientName { get; set; }
    public virtual Institution Institution { get; set; }
}

public class Institution
{
    [Key]
    public int InstitutionId { get; set; }
    public string InstitutionName { get; set; }
    public virtual ICollection&lt;Patient&gt; Patients { get; set; }
}
</code></pre>

<p>Now, let's say I create a <code>Patient</code> object by hand, something like that:</p>

<pre><code>var newPatient = new Patient {
    PatientName = "Edward",
    Institution = new Institution {
        InstitutionName = "SomeInstitution"
    },
};
</code></pre>

<p>Now I want to check if I already have a patient named "Edward" in the institution "SomeInstitution".</p>

<p>My question is how to do that, for now I have this query:</p>

<pre><code>public static Patient QueryFromAllProperties(MyDbContextcontext, Patient patient)
{
    return context.Patients
            .Where(p =&gt; p.PatientName == patient.PatientName)
            .SingleOrDefault();
}

var patient = QueryFromAllProperties(context, newPatient);
</code></pre>

<p>With that I can find if I have a patient with the same name as the one I created (<code>newPatient</code>), but I'm not sure how could I expand this query to check the institution too.</p>

<p>Note that I think I could just change the where to:</p>

<pre><code>.Where(p =&gt; p.PatientName == patient.PatientName
            &amp;&amp; p.Institution.InstitutionName == patient.Institution.InstitutionName)
</code></pre>

<p>This would work more or less, but it is not clean (this is just a simple example, in my code I have way more nested entities with more properties that I need to check), very boilerplate, and would break if <code>Institution</code> is <code>null</code>.</p>

<p>PS: note that I ignore <code>InstitutionId</code> since I don't want to compare the keys (I want to find the key in the db that configures that exactly object values) and I ignore <code>ICollection&lt;Patient&gt; Patients</code> since It is just a list to configure the many-to-one relation.</p>

<p>So, is there some other better way to do that?</p>

<p>Also, I would like to know how to handle that too in case of a many-to-many relation, so in that case, we can rewrite the tables as:</p>

<pre><code>public class Patient
{
    [Key]
    public int PatientId { get; set; }
    public string PatientName { get; set; }
    public virtual ICollection&lt;Institution&gt; Institutions { get; set; }
}

public class Institution
{
    [Key]
    public int InstitutionId { get; set; }
    public string InstitutionName { get; set; }
    public virtual ICollection&lt;Patient&gt; Patients { get; set; }
}
</code></pre>

<p>And in that case, from the <code>Institutions</code> part I would like to check if a <code>Patient</code> inside the database would contain all the institutions the object currently have (doesn't matter if the database <code>Patient</code> have more <code>Institutions</code> than the one I created.</p>

## Answers
### Answer ID: 49713101
<p>Using the <a href="https://msdn.microsoft.com/en-us/library/bb534972(v=vs.110).aspx" rel="nofollow noreferrer"><code>Any</code></a> function might simplify it a little bit. <code>Any</code> is a function that will return <code>true</code> if there is any element in the collection that matches the condition you pass it.</p>

<pre><code>var exists = context
    .Patients
    .Any(p =&gt; p.PatientName == patient.PatientName &amp;&amp; 
         p.Institution.InstitutionName == patient.Institution.InstitutionName);
</code></pre>

<p>This will return a <code>bool</code> telling you whether it already exists instead of a <code>Patient</code> object as well.</p>

### Answer ID: 49713104
<p>While with c#, a null object needs to be checked, it doesn't with Entity framework and Sql. Your query is translated to sql and run on the database server with an inner join.</p>

<p>For a many to many cardinality, either add the bridging table manually, or lookup how to do "fluent mapping" with EF.</p>

<p>And don't worry about trying to find shorter representations, or "cleaner" lines of code. Prioritise things the user will see, and the overall organisation of your code for maintainability: classes, functions.</p>


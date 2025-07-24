# How to flatten a list of dictionaries with LINQ
[Link to question](https://stackoverflow.com/questions/69720072/how-to-flatten-a-list-of-dictionaries-with-linq)
**Creation Date:** 1635237974
**Score:** -4
**Tags:** c#, linq
## Question Body
<p>I have a collection of <code>Employee</code> objects which have a <code>Skills</code> property. It's a dictionary where the key is particular <strong>skill</strong> and value is <strong>skill level</strong> in some abstract unit.</p>
<p>Example:</p>
<pre><code>{ &quot;C#&quot;, 5 },
{ &quot;Java&quot;, 2 },
{ &quot;XML&quot;, 5 }
</code></pre>
<p>Example code</p>
<pre class="lang-cs prettyprint-override"><code>public class Employee
{
    public int ID { get; set; }
    public Dictionary&lt;string, int&gt; Skills { get; set; }
}
public class EmployeeAssessment
{
    private readonly IEnumerable&lt;Employee&gt; employees;    

    public EmployeeAssessment(IEnumerable&lt;Employee&gt; employees)
    {
        this.employees = employees;
    }

    public List&lt;Employee&gt; GetEmployeesWithMinimalSkillLevel(string skillName)
    {
        // TODO
    }
}
</code></pre>
<p><code>GetEmployeesWithMinimalSkillLevel</code> fetches a list of employees who have a minimum skill level for a given skill, for example, &quot;Java&quot;.</p>
<p>I wrote an efficient solution using <strong>loops</strong> but it doesn't seem elegant to me and I want to rewrite it using LINQ, preferably in a single query.</p>
<p>I always end up with 2 or more LINQ statements and I wonder if it's actually possible to do in single statement. Thanks.</p>

## Answers
### Answer ID: 69720965
<p>Add this code in you <code>EmployeeAssessment.cs</code></p>
<pre><code>public List&lt;Employee&gt; GetEmployeesWithMinimalSkillLevel(string skillName)
{
   return employees.Where(x =&gt; x.Skills[skillName] == employees.Min(x =&gt; x.Skills[skillName]));
}
</code></pre>
<p>Hope this is helpful, You can optimize it further if you want to.</p>

### Answer ID: 69720907
<p>I'll start with example reproduction.</p>
<p>So, we have <code>Employee</code> model:</p>
<pre><code>public class Employee
{
    public int ID { get; set; }
    public string Name { get; set; } // &lt;-- Added just for readability
    public Dictionary&lt;string, int&gt; Skills { get; set; }

    // Simple string representation
    public override string ToString() =&gt; 
        $&quot;{Name} (ID #{ID}) skills:\t {string.Join(&quot; | &quot;, Skills.Select(skill =&gt; $&quot;{skill.Key}: {skill.Value}&quot;))}&quot;;
}
</code></pre>
<p>Let's create a List of 10 Employees with some skills and random skill levels:</p>
<pre><code>static void Main(string[] args)
{
    var random = new Random();
    var employees = new List&lt;Employee&gt;();

    for (int i = 1; i &lt;= 10; i++)
    {
        employees.Add(new Employee
        {
            ID = i,
            // Simple name
            Name = &quot;Employee #&quot; + i,
            Skills = new Dictionary&lt;string, int&gt;()
            { 
                // 0-10 is random skill level
                { &quot;C#&quot;, random.Next(0, 10) },
                { &quot;Java&quot;, random.Next(0, 10) },
                { &quot;XML&quot;, random.Next(0, 10) },
                { &quot;HTML&quot;, random.Next(0, 10) } // :D
            }
        });
    }

    Console.WriteLine(&quot;All employees:&quot;);
    employees.ForEach(employee =&gt; Console.WriteLine(employee.ToString()));
    Console.WriteLine();
}
</code></pre>
<p>That will give us this kind of output:
<a href="https://i.sstatic.net/an0nz.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/an0nz.jpg" alt="enter image description here" /></a></p>
<p><strong>ANSWER PART.</strong></p>
<p>If we want to filter employee by some <em>Minimal Skill Level</em> - we should define which level could be minimal. For example, let's take <strong>3</strong> (of 10). Than, to filter employees by skill level, we could use LINQ in <code>EmployeeAssessment.GetEmployeesWithMinimalSkillLevel</code> method:</p>
<pre><code>public class EmployeeAssessment
{
    private readonly IEnumerable&lt;Employee&gt; employees;

    public EmployeeAssessment(IEnumerable&lt;Employee&gt; employees)
    {
        this.employees = employees;
    }

    public List&lt;Employee&gt; GetEmployeesWithMinimalSkillLevel(string skillName, int minimalSkillLevel = 3)
    {
        return (from employee in employees
                from skill in employee.Skills
                where skill.Key == skillName &amp;&amp; skill.Value &lt;= minimalSkillLevel
                select employee).ToList();
    }       
}
</code></pre>
<p>Or it could be maked in 1 line using <code>.Where</code> and <code>.Any</code> extension methods:</p>
<pre><code>public List&lt;Employee&gt; GetEmployeesWithMinimalSkillLevel(string skillName, int minimalSkillLevel = 3)
{
    return employees.Where(employee =&gt; employee.Skills.Any(skill =&gt; skill.Key == skillName &amp;&amp; skill.Value &lt;= minimalSkillLevel)).ToList();
}
</code></pre>
<p>In both ways we iterating each <code>Employee</code> <code>Skills</code> dictionary to find <code>Key</code>, which equal to skill we provided as <code>skillName</code> and check that its <code>Value</code> is less than or equal to our defined <code>minimalSkillLevel</code>. Iteration in original way looks like <code>foreach</code> loops:</p>
<pre><code>public List&lt;Employee&gt; GetEmployeesWithMinimalSkillLevel(string skillName, int minimalSkillLevel = 3)
{
    List&lt;Employee&gt; employeesWithMinimalSkillLevel = new List&lt;Employee&gt;();

    foreach (Employee employee in employees)
    {
        foreach (KeyValuePair&lt;string, int&gt; skill in employee.Skills)
        {
            if (skill.Key == skillName &amp;&amp; skill.Value &lt;= minimalSkillLevel)
            {
                employeesWithMinimalSkillLevel.Add(employee);
            }
        }
    }

    return employeesWithMinimalSkillLevel;
}
</code></pre>
<p>And when we call one of this methods (or both), we will get filtered List of Employees, whos defined skill (<em>&quot;C#&quot;</em> in example) is less than or equal 3:
<a href="https://i.sstatic.net/nBJSA.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/nBJSA.jpg" alt="enter image description here" /></a></p>


# Is there a better way to do this (C#)?
[Link to question](https://stackoverflow.com/questions/36543547/is-there-a-better-way-to-do-this-c)
**Creation Date:** 1460363374
**Score:** 2
**Tags:** c#
## Question Body
<p>I really don't know what to put in the title, so don't read too much into it.</p>

<p>Anyway, to explain what I'm having trouble with is this. I have three classes: A, B and C. The class hierarchy is as follows:</p>

<p>A &lt;-- B &lt;-- C</p>

<p>(So A is the base class.)</p>

<p>The application in question is a database app. It queries information several tables (A is one table, and B and C are one) and stores it into an instance of C. That part works fine. The problem is when I want to update the table represented by B and C.</p>

<p>To avoid boilerplate code for each code, I use reflection to generate an update query from the class. But if I pass it an instance of a C class, it means it will also pick all the members from A, which is a separate table. Hence the update query will be wrong. And that's where my problem lies. I 
want to get all members of B and C without writing a lot of boilerplate code and with a clean, scalable solution. I just don't know how.</p>

<p>(I currently use an approach where I pick all members of the top-level type, then search all of the class's parents and pick all those members and stop collecting members when it finds a specific parent type, e.g. A. This is an awful solution, I think.)</p>

<p>All these classes contains variables fetched from the database and have no methods or fields. Any good ideas on how to approach this problem? I hear C# does not have multiple inheritance, a tool perfect for this job (thanks C#!).</p>

<p>I hope I'm making myself clear.</p>

<p>EDIT1:
To address some questions and give additional context. First off, here's how my system looks today. To query data, I first have a class X, and a query text. The query is run against the database and returns some rows. Then each row is converted into an instance of X and added to a list. The code knows how to convert a row into an X by using reflection and looking at the actual variables in X and the name of the columns in the fetched database row. It then takes column A and places that information into the variable called A in X. So by making a class X and matching that to the database structure is all that's necessary to fetch another table of data.</p>

<p>Sometimes you need to fetch data from multiple tables and put them together. To do this, I need a class X that matches the information fetched from the query. There are a lot of data that I fetch and all this data has a common subset fetched from table A. The rest is fetched from a lot of other tables that contain additional data. Hence the type system always looks like something A &lt;-- B, where A is the common subset of all data I fetch. This works great for queries. I can add additional data and a class and I'm done. No more boiler plate code.</p>

<p>But that's only half the story. I need to update these tables too (I don't need to update A). But to do that, I need to separate the data fetched from the table A, the common subset. Here's how I do the updating:</p>

<p>Connection.RunUpdateQuery(..., Utility.ToDictionary(Entry));</p>

<p>Where Entry is the class containing the information to update into the target table. So I convert the class into a Dictionary representing column name, column value and send that the RunUpdateQuery which generates an update sql statement and sends it to the database. Again, this is really nice because I have to write absolutely no boilerplate code.</p>

<p>But Utility.ToDicionary can't know what subset of information I actually want to insert. What it does is just take every variable in the class and transform it into a dictionary where the name of the variable is the column name (i.e. the key of the dictionary). In this case, if I pass it a C, I really only just want B and C because they're part of the target table I want to update. The A subset is part of another table which I don't want to update.</p>

<p>If there's a framework that does all this work, I'm all for it. But right now, I don't have the time to rewrite this code. So I'm going to have to wait with that that until later.</p>

<p>This is also my own database that I am designing. I'm in charge of everything regarding the project's design.</p>

<p>I really don't want to generate queries, even if it just means running a tool because a) it means more work every time the database changes and b) it means more bugs because I might forget to update certain places when something changes. With my current reflection-based solution, I don't have to change anything. I just have to design the database and an appropriate class (which I have to anyway since I need to translate the rows from the db into appropriate first-class citizens in the code so I can work with them more easily).</p>

<p>Using attributes doesn't seem like a good way of doing it either because it's all context-dependent. The caller that wants to update a table must be able to choose which fields should be updated in the database, but not at such a fine-grained level. The caller should simply be able to select the class to update, so to speak.</p>

<p>Maybe this gives some clarity into my problem.</p>

<p>EDIT2:
Examples of class A, B, C:</p>

<p>C:</p>

<pre><code>public class PumpEntry: SignalEntryD
{
    public uint? Addr;
    public uint MasterlistIdx;
    public bool MinDominant;
    public uint? TriggerInterval;
    public uint? SpDef;
    public uint? MinDef;
    public uint? MaxDef;
    public uint? Step0Def;
    public uint? Step1Def;
    public uint? Step2Def;
    public uint? Step3Def;
    public uint? Step4Def;
    public uint? Step5Def;
    public uint? ExReqFacBACNet, ExSpFacBACNet;
    public decimal? DeltaTX0Def, DeltaTX1Def, DeltaTX2Def, DeltaTX3Def;
    public uint? DeltaTYMinDef, DeltaTY0Def, DeltaTY1Def;
    public string DeltaTSensor1, DeltaTSensor2;
    public int? ReqLimitMethodDef;
}
</code></pre>

<p>B:</p>

<pre><code>public class SignalEntryD: DeviceEntry
{
    public int? Channel;
    public int? pCOeNum;
}
</code></pre>

<p>A:</p>

<pre><code>public class DeviceEntry: DbType
{
    public int Id;
    public DeviceType Type;
    public string Name;
    public string CMCategory;
    public bool Generate;

    public new string ToString() { return Name; }
}
</code></pre>

## Answers
### Answer ID: 36547663
<p>To be frank, I personally think your current solution is a mess. There are infinte amount tools available for this kind of stuff, why reinvent (and very badly to be honest) the wheel?</p>

<p>Anyhow, trying to solve your issue in your particular setup, here is what I'd do:</p>

<p>First off, get rid of inheritance. You shouldn't be using it at all. Inheritante is most definitely not a tool meant to be used as a means to avoid data duplication, the simple notion is horrendous.</p>

<p>You have 2 distinct tables in your DB, code them as such.</p>

<ol>
<li><code>DbType</code></li>
<li><code>PumpEntry</code></li>
</ol>

<p>I have no idea why you need the intermediate <code>SignalEntryD</code>. If its not a table in your DB then it shouldn't appear anywhere in your code (I'm guessing its also due to code duplication).</p>

<p>Be consistent: if fields <code>Channel</code> and <code>pCoeNum</code> are duplicated throughout different tables in your database then just duplicate them in your entities. Otherwise, create a table in your DB and then model it in your entities (as you do with <code>DbType</code>). Don't mix things up, do it the same way on both ends.</p>

<p>For reasons that become clear later on, make both your entities implement a "dummy" interface <code>ITable</code> (type safety) and a default parameterless constructor (including all your properties / fields of course).</p>

<p>Now the problem is, if I understand correctly, that you are receiving a <code>Dictionary&lt;string, object&gt;</code> with user updated values and you need to update a given table, the problem being that the dicitonary can contain fields that belong to different tables (I won't get into how you ended up with this problem to begin with, I'll just ride along...).</p>

<p>Well then, simply create a way to build any entity from a random dicitionary using reflection (my code uses properties, but it is equivalent with fields):</p>

<pre><code>public static T CreateTable&lt;T&gt;(IDictionary&lt;string, object&gt; values) where T: ITable, new()
{
     var table = new T();

     foreach (var propInfo in typeof(T).GetProperties())
     {
          if (values.ContainsKey(propInfo.Name))
          {
               propInfo.SetValue(table, values[propInfo.Name]);
          }
     }

     return table; //note that any property not defined in the dictionary will be initialized to the field's type default value.
}
</code></pre>

<p>And now, you'd use it as follows:</p>

<pre><code>Connection.RunUpdateQuery(..., CreateTable&lt;TableC&gt;(Utility.ToDictionary(Entry))); //only fields of TableC will be passed along.
</code></pre>

### Answer ID: 36545990
<p>Without learning ORM (which is a <em>proper</em> thing, but may be overkill in a simple case and by saying <em>overkill</em> I mean learning curve) you can use LINQ-to-SQL as model to access your data instead of creating <code>C</code> class yourself. Create <code>dbml</code> file (see e.g. <a href="https://stackoverflow.com/q/2495720/1997232">here</a> regarding what is it). As result you get you table class code-generated, then you just use it</p>

<pre><code>using (var context = new SomeContext()) // static connection string
{
    var query = context.SomeTable.AsQueryable();
    if (SelectedFilter == Today)
        query = query.Where(o =&gt; o.Id &gt;= DateTime.Today);
    ...
    // constructing ViewModel items (WPF, MVVM)
    foreach (var item in query)
        items.Add(new Item()
        {
            Id = item.Id,
            ...
        }
}
</code></pre>

<p><code>Item</code> (<code>B</code> in your example) is a simple class to hold values. You can populate other properties of <code>Item</code> using another query or context (another table or database).</p>

<p>When you want to update database you simply do</p>

<pre><code>using (var context = new SomeContext())
{
    var change = context.SomeTable.First(o =&gt; o.Id == item.Id);
    change.Comment = item.Comment;
    ...
    context.SubmitChanges();
}
</code></pre>

<p>Basically you write those methods once for your ready-made ViewModel item (can be a complicated query to many tables or multiple queries to different databases). Updating part can be methods of <code>Item</code> or, better, of ViewModel (because it can be optimized, e.q. when only changing <code>Comment</code> you don't need to update other fields and perform other queries).</p>

<p>Boilerplate? Not really, look into <code>SomeContext</code> generated cs-file to see some.</p>

### Answer ID: 36543682
<p>You should probably use an ORM library such as Entity Framework or NHibernate. They know how to deal with inheritance (they offer several strategies you can choose from). Then you don't need to write any boilerplate code at all.</p>

### Answer ID: 36543685
<p>You say you are using reflection. In thise case, doing this:</p>

<pre><code>C myObject = new C();    
myObject.GetType().GetProperties(System.Reflection.BindingFlags.Public 
                | System.Reflection.BindingFlags.Instance 
                | System.Reflection.BindingFlags.DeclaredOnly)
</code></pre>

<p>Should only give you the properties declared specifically in <code>C</code>, not in <code>B</code> or <code>A</code>. From there on you could use <code>myObject.GetType().BaseType</code> which would give you <code>B</code>, and its <code>BaseType</code> would be <code>A</code>.</p>

<p><a href="https://dotnetfiddle.net/Hm0lsz" rel="nofollow">Check it in this fiddle</a></p>

<p>I made a rough query generator here: <a href="https://dotnetfiddle.net/FVz6Ay" rel="nofollow">check it in this other fiddle</a>, which generates all update queries needed (if you pass a <code>C</code>, it'll generate queries for tables <code>A</code>, <code>B</code> and <code>C</code>), except for the types you pass as parameters.</p>

<p>With this information, you could easily generate your update queries dynamically and for any levels of hierarchy.</p>

<p>I'd give you more specific code but you wrote none</p>

<p>Not saying this is the perfect solution, but it's what you are asking for in your question</p>

### Answer ID: 36543953
<p>I guess the typical C# solution for this is to mark your fields with custom attributes, and use that in reflection to decide whether or not it should be included.</p>

<pre><code>public class DoSerializeAttribute : Attribute {} 

public class C : B {
    [DoSerialize]
    public MyMember { get; set; }
}
</code></pre>

<p>And later in your reflexion code you can use <a href="https://msdn.microsoft.com/en-us/library/dwc6ew1d(v=vs.100).aspx" rel="nofollow"><code>GetCustomAttribute</code></a> method.</p>


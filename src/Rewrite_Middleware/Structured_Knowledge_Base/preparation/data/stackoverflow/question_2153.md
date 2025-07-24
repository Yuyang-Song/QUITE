# A better way than generic list of anonymous type
[Link to question](https://stackoverflow.com/questions/20979534/a-better-way-than-generic-list-of-anonymous-type)
**Creation Date:** 1389120948
**Score:** 2
**Tags:** c#, linq, sqlite
## Question Body
<p>So I have an sqlite database with <code>[Raw_Data]</code> and <code>[Names]</code> tables. Raw_Data has 3 fields that hold a reference (foreign key?) to the Names table <code>(requester, worker, and approver).</code>
When I display data (<em>dgvResults is a DataGridView in a Windows Forms application</em>), I want to merge the names into the main table <code>(Raw_Data)</code>.</p>

<p>I am using sqlite-net (by praeclarum on guitub) and have this code (only relevant parts shown for brevity):</p>

<pre><code>...
using (var db=new SQLiteConnection(DB_Interop_SQLite.DB_Path, true))
{
    this.Users=db.Table&lt;User&gt;().ToList&lt;User&gt;();
    this.Records=db.Table&lt;Raw_Data&gt;().ToList&lt;Raw_Data&gt;();
    this.Roles=db.Table&lt;Role&gt;().ToList&lt;Role&gt;();
}

var items=
(
    from r in this.Records
    join requester in this.Users on r.Requester equals requester.ID into group1
    from requester in group1.DefaultIfEmpty()
    join worker in this.Users on r.Drafter equals worker.ID into group2
    from worker in group2.DefaultIfEmpty()
    join approver in this.Users on r.Approver equals approver.ID into group3
    from approver in group3.DefaultIfEmpty()
    select new {
        r.ID, r.Project, Requester=requester, r.Task_Code,
        r.DT_submitted, r.DT_required, // other fields
        Worker=worker, r.DT_completed, // other related fields
        Approver=approver, r.DT_approved, // more fields
    }
).ToList();

this.dgvResults.DataSource=items;
...
</code></pre>

<p>I have read through <a href="https://stackoverflow.com/questions/2723985/linq-join-2-listts">LINQ Join 2 List&lt;T&gt;s</a> and <a href="https://stackoverflow.com/questions/5284315/create-items-from-3-collections-using-linq">Create Items from 3 collections using Linq</a> and <a href="https://stackoverflow.com/questions/14639481/merge-multiple-lists-into-one-list-with-linq">Merge multiple Lists into one List with LINQ</a></p>

<p>They have been a great help.</p>

<p>I also referred to <a href="https://stackoverflow.com/questions/612689/a-generic-list-of-anonymous-class">A generic list of anonymous class</a>, which really helped me create the linq query and it all works beautifully.
In my code, User class has ToString() method overwritten so it displays the full name just as I want.</p>

<p>Suppose I wanted a List that holds fields from Raw_Data, but instead of the integer field that refers to the ID from Names, I want the User object as a field, which will hold the ID as well as the rest of the user information (Name, email, phone, etc), just like I have in my anonymous type in the select statement.</p>

<p>So my question is: is there a better way to implement a list (that is not of the anonymous type), without rewriting the entire Raw_Data class just to have a "user" field (from Names table) rather than just the user id?</p>

<p>Ideally, I want the exact same behaviour as my code, but preferably without the anonymous type.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 20982787
<p>You may want to look into something like <a href="http://automapper.codeplex.com/" rel="nofollow">AutoMapper</a>. This is a library that allows you to easily and consistently map from one type of object to another. It's clean and well tested.</p>

### Answer ID: 20979803
<p>Not sure if this what you're looking for, but you could specify a class just to hold that data, then select into that instead of an anonymous type:</p>

<pre><code>public class RawDataInfo
{
    public int ID { get; set; }
    public string Requester { get; set; }
    ...
}
</code></pre>

<p>then alter your select RawDataInfo()</p>

<pre><code> select new RawDataInfo(){
    ID = r.ID, 
    Requester = requester, 
    ...
}
</code></pre>


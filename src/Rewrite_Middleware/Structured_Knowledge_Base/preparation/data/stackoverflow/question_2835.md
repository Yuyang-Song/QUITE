# Relationship - EF Core
[Link to question](https://stackoverflow.com/questions/54748894/relationship-ef-core)
**Creation Date:** 1550498202
**Score:** 2
**Tags:** c#, .net, entity-framework-core
## Question Body
<p>I'm having some trouble to get into EF Core relationship.  </p>

<p>I didn't know how to search it properly, so I've not found what I need, but I got somewhere.</p>

<p>I have these two classes:</p>

<p><strong>Expense:</strong> </p>

<pre><code>public class Expense : Entity
{

    public string Title { get; set; }
    public string Description { get; set; }
    public decimal Amount { get; set; }
    public List&lt;ExpenseType&gt; Types { get; set; }
    public ValidationResult ValidationResult { get; private set; }

    public bool IsValid
    {
        get
        {
            var fiscal = new ExpenseIsValidValidation();
            ValidationResult = fiscal.Valid(this);
            return ValidationResult.IsValid;
        }
    }}
</code></pre>

<p><strong>ExepenseType:</strong></p>

<pre><code> public class ExpenseType : Entity
{
    #region properties
    public string Name { get; private set; }
    public string Description { get; private set; }
    public ValidationResult ValidationResult { get; private set; }
    public bool IsValid
    {
        get
        {
            var fiscal = new ExpenseTypeIsValidValidation();
            ValidationResult = fiscal.Valid(this);
            return ValidationResult.IsValid;
        }
    }}
</code></pre>

<p>During the ToListAsync in ExpenseType, the EF adds the column "expenseId" to the query, but this column does not exist.</p>

<p>My database has three tables, one for each class, and one for the relationship.
(Expense, ExpenseType and Expense_ExpenseType)</p>

<p>By looking for the solution here on StackOverflow I found that I should have a class for the third table. 
Here it is:</p>

<pre><code> public class Expense_ExpenseType
{
    public int ExpenseId { get; set; }
    public Expense Expense { get; set; }
    public int ExpenseTypeId { get; set; }
    public ExpenseType ExpenseType { get; set; }
}
</code></pre>

<p>My idea is that I can have an ExpenseType without having an Expense, and I can have an Expense without ExpeseType or with as many as I want of them.  </p>

<p>So ExpenseType hasn't any Expense. </p>

<p>I'm not sure what I should do now. 
Should I Map using optionsBuilder? How?
Should I ReWrite the database?</p>

## Answers
### Answer ID: 54752114
<p>If you want to create Many-to-Many relationship, you have several options how to do it:</p>

<ol>
<li><p>Create additional class how you described. In this case EF will create table and you can get access to get values only from this table.</p>

<pre><code>public class Expense_ExpenseType
{
   public int ExpenseId { get; set; }
   public Expense Expense { get; set; }
   public int ExpenseTypeId { get; set; }
   public ExpenseType ExpenseType { get; set; }
}
</code></pre></li>
<li><p>You may don't create class and just describe in the context relationship. Where you will describe everything and EF will create by yourself this table. But from the app you will not see this table. You have to use this variant if you don't want to extend table with additional fields.</p>

<pre><code> modelBuilder
   .Entity&lt;Student&gt;()
   .HasMany&lt;Course&gt;(s =&gt; s.Courses)
   .WithMany(c =&gt; c.Students)
   .Map(cs =&gt;
     {
       cs.MapLeftKey("StudentRefId");
       cs.MapRightKey("CourseRefId");
       cs.ToTable("StudentCourse");
     });
</code></pre></li>
</ol>

<p>For this relationship you can read more <a href="http://www.entityframeworktutorial.net/code-first/configure-many-to-many-relationship-in-code-first.aspx" rel="nofollow noreferrer">here</a></p>

<p>But in your case you don't need to use Many-to-Many. That's why if you don't want to add propertie <code>ExpanseTypeId</code> or <code>ExpenseId</code> in your model you can describe it like this:</p>

<pre><code>protected override void OnModelCreating(ModelBuilder modelBuilder)
{
   modelBuilder.Entity&lt;Expense&gt;()
     .HasMany&lt;ExpenseType&gt;(o =&gt; o.Types) //It is your list of expense types.
     .WithOne() //Here you can add model for expense. To have an option go back from expense type to expense
     .HasForeignKey("ForeignKey");//This key EF will create for you in DB but not in you app model
}
</code></pre>

<p>What do you want to use you have to decide. If you have an idea that expense has a lot of expensetypes and each expense type has a lot of expenses. You have to use Many-To-Many how I described.</p>

### Answer ID: 54749575
<p>I think that your main question is "My idea is that I can have an ExpenseType without having an Expense, and I can have an Expense without ExpeseType or with as many as I want of them."</p>

<p>so you can do that by creating a nullable foreign key ExpenseTypeId in Expanse class and HashSet of Expanse in ExpeseType class. </p>

<p>Like this:</p>

<pre><code>public class ExpenseType : Entity
{
 public ICollection&lt;Expanse&gt; Expanses {get; set;} = new HashSet&lt;Expanse&gt;()
}

public class Expense : Entity
{
 public int? ExpanseTypeId {get; set;}
 public ExpanseType ExpanseType {get; set;}
}
</code></pre>


# How should I model static reference data with Entity Framework?
[Link to question](https://stackoverflow.com/questions/48630029/how-should-i-model-static-reference-data-with-entity-framework)
**Creation Date:** 1517858783
**Score:** 3
**Tags:** c#, entity-framework, oop, design-patterns, data-modeling
## Question Body
<p>I have a simulation model that uses a database to store both input and output data, using Entity Framework and the Database First approach. The database is queried through a data access layer more-or-less as described here: <a href="https://blog.magnusmontin.net/2013/05/30/generic-dal-using-entity-framework/" rel="nofollow noreferrer">https://blog.magnusmontin.net/2013/05/30/generic-dal-using-entity-framework/</a></p>

<p>However, some of the static input data used is <em>not</em> stored in the database, but is instead hard-coded into the application as fields. This data is genuinely static and will not change while the application is running. For example: </p>

<pre><code>public class Currency
{
    public string Symbol { get; private set; }
    public string Name { get; private set; }

    private Currency()
    {
    }

    // Fields like this store reference data
    public static readonly Currency USD = new Currency
    {
        Symbol = "USD",
        Name = "US Dollar"
    };

    public static readonly Currency EUR = new Currency
    {
        Symbol = "EUR",
        Name = "Euro"
    };
}
</code></pre>

<p>This has the advantage that referring to the reference data is as easy as using e.g. <code>Currency.USD</code> throughout the model, without having to go through the data access layer. The disadvantage with how this is implemented is that the data model is clumsy and not really relational anymore (in the sense that relations are enforced through foreign keys); a model object that uses the above reference data like e.g.</p>

<pre><code>public class Transaction
{
    public int Id { get; set; }
    public Currency Currency { get; set; }
    public double Price { get; set; }
}
</code></pre>

<p>has a backing table in the DB that looks like this:</p>

<pre><code>create table Transaction
(
    Id int not null primary key,
    Currency nvarchar(3) not null , -- Currency symbol, not a foreign key
    Price float not null 
);
</code></pre>

<p>The currency attribute is converted back and forth between a string and an object when reading and writing through the business layer. </p>

<p>I would like to rewrite this with the following goals:</p>

<ul>
<li>Storing static reference data in the DB along with all other data to keep the data model clean. </li>
<li>Not having to query the data access layer every time the static reference data is needed (i.e. to get as close to a hard-coded <code>Currency.USD</code> as possible). Throughout a simulation run, the reference data might be read once at startup and then queried 1,000,000,000 times.</li>
</ul>

<p>Is some sort of caching mechanism what I'm looking for here? Is that likely to be performant enough? What would be an elegant way to solve this in general and for Entity Framework in particular?</p>

<p>Thanks.</p>

## Answers
### Answer ID: 48630987
<p>Here's an idea for a pattern for doing this with EF:</p>

<p>The static reference data in this example "Color" has both a non-int key and extra properties.  Both of which you can't do with an Enum.  It adds the reference data to the database using an Initializer, but in database-first you would just add it ahead-of-time, and assume it's there.</p>

<p>A variant of this pattern would use a lazy static collection of reference entities retrieved from the database on startup, instead of having the values hard-coded in the class definition.  In either case, marking the reference entities as Unchanged in SaveChanges prevents EF from trying to insert them into the database.</p>

<pre><code>using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.Entity;
using System.Linq;

namespace Ef6Test
{

    public class Color
    {
        public static Color Red = new Color() { Name = "Red", RGB = 0xFF0000 };
        public static Color Green = new Color() { Name = "Green", RGB = 0x00FF00 };
        public static Color Blue = new Color() { Name = "Blue", RGB = 0x0000FF };
        [Key]
        public string Name { get; set; }
        public int RGB { get; set; }
    }

    public class Car
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public string ColorName { get; set; }
        public Color Color { get; set; }
    }

    class Db : DbContext
    {

        public DbSet&lt;Color&gt; Colors { get; set; }
        public DbSet&lt;Car&gt; Cars { get; set; }


        public override int SaveChanges()
        {
            return SaveChanges(false);
        }
        public int SaveChanges(bool includeStatic = false)
        {
            if (!includeStatic)
            {
                foreach (var e in ChangeTracker.Entries&lt;Color&gt;())
                {
                    e.State = EntityState.Unchanged;
                }
            }

            return base.SaveChanges();
        }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
        }
    }

    class MyInitializer : DropCreateDatabaseAlways&lt;Db&gt;
    {
        protected override void Seed(Db context)
        {
            base.Seed(context);
            context.Colors.AddRange(new[] {Color.Red,Color.Green,Color.Blue });
            context.SaveChanges(true);

        }
    }

    class Program
    {    
        static void Main(string[] args)
        {    
            Database.SetInitializer(new MyInitializer());

            using (var db = new Db())
            {
                db.Database.Log = m =&gt; Console.WriteLine(m);
                db.Database.Initialize(true);
            }
            using (var db = new Db())
            {
                db.Database.Log = m =&gt; Console.WriteLine(m);

                var c = db.Cars.Create();
                c.Color = Color.Red;
                db.Cars.Add(c);

                db.SaveChanges();

            }


            Console.WriteLine("Hit any key to exit");
            Console.ReadKey();
        }
    }
}
</code></pre>


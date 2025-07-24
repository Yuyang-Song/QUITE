# Relational Table Design For Single Object w/Multiple Types
[Link to question](https://stackoverflow.com/questions/23941571/relational-table-design-for-single-object-w-multiple-types)
**Creation Date:** 1401392248
**Score:** 0
**Tags:** mysql, database-design, relational-database, database-schema
## Question Body
<p>I am creating a database for a web application and am looking for some suggestions to model a single entity that might have multiple types, with each type having differing attributes.</p>

<p>As an example assume that I want to create a relational model for a "Data Source" object.  There will be some shared attributes of all data sources, such as a numerical identifier, a name, and a type.  Each type will then have differing attributes based on the type.  For the sake of argument let's say we have two types, "SFTP" and "S3".  </p>

<p>For the S3 type we might have to store the bucket, AWSAccessKeyId, YourSecretAccessKeyID, etc.  For SFTP we would have to store the address, username, password, potentially a key of some sort.  </p>

<p>My first inclination would be to break out each type into their own table with any non-common fields being represented in that new table with a foreign key in the main "Data Source" table.  What I don't like about that is that I would then have to know which table is associated with each type that is stored in the main table and rewrite the queries coming from the web app dynamically based on that type.</p>

<p>Is there a simple solution or best practices I'm missing here?</p>

## Answers
### Answer ID: 23956272
<p>What you are describing is a situation where you want to implement table inheritance. There are three methods for doing this, all described in Martin Fowler's excellent book, <a href="https://rads.stackoverflow.com/amzn/click/com/0321127420" rel="nofollow noreferrer" rel="nofollow noreferrer">Patterns of Enterprise Application Architecture</a>.</p>

<p>What you describe as your first inclination is called <a href="http://www.martinfowler.com/eaaCatalog/classTableInheritance.html" rel="nofollow noreferrer">Class Table Inheritance</a> by Fowler. It is the method that I tend to use in my database designs, but doesn't always fit well. This method corresponds most closely to an OO view of the database, with a table representing an abstract class and other tables representing concrete implementations of the abstract class. Data must be queried and updated from multiple tables.</p>

<p>It sounds like what you actually want to use is called <a href="http://www.martinfowler.com/eaaCatalog/singleTableInheritance.html" rel="nofollow noreferrer">Single Table Inheritance</a> by Fowler. In this method, you'd actually put columns for all of your data in one table, with a discriminator column to identify which fields are associated with the element type. Queries are generally simpler, although you do have to deal with the discriminator column.</p>

<p>Finally, the third type is called <a href="http://www.martinfowler.com/eaaCatalog/concreteTableInheritance.html" rel="nofollow noreferrer">Concrete Table Inheritance</a> by Fowler. In my mind, this is the least useful. In this method, you give up all concepts of having any kind of hierarchical data, and create a single table for each element type. Still, there are times when this might work for you.</p>

<p>All three methods have their pros and cons. You should consult the links above to see which might work best for you in your project.</p>


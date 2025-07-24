# How would you code a repository pattern like a &quot;factory&quot; design pattern?
[Link to question](https://stackoverflow.com/questions/1064378/how-would-you-code-a-repository-pattern-like-a-factory-design-pattern)
**Creation Date:** 1246375989
**Score:** 0
**Tags:** c#, linq-to-sql, repository-pattern, entity-attribute-value, factory-pattern
## Question Body
<p>I thought I would rewrite this question (same iteration).  The original was how to wrap a repository pattern around an EAV/CR database.  I am trying a different approach.</p>

<p><strong>Question: How could you code a data repository in a "factory" design pattern way?</strong>  I have a fixed number of entities, but the attributes to these entities are fairly customer specific.  They advertise Products which are all similar, but each customer attaches different information to them based on their business model.  For example, some care about the percent slab off waste while others care about the quantity of pounds sold.  Every time we find another customer, we add a bunch of fields, remove a bunch of fields, and then spend hours keeping each solution current to the latest common release.</p>

<p>I thought we could put the repository classes in a factory pattern, so that when I know the customer type, then I know what fields they would use.  Practical?  Better way?  The web forms use User Controls which are modified to reflect what fields are on the layouts.  We currently "join" the fields found on the layout to the fields found in the product table, then CRUD common fields.</p>

<p><strong>Previous question content</strong>:</p>

<p>We have an EAV/CR data model that allows different classes for the same entity.  This tracks products where customers have wildly different products.  Customers can define a "class" of product, load it up with fields, then populate it with data.  For example, <br /></p>

<p><code>Product.Text_Fields.Name</code><br />
<code>Product.Text_Fields.VitaminEContent</code></p>

<p><strong>Any suggestion on how to wrap a repository pattern around this?</strong><br /><br />
We have a three table EAV: a Product table, a value table, and a meta table that lists the field names and data types (we list the data types because we have other tables like Product.Price and Product.Price Meta data, along with others like Product.Photo.)  Customers track all kinds of prices like a competitor's percent off difference as well as on the fly calculations.</p>

<p>We currently use Linq to SQL with C#.</p>

<p>Edit:</p>

<p>I like the "Dynamic Query" Linq below.  The idea behind our DB is like a locker room locker storage.  Each athlete (or customer) organizes their own locker in the way they wish, and we handle storing it for them.  We don't care what's in the locker as long as they can do what they need with it.</p>

<p>Very interesting...  The objects passed to the repository could be dynamic?  This almost makes sense, almost like a factory pattern.  Would it be possible for the customer to put their own class definitions in a text file, then we inherit them and store them in the DB?</p>

## Answers
### Answer ID: 1064501
<p>As I understand it the repository pattern abstracts the physical implementation of the database from the application. Are you planning to store the data in differing data stores? If you are happy with Linq to SQL then I'd suggest that perhaps you don't need to abstract in this way as it looks to be extremely complex. That said, I can see that providing an EAV-style repository, i.e. a query would need to be passed Table, Field Type, and Field Name along with any conditional required, might offer you the abstraction you are seeking.</p>

<p>I'm not sure if that would still qualify as a repository pattern in the strictest terms as you aren't really abstracting the storage from the application. It's going to be a toss-up between benefit and effort and there I'm unable to help.</p>

<p>You might want to take a look at the Dynamic Linq extensions found in the dynamic data preview on Codeplex.</p>


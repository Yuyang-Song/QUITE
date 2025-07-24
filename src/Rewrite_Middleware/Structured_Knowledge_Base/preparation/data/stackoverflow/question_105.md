# Entity data inheritance
[Link to question](https://stackoverflow.com/questions/12991128/entity-data-inheritance)
**Creation Date:** 1350755697
**Score:** 0
**Tags:** c#, .net, linq-to-entities
## Question Body
<p>I'm currently involved in a project where we will present data from an external data source to visitors, but we will also provide meta data for the entities/rewrite some of the original data.</p>

<p>The external data source is a SQL Server database which I've created an .edmx file from and I've created an additional, controllable, SQL Server database with it's own .edmx file. But I'm not comfortable with using two entities for what, in my eyes, is one type of data.</p>

<p>Somehow I would like to merge the two data sources into one, and use only one entity class which I could query. Inheritance in LINQ to Entities would be perfect, but I would prefer no to change the .edmx files manually.</p>

<p>As it is now I have to create wrapper classes and populate them manually with the entity classes, or use multiple database queries to fetch the required data which is a big turn off performance wise.</p>

<p>It feels like it have to exist some sort of work around for these problems I'm facing?</p>

## Answers
### Answer ID: 12991173
<p>You have two options here.</p>

<ul>
<li><p>First you can extend the entity framework class by using partial
classes. It will help you avoiding changes to the generated classes.</p></li>
<li><p>Second you can use Entity Framework code first, Which i will
recommend as you will have more control on your entities.</p></li>
</ul>


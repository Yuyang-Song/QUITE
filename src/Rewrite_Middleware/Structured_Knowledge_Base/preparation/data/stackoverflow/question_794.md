# eclipse generating entity classes from database is not pulling associations
[Link to question](https://stackoverflow.com/questions/42600976/eclipse-generating-entity-classes-from-database-is-not-pulling-associations)
**Creation Date:** 1488658987
**Score:** 5
**Tags:** java, eclipse, hibernate, sybase
## Question Body
<p>I am working on rewriting an application using hibernate with existing database.This application has all select queries it is basically read only application.</p>

<p>I am trying to create entity classes from tables using JPA tools in eclipse, as there are no constraints defined on database , the generated model classes have no relationships.There are around 100 tables using by the application in that database.</p>

<p>I tried to figure out the relationships between tables from the existing sql queries and also using data in database.But as there are lot of tables it is hard to do it manually.</p>

<p>As the database used by number of applications there is no way of enforcing relationships on database</p>

<p>Question:</p>

<p>1.Is there any way of to generate entities with relationships if there are no constraints on database?</p>

<p>2.If it needs to be done manually, what is the best approach?</p>

## Answers
### Answer ID: 44851114
<blockquote>
  <p>1.Is there any way of to generate entities with relationships if
  there are no constraints on database?</p>
</blockquote>

<p>Even if it was possible, it would be very error prone. On which rule, the relationships could be generated in a idiomatic and reliable way ?
<br></p>

<blockquote>
  <p>2.If it needs to be done manually, what is the best approach?</p>
</blockquote>

<p>If I was to your place, I would do the things in a safety way.<br>
Adding manually all relationships between entities after entities be generated may be error-prone and cumbersome.<br></p>

<p>Suppose that you make mistakes during the generation phase of the entities (and you could seeing the number of tables) and you want to generate them again while you already added dozen and dozen of relationships manually in your entities.<br>
By starting again the generation, you will lose all these manually added relationships in the entities.<br> You have to start again from zero.</p>

<p>I think that you should do the things in the reverse way.<br></p>

<p>You could for example create a copy of the database (I refer to a copy as I suppose that if you have no constraints on the tables, it is intentional) and add constraints on the tables of the database copy.<br>
Then, from these tables with specified constraints, you could generate entities with all required relationships. <br></p>

<p><strong>This way provides two advantages</strong> :</p>

<ul>
<li><p>ability to have a fast feedback whether the PK/FK constraints that you want to add one the tables are compatible with your existing data.<br></p></li>
<li><p>ability to proceed in an incremental way and be able to do some steps back if required. <br>
For example if you make some mistakes during the generation phase of the entities (and you could make them seeing the number of tables), you could repeat the generation phase without losing the automatic generated relationship resulting of PK/FK constraints you added on the tables.</p></li>
</ul>

### Answer ID: 44880840
<p>There is no direct way to create all entity classes with required relationship .</p>

<p>But if you wanna add relationships in generated entities the most simplest way which i guess is provide relationship in <strong>Table association</strong>.</p>

<p>You can follow the link for more reference.</p>

<p><a href="http://help.eclipse.org/luna/index.jsp?topic=%2Forg.eclipse.jpt.doc.user%2Ftasks024.htm" rel="nofollow noreferrer">http://help.eclipse.org/luna/index.jsp?topic=%2Forg.eclipse.jpt.doc.user%2Ftasks024.htm</a></p>


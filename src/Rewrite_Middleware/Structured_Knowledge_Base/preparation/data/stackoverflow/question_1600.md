# Add framework to java project
[Link to question](https://stackoverflow.com/questions/973682/add-framework-to-java-project)
**Creation Date:** 1244608057
**Score:** 1
**Tags:** java, frameworks
## Question Body
<p>I've been working on a java web project. </p>

<p>Currently this project doesnt use any framework. Its a standard MVC application, using servlets and DAO with jdbc access to database (all queries are handwritten).</p>

<p>The project has a good code (all project developed using TDD), but its way too slow to add any feature, since all have to be done by hand.</p>

<p>In this case, which framework would you suggest to add this project?
I can't use a framework that requires me to rewrite all current code base to fit in this framework.</p>

<p>I think that Hibernate is a great choice for persistence.</p>

<p>But what else? Spring? VRaptor? Struts? </p>

## Answers
### Answer ID: 973703
<p>You might add interfaces for your classes, use Hibernate for the persistence layer replacing your DaoSqlImplementation by DaoHibernateImplementation one per time. As long as you wire your application with interfaces you won't have any problem.</p>

<p>Also I recommend you to use Spring, this way you can <em>switch</em> between implementations declaratively by just modifying the XML. One of the principles Spring follows is <a href="http://en.wikipedia.org/wiki/Inversion_of_Control" rel="nofollow noreferrer">IoC (Inversion of Control)</a>. In this case means your application controls the framework and not the framework controls the application which is exactly what you requested.</p>

<p>One important thing is that you must justify every framework you decide to add to the application and not just add it because <em>it is very cool</em>.</p>


# Should I use MongoDB with entity&#39;s relations to be non-blocking end to end with my Spring 5 project?
[Link to question](https://stackoverflow.com/questions/51859342/should-i-use-mongodb-with-entitys-relations-to-be-non-blocking-end-to-end-with)
**Creation Date:** 1534338438
**Score:** 1
**Tags:** java, spring, spring-data, reactive-programming, spring-webflux
## Question Body
<p>I started a Spring WebFlux project some times ago, the goal of this project is to offer an REST API which collects its data from a database.</p>

<p>I currently go with a reactive approach thanks Reactor project included inside Spring 5 release and created reactive controllers. I need to persist in my database normalized datas with relations, this is why I use PostgreSQL.</p>

<p>At the time I am writing this lines, no reactive programming support is provided for JDBC and so JPA. But my controllers are only truly non-blocking if other components that they work with are also non-blocking. If I write Spring WebFlux controllers that still depend on blocking repositories, then my reactive controllers will be blocked waiting for them to produce data.</p>

<p>I would like to be non-blocking end to end, so I wonder to move on one of the NoSQL databases supported by Spring Data : Cassandra DB or MongoDB. I don't think Cassandra DB really fits to my needs, I will need to rewrite my entities and think differently my database's structure to be query oriented.</p>

<p>I read it is possible to keep some relations between my entities with MongoDB, especially with the last 4.0 version without refractor completely my db schema. But I wonder what is worth ?</p>

<ul>
<li>Switch to MongoDB even if I need to keep relational datas</li>
<li>Keep to fetch data in a blocking fashion and then translate it into a reactive type as soon as possible</li>
<li>Forget Spring WebFlux and go back to Spring MVC (probably not)</li>
</ul>

<p>Thank you for any help and advice !</p>

## Answers
### Answer ID: 51859896
<p>I think it depends on your context, it seems that moving to a document db might not be a good fit for your data as it seems fully relational unless you are sure you can model your data as a bunch of aggreates, otherwise you might end up having other problems such as transaction consistency when checking consistency rules between your models. As a first option i would try to fetch data in another thread, perhaps wrapping the call in an rxjava observable. Although it is still a blocking call it will not block the main thread and you will be able to make better use of resources.</p>

<p>Those are my 2 cents.
Regards </p>


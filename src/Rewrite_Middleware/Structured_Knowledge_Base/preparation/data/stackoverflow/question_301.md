# Symfony2 Create an entity from two databases in one repository
[Link to question](https://stackoverflow.com/questions/19844511/symfony2-create-an-entity-from-two-databases-in-one-repository)
**Creation Date:** 1383851253
**Score:** 2
**Tags:** symfony, doctrine, repository, entity
## Question Body
<p>I have a legacy database from which I have to extract some data and provide it as xml. For that I chose Symfony2 but now I am stuck. I would like to create one entity object, but the problem is, the data for it is distributed in two databases´(on the same server). I don't want to rewrite what I already made, so the easiest way would be to load the other database connections EntityManager in the existing repository. This is where I'am stuck. How can I load an EntityManager in a repository that uses the other connection? And what is the easiest way to "fill-in" the rest of the data of the entity? (By the way, I've used native queries in the repositories, because the legacy database is really complex and does not obey to any rules of DB design). I would be appreciate any help.</p>

## Answers
### Answer ID: 19856885
<p>You could manage a second database connection called 'legacy', linking to the same database</p>

<p>than you need to map the entities to your managed connections than you could access your legacy table => entity and do whatever you want to with it ;)</p>

<p><a href="http://symfony.com/doc/current/cookbook/doctrine/multiple_entity_managers.html" rel="nofollow">http://symfony.com/doc/current/cookbook/doctrine/multiple_entity_managers.html</a></p>


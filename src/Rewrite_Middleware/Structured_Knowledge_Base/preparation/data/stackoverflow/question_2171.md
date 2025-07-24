# Is it possible to have Symfony and/or Doctrine hydrate associated objects managed by different entity managers?
[Link to question](https://stackoverflow.com/questions/21682805/is-it-possible-to-have-symfony-and-or-doctrine-hydrate-associated-objects-manage)
**Creation Date:** 1392050165
**Score:** 1
**Tags:** php, symfony, doctrine-orm
## Question Body
<p>I have a legacy application that was using Xaraya to manage user content that I am trying to replace with a rewrite using Symfony/Sonata to manage users and/or content.</p>

<p>For whatever reason, previous developers managed this with two different databases (MySQL for Xaraya, and SQL Server for other things, including authenticating users).</p>

<p>I am trying to create Entity mappings such that the users/groups from SonataUserBundle (which extends FOSUserBundle) use the entity manager associated with the login database connection, and this works for logging into the admin site itself, but blows up when it tries to hydrate objects that have associations to the User entity.</p>

<p>It appears that Doctrine does not try to find the entity manager associated with an entity when hydrating an object's associations.</p>

<p>My question is this: it it possible to make Doctrine hydrate objects using the entity manager for an entity instead of assuming it's mapped to the current entity manager, and if not, is there any form of a clean code work-around for it?</p>

<p>Thanks.</p>

<p>(Note: The method of using the "databasename.tablename" syntax in the query that I have seen mentioned elsewhere will not work for my use case.)</p>


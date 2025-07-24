# hibernate object vs database physical model
[Link to question](https://stackoverflow.com/questions/698922/hibernate-object-vs-database-physical-model)
**Creation Date:** 1238445767
**Score:** 2
**Tags:** java, performance, hibernate
## Question Body
<p>Is there any real issue - such as performance - when the hibernate object model and the database physical model no longer match?  Any concerns?  Should they be keep in sync?</p>

<p>Our current system was original designed for a low number of users so not much effort was done to keep the physical and objects in sync.  The developers went about their task and the architects did not monitor. Now that we are in the process of rewriting/importing the legacy system into the new system, a concern has been raised in that the legacy system handles a lot of user volume and might bring the new system to its knees.</p>

<p><strong>Update 20090331</strong><br>
From Pete's comments below - the concern was about table/data relationships in the data layer vs the object layer.  If there is no dependencies between the two, then there is no performance hits if these relationships do not match? Is that correct?</p>

<p>The concern from my view is that the development team spends a lot of time "tuning" the hibernate queries/objects but nothing at the database layer to improve the performance of the application.  I would have assumed that they would tune at both layers.</p>

<p>Could these issue be from just a poor initial design of the database to begin with and trying to cover/make up the difference by the use of Hibernate?</p>

<p>(I am new to this project so playing catchup)</p>

## Answers
### Answer ID: 699588
<p><strong>Update: in response to comment:</strong>  It is CRUCIAL that the database be optimized in addition to the Hibernate use.  When you think about it, after all the work hibernate does, in the end it is just querying the database.  If the database doesn't perform well (wrong or missing indexes, poorly set up table spaces, etc) it doesn't matter how much you tune Hibernate.  On the flip side if your database is set up well but Hibernate isn't (perhaps the caching is not set up properly, etc., and you are going back to the database a lot more then you need to) then performance will suffer as well.  It is always important to tune the system end to end, but start at the foundation (database) and work up.</p>

<p><strong>End Update</strong></p>

<p>I'm curious what you mean about 'don't match' - do you mean columns have been added to tables that aren't represented in the hibernate data objects?   Tables have been added?  I don't think anything like that would affect performance (more likely data integrity if you are not inserting/updating all columns)</p>

<p>In general, the goal of the object model should NOT be match the database schema verbatim.  You want to abstract the underlying data complexity / joins / normalization, that is the whole point of using something like Hibernate.</p>

<p>So for example lets say you have (keeping things very simple) 'orders' and 'order items',</p>

<p>your application code should be able to do something like</p>

<p>order.getItems()</p>

<p>without having to know that underneath it is a one to many relationship.  The details in your hibernate code control how the load is done (lazy, caching, etc).</p>

<p>If that doesn't answer your question then please provide more detail</p>

### Answer ID: 698962
<p>It's certainly possible that the changes you describe could cause performance problems.
I would have thought that this should have been part of the design spec.<br>
So when you're coding it, you bear the performance critiera in mind.  </p>

<p>The only way to really know though is to load the data onto a test environment, and run some tests.</p>

<p>This should definately be done before going live, as it might produce some quite interesting results.</p>

### Answer ID: 698954
<p>You could of course code your abstraction layer in asm - "might" (awful word for a developer) be faster. </p>

<p>This is premature optimization - maybe breaking a clean project-layout. </p>

<p>As in the hibernate-manual - optimization can look different ways - plain coding some parts "might" be part of it.</p>


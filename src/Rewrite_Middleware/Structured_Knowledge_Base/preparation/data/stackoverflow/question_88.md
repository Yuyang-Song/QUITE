# Working with two non-directly related tables in one NHibernate query
[Link to question](https://stackoverflow.com/questions/12361223/working-with-two-non-directly-related-tables-in-one-nhibernate-query)
**Creation Date:** 1347323430
**Score:** 0
**Tags:** c#, nhibernate
## Question Body
<p>I am new to NHibernate and am not sure if what I am asking makes sense.</p>

<p>I am trying to rewrite some code I currently have:</p>

<pre><code>public IEnumerable&lt;Order&gt; GetByQueue(OrderStatus orderStatus, Queue queue)
{
    var criteria = NHibernateSession.CreateCriteria(typeof (TaskDevice), "TaskDevice");

    //Pull up all Tasks where a Task's TaskDevice's SourceSiteID or DestinationSiteID are represented in a Queue's QueueLocations.
    foreach(QueueLocation queueLocation in queue.QueueLocations)
    {
        criteria.Add(
                Expression.Disjunction()
                    .Add(Restrictions.Eq("OriginalLocationID", queueLocation.ComponentID))
                    .Add(Restrictions.Eq("LocationID", queueLocation.ComponentID))
            );
    }

    //Get a hold on all the Tasks returned from TaskDevices.
    List&lt;Task&gt; tasks = criteria.List&lt;TaskDevice&gt;().Select(taskDevice =&gt; taskDevice.Task).ToList();

    //Return all Orders of the given Tasks whose OrderStatus matched the provided orderStatus.
    return tasks.Where(task =&gt; task.Order.OrderStatus == orderStatus).Select(task =&gt; task.Order);
}
</code></pre>

<p>This code currently depends on a Queue object. I would like to change this code such that a queueID is provided instead of a Queue object. The table QueueLocation contains 'QueueID' for one of its columns.</p>

<p>This means that I now need to interact with another table in my database, QueueLocation, load the QueueLocation who has a QueueID matching the provided QueueID, and then emulate the adding of restrictions without iterating over a Queue object.</p>

<p>Task does not know of Queue and Queue does not know of Task. They are related by the fact that a Queue may contain a QueueLocation whose ComponentID matches a Task's OriginalLocationID or LocationID.</p>

<p>If I change my initial criteria declaration to:</p>

<pre><code>var criteria = NHibernateSession
    .CreateCriteria(typeof (TaskDevice), "TaskDevice")
    .CreateCriteria("QueueLocation", "QueueLocation");
</code></pre>

<p>then an exception is generated indication that NHibernate could not find property QueueLocation on TaskDevice. This is a valid exception -- TaskDevice does not know of QueueLocation.</p>

<p>I am wondering how to load two non-related tables using NHibernate such that I may filter my restrictions fully through NHibernate in one query. Is this possible?</p>

## Answers
### Answer ID: 12361406
<p>Criteria is not a good API for queries with entities that are not related in the model.</p>

<p>Use HQL instead.</p>


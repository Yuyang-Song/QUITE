# Unable to determine if entity is transient or detached on deletion
[Link to question](https://stackoverflow.com/questions/46639909/unable-to-determine-if-entity-is-transient-or-detached-on-deletion)
**Creation Date:** 1507529934
**Score:** 1
**Tags:** nhibernate
## Question Body
<p>Our schema contains a table with a composite primary key. The entity does not have any version/timestamp columns. The mapping is:</p>

<pre><code>mapping.CompositeId().KeyReference(e =&gt; e.ParentEntity).KeyProperty(e =&gt; e.DTFR);
</code></pre>

<p>When user clicks Delete button, HTTP request is posted to the server, the server creates new NHibernate session and invokes <code>session.Delete()</code>:</p>

<pre><code>        using (var session = SessionFactory.OpenSession())
        using (var trans = session.BeginTransaction())
        {
            foreach (var entity in entities)
                session.Delete(entity);
            return trans.TryCommit();
        }
</code></pre>

<p>But NHibernate gives a warning:</p>

<blockquote>
  <p>Unable to determine if {Entity} with assigned identifier {Entity} is
  transient or detached; querying the database. Use explicit Save() or
  Update() in session to prevent this.</p>
</blockquote>

<p>and loads the entity from database before deletion of it.</p>

<p>We cannot follow recommendation from the warning and use <code>Save()</code> or <code>Update()</code> to delete entity.</p>

<p><strong>How should we rewrite our code to avoid excessive querying of database on deletion?</strong></p>

## Answers
### Answer ID: 46642571
<p>I think this is because the NH session that you're using to delete the entities doesn't know about/isn't tracking them.</p>

<p>For deletion, there's an overload of the <code>Delete()</code> <a href="http://nhibernate.info/doc/nh/en/index.html#manipulatingdata-deleting" rel="nofollow noreferrer">method</a> that takes an HQL query. This might be a viable, and arguably more efficient, way to do what you want?</p>

<p>Something like:</p>

<pre><code>using (var session = SessionFactory.OpenSession())
using (var trans = session.BeginTransaction())
{
    session.Delete($"FROM EntityTable WHERE Id IN ({entities.Select(e =&gt; e.Id})");

    return trans.TryCommit();
 }
</code></pre>


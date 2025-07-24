# Can&#39;t get hibernate to delete children instances via cascade, that were removed from a one-to-many relation
[Link to question](https://stackoverflow.com/questions/13067698/cant-get-hibernate-to-delete-children-instances-via-cascade-that-were-removed)
**Creation Date:** 1351164912
**Score:** 0
**Tags:** java, hibernate, one-to-many, cascade, all-delete-orphan
## Question Body
<p>slight problem here:</p>

<p>I have two entity classes, let's say</p>

<pre><code>class Parent {
    Set&lt;Child&gt; children;
}
class Child {
    SomethingElse reference;
}
</code></pre>

<p>now the mapping is essentially:</p>

<pre><code>&lt;class name="Parent" lazy="false"&gt;
    &lt;set name="children" lazy="false" cascade="all-delete-orphan"&gt;
        &lt;key column="parent_id"/&gt;
        &lt;one-to-many class="Child"/&gt;
    &lt;/set&gt;
&lt;/class&gt;
</code></pre>

<p>(i omitted the id mappings and fields here, i use regular generated ids)</p>

<p>i essentially need to keep a clean database as in when i remove elements from a parent's list and then commit the parent, the according removed child database entries need to be deleted. The Child instances reference other entities that i need to be able to delete later, so if the child instance remains in the database i cannot delete those referenced objects.</p>

<p>What i have found out so far: any of the things i try below should work if i were to keep hibernate's PersistentCollection wrapper in place. The issue is, my database objects come through a few layers of frameworks, which include a UI framework, that uses bean property abstractions to invoke setters, and a network communication layer that clones and serializes the objects back and forth. Both of these layers internally replace the collection instances and thus remove these PersistentCollection wrappers. Rewriting these to not do so is not an option.</p>

<p>That said, there's 8 things i tried that did not work:</p>

<p>1) configure the relation as cascade="all", use session.update(parent).</p>

<p>2) configure the relation as cascade="all-delete-orphan", use session.update(parent).</p>

<p>3) configure the relation as cascade="all" and use session.merge(parent)</p>

<p>All of these result in hibernate executing a "UPDATE CHILD SET parent.id = null WHERE parent.id = ...". This succeeds in removing the children from the parent list when reloading the parent instance, but the child instance remains in the database and prevents me from deleting the other referenced entities.</p>

<p>4-6) using configuration 1-3 while additionally having the parent key column defined as non-null</p>

<p>This results in hibernate not doing anything. I read in another post that making the key column non-null would cause the deletion. Sounded possible since updating to null is no longer an option, but doesn't work. If i remove children from the collection, commit the change and reload the instance from the database, the children re-appear.</p>

<p>7+8) parent key nullable or non-null doesn't matter, but configure the relation as cascade=all-delete-orphans and use session.merge(parent)</p>

<p>This causes hibernate to throw an exception "A collection with cascade="all-delete-orphan" was no longer referenced by the owning entity instance", due to the removed PersistentCollection wrapper.</p>

<p>To solve my problem, the only thing that i need is hibernate to execute the query from options 1-3 as a DELETE instead of an UPDATE. I hope i am just unable to find the option to configure the mapping in a way that deletes these without the PersistentCollection wrappers, but to me currently it appears like there is no such option. Does anyone know if there is a way to configure this?</p>

<p>/edit: To clarify, example of what i want to happen:</p>

<pre><code>Parent parent = new Parent();
parent.setChildren(new HashSet&lt;Child&gt;(Arrays.asList(new Child()))));
session.insert(parent)
// this correctly results in (approximately):
// SQL&gt; INSERT INTO PARENT ...
// SQL&gt; INSERT INTO CHILD ...

parent.setChildren(new HashSet&lt;Child&gt;()); // using .clear() is not an option.
session.update(parent);
// this results in:
// SQL&gt; UPDATE CHILD set parent_id = null WHERE parent_id = ${id.of.parent}
// but i need this to result in:
// SQL&gt; DELETE FROM CHILD WHERE parent_id = ${id.of.parent}
</code></pre>

## Answers
### Answer ID: 13094893
<p>Okay i apparently fixed it now. The issue was i was not assigning an empty set, but null. Apparently, in the case of session.merge(updated), hibernate suddenly differentiates between empty collections and null collections. Using cascade="all-delete-orphan" and .merge() with empty collection instances assigned to the properties works, assigning null instead of an empty collection instance throws the mentioned exception. This is the same regardless of nullability constraints on the key column.</p>

<p>I don't know if that is considered intentional behavior as usually null values act the same way as empty collections. I'll see if i can find out some more about this and then maybe put up a bug report.</p>

<p>update: issue at <a href="https://hibernate.atlassian.net/browse/HHH-7726" rel="nofollow">https://hibernate.atlassian.net/browse/HHH-7726</a></p>

### Answer ID: 13085409
<p>This doesn't fully answers your question, but I hope it can help a little.<br>
First, I'd recommend you to look at <a href="http://www.mkyong.com/hibernate/inverse-true-example-and-explanation/" rel="nofollow">this explanation</a>, as well as <a href="http://www.mkyong.com/hibernate/different-between-cascade-and-inverse/" rel="nofollow">this one</a>. </p>

<p>Now, you said it yourself that child objects do not reference the parent, and that this is a one way relationship. I don't know what kind of mapping you came up with, but this:</p>

<pre><code>Parent parent = new Parent();
parent.setChildren(Collections.singleton(new Child())));
session.save(parent);
// this correctly results in:
// SQL&gt; INSERT INTO PARENT ...
// SQL&gt; INSERT INTO CHILD ...
</code></pre>

<p>is possible to work, only if:  </p>

<ul>
<li><code>cascade</code> in the set mapping is <strong>enabled</strong> (e.g. <code>cascade="all"</code>, otherwise Hibernate will complain about the unsaved transient instance of the new <code>Child</code> object)</li>
<li>the parent_id column <strong>is nullable</strong> (otherwise Hibernate will expect you to preset this field, which is only possible if you have other side of the relationship mapped)</li>
</ul>

<p>Plus, Hibernate will generate one more <code>SQL UPDATE</code> in addition to these two inserts you mentioned in the comments (what you can see is actually explained in the links I gave you). </p>

<p>Hope you get something out of this.</p>


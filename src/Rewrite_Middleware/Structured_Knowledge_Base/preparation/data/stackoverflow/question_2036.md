# JPA and Table Views. Can it be done?
[Link to question](https://stackoverflow.com/questions/16686501/jpa-and-table-views-can-it-be-done)
**Creation Date:** 1369209712
**Score:** 37
**Tags:** java, jakarta-ee, jpa, view, ejb-3.0
## Question Body
<p>We currently have a Java EE system where we are mapping to our database using JPA. It is a fairly well developed system with about 20 entities.</p>

<p>We now have been ordered to use Views for everything. Eg: if we have a table called <strong>PERMISSION</strong> then we also need a view called <strong>PERMISSION_VIEW</strong>. Basically we need to do this to every table, and our applications can only access the data by querying the view.</p>

<p>Now all our entity beans look like this :</p>

<pre><code>@Entity
@Table(name = "PERMISSION")
@NamedQueries({
        @NamedQuery(name = "Permission.findByPK", query = "SELECT p FROM Permission p WHERE p.dpNum = :dpNumber"),
        @NamedQuery(name = "Permission.deleteAll", query = "DELETE FROM Permission") })
public class Permission implements Serializable {

}
</code></pre>

<ul>
<li>Firstly, how is it possible to update tables if you are only allowed to use Views. Can Materialised Views work for this?</li>
<li>Secondly, how much rewriting is going to be needed, if we can only use Views? Eg. For each entiry we will need to write <strong>@Table(name = "PERMISSION_VIEW")</strong>, to describe the entity, BUT, when doing an update it needs to do that to the PERMISSION table. How on earth do you consolidate this in an entity bean?</li>
</ul>

## Answers
### Answer ID: 16693434
<p>For more info on JPA and database views see, <a href="http://en.wikibooks.org/wiki/Java_Persistence/Advanced_Topics#Views" rel="noreferrer">http://en.wikibooks.org/wiki/Java_Persistence/Advanced_Topics#Views</a></p>

<blockquote>
  <p>In JPA you can map to a <code>VIEW</code> the same as a table, using the @Table annotation. You can then map each column in the view to your object's attributes. Views are normally read-only, so object's mapping to views are normally also read-only. In most databases views can also be updatable depending on how complex to query is that they encapsulate. Even for complex queries database triggers can normally be used to update into the view.</p>
</blockquote>

### Answer ID: 16686758
<p>Most modern RDBMSs support insertable and updatable views. 
If your RDBMS supports it, then you shouldn't have any problem. A view that is identical to a table should be updatable in any RDBMS that supports such views. So you only need to change your mapping and replace the table names with the view names.</p>


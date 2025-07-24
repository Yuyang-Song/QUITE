# Exception when retrieving items modeled by inheritance classes from MongoDB using Datanucleus
[Link to question](https://stackoverflow.com/questions/49741053/exception-when-retrieving-items-modeled-by-inheritance-classes-from-mongodb-usin)
**Creation Date:** 1523305069
**Score:** 1
**Tags:** java, mongodb, datanucleus
## Question Body
<p>me and my team are working on an upgrade of our company's system which as getting kind of forgotten and was running old versions of everything it uses; so developing newer features was becoming a pain with newer and unsupported technologies.</p>
<p>So far we have managed to produce an almost fully working version of the system; but we got stuck at a feature which involves Datanucleus-JDO, MongoDB and inheritance.</p>
<p>We have some models which are tremendously similar (from the code's perspective). In the current in-production version, to apply a change to it usually involves to rewrite the same piece of code in all classes, so we thought that inheritance would make the job easier and better. So we have two interfaces at the top hierarchy level (which as far we know, Datanuclues nor MongoDB doesn't care about them at all); which go like this:</p>
<pre><code>public interface Entity extends Serializable {

    String getDate();
    double getQty();
    void setQty(double qty);
    void setDate(String date);
    void setKey(Key key);
    
}
</code></pre>
<p>And</p>
<pre><code>public interface HourEntity extends Entity {

    String getHour();
    
}
</code></pre>
<p>We use application defined keys, we use this unique class to build different kind of keys. We only want the toString representation of this class to store and retrieve data in Mongo.</p>
<pre><code>public final class Key implements Serializable {
    static final long serialVersionUID = -448150158203091507L;
    public final String targetClassName;
    public final String id;
    public final String toString;
    public final int hashCode;

    public Key() {
        targetClassName = null;
        id = null;
        toString = null;
        hashCode = -1;
    }

    public Key(String str) {
        String[] parts = str.split(&quot;\\(&quot;);
        parts[1] = parts[1].replaceAll(&quot;\\)&quot;, &quot; &quot;);
        parts[1] = parts[1].replace(&quot;\&quot;&quot;, &quot; &quot;);
        parts[1] = parts[1].trim();
        this.targetClassName = parts[0];
        this.id = parts[1];
        toString = this.toString();
        hashCode = this.hashCode();
    }

    public Key(String classCollectionName, String id) {
        if (StringUtils.isEmpty(classCollectionName)) {
            throw new IllegalArgumentException(&quot;No collection/class name specified.&quot;);
        }
        if (id == null) {
            throw new IllegalArgumentException(&quot;ID cannot be null&quot;);
        }
        targetClassName = classCollectionName;
        this.id = id;
        toString = this.toString();
        hashCode = this.hashCode();
    }

    public String getTargetClassName() {
        return targetClassName;
    }

    public int hashCode() {
        if(hashCode != -1) return hashCode; 
        int prime = 31;
        int result = 1;
        result = prime * result + (id != null ? id.hashCode() : 0);
        result = prime * result + (targetClassName != null ? targetClassName.hashCode() : 0);
        return result;
    }

    public boolean equals(Object object) {
    if (object instanceof Key) {
        Key key = (Key) object;
        if (this == key)
            return true;
        return targetClassName.equals(key.targetClassName) &amp;&amp; Objects.equals(id, key.id);
    } else {
        return false;
    }
}

    public String toString() {
        if(toString != null) return toString;
        StringBuilder buffer = new StringBuilder();
        buffer.append(targetClassName);
         buffer.append(&quot;(&quot;);
        if (id != null) {
            buffer.append((new StringBuilder()).append(&quot;\&quot;&quot;).append(id)
                    .append(&quot;\&quot;&quot;).toString());
        } else {
            buffer.append(&quot;no-id-yet&quot;);
        }
        buffer.append(&quot;)&quot;);
        return buffer.toString();
    }

}
</code></pre>
<p>This application defined identity is working fine on all other models which does not involve inheritance.</p>
<p>This is one of the actual models that we intend to store in our datastore:</p>
<pre><code>@PersistenceCapable(detachable=&quot;true&quot;)
@Inheritance(strategy=InheritanceStrategy.COMPLETE_TABLE)
public class Ticket implements Entity {

    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.UNSPECIFIED, column=&quot;_id&quot;)
    protected Key key;

    protected String date;
    protected int qty;
    
    public Ticket() {
        this.qty = 0;
    }
    
    public Key getKey() {
        return key;
    }

    @Override
    public void setKey(Key key) {
        this.key = key;
    }

    public double getQty() {
        return qty;
    }

    public void setQty(double qty) {
        this.qty = (int) qty;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((key == null) ? 0 : key.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Ticket other = (Ticket) obj;
        if (key == null) {
            if (other.key != null)
                return false;
        } else if (!key.equals(other.key))
            return false;
        return true;
    }

    @Override
    public String toString() {
        return &quot;Ticket [key=&quot; + key + &quot;, date=&quot; + date + &quot;, qty=&quot;
                + qty + &quot;]&quot;;
    }

}
</code></pre>
<p>And this is its subclass (all models which involve this problem just involve one super class and only one children per every super class):</p>
<pre><code>@PersistenceCapable(detachable=&quot;true&quot;)
@Inheritance(strategy=InheritanceStrategy.COMPLETE_TABLE)
public class HourTicket extends Ticket implements HourEntity {

    private String hour;
    
    public HourTicket() {
        super();
    }
    
    public Key getKey() {
        return key;
    }

    @Override
    public void setKey(Key key) {
        this.key = key;
    }

    public String getHour() {
        return hour;
    }

    public void setHour(String hour) {
        this.hour = hour;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((key == null) ? 0 : key.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        HourTicket other = (HourTicket) obj;
        if (key == null) {
            if (other.key != null)
                return false;
        } else if (!key.equals(other.key))
            return false;
        return true;
    }

    @Override
    public String toString() {
        return &quot;HourTicket [key=&quot; + key + &quot;, date=&quot; + date
                + &quot;, hour=&quot; + hour + &quot;, qty=&quot; + qty + &quot;]&quot;;
    }

}
</code></pre>
<p>Finally, the persisntance.xml is like this</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; ?&gt;
&lt;persistence xmlns=&quot;http://java.sun.com/xml/ns/persistence&quot;
    xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;
    xsi:schemaLocation=&quot;http://java.sun.com/xml/ns/persistence
        http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd&quot; version=&quot;2.0&quot;&gt;

    &lt;!-- JOSAdmin &quot;unit&quot; --&gt;
    &lt;persistence-unit name=&quot;ourdatastore&quot;&gt;
        &lt;class&gt;mx.ourdomain.Ticket&lt;/class&gt;
        &lt;class&gt;mx.ourdomain.HourTicket&lt;/class&gt;
        &lt;exclude-unlisted-classes/&gt;

    &lt;/persistence-unit&gt;
&lt;/persistence&gt;
</code></pre>
<p>And package-mongo.orm</p>
<pre><code>&lt;?xml version=&quot;1.0&quot;?&gt;
&lt;!DOCTYPE orm SYSTEM &quot;file:/javax/jdo/orm.dtd&quot;&gt;
&lt;orm&gt;
    &lt;package name=&quot;mx.ourdomain&quot; &gt;
        &lt;class name=&quot;Ticket&quot; table=&quot;Ticket&quot;&gt;
            &lt;field name=&quot;key&quot; primary-key=&quot;true&quot; &gt;
                &lt;column name=&quot;_id&quot; length=&quot;100&quot; /&gt;
            &lt;/field &gt;
        &lt;/class&gt;

        &lt;class name=&quot;HourTicket&quot; table=&quot;HourTicket&quot;&gt;
            &lt;primary-key &gt;
                &lt;column name=&quot;_id&quot; target=&quot;_id&quot; /&gt;
            &lt;/primary-key&gt;
        &lt;/class&gt;
     &lt;/package&gt;
&lt;/orm&gt;
</code></pre>
<p>So, the problems comes when trying to perform any read or write operations using either the super class or the subclass. This has happened with the same exact results in several (all possible as far we know) scenarios, but the test scenario we are study begins with this call:</p>
<pre><code>Ticket ticket = persistenceManager.getObjectById(Ticket.class, key);
</code></pre>
<p>The key is generated with an standard procedure which is used by other models which do store and read successfully; and of course, it is of the previously shown key class.</p>
<p>We have gone as far as debugging the datanucleus tasks beyond this. And we have found that as expected:</p>
<ol>
<li>The metadata shows that its the super class of others.</li>
<li>Its using application managed keys.</li>
</ol>
<p>But when trying to get the class name to determine which is the correct Mongo collection to query, datanucleus-mongodb tries to query both classes (Ticket and HourTicket); but then it handles to the mongo driver the <strong>key</strong> object <em>perse</em>, and then a <strong>CodecConfigurationException</strong> is thrown since mongo does not know how to work with the key class (when building the query, datanucleus-mongo creates a BasicDBObject which has the structure {_id:key}, which cannot be constructed without the codec because of the <strong>key</strong> entry. This happens at the MongoDBUtils class in the datanucleus-mongodb project v5.1.0; class MongoDBUtils, method getClassNameForIdentity(Object, AbstractClassMetaData, ExecutionContext, ClassLoaderResolver)).</p>
<p>So, we suppose that we have some configuration missing to tell datanucleus that it should use the toString() form of the key; since the Monogo driver handles String just fine (datanuclues docs actually states that when using custom classes as datastore keys it will use the toString() form of the key; so I'm unsure if this could be a bug).</p>
<p>We have tried to use a KeyTraslator plugin and making the key class a DatastoreId and wrapping in a StringId with no success: the same exception is fired, except when wrapping the Key class in a StringId: the mongo lecture is sucessful but then when trying to build the model object, an ClassCastException is thrown since String cannot be casted into Key, and refactoring the code to use a String key will badly break data already in database; since it has a special format the key class can read and produce.</p>
<p>Is there something we are missing using inheritance with datanucleus JDO w/mongoDB?</p>

## Answers
### Answer ID: 49789676
<p>I was not putting much attention to the settings around the objectIdClass metadata; since from the docs I got that they were intended for composed keys only. It results that if you define an objectId class with only one attribute; then it behaves as a custom SingleFieldId; which is what we wanted.</p>

<p>I found "funny" the fact that non annotated (or non declared metadata for objectIdClass) classes will work fine and the custom key used will be threated just fine; but once you make any of them a super class, then you are obligated to add the objectIdClass metadata.</p>

<p>Beside annotating the Ticket class (and all other super classes) with objectIdClass, we:</p>

<ul>
<li>Removed the toString and hashCode attributes from the Key class (@NotPersistent and transient keyword won't make Datanucleus ignore them; so I guess there is no performance improvement for toString() and hashCode() methods on custom keys right now).</li>
<li>Removed all the <em>final</em> qualifiers from the Key class attributes (Datanucleus docs don't say that custom key fields cannot be final; but guess what, they can't be)</li>
<li>Changed the <em>Key key</em> class member from all superclass for <em>String id</em> (as in the key class). We also had to change the implementation of the getters and setters for the id member; using the required string constructor of the key class to build the key when calling the method. Of course, the "key" field declared in the package-mongo.orm was changed to <em>id</em> in the super classes.</li>
</ul>

<p>And that was it! with those little changes our system is working great; no other changed were required on other persistable classes nor DAOs.</p>


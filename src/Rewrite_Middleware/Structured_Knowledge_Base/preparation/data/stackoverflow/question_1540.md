# How to avoid multiple single selects and create a multiselect with NHibernate
[Link to question](https://stackoverflow.com/questions/9017692/how-to-avoid-multiple-single-selects-and-create-a-multiselect-with-nhibernate)
**Creation Date:** 1327578408
**Score:** 1
**Tags:** nhibernate, subquery
## Question Body
<p>We have a complex business model and is using NHibernate to create and maintain the database. This results in poor performance from time to time when a fairly straight forward query results in a large object graph. </p>

<p>Usually we are able to rewrite the query and gain a good performance boost while at the same time getting to know the business model better. However now we have stumbled over a case where we are unable to get a better result that what we currently have which, frankly, is really really poor.</p>

<p>We have the following classes with associated mappings. The classes have been stripped down to minimum just let me know if you need more information.</p>

<pre><code>public class GraphPoint
{
   public DateTime datum;
   public IDictionary&lt;Avtal, Value&gt; values;
   public Calculation calculation;
   public bool isCalculated;
   public Int64 graphPointId;

   ...
}

public class Value
{
   public int numbers;
   public int points;
}

public class Avtal
{
   public string name;
   public Int64 avtalId

   ...
}

&lt;class name="GraphPoint" lazy="false"&gt;
   &lt;id name="GraphPointId" column="GraphPointId" type="Int64"&gt;
     &lt;generator class="Business.Data.IncrementGenerator, Business"/&gt;
   &lt;/id&gt;

   &lt;property name="Datum" not-null="true" unique-key="UIX1_GraphPoint" /&gt;
   &lt;map name="Values" table="GraphPointValue" cascade="all-delete-orphan"&gt;
     &lt;key column="GraphPointId" foreign-key="FK_GraphPoint_GraphPointValue" /&gt;
     &lt;map-key-many-to-many class="Avtal" column="AvtalId" 
                           foreign-key="FK_GraphPoint_GraphPointValue_Avtal"  /&gt;
     &lt;composite-element class="GraphPoint+Value"&gt;
       &lt;property name="Numbers" not-null="true" /&gt;
       &lt;property name="Points" not-null="true" precision="26" scale="15" /&gt;
     &lt;/composite-element&gt;
   &lt;/map&gt;
   &lt;property name="IsCalculated" not-null="true" /&gt;
   &lt;many-to-one name="Calculation" column="CalculationId" 
                foreign-key="FK_Calculation_GraphPoint" /&gt;
&lt;/class&gt;
</code></pre>

<p>So in this scenario we the following criterias:
* Return all GraphPointValues between two dates
* Aggregate these based on the Avtal object</p>

<p>We currently have been trying with this:</p>

<pre><code>from punkt in (from punkt in Session.Query&lt;GraphPoint&gt;()
               where punkt.IsCalculated &amp;&amp; 
                     punkt.Datum &gt;= lowDate &amp;&amp; 
                     punkt.Datum &lt;= highDate
               select punkt).ToArray()
let values = from value in punkt.Values
             where forAvtal.Contains(value.Key.AvtalId)
             select value.Value
select new GraphPointValuePresentationObject
{
   Datum = punkt.Datum,
   Numbers = värden.Sum(v =&gt; v.Antal),
   Points = värden.Sum(v =&gt; v.Poäng),
   IsCalculated = punkt.IsCalculated
}
</code></pre>

<p>forAvtal is a list containing id's for these objects that shoudl be met. </p>

<p>When we run this we get one sql-statement against the database which fetches all the GraphPoints that lay between the dates and then we get one sql-statment for each and everyone of the points that the first sql-statement returns.</p>

<p>I want to rewrite this so that we only need a couple of sql-statements and not several hundreds as it is today. Can anyone give me a pointer in the right direction, I've tried Critierias and DetachedQueries but can't get it to work as I want to.</p>

## Answers
### Answer ID: 9017985
<p>inserting <code>.Fetch(x =&gt; x.Values)</code> befor <code>.ToArray()</code> should do the trick. It will generate a join to fetch all related values along with the Graphpoints</p>


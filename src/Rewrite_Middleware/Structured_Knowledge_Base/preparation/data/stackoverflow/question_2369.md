# Convert LINQ expressions between model and DTO for use in repositories and DAO
[Link to question](https://stackoverflow.com/questions/31528435/convert-linq-expressions-between-model-and-dto-for-use-in-repositories-and-dao)
**Creation Date:** 1437438161
**Score:** 0
**Tags:** c#, linq, linq-expressions
## Question Body
<p>I'm trying to abstract out the data access layer and repository/model layers in my application. </p>

<p>So far, I have my architecture such that I have my repositories returning and accepting my model classes. </p>

<p>Example: Vehicle model is managed by the VehicleRepository repo. </p>

<p>Now, to abstract away database layer specific types from the actual models, I have implemented DAO objects, with implement a DTO. </p>

<p>Example: VehicleDao will only accept and return VehicleDto objects (which has slightly different properties to Vehicle model to account for the database specific types). It is the job of the VehicleRepository to convert the Vehicle model to the VehicleDto and back again. </p>

<p>The question I have is for when I want to send through a LINQ expression. My repository will only accept an expression based on the Vehicle model class:</p>

<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IList&lt;Vehicle&gt;&gt; GetAll(Expression&lt;Func&lt;Vehicle, bool&gt;&gt; condition)
{
    // Return the results
    // _dao is type VehicleDao
    return await _dao.Find&lt;T&gt;(condition);
}
</code></pre>

<p>My DAO object has a similar method, but it accepts and returns the VehicleDto object, and works directly on the database collection. </p>

<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IList&lt;VehicleDto&gt;&gt; GetAll(Expression&lt;Func&lt;VehicleDto, bool&gt;&gt; condition)
{
    // Return the results
    // _collection is my database managed collection (MongoDB in this case)
    return await _collection.Find&lt;T&gt;(condition).ToListAsync();
}
</code></pre>

<p>Obviously, I'm getting a build error because the LINQ Expressions are not compatible between the Vehicle and VehicleDto objects... </p>

<p>So, I'm wondering what the best way to tackle this problem is? Should I move the conversion of Model > DTO into the DAO object? Should I not use Expressions for querying data from the MongoDB collection, and use concrete functions such as GetByName, GetByMake etc, instead of having the ability to specify the query in the method. </p>

<p>My ultimate goal is to have the model/repo layer completely isolated from the DAO layer. 1) Testing purposes obviously, but 2) if I need to move from MongoDB to something else down the track, I only need to rewrite/test the data access layer. </p>

<p>Any help with this problem would be awesome!</p>

## Answers
### Answer ID: 31528465
<p>If you are trying to abstract layers then you must use abstractions.</p>

<p>Base your functions on interfaces instead of concrete types would be first thing that comes to my mind:</p>

<pre><code>public interface IVehicleDomain  : IDomain   //you could extend a base interface if you wanted.
{
   public string Field1 { get; set; }
}
</code></pre>

<p>Then implement this interface amongst your domain and dto classes.  Finally use the interface on both architecure layers, the interfaces should exist in a common assembly that both the dto and domain classes can access.</p>

<pre><code>public async Task&lt;IList&lt;Vehicle&gt;&gt; GetAll(Expression&lt;Func&lt;Vehicle, bool&gt;&gt;   condition)
{
   // Return the results
   // _dao is type VehicleDao
   return await _dao.Find&lt;T&gt;(condition);
}
public async Task&lt;IList&lt;IVehicle&gt;&gt; GetAll(Expression&lt;Func&lt;IVehicle, bool&gt;&gt; condition)
{
   // Return the results
   // _collection is my database managed collection (MongoDB in this case)
   return await _collection.Find&lt;T&gt;(condition).ToListAsync();
}
</code></pre>


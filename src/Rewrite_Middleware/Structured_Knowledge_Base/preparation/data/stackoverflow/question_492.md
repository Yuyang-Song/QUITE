# Laravel database query distance between two coordinates
[Link to question](https://stackoverflow.com/questions/28307257/laravel-database-query-distance-between-two-coordinates)
**Creation Date:** 1422992113
**Score:** 1
**Tags:** mysql, laravel, eloquent
## Question Body
<p>So i have this query for my MySQL database,</p>

<pre><code>$sql = "SELECT  samples.* ,
                CONCAT(costumers.name, ' ', costumers.lastName) AS name, costumers.telefon AS telefon
FROM samples
LEFT OUTER JOIN costumers
ON samples.id = costumers.costumer_id
WHERE (sqrt(pow( :x_center - `Y` , 2) + pow( :y_center - `X`, 2 ))) &lt; :radius";
</code></pre>

<p>This is working real nice as it is. But as i'm moving over to Laravel, id like to rewrite this query.</p>

<p>So what I'm querying is my X coordinate and my Y coordinate for soil samples. (In Sweden we have a coordinate system called RT90 that uses X and Y instead of Lat/Long). And i also input the search radius. 
I want to find every sample there is that is inside a circle with that radius.</p>

<p>And i've been trying to translate my previous query into something useful in Laravel for the last hour. But I'm having some trouble. </p>

<p>Does anyone have suggestions for a nice query using Eloquent or DB::raw ? 
When that query then is done, the results are going to be passed to a json_encode. For further handling in JavaScript.
That worked fine with my previous query, and it would be good if you guys had that in mind as well.</p>

<p>My Laravel models are, Sample and Costumer.</p>

<p>Thanks, Simon</p>

## Answers
### Answer ID: 28308473
<p>The quickest solution would be to just run the query as you have it:</p>

<pre><code>$results = DB::select($sql, array(
    'x_center' =&gt; 0,
    'y_center' =&gt; 0,
    'radius' =&gt; 0
);
</code></pre>

<p>After this, <code>$results</code> would be an array of stdClass objects with the properties that you selected.</p>

<p>If you are looking for a more Laravel-ish solution, you could use the Eloquent models to build a query that would give you similar results. Assuming your Sample/Costumer relationships are setup correctly, you could do:</p>

<pre><code>$results = Sample::with('costumers')
    -&gt;whereRaw("(sqrt(pow( :x_center - `Y` , 2) + pow( :y_center - `X`, 2 ))) &lt; :radius", array(
        'x_center' =&gt; 0,
        'y_center' =&gt; 0,
        'radius' =&gt; 0,
    ))
    -&gt;get();
</code></pre>

<p>In this case, <code>$results</code> will be a Collection of Sample objects, and each Sample object will have its related Costumers eager loaded onto it. From here, you would need to use your objects to build the final result set, and there are a lot of possibilities on how to do that.</p>

<p>Some information on converting models to array/json is <a href="http://laravel.com/docs/4.2/eloquent#converting-to-arrays-or-json" rel="nofollow">here</a>, which goes over the toArray()/toJson() methods, as well as mentions accessors and the appends/visible/hidden attributes. For example, you may want to consider adding a full_name accessor (<a href="http://laravel.com/docs/4.2/eloquent#accessors-and-mutators" rel="nofollow">documenation here</a>) to the Costumer model, and then add that to the appends attribute to make sure it is included in the array/json.</p>


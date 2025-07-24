# Legacy Database Schema - Key/Value Tables
[Link to question](https://stackoverflow.com/questions/12371838/legacy-database-schema-key-value-tables)
**Creation Date:** 1347373107
**Score:** 0
**Tags:** ruby-on-rails, activerecord
## Question Body
<p>I've got a legacy database schema which consists of objects similar to the following:</p>

<pre><code>table=car
oid, something, something_else, ...
has many properties -&gt; car_properties

table=car_properties
oid, car_id, keyname, value, ...
belongs to car
</code></pre>

<p>The Car object is actually (logically) a combination of the columns in the "car" table, and multiple rows in the "car_properties" table.</p>

<p>I'm looking at doing a parallel rewrite of the application which uses this schema, so I need some way to map this table schema back to a nice ActiveRecord object.  Ideally I'd like each of the properties in the _properties table to be accessible as a method on the "Car" class, so I can change the underlying table later without breaking things.</p>

<p>I can statically define the methods in the Car class, but I want to ensure that the ActiveRecord magic works, so things like .save work, and I can change the underlying schema at a later date (realising this will probably be an outage to the application).</p>

<p>How would I go about doing this in ActiveRecord?</p>

<p>To Clarify:</p>

<p>Basically, I want the following to work</p>

<pre><code>@car = Car.first
@car.something = something
@car.someprop = something
</code></pre>

<p>However in the above, <code>@code.someprop</code> is actually <code>@car.properties.where( "keyname = ?", "someprop" ).value</code></p>

<p>Obviously I don't want to be doing a SQL Query every time for this though, so I'm looking for a nice way to do this.</p>

## Answers
### Answer ID: 12372546
<p>Unless I'm underthinking it, it should be something as simple as:</p>

<pre><code>class CarProperty &lt; ActiveRecord::Base
   set_primary_key :oid

   belongs_to :car
end

class Car &lt; ActiveRecord::Base
   set_table_name :car
   set_primary_key :oid

   has_many :car_properties

   accepts_nested_attributes_for :car_properties
end
</code></pre>


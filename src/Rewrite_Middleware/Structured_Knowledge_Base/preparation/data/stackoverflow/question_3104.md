# Adding ST_Transform in a PL/pgSQL function
[Link to question](https://stackoverflow.com/questions/66777343/adding-st-transform-in-a-pl-pgsql-function)
**Creation Date:** 1616574790
**Score:** 3
**Tags:** sql, postgresql, postgis, plpgsql, coordinate-transformation
## Question Body
<p>I use a function from <a href="http://blog.cleverelephant.ca/2019/03/geojson.html" rel="nofollow noreferrer">Paul Ramsey´s blog</a> to query geoJSON data from a postGIS database.
I adjusted the function a little, which worked so far:</p>
<pre><code>CREATE OR REPLACE FUNCTION rowjsonb_to_geojson(
  rowjsonb JSONB, 
  geom_column TEXT DEFAULT 'geom')
RETURNS json AS 
$$
DECLARE 
 json_props jsonb;
 json_geom jsonb;
 json_type jsonb;
BEGIN
 IF NOT rowjsonb ? geom_column THEN
   RAISE EXCEPTION 'geometry column ''%'' is missing', geom_column;
 END IF;
 json_geom := ST_AsGeoJSON((rowjsonb -&gt;&gt; geom_column)::geometry)::jsonb;
 json_geom := jsonb_build_object('geometry', json_geom);
 json_props := jsonb_build_object('properties', rowjsonb - geom_column);
 json_type := jsonb_build_object('type', 'Feature');
 return (json_type || json_geom || json_props)::text;
END; 
$$ 
LANGUAGE 'plpgsql' IMMUTABLE STRICT;
</code></pre>
<p>Now I´m on the point, where I want to integrate a ST_Transform(geom_column, 4326) to give me back lat/lng data for a leaflet application:</p>
<ul>
<li>I tried adjusting the line</li>
</ul>
<pre><code>json_geom := ST_AsGeoJSON(((rowjsonb -&gt;&gt; ST_Transform(geom_column, 4326))::geometry)::jsonb;
</code></pre>
<p>which doesn´t work, because ST_Transform needs to be performed on a geometry and not a text, or json;</p>
<ul>
<li>My other idea, to declare a new variable geom_c and perform the transformation as first in the block</li>
</ul>
<pre><code>geom_c := ST_Transform(geom_column, 4326)::geometry;
</code></pre>
<p>which also doesn´t work either.</p>
<p>I also tried the following:</p>
<p><code>json_geom := ST_AsGeoJSON(rowjsonb -&gt;&gt; ST_Transform((geom_column-&gt;&gt;'geom')::geometry, 4326))::jsonb;</code> which gives back the error: operator does not exist: text -&gt;&gt; unknown</p>
<p><code>json_geom := ST_AsGeoJSON(rowjsonb -&gt;&gt; ST_Transform(ST_GeomFromGeoJSON(geom_column), 4326))::jsonb;</code> which gives the error unexpected character (at offset 0)</p>
<p>Here are a two sample points from the standorts table, that I´m querying:</p>
<pre><code>&quot;id&quot;: &quot;0&quot;, &quot;geom&quot;: &quot;0101000020787F0000000000001DDF2541000000800B285441&quot;
&quot;id&quot;: &quot;1&quot;, &quot;geom&quot;: &quot;0101000020787F000000000000EFE42541000000A074275441&quot;
     
</code></pre>
<p>The query I use is:</p>
<pre><code>SELECT 'FeatureCollection' AS type, 
   'standorts' AS name, 
   json_build_object('type', 'name', 'properties', 
   json_build_object('name', 'urn:ogc:def:crs:OGC:1.3:CRS84')) AS CRS,
   array_to_json(array_agg(rowjsonb_to_geojson(to_jsonb(standort.*)))) AS FEATURES FROM standort&quot;;

</code></pre>
<p>Can I even integrate the ST_Transform function into the block segment? Or do I need to rewrite the block logically?</p>

## Answers
### Answer ID: 66777621
<p>Welcome to SO. The parameter must be a geometry, so you need to cast the string in the parameter itself, not the result of function, e.g.</p>
<pre><code>json_geom := ST_AsGeoJSON(((rowjsonb -&gt;&gt; ST_Transform(geom_column::geometry, 4326)))::jsonb;
</code></pre>
<p>Example:</p>
<pre><code>SELECT 
  ST_AsGeoJSON(
    ST_Transform('SRID=32636;POINT(1 2)'::GEOMETRY,4326));

                       st_asgeojson                        
-----------------------------------------------------------
 {&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[28.511265075,0.000018039]}
</code></pre>
<p>That being said, your function could be modified like that:</p>
<pre><code>CREATE OR REPLACE FUNCTION rowjsonb_to_geojson(
  rowjsonb JSONB, 
  geom_column TEXT DEFAULT 'geom')
RETURNS json AS 
$$
DECLARE 
 json_props jsonb;
 json_geom jsonb;
 json_type jsonb;
BEGIN
 IF NOT rowjsonb ? geom_column THEN
   RAISE EXCEPTION 'geometry column ''%'' is missing', geom_column;
 END IF;
 json_geom := ST_AsGeoJSON(ST_Transform((rowjsonb -&gt;&gt; geom_column)::geometry,4326))::jsonb;
 json_geom := jsonb_build_object('geometry', json_geom);
 json_props := jsonb_build_object('properties', rowjsonb - geom_column);
 json_type := jsonb_build_object('type', 'Feature');
 return (json_type || json_geom || json_props)::text;
END; 
$$ 
LANGUAGE 'plpgsql' IMMUTABLE STRICT;
</code></pre>
<p>Test with your sample data</p>
<pre><code>WITH standort (id,geom) AS (
  VALUES
    (0,'0101000020787F0000000000001DDF2541000000800B285441'),
    (1,'0101000020787F000000000000EFE42541000000A074275441')
) 
SELECT row_to_json(q) AS my_collection FROM (
SELECT 'FeatureCollection' AS type, 
   'standorts' AS name, 
   json_build_object('type', 'name', 'properties', 
   json_build_object('name', 'urn:ogc:def:crs:OGC:1.3:CRS84')) AS CRS,
   array_to_json(array_agg(rowjsonb_to_geojson(to_jsonb(standort.*)))) AS features 
FROM standort) q;

                      my_collection
-----------------------------------------------

{
  &quot;type&quot;: &quot;FeatureCollection&quot;,
  &quot;name&quot;: &quot;standorts&quot;,
  &quot;crs&quot;: {
    &quot;type&quot;: &quot;name&quot;,
    &quot;properties&quot;: {
      &quot;name&quot;: &quot;urn:ogc:def:crs:OGC:1.3:CRS84&quot;
    }
  },
  &quot;features&quot;: [
    {
      &quot;type&quot;: &quot;Feature&quot;,
      &quot;geometry&quot;: {
        &quot;type&quot;: &quot;Point&quot;,
        &quot;coordinates&quot;: [
          11.886684554,
          47.672030583
        ]
      },
      &quot;properties&quot;: {
        &quot;id&quot;: 0
      }
    },
    {
      &quot;type&quot;: &quot;Feature&quot;,
      &quot;geometry&quot;: {
        &quot;type&quot;: &quot;Point&quot;,
        &quot;coordinates&quot;: [
          11.896296029,
          47.666357408
        ]
      },
      &quot;properties&quot;: {
        &quot;id&quot;: 1
      }
    }
  ]
}
</code></pre>
<p><strong>Note</strong> to the usage of ST_AsGeoJSON: <code>ST_Transforms</code> expects a geometry and <code>ST_AsGeoJSON</code> returns a text containing a representation of the geometry, not the geometry itself. So you first need to transform the geometry and then you can serialise it as GeoJSON.</p>
<p>Demo: <a href="https://dbfiddle.uk/?rdbms=postgres_12&amp;fiddle=6fdf76b637da541b66d69ae7fc1406c4" rel="nofollow noreferrer"><code>db&lt;&gt;fiddle</code></a></p>


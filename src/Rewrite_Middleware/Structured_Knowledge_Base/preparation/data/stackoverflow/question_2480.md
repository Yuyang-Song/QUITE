# How to use Not Exists in Netezza
[Link to question](https://stackoverflow.com/questions/36580907/how-to-use-not-exists-in-netezza)
**Creation Date:** 1460484399
**Score:** 1
**Tags:** sql, netezza, correlated-subquery, not-exists, subquery
## Question Body
<p>I have 3 tables in Netezza. </p>

<p>Table 1: STORES</p>

<pre><code>CREATE TABLE STORES
(
    STORE_NAME CHARACTER VARYING(10),
    STORE_TYPE CHARACTER VARYING(10)
);
</code></pre>

<p>Table 2: CITIES</p>

<pre><code>CREATE TABLE CITIES
(
    CITY CHARACTER VARYING(10)
);
</code></pre>

<p>Table 3: CITIES_STORES</p>

<pre><code>CREATE TABLE CITIES_STORES
(
    STORE_TYPE CHARACTER VARYING(10),
    CITY CHARACTER VARYING(10)
);
</code></pre>

<p>I need to find the store_type which is present in all the cities. So I was trying to do this the following way. If for a particular,
<code>store_type</code> (present in <code>Stores</code> table) , I cannot find any state in which the <code>store_type</code> is not present, then that <code>store_type</code> is my answer.</p>

<p>I wrote the following query and run in Netezza:</p>

<pre><code>select distinct
    store_type
from
    stores
where
    not exists (
                    select *
                    from
                        cities
                    where
                        not exists (
                                        select *
                                        from
                                            cities_stores
                                        where
                                            cities_stores.city = cities.city
                                            and cities_stores.store_type = stores.store_type
                                    )
               );
</code></pre>

<p>but it is giving an error as </p>

<blockquote>
  <p>ERROR:  (2) This form of correlated query is not supported - consider
  rewriting</p>
</blockquote>

<p>Please tell me where I went wrong. Is this any problem with Netezza database?</p>

## Answers
### Answer ID: 36649922
<p>In general, correlated subqueries in Netezza are a bad idea. There are a lot of good resources that indicate this. In fact, Netezza attempts to determine the <a href="https://www.ibm.com/support/knowledgecenter/SSULQD_7.0.3/com.ibm.nz.dbu.doc/c_dbuser_correlated_subqueries_ntz_sql.html" rel="nofollow">equivalent join syntax for you</a> instead of performing the statement as written. When it can't, you get that error.</p>

<p>To get around it, just write the equivalent join the first time.</p>

<pre><code>select distinct
  store_type
from
  stores str
  left outer join cities_stores cts using (store_type)
  left outer join cities cit using (city)
where
  city is null
</code></pre>

<p>Note: you said that you wanted to find the <code>store_type</code> that is present in all the cities, but your statement returns <code>store_type</code>s that are <em>not</em> present in any of the cities. I rewrote your SQL, not what you indicated in the question.</p>


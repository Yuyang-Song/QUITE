# Dynamic SQL via jOOQ for paginating joined tables with same-named columns
[Link to question](https://stackoverflow.com/questions/74904544/dynamic-sql-via-jooq-for-paginating-joined-tables-with-same-named-columns)
**Creation Date:** 1671835567
**Score:** 2
**Tags:** java, sql, postgresql, jooq, dynamicquery
## Question Body
<p>I'm following a <a href="https://blog.jooq.org/calculating-pagination-metadata-without-extra-roundtrips-in-sql/" rel="nofollow noreferrer">jOOQ blog post about paging metadata</a>, and trying to implement it generally for a project. It demonstrates how to generically take an existing <code>Select&lt;?&gt;</code> and wrap it up to contain information about the current page, and how many other pages exist:</p>
<blockquote>
<pre class="lang-java prettyprint-override"><code>public static Select&lt;?&gt; paginate(
    DSLContext ctx,
    Select&lt;?&gt; original,
    Field&lt;?&gt;[] sort,
    int limit,
    int offset ) {
    Table&lt;?&gt; u = original.asTable(&quot;u&quot;);
    Field&lt;Integer&gt; totalRows = count().over().as(&quot;total_rows&quot;);
    Field&lt;Integer&gt; row = rowNumber().over().orderBy(u.fields(sort))
        .as(&quot;row&quot;);
 
    Table&lt;?&gt; t = ctx
        .select(u.asterisk())
        .select(totalRows, row)
        .from(u)
        .orderBy(u.fields(sort))
        .limit(limit)
        .offset(offset)
        .asTable(&quot;t&quot;);
 
    Select&lt;?&gt; result = ctx
        .select(t.fields(original.getSelect().toArray(Field[]::new)))
        .select(
            count().over().as(&quot;actual_page_size&quot;),
            field(max(t.field(row)).over().eq(t.field(totalRows)))
                .as(&quot;last_page&quot;),
            t.field(totalRows),
            t.field(row),
            t.field(row).minus(inline(1)).div(limit).plus(inline(1))
                .as(&quot;current_page&quot;))
        .from(t)
        .orderBy(t.fields(sort));
 
    // System.out.println(result);
    return result;
} 
</code></pre>
<p>And here’s how you call the utility:</p>
<pre><code>java System.out.println(
    paginate(
        ctx,
        ctx.select(ACTOR.ACTOR_ID, ACTOR.FIRST_NAME, ACTOR.LAST_NAME)
           .from(ACTOR),
        new Field[] { ACTOR.ACTOR_ID },
        15,
        30
    ).fetch() ); 
</code></pre>
<p>Notice that you can plug in arbitrary SQL fragments into that utility and paginate them. Irrespective of the complexity (including joins, other window functions, grouping, recursion, and what not), jOOQ will have you covered and will now paginate things for you.</p>
</blockquote>
<p>This works nicely for simple cases, but I am finding that it fails in any case where two columns happen to have the same name across joins - normally, the <code>record.into(FooRecord.class)</code> and <code>record.into(BarRecord.class)</code> would extract those columns and make them separately available to the caller.</p>
<p>For example, given two tables, <code>foo</code> and <code>bar</code>, where both have an <code>id</code> column, and <code>bar</code> has a <code>foo_id</code> foreign key. Then, I can write:</p>
<pre class="lang-java prettyprint-override"><code>var select = ctx
   .select(FOO.fields())
   .select(BAR.fields())
   .from(BAR)
   .leftJoin(FOO).on(BAR.FOO_ID.eq(FOO.ID));

// Render the SQL
System.out.println(select);
var data = select.fetch();

// Show the full query's results, then the fields that came from FOO and BAR
System.out.println(data);
System.out.println(data.get(2).into(FOO));
System.out.println(data.get(2).into(BAR));
</code></pre>
<p>Results:</p>
<pre><code>select &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot;
from &quot;myschema&quot;.&quot;bar&quot;
  left outer join &quot;myschema&quot;.&quot;foo&quot;
    on &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot; = &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;
+----+----+------+
|  id|  id|foo_id|
+----+----+------+
|   1|   1|     1|
|   2|   2|     2|
|   2|   3|     2|
+----+----+------+

+----+
|  id|
+----+
|   2|
+----+

+----+------+
|  id|foo_id|
+----+------+
|   3|     2|
+----+------+
</code></pre>
<p>Both jOOQ and the database (Postgres in this case) are happy with this, despite having more than one column with the same name.</p>
<p>Next, I try to pass this <code>Select&lt;?&gt;</code> to the paginate() method above:</p>
<pre><code>var pagedSelect = paginate(ctx, original, new Field[] { FOO.ID }, 10, 0);

System.out.println(pagedSelect);
var pagedData = pagedSelect.fetch();//error
</code></pre>
<pre><code>select
  &quot;t&quot;.&quot;id&quot;,
  &quot;t&quot;.&quot;id&quot;,
  &quot;t&quot;.&quot;foo_id&quot;,
  count(*) over () as &quot;actual_page_size&quot;,
  (max(&quot;t&quot;.&quot;row&quot;) over () = &quot;t&quot;.&quot;total_rows&quot;) as &quot;last_page&quot;,
  &quot;t&quot;.&quot;total_rows&quot;,
  &quot;t&quot;.&quot;row&quot;,
  (((&quot;t&quot;.&quot;row&quot; - 1) / 10) + 1) as &quot;current_page&quot;
from (
  select
    &quot;u&quot;.*,
    count(*) over () as &quot;total_rows&quot;,
    row_number() over (order by &quot;u&quot;.&quot;id&quot;) as &quot;row&quot;
  from (
    select &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot;
    from &quot;myschema&quot;.&quot;bar&quot;
      left outer join &quot;myschema&quot;.&quot;foo&quot;
        on &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot; = &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;
  ) as &quot;u&quot;
  order by &quot;u&quot;.&quot;id&quot;
  offset 0 rows
  fetch next 10 rows only
) as &quot;t&quot;
order by &quot;t&quot;.&quot;id&quot;

</code></pre>
<pre><code>ERROR: column referenced &quot;id&quot; is ambiguous
</code></pre>
<p>My naive approach was to first try to modify <code>paginate(...)</code> to make the outer-most <code>SELECT</code> reference the fully qualified fields, table and all, but since we're querying from an anonymous table, that doesn't work, same error (though for a different reason, since now jOOQ is generating an alias for <code>original</code>.</p>
<p>Next I considered trying to visit <code>original</code> and create a copy of it, using <code>AS</code> to rename columns as f1, f2, f3, but I couldn't find a straightforward way to do this rewrite. Even if this had worked, it would make it hard to map them back again from the caller, which would need to then know the order of all the .select()ed fields to be able to find them again - and since the <code>original</code> might have itself been built from other dynamic SQL operations, that might not be feasible.</p>
<p>Finally I considered an approach where every column of every table was already qualified with the table name already, but beyond this being onerous, it also doesn't help at all in cases where a table could be joined twice into the same query.</p>
<p>What's the correct dynamic SQL approach with jOOQ to make it possible to wrap a query with pagination, and still map records back to their individual tables?</p>
<p>--</p>
<p><em>EDIT: Based on the comments, I've modified the query from the blog post, and while this actually emits runnable SQL, the premise of the blog post still seems faulty, and still eludes me.</em></p>
<blockquote>
<p>Irrespective of the complexity (including joins, other window functions, grouping, recursion, and what not), jOOQ will have you covered and will now paginate things for you.</p>
</blockquote>
<p>In this iteration, the <code>as</code> syntax for the nested selects now come with renamed columns, and the outer query uses those column names. In an attempt to still permit <code>Record.into(Table)</code> to work, it maps back again to the original columns, in order:</p>
<pre class="lang-java prettyprint-override"><code>  public static Select&lt;?&gt; paginate(
          DSLContext ctx,
          Select&lt;?&gt; original,
          Field&lt;?&gt;[] sort,
          int limit,
          int offset ) {
    Map&lt;List&lt;String&gt;, String&gt; aliases = new LinkedHashMap&lt;&gt;();
    List&lt;Field&lt;?&gt;&gt; reverseAlias = new ArrayList&lt;&gt;();

    List&lt;Field&lt;?&gt;&gt; select = original.getSelect();
    for (int i = 0; i &lt; select.size(); i++) {
      Field&lt;?&gt; field = select.get(i);
      aliases.put(Arrays.asList(field.getQualifiedName().getName()), &quot;c&quot; + i);
    }

    Table&lt;?&gt; u = original.asTable(&quot;u&quot;, aliases.values().toArray(String[]::new));
    Field&lt;Integer&gt; totalRows = count().over().as(&quot;total_rows&quot;);
    String[] sortFieldNames = Arrays.stream(sort).map(o -&gt; aliases.get(Arrays.asList(o.getQualifiedName().getName()))).toArray(String[]::new);
    Field&lt;Integer&gt; row = rowNumber().over().orderBy(u.fields(sortFieldNames))
            .as(&quot;row&quot;);

    Table&lt;?&gt; t = ctx.select(u.asterisk())
            .select(totalRows, row)
            .from(u)
            .orderBy(u.fields(sortFieldNames))
            .limit(limit)
            .offset(offset)
            .asTable(&quot;t&quot;);

    for (int i = 0; i &lt; select.size(); i++) {
      Field&lt;?&gt; field = select.get(i);
      reverseAlias.add(t.field(&quot;c&quot; + i).as(field.getName()));
    }

    Select&lt;?&gt; result = ctx
            .select(reverseAlias)
            .select(
                    count().over().as(&quot;actual_page_size&quot;),
                    field(max(t.field(row)).over().eq(t.field(totalRows)))
                            .as(&quot;last_page&quot;),
                    t.field(totalRows),
                    t.field(row),
                    t.field(row).minus(inline(1)).div(limit).plus(inline(1))
                            .as(&quot;current_page&quot;))
            .from(t)
            .orderBy(t.fields(sortFieldNames));

    return result;
  }
</code></pre>
<p>This generates the following SQL:</p>
<pre class="lang-sql prettyprint-override"><code>select
  &quot;t&quot;.&quot;c1&quot; as &quot;id&quot;,
  &quot;t&quot;.&quot;c2&quot; as &quot;id&quot;,
  &quot;t&quot;.&quot;c3&quot; as &quot;foo_id&quot;,
  count(*) over () as &quot;actual_page_size&quot;,
  (max(&quot;t&quot;.&quot;row&quot;) over () = &quot;t&quot;.&quot;total_rows&quot;) as &quot;last_page&quot;,
  &quot;t&quot;.&quot;total_rows&quot;,
  &quot;t&quot;.&quot;row&quot;,
  (((&quot;t&quot;.&quot;row&quot; - 1) / 10) + 1) as &quot;current_page&quot;
from (
  select
    &quot;u&quot;.*,
    count(*) over () as &quot;total_rows&quot;,
    row_number() over (order by &quot;u&quot;.&quot;c1&quot;) as &quot;row&quot;
  from (
    select &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;id&quot;, &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot;
    from &quot;myschema&quot;.&quot;bar&quot;
      left outer join &quot;myschema&quot;.&quot;foo&quot;
        on &quot;myschema&quot;.&quot;bar&quot;.&quot;foo_id&quot; = &quot;myschema&quot;.&quot;foo&quot;.&quot;id&quot;
  ) as &quot;u&quot; (&quot;c1&quot;, &quot;c2&quot;, &quot;c3&quot;)
  order by &quot;u&quot;.&quot;c1&quot;
  offset 0 rows
  fetch next 10 rows only
) as &quot;t&quot;
order by &quot;t&quot;.&quot;c1&quot;
</code></pre>
<p>Note that as in the initial result sets, the first two columns are still labeled as <code>id</code>. However, <code>Record.into(Table)</code> no longer has the context it needs to understand that the first <code>id</code> column is for the <code>foo</code> table, and the second is for the <code>bar</code> table:</p>
<pre><code>+----+----+------+----------------+---------+----------+----+------------+
|  id|  id|foo_id|actual_page_size|last_page|total_rows| row|current_page|
+----+----+------+----------------+---------+----------+----+------------+
|   1|   1|     1|               3|true     |         3|   1|           1|
|   2|   2|     2|               3|true     |         3|   2|           1|
|   2|   3|     2|               3|true     |         3|   3|           1|
+----+----+------+----------------+---------+----------+----+------------+

+----+
|  id|
+----+
|   2|
+----+

+----+------+
|  id|foo_id|
+----+------+
|   2|     2|
+----+------+
</code></pre>
<p>So, to put the question in concrete terms: Is there a way to indicate to jOOQ that a <code>Select&lt;?&gt;</code>'s fields should be mapped to a particular Table?</p>
<p>And, as a more general question, but less subject to the X/Y problem: How can this paginate() method actually be used as in the example, with joins, where the joined tables have colliding column names? Is there a problem with this strategy of building up a query dynamically, and is there another strategy that can be followed instead, without this shortcoming?</p>


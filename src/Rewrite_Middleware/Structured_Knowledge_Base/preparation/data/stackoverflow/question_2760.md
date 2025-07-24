# Is there a better way to create extremely dynamic SQL from user input with Java?
[Link to question](https://stackoverflow.com/questions/51135254/is-there-a-better-way-to-create-extremely-dynamic-sql-from-user-input-with-java)
**Creation Date:** 1530531259
**Score:** 0
**Tags:** java, mysql, sql, dynamic-sql
## Question Body
<p>Reporting is a big part of our requirements and I have been tasked with creating a generic reporting framework that allows the User to specify which columns they would like data from (across numerous tables), which conditions to apply, and which output format they want the data in. </p>

<p>I will need to store this information into a 'Template' object so that I can generate the same Report over and over with consistent results. Once I finish I will give the Users the ability to specify a Reoccurence option to automatically invoke their 'Template' daily, weekly, monthly, or annually if they choose to enable it. </p>

<p>I want to avoid taking the SQL String as input to remove the risk of SQL Injection and I got something working, but it seems like there can be a much better way than the way I am doing it currently. </p>

<p>I created 4 types of Java classes to construct the Query. </p>

<ol>
<li>Query: This is what the User will provide specifying their SQL in JSON.</li>
<li>Filter: This is used to specify a condition to be applied to the query. </li>
<li>Select: This is used to specify a column to be returned from the result.</li>
<li>Join: This is used to specify that a join should connect another table. </li>
</ol>

<p>Note: I am validating all Table Names and Field Names against the Hibernate Table and Column annotations to ensure they are valid. </p>

<p>Some things that are missing are the ability to use aliases and NOT clauses, which I will want to add later. </p>

<p>I am using mySQL at the moment and my query doesn't need to be database agnostic. If I need to rewrite it if I move to another vendor than so be it.</p>

<p>--</p>

<pre><code>// This is my RequestBody
public class Query {

    private String from;
    private Filter filter;
    private List&lt;Join&gt; joins; 
    private List&lt;Select&gt; selections;
</code></pre>

<p>--</p>

<pre><code>@ApiModel(value="filter", discriminator = "type", subTypes = {
          JoinerFilter.class, MultiFilter.class, SimpleFilter.class
})
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, 
              include = JsonTypeInfo.As.PROPERTY, 
              property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = JoinerFilter.class, name = "joiner"),
    @JsonSubTypes.Type(value = MultiFilter.class, name = "multi"),
    @JsonSubTypes.Type(value = SimpleFilter.class, name = "simple")
})
public abstract class Filter {

    public abstract void validate();

    public abstract String toSQL();
}
</code></pre>

<p>--</p>

<pre><code>// This Filter is used to concatenate 2 Filters
@ApiModel(value = "joiner", parent = Filter.class)
public class JoinerFilter extends Filter {

    private enum JoinerCondition {
        AND, OR
    }

    private JoinerCondition condition;
    private Filter lhsFilter;
    private Filter rhsFilter;
</code></pre>

<p>--</p>

<pre><code>// This Filter is used to perform a simple evaluation
@ApiModel(value = "simple", parent = Filter.class)
public class SimpleFilter extends Filter {

    private enum SimpleCondition {
        EQUAL, GREATER_THAN, LESS_THAN, LIKE
    }

    private String table;
    private String field;
    private String lhsFunction;
    private String rhsFunction;
    private SimpleCondition condition;
    private String value;
</code></pre>

<p>--</p>

<pre><code>// This Filter is used to search multiple values at once
@ApiModel(value = "multi", parent = Filter.class)
public class MultiFilter extends Filter {

    private enum MultiCondition {
        BETWEEN, IN
    }

    private String table;
    private String field;
    private String lhsFunction;
    private String rhsFunction;
    private MultiCondition condition;
    private List&lt;String&gt; values;
</code></pre>

<p>--</p>

<pre><code>public class Select {

    private String table;
    private String field;
    private String function;
</code></pre>

<p>--</p>

<pre><code>public class Join {

    private enum JoinType {
        INNER_JOIN, LEFT_JOIN, CROSS_JOIN
    }

    private Filter on;
    private String table;
    private JoinType type;
</code></pre>


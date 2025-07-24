# Filter joined table in where statement instead of subquery
[Link to question](https://stackoverflow.com/questions/74959558/filter-joined-table-in-where-statement-instead-of-subquery)
**Creation Date:** 1672388860
**Score:** 0
**Tags:** .net, entity-framework, linq
## Question Body
<p>This is my database models with EntityFramework for MySQL</p>
<pre><code>public class User
    {
        public Guid id { get; set; }
        public string? firstName { get; set; }
        public string? lastName { get; set; }
        public string? email { get; set; }
        public string? displayName { get; set; }
        public virtual List&lt;UserRequest&gt;? userRequests { get; set; }
    }
</code></pre>
<pre><code>public class UserRequest
    {
        public int id { get; set; }
        public string? action { get; set; }
        public string? domain { get; set; }
        public string? pathAccessing { get; set; }
        public string? applicationName { get; set; }
        public string? type { get; set; }
        public DateTime createdDate { get; set; }
        public Guid userId { get; set; }
        public User? user { get; set; }
    }
</code></pre>
<p>In this models, 1 user can have multiple userRequest. So I will like to query whether user access this domains before.</p>
<p>In SQL statement, this will be my statement</p>
<pre><code>select * from User u 
inner join UserRequest ur on ur.userId = u.id
where ur.domains in (&quot;http://localhost&quot;, &quot;http://localhost.dev&quot;)
</code></pre>
<p>This is my statement in linq</p>
<pre><code>var domainsList = new string[] {&quot;http://localhost&quot;, &quot;http://localhost.dev&quot;};
     var result = _DBContext.User
                   .Include(q=&gt;
                      q.userRequests             
                   ).Where((t)=&gt; t.userRequests.any(u=&gt;domainsList.Contains(u.domain)));
</code></pre>
<p>Generated SQL statement</p>
<pre><code>SELECT `u`.`id`, `u`.`displayName`, `u`.`email`, `u`.`firstName`, `u`.`lastName`, `u1`.`id`, `u1`.`action`, `u1`.`applicationName`, `u1`.`createdDate`, `u1`.`domain`, `u1`.`pathAccessing`, `u1`.`type`, `u1`.`userID`
      FROM `user` AS `u`
      LEFT JOIN `userRequest` AS `u1` ON `u`.`id` = `u1`.`userID`
      WHERE EXISTS (
          SELECT 1
          FROM `userRequest` AS `u0`
          WHERE (`u`.`id` = `u0`.`userID`) AND `u0`.`domain` IN ('http://localhost', 'http://localhost.dev'))
      ORDER BY `u`.`id`
</code></pre>
<p>The generated sql statement is using subquery instead of my expected simple where expression. My database is not large so subquery is slower than join+where expression in my case.</p>
<p>Is there a way I can rewrite my linq statement to have dotnet generate the SQL statement similar to what I expect? Or this is not possible in Linq?</p>
<p>Found a few similar question, but none is trying to achieve the end result I'm hoping for.</p>
<p>sorry for my bad english</p>

## Answers
### Answer ID: 74962267
<p>Remove include and use join. Please follow the sample query syntax</p>
<pre><code>    var query = from u in User
            join ur in UserRequest
                on u.ID equals ur.userID
                where (new string[] {'exampleofdomainList'}).Contains(ur.domain)
            select new { u, ur}
</code></pre>


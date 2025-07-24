# Cypher multiple OPTIONAL MATCH - Pattern Comprehension - COUNT DISTINCT
[Link to question](https://stackoverflow.com/questions/72846587/cypher-multiple-optional-match-pattern-comprehension-count-distinct)
**Creation Date:** 1656852038
**Score:** 3
**Tags:** neo4j, cypher, list-comprehension
## Question Body
<p>I have read a lot of comments about OPTIONAL MATCH and Pattern Comprehesion, but I can't find a solution for my case.</p>
<p>I have a node (Account) in my Neo4j Database and I'd like to count the nodes which belongs to each account.
The following code works with one or two optional matches, but the many optional matches produce a cross product and a timeout.</p>
<pre><code>// Account
MATCH (a:Account{billingCountry: &quot;DE&quot;, isDeleted: false})
WHERE a.id IS NOT NULL

// User
MATCH (a)&lt;-[:CREATED]-(u:User)

// Contact
OPTIONAL MATCH (a) &lt;-[:CONTACT_OF]- (c:Contact{isDeleted: false})

// Opportunity
OPTIONAL MATCH (a) &lt;-[:OPPORTUNITY_OF]- (o:Opportunity{isDeleted: false, s4sMarked_For_Deletion__C: false})

// Open Opportunity
OPTIONAL MATCH (a)&lt;-[:OPPORTUNITY_OF]-(open:Opportunity{isClosed: false, isDeleted: false})

// Attribute
OPTIONAL MATCH (a) &lt;-[:ATTRIBUTE_OF]- (aa:Attribute_Assignment{isDeleted: false})

// Sales Planning
OPTIONAL MATCH (a) &lt;-[:SALESPLAN_OF]- (s:Sales_Planning)

// Task
OPTIONAL MATCH (a) &lt;-[:TASK_OF]- (t:Task{isDeleted: false})

// Event
OPTIONAL MATCH (a) &lt;-[:EVENT_OF]- (e:Event{isDeleted: false})

// Contract
OPTIONAL MATCH (a) &lt;-[:CONTRACT_OF]- (ct:Contract{isDeleted: false})

RETURN
a.id

u.name AS User_Name,
u.department AS User_Department,

COUNT(DISTINCT c.id) AS Contact_Count,
COUNT(DISTINCT o.id) AS Opportunity_Count,
COUNT(DISTINCT open.id) AS OpenOpp_Count,
COUNT(DISTINCT aa.id) AS Attribute_Count,
COUNT(DISTINCT s.timeYear) AS Sales_Plan_Count,
COUNT(DISTINCT t.id) AS Task_Count,
COUNT(DISTINCT e.id) AS Event_Count,
COUNT(DISTINCT ct.id) AS Contract_Count
</code></pre>
<p>I can rewrite the query with a Pattern Compression, but then I just get back the non distinct ids in arrays.
Is there a way to count the distinct values inside the arrays or another way how to count the values in pattern compression?</p>
<pre><code>MATCH (a:Account{billingCountry: &quot;DE&quot;, isDeleted: false})
WHERE a.id IS NOT NULL

RETURN a.id,
[
[(a)&lt;-[:CONTACT_OF]- (c:Contact{isDeleted: false}) | c.id],
[(a)&lt;-[:OPPORTUNITY_OF]- (o:Opportunity{isDeleted: false, s4sMarked_For_Deletion__C: false}) | o.id],
[(a)&lt;-[:OPPORTUNITY_OF]-(open:Opportunity{isClosed: false, isDeleted: false}) | open.id],
[(a) &lt;-[:ATTRIBUTE_OF]- (aa:Attribute_Assignment{isDeleted: false}) | aa.id],
[(a) &lt;-[:SALESPLAN_OF]- (s:Sales_Planning) | s.timeYear],
[(a) &lt;-[:TASK_OF]- (t:Task{isDeleted: false}) | t.id],
[(a) &lt;-[:EVENT_OF]- (e:Event{isDeleted: false}) | e.id],
[(a) &lt;-[:CONTRACT_OF]- (ct:Contract{isDeleted: false}) | ct.id]
]
</code></pre>
<p>If I made a formal mistake in my first stockoverflow post, I would appreciate feedback :)</p>

## Answers
### Answer ID: 72847484
<p>The problem lies, in the <code>RETURN</code> statement, because you are calculating all the counts at the last, neo4j has to calculate the cartesian products. If you calculate each node count at each step, it will be much more optimal. Like this:</p>
<pre><code>MATCH (a:Account{billingCountry: &quot;DE&quot;, isDeleted: false})
WHERE a.id IS NOT NULL
MATCH (a)&lt;-[:CREATED]-(u:User)
OPTIONAL MATCH (a) &lt;-[:CONTACT_OF]- (c:Contact{isDeleted: false})
WITH a, u, COUNT(DISTINCT c.id) AS Contact_Count,
OPTIONAL MATCH (a) &lt;-[:OPPORTUNITY_OF]- (o:Opportunity{isDeleted: false, s4sMarked_For_Deletion__C: false})
WITH a, u, Contact_Count, COUNT(DISTINCT o.id) AS Opportunity_Count
OPTIONAL MATCH (a)&lt;-[:OPPORTUNITY_OF]-(open:Opportunity{isClosed: false, isDeleted: false})
WITH a, u, Contact_Count, Opportunity_Count, COUNT(DISTINCT open.id) AS OpenOpp_Count
OPTIONAL MATCH (a) &lt;-[:ATTRIBUTE_OF]- (aa:Attribute_Assignment{isDeleted: false})
WITH a, u, Contact_Count, Opportunity_Count, OpenOpp_Count, COUNT(DISTINCT aa.id) AS Attribute_Count
OPTIONAL MATCH (a) &lt;-[:SALESPLAN_OF]- (s:Sales_Planning)
WITH a, u, Contact_Count, Opportunity_Count, OpenOpp_Count, Attribute_Count,COUNT(DISTINCT s.timeYear) AS Sales_Plan_Count
OPTIONAL MATCH (a) &lt;-[:TASK_OF]- (t:Task{isDeleted: false})
WITH a, u, Contact_Count, Opportunity_Count, OpenOpp_Count, Attribute_Count, Sales_Plan_Count, COUNT(DISTINCT t.id) AS Task_Count
OPTIONAL MATCH (a) &lt;-[:EVENT_OF]- (e:Event{isDeleted: false})
WITH a, u, Contact_Count, Opportunity_Count, OpenOpp_Count, Attribute_Count, Sales_Plan_Count, Task_Count, COUNT(DISTINCT e.id) AS Event_Count
OPTIONAL MATCH (a) &lt;-[:CONTRACT_OF]- (ct:Contract{isDeleted: false})
RETURN
a.id, u.name AS User_Name, u.department AS User_Department, Contact_Count,
Opportunity_Count, OpenOpp_Count, Attribute_Count, Sales_Plan_Count,
Task_Count, Event_Count, COUNT(DISTINCT ct.id) AS Contract_Count
</code></pre>


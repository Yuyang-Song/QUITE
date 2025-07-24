# Rewriting an ActiveRecord query as recursive SQL
[Link to question](https://stackoverflow.com/questions/60841892/rewriting-an-activerecord-query-as-recursive-sql)
**Creation Date:** 1585100415
**Score:** 4
**Tags:** sql, ruby-on-rails, postgresql, recursion, activerecord
## Question Body
<p>I have a tree like active record structure with a self referencing object - as in, the object can be a parent or child to another object of the same class.  I need a way to efficiently map this structure in code.  So far I've been doing it in ruby with the active record ORM and it's terribly inefficient.</p>

<p>Here is what the pod.rb model looks like:</p>

<pre><code>    has_many :pod_parents, class_name: "PodPod", dependent: :delete_all
    has_many :parents, through: :pod_parents, :foreign_key =&gt; 'parent_id', :source =&gt; 'parent'
    has_many :pod_children, class_name: "PodPod", :foreign_key =&gt; 'parent_id'
    has_many :children, through: :pod_children, :source =&gt; 'pod'

    scope :active, -&gt; {
        where(pod_state: "active").where(pod_type: ["standard","readonly"])
    }
</code></pre>

<p>Here is the relevant database schema:</p>

<pre><code>table "pods"
  t.string "intention"
  t.integer "user_id"
  t.string "slug"
  t.string "url_handle"
  t.index ["slug"], name: "index_pods_on_slug"
  t.index ["url_handle"], name: "index_pods_on_url_handle"

table "pod_pods"
  t.integer "parent_id"
  t.integer "pod_id"
  t.index ["parent_id", "pod_id"], name: "index_pod_pods_on_parent_id_and_pod_id", unique: true
  t.index ["parent_id"], name: "index_pod_pods_on_parent_id"
  t.index ["pod_id"], name: "index_pod_pods_on_pod_id"
</code></pre>

<p>And here are the specific functions that I'm working on optimizing:</p>

<pre><code>def get_all_parents
    parents = []
    self.parents.active.each do |parent|
        parents &lt;&lt; parent
        parents.concat(parent.get_all_parents)
    end
    return parents
end

def get_all_children
    children = []
    self.children.each do |child|
        children.concat(child.get_all_children)
    end
    return children
end

def get_all_parents_and_children
    pod_array = self.get_all_parents
    pod_array.concat(self.get_all_children)
    return pod_array
end

def get_all_relations(inclusive = false)
    circles_array = self.get_all_parents
    circles_array.each do |parent|
        circles_array = circles_array.concat(parent.get_all_children)
    end
    circles_array = circles_array.concat(self.get_all_children)
    unique_ids = circles_array.compact.map(&amp;:id).uniq - [self.id]
    circles = Pod.where(id: unique_ids)
end
</code></pre>

<p>As far as I've been able to research, Postgres supports a type of recursive SQL query.  I've been using these articles to point the way: <a href="https://prograils.com/posts/three-ways-iterating-tree-like-active-record-structures" rel="nofollow noreferrer">1</a>, <a href="https://hashrocket.com/blog/posts/recursive-sql-in-activerecord" rel="nofollow noreferrer">2</a>.</p>

<p>And this is as far as I've gotten:</p>

<pre><code>def get_all_parents2
      sql =
        &lt;&lt;-SQL
            WITH RECURSIVE pod_tree(id, path) AS (
                SELECT id, ARRAY[id]
                FROM pods
                WHERE id = #{self.id}
            UNION ALL
                SELECT pods.id, path
                FROM pod_tree
                JOIN pods ON pods.id=pod_tree.id
                JOIN pod_pods ON pod_pods.parent_id = pods.id
                WHERE NOT pods.id = ANY(path)
            )
            SELECT * FROM pod_tree
            ORDER BY path;
        SQL
      sql.chomp
        Pod.find_by_sql(sql)
    end
</code></pre>

<p>My SQL isn't particularly good and I'm at a loss how to navigate the tree structure upwards and downwards to be able to rewrite the functions I've mentioned above as recursive SQL.  I would be grateful for some help with this.  Thank you.</p>

## Answers
### Answer ID: 60978770
<p>What you are trying to accomplish is definitely possible through recursive CTEs. I will cover the first two scenarios you have as the other two are just an extension of the first two.</p>

<p>In all the SQL examples I am going to use the id 1 to illustrate the value that you are substituting at the model level. Since you wrote that query, I am going to assume some familiarity with recursive CTEs and try to walk to a solution. </p>

<h3><code>get_all_children</code></h3>

<p>Let us take the method <code>get_all_children</code> first. This method involves walking down the tree, level by level and covering nodes that we encounter.</p>

<p>Since pod_pods contains all the info regarding hierarchy and in getting the children there is no scope involved, we can just recurse on pod_pods for children.</p>

<pre class="lang-sql prettyprint-override"><code>-- Snippet #1
WITH RECURSIVE pod_tree AS (
  SELECT pod_id -- Get the pod_id of the children of the base case node
  FROM pod_pods
  WHERE parent_id = 1 -- Base case
  UNION ALL -- Recurse on this and do a union with the previous step
  SELECT p.pod_id
  FROM pod_pods p
    INNER JOIN pod_tree ptree 
      ON ptree.pod_id = p.parent_id -- Get the children nodes for nodes found at the previous recursion step.
)

SELECT * FROM pods 
WHERE id IN (SELECT DISTINCT(pod_id) FROM pod_tree);
</code></pre>

<p>Your Ruby code doesn't cover the possibility for an infinite loop happening because of a cycle but if there is a chance it can happen, the way you will tackle this is by keeping track of ids you have already seen.</p>

<pre class="lang-sql prettyprint-override"><code>-- Snippet #2
WITH RECURSIVE pod_tree(pod_id, rtree) AS ( -- Extra rtree parameter to keep track of visited nodes
  SELECT pod_id, ARRAY[pod_id] -- Make the base case array with pod_id
  FROM pod_pods
  WHERE parent_id = 1 -- Base case
  UNION ALL
  SELECT p.pod_id, rtree || p.pod_id -- Add the current pod_id to array
  FROM pod_pods p
    INNER JOIN pod_tree ptree 
      ON ptree.pod_id = p.parent_id
  WHERE NOT (p.pod_id = ANY(rtree)) -- Exclude nodes which have already been seen  
)

SELECT * FROM pods 
WHERE id IN (SELECT DISTINCT(pod_id) FROM pod_tree);
</code></pre>

<p>If you can have orphan relations in pod_pods and want to ignore them, then a join is necessary between pods.</p>

<pre class="lang-sql prettyprint-override"><code>-- Snippet #3
WITH RECURSIVE pod_tree(id, rtree) AS (
  SELECT p1.id, ARRAY[p1.id]
  FROM pods p1 INNER JOIN pod_pods p2 ON p1.id = p2.pod_id 
  WHERE parent_id = 1
  UNION ALL
  SELECT p1.id, rtree || p1.id
  FROM pods p1 
    INNER JOIN pod_pods p2 ON p1.id = p2.pod_id
    INNER JOIN pod_tree ptree ON p2.parent_id = ptree.id
  WHERE NOT (p1.id = ANY(ptree.rtree))  
)

SELECT * FROM pods WHERE id IN (SELECT DISTINCT(id) FROM pod_tree);
</code></pre>

<p>If you don't have orphan links, my advice would be to go with either Snippet #1 or #2 as they would be faster than #3 as it involves extra joins.</p>

<h3><code>get_all_parents</code></h3>

<p>At first for simplicity let us add the scope fields that are being added because of active later.First we just walk down the tree of pod_pods table to get all the parent ids and then we apply the scope.</p>

<pre class="lang-sql prettyprint-override"><code>-- Snippet #4
WITH RECURSIVE pod_tree AS (
  SELECT parent_id -- Get the parent_id of the parents of the base case node
  FROM pod_pods
  WHERE pod_id = 1 -- Base case
  UNION ALL -- Recurse on this and do a union with the previous step
  SELECT p.parent_id
  FROM pod_pods p
    INNER JOIN pod_tree ptree 
      ON ptree.parent_id = p.pod_id -- Get the parent nodes for nodes found at the previous recursion step.
)

SELECT * FROM pods 
WHERE 
  id IN (SELECT DISTINCT(parent_id) FROM pod_tree)
  AND pod_state = 'active'
  AND pod_type IN ('standard', 'readonly')
;
</code></pre>

<p>However, this only applies the active filter once all the nodes have been fetched. This might not be ideal as it might walk more tree than required and might even return the parents of nodes which are not active. To make it like the method is doing in the Ruby code, we need to join it with pods. I am adding the infinite recursion avoiding step here as well as you have an idea about it now.</p>

<pre class="lang-sql prettyprint-override"><code>-- Snippet #5
WITH RECURSIVE pod_tree(id, rtree) AS (
  SELECT p1.id, ARRAY[p1.id]
  FROM pods p1 
    INNER JOIN pod_pods p2 ON p1.id = p2.parent_id 
  WHERE pod_id = 1
    AND p1.pod_state = 'active' 
    AND p1.pod_type IN ('standard', 'readonly')
  UNION ALL
  SELECT p1.id, rtree || p1.id
  FROM pods p1 
    INNER JOIN pod_pods p2 ON p1.id = p2.parent_id
    INNER JOIN pod_tree ptree ON p2.pod_id = ptree.id
  WHERE p1.pod_state = 'active' 
    AND p1.pod_type IN ('standard', 'readonly')
    AND NOT (p1.id = ANY(ptree.rtree))  
)

SELECT * FROM pods WHERE id IN (SELECT DISTINCT(id) FROM pod_tree);
</code></pre>

<p>In Rails based on your stub method, the code for snippet #5 will look like</p>

<pre class="lang-rb prettyprint-override"><code>def get_all_parents
  sql =
    &lt;&lt;-SQL
      WITH RECURSIVE pod_tree(id, rtree) AS (
        SELECT p1.id, ARRAY[p1.id]
        FROM pods p1 
          INNER JOIN pod_pods p2 ON p1.id = p2.parent_id 
        WHERE pod_id = #{self.id}
          AND p1.pod_state = 'active' 
          AND p1.pod_type IN ('standard', 'readonly')
        UNION ALL
        SELECT p1.id, rtree || p1.id
        FROM pods p1 
          INNER JOIN pod_pods p2 ON p1.id = p2.parent_id
          INNER JOIN pod_tree ptree ON p2.pod_id = ptree.id
        WHERE p1.pod_state = 'active' 
          AND p1.pod_type IN ('standard', 'readonly')
          AND NOT (p1.id = ANY(ptree.rtree))  
      )

      SELECT * FROM pods WHERE id IN (SELECT DISTINCT(id) FROM pod_tree);
    SQL
  # IMP!
  # sql = sql_sanitize(sql)
  # Add some sanitize step here
  sql.chomp
  Pod.find_by_sql(sql)
end
</code></pre>

<p>This should cover your first two usecases. As mentioned earlier, the other two are an extension of these two, so you can just use these to expand to those.</p>

<p>Note:</p>

<ul>
<li>If you don't have cycles, you can avoid the infinite recursion columns as it is extra bookkeeping.</li>
<li>If you don't have orphan links, prefer iterating on just <code>pod_pods</code> for children as it avoids needless joins</li>
<li><code>rtree</code> in the above sql queries contains the hierarchy. You can choose to pass it back if you need that info. I skipped it as you anyway end up flattening the result.</li>
<li>I was fetching unique nodes. Your Rails code currently will fetch multiple occurrences of a node if it is visited multiple times. If you want this, plus the order of the tree as well, you can have this behaviour like this:</li>
</ul>

<pre class="lang-sql prettyprint-override"><code>-- Example for getting all parents
WITH RECURSIVE pod_tree(id, slug, pod_type, parent_id, rtree) AS (
  SELECT p1.id, p1.slug, p1.pod_type, p2.parent_id, ARRAY[p1.id] -- Select the fields you need
  FROM pods p1 INNER JOIN pod_pods p2 ON p1.id = p2.parent_id 
  WHERE pod_id = 1
  AND p1.pod_state = 'active' AND p1.pod_type IN ('standard', 'readonly')
  UNION ALL
  SELECT p1.id, p1.slug, p1.pod_type, p2.parent_id, rtree || p1.id
  FROM pods p1 INNER JOIN pod_pods p2 ON p1.id = p2.parent_id
  INNER JOIN pod_tree ptree ON p2.pod_id = ptree.id
  WHERE p1.pod_state = 'active' AND p1.pod_type IN ('standard', 'readonly')
  AND NOT (p1.id = ANY(ptree.rtree))  
)

SELECT * FROM pod_tree;

</code></pre>

### Answer ID: 60847061
<p>I advise you to look at the <a href="https://en.wikipedia.org/wiki/Nested_set_model" rel="nofollow noreferrer">nested set model</a> of tree implementation. Rails already has gem that realize that logic <a href="https://github.com/collectiveidea/awesome_nested_set" rel="nofollow noreferrer">awesome_nested_set</a></p>


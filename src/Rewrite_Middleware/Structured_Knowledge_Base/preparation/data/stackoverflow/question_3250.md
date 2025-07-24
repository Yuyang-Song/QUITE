# How to rewrite a php script to JavaScript
[Link to question](https://stackoverflow.com/questions/73509218/how-to-rewrite-a-php-script-to-javascript)
**Creation Date:** 1661586373
**Score:** 0
**Tags:** php, sql, node.js
## Question Body
<p>I have an express server running using nodejs, and I'm using SQL syntax to query data from my MYSQL database.</p>
<p>The query is to get all members under the current user ID and also get members under it's children and so on, to get a genealogy tree. I'm trying to query a genealogy tree for a user.</p>
<p>I have a PHP script for the query, which worked fine</p>
<p>This is the PHP script:</p>
<pre><code>$memory = $_GET['memory'];  
echo '&lt;div style=&quot;background:#ccc;display:flex;width:50px;height:50px;justify- 
content:center;align-items:center;border-radius:50%;&quot;&gt;'.$memory.'&lt;/div&gt;';
$transend = array($memory);
$step = 1;
for ($i=0; $i &lt; $step; $i++) {
    $under = $transend[$i];
    $get = $con-&gt;query(&quot;SELECT * FROM multilevel WHERE `under`='$under'&quot;);
    $cnt = $get-&gt;num_rows;
    if ($cnt&gt;0) {
        for ($g=0; $g &lt; $cnt; $g++) {
            $fet = $get-&gt;fetch_object();
            $id = $fet-&gt;id;
            $position = $fet-&gt;position;
            array_push($transend, $id);
            $step = $step*2;
            echo '&lt;div style=&quot;background:#ccc;display:flex;width:50px;height:50px;justify-content:center;align-items:center;border-radius:50%;&quot;&gt;'.$id.'-'.$position.'&lt;/div&gt;';
        }
    } else {
        break;
    }
}
</code></pre>
<p>I am trying to rewrite it using SQL syntax in node. This is my nodejs code:</p>
<p>A Tree Constructor</p>
<pre><code>const Tree = function (binary) {
 this.position = binary.position;
 this.level = binary.level;
 this.user_id = binary.user_id;
 this.under_user_id = binary.under_user_id;
 this.brought_by = binary.brought_by;
 this.username = binary.username;
 };
</code></pre>
<p>A method to get all binary for a user</p>
<pre><code>Tree.findBinaries = async (id, result) =&gt; {
  const theId = parseInt(id);
  let transend = [theId];
  let step = 1;
  let data = [];

  for (let i = 0; i &lt; step; i++) {
    const under = transend[i];
    connection.query(
      `SELECT * FROM multilevel WHERE under = ?`,
      under,
      (err, res) =&gt; {
        if (err) {
          result(null, err);
          return;
        }
        if (res.length) {
          for (let index = 0; index &lt; res.length; index++) {
            const { id } = res[index];
            // push id
            transend.push(id);
            data.push(res[index]);
            step = step * 2;
          }
          result(null, data);
        } else {
          result(null, &quot;no data found&quot;);
        }
      }
    );
  }
};
</code></pre>
<p>The transend.push(id) and data.push(res[index]), are not been pushed to the top level, also the step is not been updated. So the loop is running just once.</p>
<p>The expected Result is supposed to be 16 items of children and children of children, But it is currently returning to just the first level. I don't know what I'm currently doing wrong.</p>


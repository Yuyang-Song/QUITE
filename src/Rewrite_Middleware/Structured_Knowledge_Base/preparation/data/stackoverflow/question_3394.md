# Sequelize WHERE string LIKE `column_name`
[Link to question](https://stackoverflow.com/questions/78376891/sequelize-where-string-like-column-name)
**Creation Date:** 1713946444
**Score:** 0
**Tags:** mysql, sequelize.js, where-clause
## Question Body
<p>I have table <code>devices</code> with models names:</p>
<pre><code>+--------+-----------+
| models | id_number |
+--------+-----------+
| aaaaa  |     11111 |
| bbbbb  |     22222 |
| ccccc  |     33333 |
| ddddd  |     44444 |
+--------+-----------+
</code></pre>
<p>and I check whether the file <code>path</code> contains the <code>model</code> saved in the database:</p>
<pre><code>/folder1/subfolder/filename_bbbbb_ver.zip
/folder1/filename_ddddd_ver.zip
/filename_aaaaa_ver.zip
</code></pre>
<p>for this I use this mysql query, which works very well:</p>
<pre><code>sequelize.query(&quot;SELECT * FROM `devices` WHERE :path LIKE CONCAT('%\\_',`models`, '\\_%')&quot;,
  { replacements: { path: el.path_name} }
)
</code></pre>
<p>But now I want to rewrite above query to Sequelize &quot;object&quot; findAll, but I'm not sure that this is possible. Now I have like this:</p>
<pre><code>const model_list = await devices.findAll({
  where: {
      [el.path_name]: { [Op.like]: sequelize.fn('%\\_'+sequelize.col('models')+'\\_%') }
  }
})
</code></pre>
<p>But <code>[el.path_name]</code> but treats it as a column name, not text.</p>


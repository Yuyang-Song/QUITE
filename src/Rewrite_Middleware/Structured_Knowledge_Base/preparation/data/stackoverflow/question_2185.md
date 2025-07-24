# The Best way to Access related field in mysql
[Link to question](https://stackoverflow.com/questions/22664760/the-best-way-to-access-related-field-in-mysql)
**Creation Date:** 1395845593
**Score:** 0
**Tags:** mysql
## Question Body
<p>I have a very unique situation where I have inherited a compiled application but no source to alter it. As such I wish to temporarily extend the system in order to buy a few weeks in order to rewrite it. </p>

<p>First of all let me lay down A small example database to make things easier to understand.</p>

<pre><code>Table Team

ID         Name           City
1          Fish           Carson City
2          Rats           Springfiled
3          Salamanders    Lubboch


Table Players

ID        Team_ID         Name
1         1               Bill
2         1               Ted
3         2               Moe
4         3               Al
5         3               Stan
</code></pre>

<p>Looking at a configuration file I can see that the application is using the following configuration string is used to produce the following SQL query.  </p>

<p>Configuration String:    <code>ID,Team_ID,Name</code></p>

<p>SQL QUERY  <code>SELECT ID,Team_ID,Name FROM Players WHERE ID = 2</code></p>

<p>I cannot edit the SQL query BUT I can edit the config string</p>

<p>Of course the result is:      <code>2,  1,  Ted</code></p>

<p>But this is not optimal. What I really would like to result to be is:  <code>2,  Fish,  Ted</code></p>

<p>Given that I cannot access the code that generates the query and that's I cannot alter the query other than to change the configuration string. </p>

<p>As I am not an advanced SQL user, I lay awake at night thinking I wish there was a way to insert the following pseudo-query the configuration string.</p>

<p>Configuration String:    <code>ID,team.name(Team_ID),Name</code></p>

<p>SQL QUERY  <code>SELECT ID,team.name(Team_ID),Name FROM Players WHERE ID = 2</code></p>

<p>I do have full Rights to the database. Can anyone think of a way I can add a stored or calculated or something with the name that will allow me to query this way?</p>

## Answers
### Answer ID: 22665082
<p>You could try to insert a dependent subquery into the configuration string:</p>

<pre><code>ID,(SELECT Name FROM Team WHERE ID = Players.Team_ID),Name
</code></pre>

<p>if this works with your application is another question...</p>

<p>Maybe try this, which keeps column names as they are:</p>

<pre><code>ID,(SELECT Name FROM Team WHERE ID = Players.Team_ID) AS Team_ID,Name
</code></pre>


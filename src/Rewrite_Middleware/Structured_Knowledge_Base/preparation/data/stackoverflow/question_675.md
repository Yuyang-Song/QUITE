# Laravel Query Builder, How does it work
[Link to question](https://stackoverflow.com/questions/36689836/laravel-query-builder-how-does-it-work)
**Creation Date:** 1460970888
**Score:** 0
**Tags:** php, laravel
## Question Body
<p>Sorry for this very noob question. I started PHP for almost 1 months. I don't have any background in programming. Without using a framework. A friend of mine lets me work with him on a project. which uses a php it had a framework which was built by them.  Since their team lead decided to pick a new framework, which was laravel and rewrite the whole project. Luckily he still let me join them. I've been working only on the small stuff in the project. I haven't touched any database related during my work with them.  after a week I had to go back to my home town so I can't work with them anymore. Since then I keep reading the laravel documentation. And tried database. I stumbled on this eloquent which builds query from class names or method name. I was so confused. But I don't know what to search for or how does this work. I scanned the code and hell it was so advance I give up. I can't sleep on how to make this. so if any of you could give me an example how this works I would be very happy.</p>

<pre><code>class User extends Model
{

}
</code></pre>

<p>which when called like this</p>

<pre><code>User::all()
</code></pre>

<p>it will give some data. but how.? it this part of php? All I see about php mysql is about pdo. I can't find any examples like this</p>

## Answers
### Answer ID: 36690024
<p>A model in laravel is linked to a snake cased table. This means that a <code>User</code> model maps to a <code>users</code> table but this can be overwritten by adding this in your model class</p>

<p><code>protected $table == "my_custom_table_name"</code></p>

<p>When you use <code>User:all()</code> It will return all the records in the <code>users</code> table. It simply runs <code>select * from users</code> beneath it.</p>

<p>The <code>all()</code> method is defined in the extended <code>model class</code>. You can check it out to understand how laravel automagically does stuff.</p>


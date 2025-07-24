# How to create/update a many-to-many relation where order/index matters?
[Link to question](https://stackoverflow.com/questions/69194046/how-to-create-update-a-many-to-many-relation-where-order-index-matters)
**Creation Date:** 1631712237
**Score:** 0
**Tags:** postgresql, many-to-many, relational-database, supabase
## Question Body
<p>Let's say that you're creating a music app. You have a table of playlists and a table of songs. How would you model that relationship of song order in a playlist in a SQL environment?</p>
<p>Requirements:</p>
<ul>
<li>Each playlist can have multiple songs</li>
<li><strong>Song order in the playlist matters</strong></li>
<li>Each song has its own rich information (artist, album, etc.)</li>
</ul>
<p>On the client side, this is easy, just have an array of product ids on the playlist, and get the song information from those. If the order changes, just update the array and push a new one. Computationally intensive but very easy to reason about and no chance of a doubled index entry.</p>
<p>In relational database world, normally for a many-to-many relationship, you'd use a junction table. Where each playlist_id corresponds to a song_id. You could add a column for index, but then when you update the order of a playlist, you have to rewrite the order of all the indexes.</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>playlist_id</th>
<th>song_id</th>
<th>index</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>1</td>
<td>50</td>
<td>1</td>
</tr>
<tr>
<td>2</td>
<td>1</td>
<td>24</td>
<td>2</td>
</tr>
<tr>
<td>3</td>
<td>1</td>
<td>21</td>
<td>3</td>
</tr>
<tr>
<td>4</td>
<td>2</td>
<td>12</td>
<td>1</td>
</tr>
</tbody>
</table>
</div>
<p>I'm struggling to find an answer to this question.</p>
<p>For my specific situation, I'm currently using Supabase and their Javascript SDK which references a hosted PostgreSQL database and everything is done from a client side app with queries. <strong>I don't know how to write an SQL function that would deal with this.</strong> It all seems like it'd be very complex compared to just pushing a new array each time, even though it's the &quot;correct&quot; way. It doesn't look like PostgreSQL supports an array of foreign keys yet, so is there a better way?</p>

## Answers
### Answer ID: 69215892
<blockquote>
<p>In relational database world, normally for a many-to-many relationship, you'd use a junction table.</p>
</blockquote>
<p>Yes, and that junction table would be 'all key' -- that is in this case its schema would be its key would be <code>{playlist_id, song_id}</code>.</p>
<p>Presumably (you don't say this) a song can appear on many playlists, and at a different sequence in each. Furthermore you can't infer <code>index</code> from any other table.  <code>index</code> is only held on this table. Also (I guess) a user might resequence their playlist by shuffling the same set of songs.</p>
<p>Adding <code>index</code> means you no longer have a junction table. But you do still have a table (one of) whose key(s) is <code>{playlist_id, song_id}</code>. There might be an alternative key <code>{playlist_id, index}</code>, or if a user inadvertently shuffles two songs to the same position on a playlist, that might be allowed, and you'll use <code>song_id</code> to resolve ties. (That's what I'd do, to keep it simple. In a manufacturing step, that's like saying I need 4 bolts and 2 clips here, but it doesn't matter which order you attach them.)</p>
<p>What you don't want or need is an additional <code>id</code> in this table. It does nothing but get in the way of the true key(s) and, as you say, trying to shuffle the order would give a maintenance headache. Perhaps you're not aware any table can have a <a href="https://en.wikipedia.org/wiki/Composite_key" rel="nofollow noreferrer">composite key</a>.</p>


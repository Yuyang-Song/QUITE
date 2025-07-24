# Laravel 4 Eloquent: Many-to-many with conditions on joining table
[Link to question](https://stackoverflow.com/questions/14963639/laravel-4-eloquent-many-to-many-with-conditions-on-joining-table)
**Creation Date:** 1361294637
**Score:** 2
**Tags:** many-to-many, laravel, laravel-4, eloquent
## Question Body
<p>I am attempting to rewrite some logic for a database which was previously used with Codeigniter. The design is such that some of the conditions for a many-to-many join are stored in the joining table like so:</p>

<pre><code>Table user
  - user_id
  ...

Table avatars
  - user_id
  - image_id
  - uploaded_timestamp
  - deleted_timestamp

Table images
  - image_id
  ...
</code></pre>

<p>In this case, I want to get all images associated with a user through the avatars table, ordered by time uploaded time descending, and not including deleted avatars (deleted_timestamp not null).</p>

<p>I have discovered that using Eloquent's hasMany does not allow conditions on the joining table. What is the cleanest way to achieve this affect, or do i need to resort to building a full query in the way I used to with Codeigniter's active record class?</p>

<p><strong>Note:</strong> I have found <a href="https://stackoverflow.com/a/14346014/2047696">this answer</a> which suggests using <code>-&gt;hasMany(..)-&gt;with('another_column_from_pivot_table')</code>, but that only seems to work with Laravel 3's Eloquent implementation. It seems ->with is now for eagar loading only.</p>

## Answers
### Answer ID: 14966736
<p><em>hasMany()</em> is intended for one-to-many relations.  Many-to-many expects <em>belongsToMany()</em> -- that's the statement that ties to the itermediate ("pivot") table.</p>

<p>I haven't tried it, but I can believe that belongsToMany() wouldn't work with a where() statement. I know that hasMany() does fine with a where().</p>

<p>What you may need to do is create a third model class:</p>

<p>(WARNING: untested code)</p>

<pre><code>class User extends Eloquent {
   public avatars() {
      return $this-&gt;hasMany('Avatar')
                  -&gt;where ('deleted_timestamp',0)
                  -&gt;orderBy('uploaded_timestamp','desc');
   }
}

class Avatar extends Eloquent {
  public image() {
    return $this-&gt;belongsTo('Image');
  }
}

class Image extends Eloquent {
}
</code></pre>

<p>You'd access your images as...</p>

<pre><code>$avatars = User::find($user_id)-&gt;avatars();
foreach ($avatars as $avatar) {
   echo '&lt;img src="$avatar-&gt;image-&gt;url"&gt;';
}
</code></pre>


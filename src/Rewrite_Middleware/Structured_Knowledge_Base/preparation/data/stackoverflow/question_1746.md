# Should I drop a polymorphic association?
[Link to question](https://stackoverflow.com/questions/6147052/should-i-drop-a-polymorphic-association)
**Creation Date:** 1306461181
**Score:** 1
**Tags:** ruby-on-rails-3, inheritance, polymorphic-associations, eager-loading, will-paginate
## Question Body
<p>My code is still just in development, not production, and I'm hitting a wall with generating data that I want for some views.</p>

<p>Without burying you guys in details, I basically want to navigate through multiple model associations to get some information at each level.  The one association giving me problems is a polymorphic belongs_to.  Here are the most relevant associations</p>

<pre><code>Model Post
  belongs_to :subtopic
  has_many :flags, :as =&gt; :flaggable

Model Subtopic
  has_many :flags, :as =&gt; :flaggable

Model Flag
  belongs_to :flaggable, :polymorphic =&gt; true
</code></pre>

<p>I'd like to display multiple flags in a Flags#index view.  There's information from other models that I want to display, as well, but I'm leaving out the specifics here to keep this simpler.</p>

<p>In my Flags_controller#index action, I'm currently using <code>@flags = paginate_by_sql</code> to pull everything I want from the database.  I can successfully get the data, but I can't get the associated model objects eager-loaded (though the data I want is all in memory).  I'm looking at a few options now:</p>

<ul>
<li><p>rewrite my views to work on the SQL data in the @flags object.  This should work and will prevent the 5-6 association-model-SQL queries per row on the index page, but will look very hackish.  I'd like to avoid this if possible</p></li>
<li><p>simplify my views and create additional pages for the more detailed information, to be loaded only when viewing one individual flag</p></li>
<li><p>change the model hierarchy/definitions away from polymorphic associations to inheritance.  Effectively make a module or class <code>FlaggableObject</code> that would be the parent of both <code>Subtopic</code> and <code>Post</code>.</p></li>
</ul>

<p>I'm leaning towards the third option, but I'm not certain that I'll be able to cleanly pull all the information I want using Rails' ActiveRecord helpers only.</p>

<p>I would like insight on whether this would work and, more importantly, if you you have a better solution</p>

<p>EDIT: Some nit-picky <code>include</code> behavior I've encountered</p>

<pre><code>@flags = Flag.find(:all,:conditions=&gt; "flaggable_type = 'Post'", :include =&gt; [{:flaggable=&gt;[:user,{:subtopic=&gt;:category}]},:user]).paginate(:page =&gt; 1)

=&gt; (valid response)


@flags = Flag.find(:all,:conditions=&gt; ["flaggable_type = 'Post' AND 
  post.subtopic.category_id IN ?", [2,3,4,5]], :include =&gt; [{:flaggable=&gt;
  [:user, {:subtopic=&gt;:category}]},:user]).paginate(:page =&gt; 1)

=&gt; ActiveRecord::EagerLoadPolymorphicError: Can not eagerly load the polymorphic association :flaggable
</code></pre>

## Answers
### Answer ID: 11111996
<p>Issues: Count over a polymorphic association.</p>

<pre><code>@flags = Flag.find(:all,:conditions =&gt; ["flaggable_type = 'Post' AND post.subtopic.category_id IN ?",
[2,3,4,5]], :include =&gt; [{:flaggable =&gt; [:user, {:subtopic=&gt;:category}]},:user])
.paginate(:page =&gt; 1)
</code></pre>

<p>Try like the following:</p>

<pre><code>@flags = Flag.find(:all,:conditions =&gt; ["flaggable_type = 'Post' AND post.subtopic.category_id IN ?",
[2,3,4,5]], :include =&gt; [{:flaggable =&gt; [:user, {:subtopic=&gt;:category}]},:user])
.paginate(:page =&gt; 1, :total_entries =&gt; Flag.count(:conditions =&gt; 
["flaggable_type = 'Post' AND post.subtopic.category_id IN ?", [2,3,4,5]]))
</code></pre>

### Answer ID: 6147437
<p>Don't drop the polymorphic association. Use <code>includes(:association_name)</code> to eager-load the associated objects. <code>paginate_by_sql</code> won't work, but <code>paginate</code> will.</p>

<pre><code>@flags = Flag.includes(:flaggable).paginate(:page =&gt; 1)
</code></pre>

<p>It will do exactly what you want, using one query from each table.</p>

<p>See <a href="http://guides.rubyonrails.org/association_basics.html" rel="nofollow">A Guide to Active Record Associations</a>. You may see older examples using the <code>:include</code> option, but the <code>includes</code> method is the <a href="http://m.onkey.org/active-record-query-interface" rel="nofollow">new interface</a> in Rails 3.0 and 3.1.</p>

<p><strong>Update from original poster:</strong></p>

<p>If you're getting this error: <code>Can not eagerly load the polymorphic association :flaggable</code>, try something like the following:</p>

<pre><code>Flag.where("flaggable_type = 'Post'").includes([{:flaggable=&gt;[:user, {:subtopic=&gt;:category}]}, :user]).paginate(:page =&gt; 1)
</code></pre>

<p>See comments for more details.</p>


# How templates streaming works in Rails?
[Link to question](https://stackoverflow.com/questions/28903001/how-templates-streaming-works-in-rails)
**Creation Date:** 1425658801
**Score:** 0
**Tags:** ruby-on-rails, streaming, lazy-evaluation
## Question Body
<p>In the Rails API documentation, here what is said about streaming templates.</p>

<blockquote>
  <p><strong>When to use streaming</strong></p>
  
  <p>Streaming may be considered to be overkill for lightweight actions
  like new or edit. The real benefit of streaming is on expensive
  actions that, for example, do a lot of queries on the database.</p>
  
  <p>In such actions, you want to delay queries execution as much as you
  can. For example, imagine the following dashboard action:</p>

<pre><code>def dashboard
  @posts = Post.all
  @pages = Page.all
  @articles = Article.all
end
</code></pre>
  
  <p>Most of the queries here are happening in the controller. In order to
  benefit from streaming you would want to rewrite it as:</p>

<pre><code>def dashboard
  # Allow lazy execution of the queries
  @posts = Post.all
  @pages = Page.all
  @articles = Article.all
  render stream: true
end 
</code></pre>
  
  <p>Notice that :stream only works with templates. Rendering :json or :xml with :stream won't work.</p>
</blockquote>

<p>The thing that I do not understand is, how does using <code>stream: true</code> option, will make the queries go through a lazy execution? The queries here are called before the render method, so how all this works?</p>

## Answers
### Answer ID: 29570160
<p>Those queries will already be lazy by default, regardless of <code>render stream: true</code>. That's just how <code>Model.all</code> works. It isn't until you call a method that triggers the query to actually run (e.g. <code>inspect</code> when you run this code in the rails console). See <a href="https://github.com/rails/rails/blob/f0d3c920a5aeb3babc35500e13288e148238b65e/activerecord/lib/active_record/scoping/named.rb#L24-30" rel="nofollow">https://github.com/rails/rails/blob/f0d3c920a5aeb3babc35500e13288e148238b65e/activerecord/lib/active_record/scoping/named.rb#L24-30</a>. </p>

<p>Also, for what it's worth, I believe streamed template rendering is opt-in in rails 3, but the default in rails 4. </p>


# Laravel: When call function from another controller, the relationship query not work
[Link to question](https://stackoverflow.com/questions/74130038/laravel-when-call-function-from-another-controller-the-relationship-query-not)
**Creation Date:** 1666202910
**Score:** 0
**Tags:** laravel, eloquent, controller, eloquent-relationship
## Question Body
<p>I have two controllers (FirstController, SecondController) that use the same functions, to avoid rewriting them I thought of creating another controller (ThirdController) and subsequently calling the functions through it.</p>
<p>the problem is that if in ThirdController there are relationship query they give me the error that &quot;they don't exist&quot;.</p>
<p>example:</p>
<blockquote>
<p>User Model</p>
</blockquote>
<pre><code>class User extends Authenticatable implements AuthenticatableUserContract
{
    use HasFactory, Notifiable;

    public function comments(){
        return $this-&gt;hasMany('App\Models\Comment');
}
</code></pre>
<blockquote>
<p>ThirdController</p>
</blockquote>
<pre><code>class ThirdController extends Controller
{
    public static function example($id){
        $comments = Comment::find($id)-&gt;comments();
        return $comments;
    }
}
</code></pre>
<blockquote>
<p>FirstController/SecondController</p>
</blockquote>
<pre><code>public function example2(Request $request){
    return ThirdController::example($request-&gt;id);
</code></pre>
<p>When call the route it give me error:
BadMethodCallException: Method Illuminate\Database\Eloquent\Collection::comments does not exist.</p>
<p>my questions are:</p>
<ol>
<li><p>Is there any better method instead of creating a third controller?</p>
</li>
<li><p>Is there a solution to this?</p>
</li>
</ol>
<p>p.s. I know I could very well build the queries without exploiting the relationship, but where's the beauty of that? :D</p>

## Answers
### Answer ID: 74130439
<ol>
<li><p>First thing that's not a best practice to define a <code>static method</code> in one controller and call it in another controller <strong>(not recommended way)</strong>.</p>
</li>
<li><p>Second you're calling <code>Comment::find($id)</code> with <code>comments()</code> relation. you should call a <code>User</code> class, like below snippet:</p>
</li>
</ol>
<pre><code>class ThirdController extends Controller
{
    public static function example($id){
        $comments = User::find($id)-&gt;comments();
        return $comments;
    }
}
</code></pre>
<h6>RECOMEND APPROACH:</h6>
<p>Creat a one seperate <code>service/repository</code> class in which you'll define a common method i.e. <code>getUserComments()</code> and use it in both or all of three controllers <strong>(upto your requirement/needs)</strong>. By this way you implementations will be on a  centric place.</p>
<blockquote>
<p>If you want learn about <code>Repository pattern</code> you can get basic idea from: <a href="https://www.twilio.com/blog/repository-pattern-in-laravel-application" rel="nofollow noreferrer">Article#1</a></p>
</blockquote>

### Answer ID: 74130261
<p>You do not need to create 3rd controller.  You can create a class and here you write the query in a function and use this class in controller1 and controller2 by dependency injection.</p>


# Codeigniter MVC, should i move my business logic from model into Controller to use ORM?
[Link to question](https://stackoverflow.com/questions/15614905/codeigniter-mvc-should-i-move-my-business-logic-from-model-into-controller-to-u)
**Creation Date:** 1364214329
**Score:** 2
**Tags:** php, codeigniter, design-patterns, orm, workflow
## Question Body
<p>Im trying to migrate my current project from using regular CI query builder to use an ORM since my database is growing larger and i have more that 20 FK and relation between tables.</p>

<p>so i'm currently searching for a nice orm for CI. i found IgnitedRecord but i faced a huge problem.</p>

<p>example models/users.php:</p>

<pre><code>class user extends IgnitedRecord {

public function is_loged(){
return $this-&gt;session-&gt;userdata('user');
}
</code></pre>

<p>Problem is that <code>$this</code> is not pointing to CI anymore, and it return  <code>Undefined property: user::$session</code> same with any CI class/library.</p>

<p><strong>so is there a way to fix that ?</strong> or do I need to use <code>$CI =&amp; get_instance();</code> inside each i.r. model ?</p>

<p>As <strong>my models contain most of my app business logic</strong>, I find it a bit uncomfortable to do <code>$CI =&amp; get_instance();</code> in all my models , </p>

<p>other solution would be to move all logic into controller ! OR trash this orm and stick with native query builder :p.</p>

<p>** SO next question** When using orm's (I have never used one before between) should I move my logic to controllers and only keep models for the orm !!!?? </p>

<p>that will destroy my D.R.Y mana, because a lots of time I set properties/methods into a model and access them from views/other controllers a feature that cannot be done inside controllers as I cannot reference a controller property/methode from views/other controller.</p>

<p>example of problem:</p>

<pre><code>class Auth extends CI_Controller{
public $msg='hello world';

function index(){
$this-&gt;load-&gt;view('login');
}
}


class user extends CI_MODEL{
public $msg='HELLO FROM YOUR MODEL';
}

/*VIEW */
&lt;?
echo $this-&gt;user-&gt;msg;//WORKS fine.
echo $this-&gt;auth-&gt;msg;//WILL NOT WORK. will throw an UNIDENTIFIED auth error
?&gt;
</code></pre>

<p>Also way i designed my flow usually that controller start by loading all plugins(eg: models/plugins/*.php ) these plugins set some data properties for the main model to utilize, after loading all plugins controller loads the main model and excute its logic and send result back to view :).</p>

<p>example </p>

<pre><code>models/plugins/settings.php:
    function config(){
        $this-&gt;msg = 'hello';
        $this-&gt;user = 'sam';
        return;
    }

models/hello.php
    function replace_sam (){
        $new='NONAME';
        if($this-&gt;settings-&gt;user=='sam') return $this-&gt;settings-&gt;msg.' '.$new
        else return $this-&gt;settings-&gt;msg.' '.$this-&gt;settings-&gt;user;
    }

controllers/home.php
    function index(){
        $this-&gt;load-&gt;model('plugins/settings');
        $this-&gt;settings-&gt;config();

        $this-&gt;load-&gt;model('hello');   

        echo $this-&gt;hello-&gt;replace_sam();
        //echo hello NONAME
    }
</code></pre>

<p>well i hope u got my point from this simple example.. so do you think i should rewrite every thing and move logic to controller !!</p>

<p>i appreciate your opinions. so if you think yes i should leave model for orm, then please explain to me how that would not be a huge waste !</p>

## Answers
### Answer ID: 15623502
<p>If you look at system/core/model.php, you will see that it is a very simple class. All it does is call <code>$CI =&amp; get_instance()</code> when needed. So adding that same <code>__get()</code> method to your class will make them every bit as good as the built-in ones.</p>


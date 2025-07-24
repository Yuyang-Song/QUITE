# How can I add an external code or script to Codeigniter as class library?
[Link to question](https://stackoverflow.com/questions/28809101/how-can-i-add-an-external-code-or-script-to-codeigniter-as-class-library)
**Creation Date:** 1425296994
**Score:** 0
**Tags:** codeigniter
## Question Body
<p>I have an external script or code, for example, including functions, classes, and database inside it. Is there any way to add it to Codeigniter as class library? If yes, please explain more details as possible. My script has some important files included a number of good functions and classes, even database connection and mysql queries inside, but I am confused about how to add it to Codeigniter without rewriting code lines in Codeigniter.  Suggest me some good methods to resolve my problem effectively as possible because I do not want to spend time   on rewriting and I am a new beginner of Codeigniter. Thank you very much for your help!</p>

## Answers
### Answer ID: 28809387
<p>The user guide is pretty well explained</p>

<p><a href="http://www.codeigniter.com/user_guide/general/libraries.html" rel="nofollow">http://www.codeigniter.com/user_guide/general/libraries.html</a></p>

<p><a href="http://www.codeigniter.com/user_guide/general/creating_libraries.html" rel="nofollow">http://www.codeigniter.com/user_guide/general/creating_libraries.html</a></p>

### Answer ID: 28809314
<p>go to application/library put your class into </p>

<p>Library file name lib.php</p>

<pre><code>class lib {
    public function __construct()
    {
    }
    public function test(){
       return "welcome";    
}
</code></pre>

<p>}</p>

<p>go to application->controllers</p>

<pre><code>class Hall_list extends CI_Controller {

    public function __construct()
    {
        parent::__construct();
    }
    public function index()
    {
           $this-&gt;load-&gt;library("lib");
           echo $this-&gt;lib-&gt;test();
     }
}
</code></pre>

<p>In this way you can load library to your controller</p>


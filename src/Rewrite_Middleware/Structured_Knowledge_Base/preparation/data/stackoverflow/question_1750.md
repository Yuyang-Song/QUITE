# PHP Structure - Interfaces and stdClass vars
[Link to question](https://stackoverflow.com/questions/6216801/php-structure-interfaces-and-stdclass-vars)
**Creation Date:** 1307029144
**Score:** 7
**Tags:** php, oop
## Question Body
<p>I'm building a class to handle Paypal IPNs as part of a project, and since I already know i'm going to need to use it again in at least two more upcoming jobs - I want to make sure I structure it in a way that will allow me to re-use it without having to recode the class - I just want to have to handle changes in the business logic.</p>

<p>The first part of the question is re. interfaces.  I haven't quite grasped their usefulness and when/where to deploy them.  If I have my class file ("class.paypal-ipn.php"), do I implement the interface in that file? </p>

<p>Here's what i'm working with so far (the function list is incomplete but its just for illustration):</p>

<p><strong>CLASS.PAYPAL-IPN-BASE.PHP</strong></p>

<pre><code>interface ipn_interface {

    //Database Functions
    // Actual queries should come from a project-specific business logic class
    // so that this class is reusable.

    public function getDatabaseConnection();
    public function setDatabaseVars($host="localhost",$user="root",$password="",$db="mydb");
    public function dbQuery($SQL);

    //Logging Functions

    public function writeLog($logMessage);
    public function dumpLogToDatabase();
    public function dumpLogToEmail();
    public function dumpLogToFile();

    //Business Logic Functions

    private function getTransaction($transactionID);

    //Misc Functions

    public function terminate();
}

class paypal_ipn_base {

    //nothing to do with business logic here.

    public function getDatabaseConnection() {
    }

    public function setDatabaseVars($host="localhost",$user="root",$password="",$db="mydb") {
    }

    public function dbQuery($SQL) {
    }

}
</code></pre>

<p><strong>CLASS.PAYPAL-IPN.PHP</strong></p>

<pre><code>final class paypal_ipn extends paypal_ipn_base implements ipn_interface {

    //business logic specific to each project here

    private function getTransaction($transactionID) {

       $SQL = "SELECT stuff FROM table";
       $QRY = this-&gt;dbQuery($SQL);

       //turn the specific project related stuff into something generic

       return $generic_stuff; //to be handled by the base class again.

    }

}
</code></pre>

<p><strong>Usage</strong></p>

<p>In this project: </p>

<ul>
<li>Require the class files for both the base, and the business logic class.</li>
<li>Instatiate *paypal_ipn*</li>
<li>Write code</li>
</ul>

<p>In other projects:</p>

<ul>
<li>Copy over the base IPN class</li>
<li>Edit/rewrite the business logic class *paypal_ipn* within the constraints of the interface.</li>
<li>Instantiate *paypal_ipn*</li>
<li>Write code</li>
</ul>

<p>So as you can see i'm literally just using it to define groups of related functions and add comments.  It makes it easier to read, but of what (if any) other benefit is it to me - is it so that I can pull the extender and the base class together and force errors if something is missing?</p>

<p><strong>stdClass Question</strong></p>

<p>The second part of the question is building on the readability aspect.  Within the class itself there is an ever increasing number of stored variables, some are set in the constructor, some by other functions - they relate to things such as holding the database connection vars (and the connection resource itself), whether the code should run in test mode, the settings for logging and the log itself, and so on...</p>

<p>I had started to just build them as per usual (again, below incomplete &amp; for illustration):</p>

<pre><code>$this-&gt;dbConnection = false;
$this-&gt;dbHost = "";
$this-&gt;dbUser = "";
$this-&gt;enableLogging = true;
$this-&gt;sendLogByEmail = true;
$this-&gt;sendLogTo = "user@domain.com";
</code></pre>

<p>But then I figured that the ever growing list could do with some structure, so I adapted it to:</p>

<pre><code>$this-&gt;database-&gt;connection = false;
$this-&gt;database-&gt;host = "";
$this-&gt;database-&gt;user = "";
$this-&gt;logging-&gt;enable = true;
$this-&gt;logging-&gt;sendByEmail = true;
$this-&gt;logging-&gt;emailTo = "user@domain.com";
</code></pre>

<p>Which gives me a much easier to read list of variables when I dump the entire class out as I code &amp; test.  </p>

<p>Once complete, I then plan to write a project specific extension to the generic class where i'll keep the actual SQL for the queries - as from one project to another, Paypal's IPN procedure and logic won't change - but each project's database structure will, so an extention to the class will sanitize everything back into a single format, so the base class doesn't have to worry about it and will never need to change once written.</p>

<p>So all in all just a sanity check - before I go too far down this road, does it seem like the right approach?</p>

## Answers
### Answer ID: 6217136
<p>if you are using a class autoloader, which I highly recommend, you would not want to keep the interface and the class in the same file so that the interface can autoload without needing to first load this one class that implements it.</p>

<p>For more info on autoloading:
<a href="http://php.net/manual/en/language.oop5.autoload.php" rel="nofollow">http://php.net/manual/en/language.oop5.autoload.php</a></p>

<p>another thing you may want to consider is that a given class may impliment multiple interfaces, and multiple classes may implement the same interface.</p>

<p>interfaces are primarily used for various design patterns, to enforce rules, and to decouple a class from any dependent classes. when you decouple a class from its dependencies, it makes it much easier to modify code at a later time.</p>

<p>for instance, let's say you have a class A that takes in another class B as an argument, and this class is spread throughout your code. you want to enforce that only a class with a specific subset of methods can be accepted as this argument, but you do not want to limit the input to one concrete class and it's decendants. in the future, you may write an entirely different class that does not extend class B, but would be useful as an input for class A. this is why you would use an interface. it is a reusable contract between classes.</p>

<p>some would argue that since PHP is a dynamic language, interfaces are an unecessary complication, and that duck typing may be used instead. I find in large multi-user code bases however, that interfaces can save a lot of time, letting you know more about how one class uses another, without having to study the code in depth.</p>

<p>if you find yourself with a large list of variables that you have to pass around between objects or functions, they often do end up deserving a class of their own, but each case is different.</p>

<p>-- dependency injection example --</p>

<pre><code>class A implements AInterface {
    public function foo($some_var) {}
}

interface AInterface {
    public function foo($some_var);
}

class B {
    protected $localProperty;

    // inject into the constructer. usually used if the object is saved in a property and used throughout the class
    public function __construct(AInterface $a_object) {
        $this-&gt;localProperty = $a_object;
    }

    // inject into a method. usually used if the object is only needed for this particular method
    public function someMethod(AInterface $a_object) {
        $a_object-&gt;foo('some_var');
    }
}
</code></pre>

<p>you can now see that you can write another class that impliments a foo method (and the AInterface) and use that within class B as well.</p>

<p>as a real world example (used often), say you have a database class with particular methods that interact with the database (getRecord, deleteRecord). now lets say at a later time you find a reason to switch database rdbms. you now need to use entirely different SQL statements to accomplish the same goals, but since you used an interface for your type hinting, you can simply create a new class that impliments that interface, but impliments those same methods in entirely different ways as it interacts with a different rdbms. when creating this new class, you will know exactly what methods need to be written for this new class in order to fit into the same objects that need to use a database object. if you use a container class that you use to create objects and inject them into other objects, you would not need to change too much application code in order to switch databases classes, and therefore switch database rdbms. you could even use a factory class, which could limit your changes to one line of code to make this type of change (in theory).</p>


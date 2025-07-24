# Save an array Row per Row in one query. How can I do that?
[Link to question](https://stackoverflow.com/questions/26153867/save-an-array-row-per-row-in-one-query-how-can-i-do-that)
**Creation Date:** 1412218606
**Score:** 0
**Tags:** php, mysql, arrays, survey
## Question Body
<p>I'm trying to make a survey using php and mysql but I have a little inconvinient with the code, because when I submit the form with the survey, it only saves the last question of the survey, and It is because of the INPUT name.</p>
<p>here is the code.</p>
<p>DATABASE STRUCTURE.</p>
<blockquote>
<p>&quot;Questions&quot; (idquestion, question)</p>
<p>&quot;Surveys&quot; (idsurvey, idquestion, answers, survey_number)</p>
</blockquote>
<p><strong>config.php</strong></p>
<pre><code>&lt;?php

class Connection{
    
    //variables para los datos de la base de datos
    public $server;
    public $userdb;
    public $passdb;
    public $dbname;
    
    public function __construct(){
        
        //Iniciar las variables con los datos de la base de datos
        $this-&gt;server = 'localhost';
        $this-&gt;userdb = 'root';
        $this-&gt;passdb = '';
        $this-&gt;dbname = 'sistema_bss';
        
    }
    
    public function get_connected(){
        
        //Para conectarnos a MySQL
        $con = mysql_connect($this-&gt;server, $this-&gt;userdb, $this-&gt;passdb);
        //Nos conectamos a la base de datos que vamos a usar
        mysql_select_db($this-&gt;dbname, $con);
        
        
    }
    
}

?&gt;
</code></pre>
<p><strong>Questions.php</strong></p>
<pre><code> public function show_questions(){

    $query = &quot;SELECT * FROM questions  Where questionsnumber = 1&quot;;
    $this-&gt;result = $this-&gt;objDb-&gt;select($query);
    return $this-&gt;result;       
    
}

public function new_survey(){
        
    
        
        $query = &quot;INSERT INTO survey VALUES('',  
        
            '&quot;.$_POST[&quot;questi&quot;].&quot;', 
            '&quot;.$_POST[&quot;answer&quot;].&quot;')&quot;;
        $this-&gt;objDb-&gt;insert($query);
                
        
    }   

            
</code></pre>
<p><strong>Survey_form.php</strong></p>
<p>hint: The form it's ok, it execute the query but the problem is, that it only store one question and answer of the survey, instead store all the questions and answers (array's rows) at the time.</p>
<pre><code>   &lt;form name=&quot;newDona&quot; action=&quot;new_survey_exe.php&quot; method=&quot;post&quot; value= &quot;&quot;&gt;

 &lt;?php
            
            //it calls the function that shows all the questions that are stored in the db
                $numrows = mysql_num_rows($survey);
                
            if($numrows &gt; 0){
                
                while($row=mysql_fetch_array($survey)){?&gt;
                    
                
                        
                        &lt;td&gt;
                    
                        &lt;?php 
                        
                        
                        echo $row[&quot;question&quot;];?&gt;&lt;/td&gt;
                    
                        
                        
                        
                          &lt;th&gt;&lt;select name=&quot;answer&quot; &gt;
                
                        &lt;option value=&quot;&quot;&gt;&lt;/option&gt;
                        &lt;option value=&quot;yes&quot;&gt;yes&lt;/option&gt;
                        &lt;option value=&quot;NO&quot;&gt;NO&lt;/option&gt;
                    
                    &lt;/select&gt;
                        
                        &lt;tr&gt;&lt;td colspan=&quot;5&quot; align=&quot;center&quot;&gt;&lt;input type=&quot;submit&quot; name=&quot;send&quot; id=&quot;send&quot; value=&quot;SAVE&quot; /&gt;&lt;/td&gt;&lt;/tr&gt;
            
                            
</code></pre>
<p>I think the problem is the &quot;select&quot; name, maybe because it rewrites the other  questions and answers for every question of the survey so it only stores the last question and answer.</p>
<p>I want to store multiple rows using one form :D</p>
<p>Thanks in advance. :)</p>

## Answers
### Answer ID: 26154227
<p>Here is your answer. Your insert command was not assigning columns, just values:</p>

<p><strong>USE PDO CONNECTION OUTSIDE OF CLASS</strong></p>

<p>In your case, if you want to just run sql queries you will want to use the raw format of the DB. That requires two changes in my DBEngine. Where it says <code>protected   $con;</code> change it to <code>public   $con;</code> then when you want to call any kind of sql statement do as follows:</p>

<pre><code>// If the DB is already set don't do this step portion
require_once('includes/classes/dbconnect.php');
$db =   new DBConnect('localhost','sistema_bss','root','');
// Here is where you use the PDO class

$query = $db-&gt;con-&gt;prepare("SELECT MAX(surveynumber) FROM survey");
$query-&gt;execute();

if($query-&gt;rowCount()&gt;0) {
        while($result = $query-&gt;fetch(PDO::FETCH_ASSOC)) {
        print_r($result);
    }
}
</code></pre>

<p><strong>newsurvey.php</strong></p>

<pre><code>&lt;?php
    // Not sure if this is proper path back to root then back
    //to files, so you'll have to fix that if wrong
    // Include db
    require_once('includes/classes/dbconnect.php');
    // Include questions class
    require_once('apps/survey/classes/questions.php');
    // Create connection
    $con    =   new DBConnect('localhost','sistema_bss','root','');

    // If answers not submitted, show form
    if(!isset($_POST['answer'])) {
            include_once('apps/survey/new.form.php');
        }
    // If answers submitted process the form
    else {
            // Create questions class, forward DB connection
            $objDona = new Questions($con);
            // Run the insert class 
            $objDona-&gt;NewSurveyMulti($_POST['answer']);
            $display    =   $con-&gt;Fetch("select * from survey");
            print_r($display);
        } ?&gt;
</code></pre>

<p><strong>new.form.php</strong></p>

<pre><code>&lt;?php
    // Fetch questions
    $cuestionario   =   $con-&gt;Fetch("SELECT * FROM questions"); ?&gt;

    &lt;form name="newDona" action="" method="post"&gt;
    &lt;/table&gt;&lt;?php
    // Confirm there are questions being drawn from database
    $numrows        =   (is_array($cuestionario))? count($cuestionario): 0;
    if($numrows &gt; 0) {
            // Loop through questions
            foreach($cuestionario as $row) { ?&gt;
            &lt;tr&gt;
                &lt;!-- Write the question --&gt;
                &lt;td&gt;&lt;?php echo $row["question"];?&gt;&lt;/td&gt;
            &lt;/tr&gt;
            &lt;th&gt;
                &lt;!-- Set the question id --&gt;
                &lt;select name="answer[&lt;?php echo $row['idquestion']; ?&gt;][]"&gt;
                    &lt;option value=""&gt;&lt;/option&gt;
                    &lt;option value="1"&gt;yes&lt;/option&gt;
                    &lt;option value="no"&gt;NO&lt;/option&gt;
                &lt;/select&gt;
            &lt;/th&gt;&lt;?php } ?&gt;
            &lt;tr&gt;
                &lt;td colspan="5" align="center"&gt;
                    &lt;input type="submit" name="send" id="send" value="SAVE" /&gt;
                &lt;/td&gt;
            &lt;/tr&gt;
        &lt;/table&gt;
    &lt;/form&gt;
    &lt;?php } ?&gt;
</code></pre>

<p><strong>dbconnect.php</strong></p>

<pre><code>&lt;?php
    // I'm adding my PDO database because yours is deprecated
    class DBConnect
        {
            public   $con;
            // Create a default database element
            public  function __construct($host = '',$db = '',$user = '',$pass = '')
                {
                    try {
                            $this-&gt;con  =   new PDO("mysql:host=$host;dbname=$db",$user,$pass, array(PDO::ATTR_ERRMODE =&gt; PDO::ERRMODE_WARNING));
                        }
                    catch (Exception $e) {
                          return 0;
                        }
                }

            // Simple fetch and return method
            public  function Fetch($_sql)
                {
                    $query  =   $this-&gt;con-&gt;prepare($_sql);
                    $query-&gt;execute();

                    if($query-&gt;rowCount() &gt; 0) {
                            while($array = $query-&gt;fetch(PDO::FETCH_ASSOC)) {
                                    $rows[]   =   $array;
                                }
                        }

                    return (isset($rows) &amp;&amp; $rows !== 0 &amp;&amp; !empty($rows))? $rows: 0;
                }

            // Simple write to db method
            public  function Write($_sql)
                {
                    $query  =   $this-&gt;con-&gt;prepare($_sql);
                    $query-&gt;execute();
                }
        } ?&gt;
</code></pre>

<p><strong>questions.php</strong></p>

<pre><code>&lt;?php
        class Questions
            {
                //atributos
                public $nameDono;
                public $objDb;
                public $result;
                public $connect;

                public function __construct($dbconnection){
                        // My PDO connection
                        $this-&gt;MyDB     =   $dbconnection;
                    }

                public function NewSurveyMulti($answer = array())
                    {
                        if(!empty($answer)) {
                                foreach($answer as $questi =&gt; $value) {
                                        $this-&gt;MyDB-&gt;Write("INSERT INTO survey (`idquestion`,`answers`) VALUES('".$questi."', '".$value[0]."')");
                                    }
                            }
                    }

                public function mostrar_survey()
                    {
                        $this-&gt;result = $this-&gt;MyDB-&gt;Fetch("SELECT * FROM questions");
                        return $this-&gt;result;       
                    }

                public function new_survey()
                    {
                        $this-&gt;MyDB-&gt;Write("INSERT INTO survey (`idquestion`,`answers`,`surveynumber`) VALUES("'".$_POST["questi"]."','".$_POST["answer"]."','".$_POST["numsurvey"]."')");
                    }  
            } ?&gt;
</code></pre>

### Answer ID: 26164004
<p>Here is the code Rasclatt</p>

<p><strong>QUESTIONS.PHP</strong></p>

<pre><code>&lt;?php

    class Questions{

        //atributos
        public $nameDono;
        public $objDb;
        public $result;

        public function __construct(){ 

            $this-&gt;objDb = new Database();

        }



        public function NewSurveyMulti($answer) {
                    if(!empty($answer)) {
                            foreach($answer as $questi =&gt; $value) {
                                    $query = "INSERT INTO survey VALUES('','".$questi."', '".$value."')";
                                    $this-&gt;objDb-&gt;insert($query);
                                }
                        }
                }


                // I don't know what the class name is but this is how
    // you would apply this method


    //--------------------------------I don't know where I have to put it, the class name is Questions.
     if(isset($_POST['answer']))
         Questions-&gt;NewSurveyMulti($_POST['answer']);



                //this functions shows all the questions for the survey
        public function mostrar_survey(){

            $query = "SELECT * FROM questions ";
            $this-&gt;result = $this-&gt;objDb-&gt;select($query);
            return $this-&gt;result;       

        }
        }

    ?&gt;
</code></pre>

<p><strong>Survey_form.php</strong></p>

<pre><code> &lt;?php
    require'../class/questions.php';

        $cuestionario= $objBdonar-&gt;show_questions();
        $survey= $objBdonar-&gt;NewSurveyMulti($answer) ;

     &lt;form name="newDona" action="new_survey_exe.php" method="post"&gt;
    &lt;/table&gt;&lt;?php


    //it calls the function that shows all the questions that are stored in the db
    $numrows = mysql_num_rows($cuestionario);
    if($numrows &gt; 0) {
            while($row = mysql_fetch_array($cuestionario)) { ?&gt;
            &lt;tr&gt;
                &lt;td&gt;
                    &lt;?php echo $row["question"];?&gt;
                &lt;/td&gt;
            &lt;/tr&gt;
            &lt;th&gt;
                &lt;select name="answer[&lt;?php echo $row['questi']; ?&gt;][]"&gt;
                    &lt;option value=""&gt;&lt;/option&gt;
                    &lt;option value="yes"&gt;yes&lt;/option&gt;
                    &lt;option value="NO"&gt;NO&lt;/option&gt;
                &lt;/select&gt;
            &lt;/th&gt;&lt;?php } ?&gt;
            &lt;tr&gt;
                &lt;td colspan="5" align="center"&gt;
                    &lt;input type="submit" name="send" id="send" value="SAVE" /&gt;
                &lt;/td&gt;
            &lt;/tr&gt;
        &lt;/table&gt;
    &lt;/form&gt;
    &lt;?php } ?&gt;
</code></pre>

<p><strong>New_survey_exe.php</strong></p>

<pre><code>&lt;?php

require'../class/questions.php';
$objCon = new Connection();
$objCon-&gt;get_connected();
$objDona = new Questions();

$objDona-&gt;NewSurveyMulti($answer) ;


header('Location: ' . $_SERVER['HTTP_REFERER']);    

?&gt;
</code></pre>


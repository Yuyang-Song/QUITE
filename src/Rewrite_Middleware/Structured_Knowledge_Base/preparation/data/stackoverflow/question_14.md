# PHP Asynchronous Method Call In The Yii Framework
[Link to question](https://stackoverflow.com/questions/10284966/php-asynchronous-method-call-in-the-yii-framework)
**Creation Date:** 1335200761
**Score:** 11
**Tags:** php, mysql, events, asynchronous, yii
## Question Body
<h1>Question</h1>

<p>I want to know if it is possible to asynchronously invoke a Yii controller method from one of its actions while the action renders a view, leaving the method to complete a long running operation. I would love to do something like the code below and I don't need to return a result from <code>my_long_running_func</code>.</p>

<pre><code>public function actionCreate() {
    $model = new Vacancies;
    if (isset($_POST['Vacancies'])) {
        $model-&gt;setAttributes($_POST['Vacancies']);
        $model-&gt;save();
        //I wish :)
        call_user_func_async('my_long_running_func',$model);
    }
    $this-&gt;render('create', array( 'model' =&gt; $model));
}
</code></pre>

<h2>Problem</h2>

<p>I am trying to write a controller action in Yii that posts a vacancy and notifies interested subscribers of the post. The problem is that it takes a long time to execute the notification query.</p>

<p>Now I am searching for a way to asynchronously run the query so the poster sees his response in as little time as possible while the query runs in the background in a way similar to C# delegates or events.</p>

<p>The solutions I googled up performed <em>asynchronous request(s)</em> during the course of the controller action but all I want to do is to run a method of the controller asynchronously and the action had to <em>wait</em> till the <em>request(s)</em> were completed.</p>

<h2>Attempted</h2>

<p>I have tried the following methods but the query is still slow for my test data of about 1500 users.</p>

<ul>
<li><p>Yii ActiveRecord</p>

<pre><code>if ($vacancy-&gt;save()) {                
    if($vacancy-&gt;is_active == 1) {
        $url = Yii::app()-&gt;createUrl('vacancies/view',array('id'=&gt;$model-&gt;id));
        $trainees = YumUser::getUsersByRole('Trainees');
        if($trainees!=null) {
            foreach($trainees as $trainee){
                $message = new YumMessage;
                $message-&gt;from_user_id = Yii::app()-&gt;user-&gt;id;
                $message-&gt;title = 'Vacancy Notification: '.date('M j, Y');
                $message-&gt;message = "A new vacancy has been posted at &lt;a href='{$url}'&gt;{$url}&lt;/a&gt;.";
                $message-&gt;to_user_id = $trainee-&gt;id;
                $message-&gt;save();                
            }
        }
    }    
}
</code></pre></li>
<li><p>Yii Data Access Objects</p>

<pre><code>if ($vacancy-&gt;save()) {        
    if($vacancy-&gt;is_active == 1) {
        $url = Yii::app()-&gt;createAbsoluteUrl('vacancies/view',array('id'=&gt;$model-&gt;id));
        $trainee_ids=Yii::app()-&gt;db-&gt;createCommand()-&gt;select('user_id')-&gt;from('trainee')-&gt;queryColumn();
        $fid=Yii::app()-&gt;user-&gt;id;
        $msg="A new vacancy has been posted at &lt;a href='{$url}'&gt;{$url}&lt;/a&gt;.";
        $ts = time();
        $tt = 'Vacancy Notification: '.date('M j, Y');
        if($trainee_ids!=null) {
            foreach($trainee_ids as $trainee_id){
                Yii::app()-&gt;db-&gt;createCommand()
                  -&gt;insert('message',array('timestamp'=&gt;$ts,'from_user_id'=&gt;$fid,'to_user_id'=&gt;$tid,'title'=&gt;$tt,'message'=&gt;$msg));
            }
        }
    }
}
</code></pre></li>
<li><p>Prepared Statements</p>

<pre><code>if ($vacancy-&gt;save()) {                
    if($vacancy-&gt;is_active == 1) {
        $url = Yii::app()-&gt;createUrl('vacancies/view',array('id'=&gt;$model-&gt;id));                    
        $trainee_ids=Yii::app()-&gt;db-&gt;createCommand()-&gt;select('user_id')-&gt;from('trainee')-&gt;queryColumn();
        $fu=Yii::app()-&gt;user-&gt;id;
        $msg="A new vacancy has been posted at &lt;a href='{$url}'&gt;{$url}&lt;/a&gt;.";
        $ts = time();
        $tt = 'Vacancy Notification: '.date('M j, Y');
        $sql="INSERT INTO message (timestamp,from_user_id,title,message,to_user_id) VALUES (:ts,:fu,:tt,:msg,:tu)";
        if($trainee_ids!=null) {
            foreach($trainee_ids as $trainee_id){

                $command=Yii::app()-&gt;db-&gt;createCommand($sql);
                $command-&gt;bindParam(":ts",$ts,PDO::PARAM_INT);
                $command-&gt;bindParam(":fu",$fu,PDO::PARAM_INT);
                $command-&gt;bindParam(":tt",$tt,PDO::PARAM_STR);
                $command-&gt;bindParam(":msg",$msg,PDO::PARAM_STR);
                $command-&gt;bindParam(":tu",$trainee_id,PDO::PARAM_INT);

                $command-&gt;execute();

            }
        }
    }
}
</code></pre></li>
</ul>

<h2>Research</h2>

<p>I have also checked the following websites (I'm only allowed to post two links) but they either require the action to wait for the request to be completed or need curl (which I don't have access to on the deployment server) or need an external library. I was hoping for a native PHP implementation. </p>

<ul>
<li>PHP Simulated Multi-Threading</li>
<li>Multithreading in php</li>
<li><a href="https://stackoverflow.com/questions/124462/asynchronous-php-calls">Asynchronous PHP calls?</a></li>
<li><a href="http://css.dzone.com/articles/asynchronous-processing-php" rel="nofollow noreferrer">Asynchronous processing in PHP</a></li>
</ul>

<h2>Edit</h2>

<p>I was able to decrease response time considerably by rewriting my query in this way (moving the user loop to the database layer):</p>

<pre><code>public function actionCreate() {
    $user=YumUser::model()-&gt;findByPk(Yii::app()-&gt;user-&gt;id);
    $model = new Vacancies;
    $model-&gt;corporate_id=$user-&gt;professional-&gt;institution-&gt;corporate-&gt;id;
    $model-&gt;date_posted=date('Y-m-d');
    $model-&gt;last_modified=date('Y-m-d H:i:s');

    if (isset($_POST['Vacancies'])) {
        $model-&gt;setAttributes($_POST['Vacancies']);
        if ($model-&gt;save()) {                
            if($model-&gt;is_active == 1) {
                $url = Yii::app()-&gt;createAbsoluteUrl('vacancies/view',array('id'=&gt;$model-&gt;id));                    
                $fu=Yii::app()-&gt;user-&gt;id;
                $msg="A new vacancy has been posted at &lt;a href='{$url}'&gt;{$url}&lt;/a&gt;.";
                $ts = time();
                $tt = 'New Vacancy: '.$model-&gt;title;
                $sql='INSERT INTO message (timestamp,from_user_id,title,message,to_user_id) SELECT :ts,:fu,:tt,:msg,t.user_id FROM trainee t';
                Yii::app()-&gt;db-&gt;createCommand($sql)-&gt;execute(array(':ts'=&gt;$ts,':fu'=&gt;$fu,':tt'=&gt;$tt,':msg'=&gt;$msg));
            }                
            if (Yii::app()-&gt;getRequest()-&gt;getIsAjaxRequest())
                Yii::app()-&gt;end();
            else
                $this-&gt;redirect(array('view', 'id' =&gt; $model-&gt;id));
        }
    }
    $this-&gt;render('create', array( 'model' =&gt; $model));
}
</code></pre>

<p>Notwithstanding, it would be nice if someone could post a way to call functions asynchronously.</p>

## Answers
### Answer ID: 21980730
<p>Typically, the solution for these kind of problems would be to integrate a message-bus in your system. You could consider a product like <a href="http://kr.github.io/beanstalkd/" rel="nofollow noreferrer">Beanstalkd</a>. This requires installing software on your server.
I suppose this suggestion would be called "using an external library".</p>

<p>If you can access the deployment server and you can add cronjob (or maybe a sysadmin can) you could consider a cronjob that does a php-cli call to a script that reads jobs from a job queue in your database which is filled by the controller method.</p>

<p>If you cannot install software on the server you're running, you could consider using a SAAS solution like <a href="http://www.iron.io/" rel="nofollow noreferrer">Iron.io</a> to host the bus functionality for you. Iron.io is using what is called a <em>push queue</em>. With a push queue the message bus actively performs a request (push) to the registered listeners with the message content. This might work since it doesn't require you to do a curl request.</p>

<p>If none of the above is possible, your hands are tied. Another post which is quite relevant on the subject: <a href="https://stackoverflow.com/questions/3115191/scalable-delayed-php-processing">Scalable, Delayed PHP Processing</a> </p>

### Answer ID: 10286535
<p>Here's an entirely different type of suggestion.  What about registering for the onEndRequest event that is fired by <a href="http://www.yiiframework.com/doc/api/1.1/CApplication#end-detail" rel="nofollow">CWebApplication's end() function</a>?</p>

<pre><code>public function end($status=0, $exit=true)
{
    if($this-&gt;hasEventHandler('onEndRequest'))
        $this-&gt;onEndRequest(new CEvent($this));
    if($exit)
        exit($status);
}
</code></pre>

<p>You'd need to register for the event and figure out how to pass your model in somehow, but the code would properly run after all the data has been flushed to the browser ...</p>

### Answer ID: 10285543
<p>I would try this, though I'm not 100% that Yii will work properly, but its relatively simple and worth a go: </p>

<pre><code>public function actionCreate() {
    $model = new Vacancies;
    if (isset($_POST['Vacancies'])) {
        $model-&gt;setAttributes($_POST['Vacancies']);
        $model-&gt;save();
        //I wish :)
    }

    HttpResponse::setContentType('text/html');
    HttpResponse::setData($this-&gt;render('create', array( 'model' =&gt; $model), true);
    HttpResponse::send();

    flush(); // writes the response out to the client

    if (isset($_POST['Vacancies'])) {
        call_user_func_async('my_long_running_func',$model);
    }
}
</code></pre>


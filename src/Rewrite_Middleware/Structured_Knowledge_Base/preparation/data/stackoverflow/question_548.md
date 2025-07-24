# Turning app offline/online on demand?
[Link to question](https://stackoverflow.com/questions/31180544/turning-app-offline-online-on-demand)
**Creation Date:** 1435828817
**Score:** 2
**Tags:** php, yii
## Question Body
<p>we are developing a browser game with Flash (front-end) and Yii 1.1.16 - PHP (Back-end). The game server is a yii web-app that receives requests from the client for the game to progress. Our intent is to have at some point multiple servers.</p>

<p><strong>What I want to do:</strong> From a central admin panel that we have built I want to be able to set a game server (yii web app) offline with a press of a button and then turn it on.</p>

<p>I have thought of two ways of doing this, one seems more logical from the other, but I want opinions on best practice.</p>

<p><strong>1)</strong> The first method is to store in the database a boolean field (isOnline) and read it with a select before each action. If it is false I will render the appropriate view informing the requester of the server being offline. The lead programmer is not so fond of this idea because he doesn't want to have one extra query to the database for every request (Do you think it is such a burden?).</p>

<p><strong>2)</strong> So because of the "problem" above I came up with a different solution that does not use the database. Instead I am using files, in yii fashion. Whenever I want to turn on/off the app I rewrite a file that contains a bool. Then I read this bool before every action/request. Some code follows:</p>

<p>In config/main.php I add this to params:</p>

<pre><code>'params'=&gt;array(
    'isOnline' =&gt; require(dirname(__FILE__).'/online.php'),
    ...
)
</code></pre>

<p>the config/online.php file is just this:</p>

<pre><code>&lt;?php
//param that decides if server is online or not
return false;
</code></pre>

<p>And in Controller beforeAction I have this:</p>

<pre><code>//If server is offline
if(!Yii::app()-&gt;params['isOnline'] )
{
    //allow only 'switch' action
    if(Yii::app()-&gt;controller-&gt;id.'/'.Yii::app()-&gt;controller-&gt;action-&gt;id == 'test/switch')
    {
        return true;
    }
    //else diplay offline view
    $this-&gt;renderPartial('//site/offline');
    Yii::app()-&gt;end();
}
</code></pre>

<p>In order to change the online status (the action needs improvement, it just works for now):</p>

<pre><code>public function actionSwitch ()
{
    //Get online input, TODO add input checks
    $isOnline = $_GET['online'];

    //Create online.php file contents, using a simple view with an echo inside
    $fileContent = $this-&gt;renderPartial('//site/online', array('online' =&gt; $isOnline), true);

    //Open config/online.php file
    $file = fopen(dirname(__FILE__).DIRECTORY_SEPARATOR.'..'.DIRECTORY_SEPARATOR.'config'.DIRECTORY_SEPARATOR.'online.php', 'w');

    //Write new content to file
    fwrite($file, $fileContent);

    //Close file
    fclose($file);
} 
</code></pre>

<p>Personally I prefer the first approach and I have doubts about the security of the second approach. What are your opinions (generally and then taking into consideration my colleagues disaproval of the db solution)? Any other approach?</p>

<p>Thanks a lot in advantange. </p>

## Answers
### Answer ID: 31754344
<p>Personaly for that simple case, I'd choose your first option plus <a href="https://dev.mysql.com/doc/refman/5.5/en/memory-storage-engine.html" rel="nofollow">Mysql Memory Storage Engine</a>.
You will have the same performance as a cache, without the infraestructure to implement it. While memory comsuption will be mimimal for a one record table. </p>

### Answer ID: 31754073
<p>Is much better to use this extension <a href="https://github.com/ekaragodin/MaintenanceMode" rel="nofollow">https://github.com/ekaragodin/MaintenanceMode</a></p>

<p>The only I had added a condition into <code>init</code> method of <code>MaintenanceMode.php</code>, as I store settings in DB.</p>

<p><em>main.php</em></p>

<pre><code>// First of all I initiate my settings component, to able getting required options from DB
'preload' =&gt; array('log','setting','maintenanceMode'),
</code></pre>

<p><em>MaintenanceMode.php</em></p>

<pre><code>public function init(){
    if ( !$this-&gt;enabledMode ) {
        return;
    }

    // Then check your flag
    if ( !Yii::app()-&gt;setting-&gt;is_offline ) {
        return;
    }
    // ...
</code></pre>

<p>With this extension you may switch off via main.php just set enabledMode false. Or you may write value into the file and then read it. Also you may setup cache.</p>


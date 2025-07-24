# codeigniter nodejs and nowjs integration
[Link to question](https://stackoverflow.com/questions/8364642/codeigniter-nodejs-and-nowjs-integration)
**Creation Date:** 1322874363
**Score:** 3
**Tags:** php, mysql, codeigniter, node.js, nowjs-sockets
## Question Body
<p>I am trying to integrate nodejs and nowjs with codeigniter framework, As I dont have time to rewrite the whole site I want to check if a user is logged in. I am using ion_auth and I am storing the session in db.</p>

<p><strong>Client js:</strong></p>

<pre><code>var session_id = $.cookie('sc_session');

$("form").submit(function() {
    now.distributeMessage($("textarea").val(),session_id);
});

now.receiveMessage = function(message){
    $("body").append("&lt;br&gt;" + message);
};
</code></pre>

<p><strong>Heres the nodejs server code:</strong></p>

<p><strong>EDIT</strong>:*<em>Simplified it a little, and get session cookie from client js</em>*</p>

<pre><code>everyone.now.distributeMessage = function(message,session_cookie) {
    exec('php index.php user_session decrypt ' + encodeURIComponent(session_cookie),
    function (error, stdout, stderr) {
        var parts = stdout.split(';');
        var session_id = parts[1].split(':')[2];
        var query = 'select * from sc_sessions where session_id=' + session_id;
        client.query(query, function (err, results, fields) {
            if (results) {
                everyone.now.receiveMessage(str);
            }
        });
    });
};
</code></pre>

<p><strong>And here is the controller called by nodejs:</strong></p>

<pre><code>&lt;?php if (!defined('BASEPATH')) exit('No direct script access allowed');

class User_session extends CI_Controller
{
  public function __construct()
  {
    parent::__construct();
    if (!$this-&gt;input-&gt;is_cli_request()) {
        redirect('index');
    }
  }

  public function decrypt($session_id)
  {
    $this-&gt;load-&gt;library('encrypt');
    $session_id = urldecode($session_id);
    echo $this-&gt;encrypt-&gt;decode($session_id);
  }
}
</code></pre>

<p>It is working and i can log the user_data to the console from the session in database, and it calls the everyone.now.receiveMessage function properly.</p>

<p>I have three questions regarding this:</p>

<p>1) there are rows inserted into the sc_sessions db table with a session_id but with empty user_data, user_agent and ip 0.0.0.0. One row each time the form is submitted.</p>

<p>What is causing this and how do i fix it?</p>

<p>I know that there is a problem with ajaxcalls and codeigniter sessions. See this thread:</p>

<p>Is there a way to see if the request was made with websockets?</p>

<p>2) What is the best way to check if the user is logged in? e.g if statement where you check to see if the query returned anything or is there a better method?</p>

<p>3) Is there a better method of doing this?</p>

<p>Any help appreciated as I am stuck on this.</p>

<p>George</p>

<p><strong>EDIT</strong>:
Calling the script from commandline caused it to create a new session. Prevent it by extending the session class.</p>

<p>application/libraries/MY_Session.php</p>

<pre><code>&lt;?php
class MY_Session extends CI_Session {

    public function __construct()
    {
        $CI = get_instance();

        if ($CI-&gt;input-&gt;is_cli_request())
        {
             return;
        }

        parent::__construct();
    }  
}
</code></pre>

## Answers
### Answer ID: 8393305
<p>Great question, but lots of overhead to test an answer.</p>

<p>My best guess is CLI doesn't pass environmental variables like user_agent and ip.  Those are handled by apache, and aren't relevant in CLI requests natively.  I'd go by session_id alone if you know it's secure in a node environment.</p>


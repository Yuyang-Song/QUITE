# how can I get a facebook Page access token from a users access token using php?
[Link to question](https://stackoverflow.com/questions/17110185/how-can-i-get-a-facebook-page-access-token-from-a-users-access-token-using-php)
**Creation Date:** 1371218103
**Score:** 0
**Tags:** facebook, token, impersonation
## Question Body
<p>I am trying to get a page access token starting out with just a users access token stored in my database and a page id.  So far I have not been using the facebook.php instead just using php's curl_* functions.  So far I can send posts to the page (with a hard coded page id) but I want to impersonate the page when doing so.  </p>

<p>Can I do this easily without facebook.php, that would be nice as it might save me from feeling like I should  rewrite what I've done so far. If not, then how would I get the page access token from the facebook object  - remember so far at least I don't store user ids or page ids in my db, just user access tokens and of course my app id and secret.</p>

<p>I've been looking at the example for getting page access tokens but I find it not quite what I need as it gets a user object and in so doing   seems to force the user to login to facebook each time, but I stored the user access token to avoid exactly that from happening.</p>

<p>Do I need more permissions than manage_page and publish_stream?  I tried adding offline_access but it doesn't seem available anymore (roadmap mentions this).</p>

<p>here is some of my code from my most recent attempt which uses the facebook.php file:  </p>

<pre><code>  // try using facebook.php
    require_once 'src/facebook.php';
    // Create our Application instance 
    $facebook = new Facebook(array(
      'appId'  =&gt; $FB_APP_ID,      // $FB_APP_ID      hardcoded earlier
      'secret' =&gt; $FB_APP_SECRET,  // $FB_APP_SECRET  hardcoded earlier
    ));

    $facebook-&gt;setAccessToken($FB_ACCESS_TOKEN );
        //got user access token  $FB_ACCESS_TOKEN from database
    // Get User ID -- why?
    $user = $facebook-&gt;getUser();

    //------ get PAGE access token
    $attachment_1 = array(
        'access_token' =&gt; $FB_ACCESS_TOKEN
    );

    $result = $facebook-&gt;api("/me/accounts", $attachment_1);
    foreach($result["data"] as $page) {
        if($page["id"] == $page_id) {// $page_id hardcoded earlier
            $page_access_token = $page["access_token"];

            break;
        }
    }
    echo '&lt;br/&gt;'.__FILE__.' '.__FUNCTION__.' '.__LINE__.' $result= ' ; 
    var_dump($result); //this prints: array(1) { ["data"]=&gt; array(0) { } }  
    $facebook-&gt;setAccessToken($page_access_token );
    // Get User ID, why - re-init with new token maybe?
    $user = $facebook-&gt;getUser();



    //------ write to page wall
    try {
        $attachment = array(
                    'access_token' =&gt; $page_access_token,
                    'link'          =&gt; $postLink,
                    'message'=&gt;  $postMessage
            );

        $result = $facebook-&gt;api('/me/feed','POST', $attachment);
        echo '&lt;br/&gt;'.__FILE__.' '.__FUNCTION__.' '.__LINE__.' $result= ' ; 
        var_dump($result);

    } catch(Exception $e) {
         echo '&lt;br/&gt;'.__FILE__.' '.__FUNCTION__.' '.__LINE__.' $e= ' ; 
         var_dump($e);   /*this gives : "An active access token must
                           be used to query information about the 
                           current user." */

    }
    die;
</code></pre>

<p>Thanks</p>

<p>PS:  I hardcoded the user id and started calling  </p>

<pre><code>$result = $facebook-&gt;api("/$user_id/accounts", $attachment_1);
</code></pre>

<p>and I still get an empty result. </p>

<p>PPS: The Graph API Explorer does not show my fan pages either  even though my account is set as the Manager.  My attempts to post work but show as being from my account rather than from the page.</p>

<p>PPPS: made a little progress by adding permissions on the graph explorer  page to get an access token that way but that doesn't help as I need to the the access token programmatically. When a user with many fan pages logs in to my site I want to show them the list of their facebook  fan pages  to choose from. In practice aren't the permissions just granted on the app?   </p>

<p>PPPPS: the list of permissions on my app now stands at : email, user_about_me, publish_actions 
and
Extended Permissions:
manage_pages, publish_stream, create_note, status_update, share_item
do I need more? when I try now I still fail to get anything from the call to: </p>

<p><code>$facebook-&gt;api("/$user_id/accounts", $attachment_1);</code> </p>

<p>Px5S:  DOH!!!  I see now that I was neglecting to add the manage_pages permissions to my call for a user access token when my scripts first get one and store it in the DB.  But when I reuse that new access token I still get the error : "An active access token must be used to query information about the current user." So, can't such tokens be reused?  Aren't they long term? will read more stuff...</p>

## Answers
### Answer ID: 17172146
<p>Here is my functioning code, still messy but seems to work, note the scopes on the first $dialog_url, and please feel free to mock my code or even suggest improvements  :</p>

<pre><code>function doWallPost($postName='',$postMessage='',$postLink='',$postCaption='',$postDescription=''){

global $FB_APP_ID, $FB_APP_SECRET; 

$APP_RETURN_URL=((substr($_SERVER['SERVER_PROTOCOL'],0,4)=="HTTP")?"http://":"https://").$_SERVER['HTTP_HOST'].$_SERVER['SCRIPT_NAME'].'?returnurl=1';

$code = $_REQUEST["code"];

$FB_ACCESS_TOKEN = getFaceBookAccessToken( );
$FB_ACCESS_TOKEN_OLD = $FB_ACCESS_TOKEN;


//if no code ot facebook access token get one
if( empty($code) &amp;&amp; empty($FB_ACCESS_TOKEN) &amp;&amp; $_REQUEST["returnurl"] != '1')  
{      
     // if(  $_REQUEST["returnurl"] == '1') die;
     $dialog_url = "http://www.facebook.com/dialog/oauth?client_id=".$FB_APP_ID."&amp;redirect_uri=".$APP_RETURN_URL."&amp;scope=publish_stream,manage_pages";                  
     header("Location:$dialog_url");
}


if( empty($FB_ACCESS_TOKEN) ){ 

    if($_REQUEST['error_code'] == '200'){
        return null;
     }else if (!empty($code)){        
        $token_url = "https://graph.facebook.com/oauth/access_token?client_id=".$FB_APP_ID."&amp;redirect_uri=".urlencode($APP_RETURN_URL)."&amp;client_secret=".$FB_APP_SECRET."&amp;code=".$code;   
        $access_token = file_get_contents($token_url);  
        $param1=explode("&amp;",$access_token);
        $param2=explode("=",$param1[0]);
        $FB_ACCESS_TOKEN=$param2[1];    
    }else{
        return null;
    }
}
if(!empty($FB_ACCESS_TOKEN) &amp;&amp; $FB_ACCESS_TOKEN_OLD != $FB_ACCESS_TOKEN)  {
    setFaceBookAccessToken( $FB_ACCESS_TOKEN);
}

$_SESSION['FB_ACCESS_TOKEN'] = $FB_ACCESS_TOKEN;

$page_name = '';
$page_id =   getFaceBookPageId(); //from db

if(empty($page_id ) ) return null;
//in case there are multiple page_ids separated by commas  
if(stripos($page_id, ',') !== false ){
   $page_ids = explode(',', $page_id)   ;// = substr($page_id, 0, stripos($page_id, ','));
}
$result = null;
foreach($page_ids as $page_id){
    $page_id = trim($page_id);
if( !empty($FB_ACCESS_TOKEN)){ 
    //get page_id
    require_once 'src/facebook.php';
    // Create our Application instance (replace this with your appId and secret).
    $facebook = new Facebook(array(
      'appId'  =&gt; $FB_APP_ID,
      'secret' =&gt; $FB_APP_SECRET 
    ));  

    $facebook-&gt;setAccessToken($FB_ACCESS_TOKEN ); 

    //------ get PAGE access token
    $page_access_token ='';
    $attachment_1 = array(
        'access_token' =&gt; $FB_ACCESS_TOKEN
    );

    $result = $facebook-&gt;api("/me/accounts", $attachment_1);
    if(count($result["data"])==0)  {
         return null;
    }

    foreach($result["data"] as $page) {
        if($page["id"] == $page_id) {
            $page_access_token = $page["access_token"];
            break;
        }
    }

    //------ write to page wall
    try {
        $attachment = array(
                    'access_token' =&gt; $page_access_token,
                    'link'          =&gt; $postLink,
                    'message'=&gt;  $postMessage 
        );

        $result = $facebook-&gt;api('/me/feed','POST', $attachment);

    } catch(Exception $e) {
         return null;
    }
    } //end if( !empty($FB_ACCESS_TOKEN)) 

}//end foreach
return $result; }
</code></pre>

<p>Now, I wonder if I can   send the same message to several  pages at once ...
Yup, just by looping over the ids, see above, it now supports multiple page ids.
And unless someone wants to contribute to the code - there's lots of ways it can be improved - I'm done.</p>


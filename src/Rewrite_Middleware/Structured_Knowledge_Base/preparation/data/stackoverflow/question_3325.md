# Getting AuthenticationError while creating meeting using MS Team 2023
[Link to question](https://stackoverflow.com/questions/76387216/getting-authenticationerror-while-creating-meeting-using-ms-team-2023)
**Creation Date:** 1685681546
**Score:** 0
**Tags:** php, azure, microsoft-graph-api, microsoft-teams, microsoft-graph-sdks
## Question Body
<p>Steps taken:</p>
<ul>
<li>Sign up for Azure</li>
<li>Go to the App Registration Page</li>
<li>Created an APP there with permission <code>OnlineMeetings.Read OnlineMeetings.ReadWrite User.Read User.ReadBasic.All User.ReadWrite offline_access</code></li>
<li>Got <code>ClientId</code> and <code>ClientSecret</code></li>
<li>In the web app, create a button <code>Conenct MS TEAM</code></li>
<li>Used <code>$tenantId = &quot;common&quot;;</code></li>
<li>When the user clicks on the button, he/she redirects to the Microsoft Login Page for the permission</li>
<li>On the redirect page, I save the access token to the database.</li>
</ul>
<p>Now a User goes to Meeting Page in Web App</p>
<ul>
<li>Click on create meeting button</li>
<li>fill the form with the date and topic and other details</li>
<li>Click on the <code>Create Meeting</code> button</li>
<li>Now at this point, I am getting below Error</li>
</ul>
<p>Do you know how I can fix this error?</p>
<p>Getting this error:</p>
<pre class="lang-json prettyprint-override"><code>{

&quot;error&quot;: {
    &quot;code&quot;: &quot;AuthenticationError&quot;,
    &quot;message&quot;: &quot;Error authenticating with resource&quot;,
    &quot;innerError&quot;: {
        &quot;date&quot;: &quot;2023-06-01T12:20:52&quot;,
        &quot;request-id&quot;: &quot;34cd542e-cf5a-41d6-b331-a312136c0404&quot;,
        &quot;client-request-id&quot;: &quot;03c0fba2-95c1-45fa-182a-558c37ad282e&quot;
    }
}

}
</code></pre>
<pre class="lang-php prettyprint-override"><code>//I rewrite the code for this issue. 

function getAccessToken(){
    $tenantId = &quot;common&quot;;

    $client_id = &quot;example_client_id&quot;;
    $client_secret = &quot;example_client_secret&quot;;

    $authorize_url = &quot;https://login.microsoftonline.com/&quot; . $tenantId . &quot;/oauth2/v2.0/authorize&quot;;
    $token_url = &quot;https://login.microsoftonline.com/&quot; . $tenantId . &quot;/oauth2/v2.0/token&quot;;

    $provider = new Microsoft([
        // Required
        'clientId' =&gt; $client_id,
        'clientSecret' =&gt; $client_secret,
        'redirectUri' =&gt; 'https://www.example.com/msteam/azure-callback',
        // Optional
        'urlAuthorize' =&gt; $authorize_url,
        'urlAccessToken' =&gt; $token_url,
        'urlResourceOwnerDetails' =&gt; ''
    ]);

    $obj_access_token = QUERY::MODEL(); // getting it from the database
    if($obj_access_token-&gt;exipre  &lt; time())
    {
        // Refresh Token
        $token = $provider-&gt;getAccessToken('refresh_token', [
            'refresh_token' =&gt; $obj_access_token-&gt;refresh_token
        ]);
        return $token-&gt;getToken();
    } else {
        return $obj_access_token-&gt;access_token;
    }
}
</code></pre>
<pre><code>$graph = new Graph();
$graph-&gt;setAccessToken($this-&gt;getAccessToken());

$user_id = &quot;Logged In User Id&quot;;
$user = $this-&gt;getUser($user_id); // Getting user details from Db and Azure

$organizer = [];
if ($user['error'] == 0) {
    $organizer = [
        &quot;id&quot; =&gt; $user['user']['id'], // User ID from Azure
        &quot;displayName&quot; =&gt; $user['user']['name'] // Name of the User from Azure
    ];
}

$data = [
    &quot;startDateTime&quot; =&gt; &quot;2023-06-02T01:00:00+10:00&quot;,
    &quot;endDateTime&quot; =&gt; &quot;2023-06-02T04:00:00+10:00&quot;,
    &quot;subject&quot; =&gt; &quot;Test Subject Meeting&quot;,
    &quot;isEntryExitAnnounced&quot; =&gt; true,
    &quot;participants&quot; =&gt; [
        &quot;organizer&quot; =&gt; [
            &quot;upn&quot; =&gt; &quot;Alex Example&quot;,
            &quot;role&quot; =&gt; &quot;presenter&quot;,
            &quot;identity&quot; =&gt; [
                &quot;user&quot; =&gt; $organizer,
            ]
        ]
    ]
];

$graphresponse = $graph-&gt;createRequest(&quot;POST&quot;, &quot;/me/onlineMeetings&quot;)
    -&gt;attachBody(json_encode($data))
    -&gt;setReturnType(Model\OnlineMeeting::class)
    -&gt;execute();

echo $graphresponse-&gt;getJoinWebUrl();


</code></pre>
<h2>Update:</h2>
<p>On further debugging, I found the scope had been changed automatically.</p>
<p>When a user redirects to the login page:
<code>https://login.microsoftonline.com/common/oauth2/v2.0/authorize?state=ExampleFakeState&amp;scope=OnlineMeetings.Read%20OnlineMeetings.ReadWrite%20User.Read%20User.ReadBasic.All%20User.ReadWrite%20offline_access&amp;response_type=code&amp;approval_prompt=auto&amp;redirect_uri=https%3A%2F%2Fwww.example.com%2Fmsteam%2Fazure-callback&amp;client_id=fakeClientId</code></p>
<p>The scope I attached is here
<code>scope=OnlineMeetings.Read%20OnlineMeetings.ReadWrite%20User.Read%20User.ReadBasic.All%20User.ReadWrite%20offline_access</code></p>
<p>Now when the user clicks on the &quot;Yes&quot; button, I print the scope on the redirect page, which is not the same.</p>
<p><img src="https://github.com/microsoftgraph/msgraph-sdk-php/assets/10128422/c3c169d0-829b-4651-8785-043698a03773" alt="image" /></p>
<pre><code>League\OAuth2\Client\Token\AccessToken Object
(
    [accessToken:protected] =&gt; FakeAccessTokenEwBwA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAbmqVvoIrXK2==
    [expires:protected] =&gt; 1685697206
    [refreshToken:protected] =&gt; FakeRefreshTokenP/dX4MNO9FwbJrlW+ctrB2F2iearn4AP8B+jaJv+zxN7P+dKs
    [resourceOwnerId:protected] =&gt; 
    [values:protected] =&gt; Array
        (
            [token_type] =&gt; Bearer
            [scope] =&gt; User.Read User.ReadWrite
            [ext_expires_in] =&gt; 3600
        )
)
</code></pre>
<p>What is wrong here?</p>


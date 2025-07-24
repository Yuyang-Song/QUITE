# e-mail verification via url with $_GET variables working on localhost but not on server
[Link to question](https://stackoverflow.com/questions/20448851/e-mail-verification-via-url-with-get-variables-working-on-localhost-but-not-on)
**Creation Date:** 1386466652
**Score:** 0
**Tags:** php, email
## Question Body
<p>I am verifying user accounts when the following succeeds:</p>

<pre><code>if (!empty($_GET['email']) AND !empty($_GET['hash'])) {
    // sanitize $_GET data
    $_GET = DB::instance(DB_NAME)-&gt;sanitize($_GET);

    // declare variables for ease of use for $_GET data
    $email = ($_GET['email']);
    $hash = ($_GET['hash']);

    // make sure the data we $_GET is the data we are expecting (matches in the database)
    $match = DB::instance(DB_NAME)-&gt;select_rows("SELECT email, verify_hash, verified FROM users WHERE email='" . $email . "' AND verify_hash='" . $hash . "' AND verified='0'");
    $match = count($match);

    // if there is a match, activate the account
    if ($match &gt; 0) {
        // change 'verified' column from 0 to 1
        $q = array('verified' =&gt; 1);
        $verify_user = DB::instance(DB_NAME)-&gt;update('users', $q, "WHERE email='" . $email . "' AND verify_hash='" . $hash . "' AND verified='0'");

        // send success message
        $this-&gt;template-&gt;content-&gt;message = "Your account has been activated, you can now login";

        // get user type from users table
        $q1 = "SELECT * FROM users WHERE email = '" . $email . "'";
        $result = DB::instance(DB_NAME)-&gt;select_row($q1, 'array');

        // if we have a teacher, update the teachers table
        if ($result['type'] == 'teacher') {
            // prepare default pic and username
            $data = Array(
                'user_id'   =&gt; $result['user_id'],
                'avatar'    =&gt; 'blank_teacher.png',

                // need a username to access profile view -- if not random enough, specify ON DUPLICATE KEY condition
                'user_name' =&gt; $result['first_name'] . rand()
            );
            $update_teacher = DB::instance(DB_NAME)-&gt;insert('users_teachers', $data);

            // prevent page errors from SQL query failing when new teachers don't have at least one subject that they teach
            $data = Array(
                // '32' stands for 'other' subject
                'subject_id'    =&gt; '32',
                'users_user_id' =&gt; $result['user_id']
            );

            $update_at_least_one_subject = DB::instance(DB_NAME)-&gt;insert('teachers_subjects', $data);
        }
    } else {
        // No match: invalid url or account has already been activated.
        $this-&gt;template-&gt;content-&gt;message = "The url is either invalid or you already have activated your account.";
    }
} else {
    // Invalid approach
    $this-&gt;template-&gt;content-&gt;message = "Invalid approach, please use the link that has been sent to your email.";
}
</code></pre>

<p>Strangely (at least to me), this works perfectly on my localhost, but miserably on my live server. I basically can't get the url received via email to work, which looks like the below:</p>

<pre><code>myurl.com/users/email_signup_verification?email=john.doe@yahoo.com&amp;hash=ccb1d45fb76f7c5a0bf619f979c6cf36
</code></pre>

<p>I keep getting my own error message: "Invalid approach" which (logically) would seem to be issued when either one of two $_GET variables, 'email' or 'hash' are empty. It seems to me that they are definitely not empty. </p>

<p>Anyway, I'm not really sure how to troubleshoot differences between local and live. Everything else seemed to work okay. Originally I was checking to make sure that the 'email' and 'hash' were also 'set', as in isset('email'), so i removed that feature, but that didn't resolve the issue.</p>

<p>UPDATE:</p>

<p>my htaccess file contents:</p>

<pre><code>RewriteEngine On

# Allow any files or directories that exist to be displayed directly
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d

# Rewrite all other URLs to index.php/URL
RewriteRule .* index.php/$0 [PT,L]
</code></pre>

## Answers
### Answer ID: 20449405
<p>Is it possible that your RewriteRule on the server make you miss the query string?
You can check the .htaccess file.</p>


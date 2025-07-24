# How do I define the value of an input for a remote check of existing values (username)?
[Link to question](https://stackoverflow.com/questions/6164563/how-do-i-define-the-value-of-an-input-for-a-remote-check-of-existing-values-use)
**Creation Date:** 1306619532
**Score:** 0
**Tags:** javascript, jquery, validation, jquery-validate
## Question Body
<p>This is using jQuery 1.6.1 and Validate 1.8.1.</p>

<p>I have been banging my head against a wall because of this problem, and now I'm trying the other approach to try and solve this problem. I need to query the database for existing usernames so that someone signing up doesn't register the same one again.</p>

<p>HTML:</p>

<pre><code>&lt;form class="cmxform" action="register.php" method="post" name="signup" id="signup"&gt;
   &lt;ul&gt;
      &lt;li&gt;
        &lt;label for="username"&gt;Username: &lt;em&gt;*&lt;/em&gt;&lt;/label&gt;
        &lt;input type="text" id="username" name="Username" size="20" class="required" placeholder="Username" /&gt;
      &lt;/li&gt;
   &lt;/ul&gt;
&lt;/form&gt;
</code></pre>

<p>This time, I'm trying to use the remote function for the validate script:</p>

<pre><code>    $("#signup").validate( {
        var username = $("#username").val();
        rules: {
            Username: {
                required: true,
                minlength: 5,
                remote: {
                    url: "dbquery.php",
                    type: "GET",
                    async: false,
                    data: "action=checkusername&amp;username="+username,
                    success: function (output) {
                            return output;
                    }
                }
            }
        },
        messages: {
            Username: {
                required: "Enter a username",
                remote: jQuery.format("Sorry, {0} is not available")
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
</code></pre>

<p>The code in question that doesn't work is <code>var username = = $("#uname").val();</code>. Firebug gives the error <code>missing : after property id</code>.</p>

<p>I'm including the mentioned variable above inside <code>validate()</code> because I only want the value of the input after I've typed something into it, not upon loading of the page.</p>

<p>The other problem I've been running into is making the remote error message ONLY show up when a username already exists in the database. Unfortunately, it shows up whether dbquery.php comes back as <code>true</code> or <code>false</code>. If I try an existing username, it returns <code>false</code>, then I rewrite a new username that returns <code>true</code>, the message doesn't go away. Similarly, when I write a username and it returns <code>true</code>, I still get the remote error message.</p>

<p>What am I doing wrong?</p>

## Answers
### Answer ID: 6164972
<p>As you can read <a href="https://stackoverflow.com/questions/6117901/how-can-i-force-jquery-validate-to-check-for-duplicate-username-in-database">How can I force jQuery Validate to check for duplicate username in database?</a></p>

<p>The solution is to use the <code>remote</code> property:</p>

<p>Example with <code>remote</code>:</p>

<pre><code>$("#signup").validate( {
    rules: {
        username: {
            required: true,
            minlength: 5,
            remote: {
                url: "dbquery.php",
                type: "get",
                data: {
                    action: function () {
                        return "checkusername";
                    },
                    username: function() {
                        var username = $("#username").val();
                        return username;
                    }
                }
            }
        }
    },
    messages: {
        username: {
            required: "Enter a username"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});
</code></pre>

<p>To set a custom error message your PHP file must return the message instead of false, so <code>echo "Sorry, this user name is not available"</code> in your PHP file.</p>

### Answer ID: 6164587
<pre><code>var username = $("#uname").val();
</code></pre>

<p>instead of </p>

<pre><code>var username = = $("#uname").val();
</code></pre>

<p>You can't have <code>= =</code>, it's a syntax error.</p>

<p>Also, make sure you properly 'escape' $("#username").val().
If someone enters: <code>myname&amp;action=dosomethingelse</code> I'd give it a fair change it will <code>dosomethingelse</code>.</p>

<p>New answer:</p>

<pre><code>$("#signup").validate( {
    var username = $("#username").val(); // -- this is wrong
    rules: {
        Username: {
            required: true,
      ...
});
</code></pre>

<p>You can fix this the easy way by just not declaring the variable at all since you're only using it is one place, but that's no fun :D</p>

<p>The solution is a closure:</p>

<pre><code>$("#signup").validate( (function () {
    var username = $("#username").val();
    return {
        rules: {
            Username: {
                required: true,
                minlength: 5,
                remote: {
                    url: "dbquery.php",
                    type: "GET",
                    async: false,
                    data: "action=checkusername&amp;username="+username,
                    success: function (output) {
                            return output;
                    }
                }
            }
        },
        messages: {
            Username: {
                required: "Enter a username",
                remote: jQuery.format("Sorry, {0} is not available")
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    };
}()));
</code></pre>

<p>(I haven't tested it, there may be a typo or syntax error).
If you have no idea what this does or why, don't worry about it :D</p>


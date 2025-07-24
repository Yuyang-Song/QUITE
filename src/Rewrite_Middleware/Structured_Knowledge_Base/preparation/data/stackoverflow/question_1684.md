# Passing a variable as an argument to the get_options() Wordpress function
[Link to question](https://stackoverflow.com/questions/3963385/passing-a-variable-as-an-argument-to-the-get-options-wordpress-function)
**Creation Date:** 1287435920
**Score:** 0
**Tags:** php, wordpress
## Question Body
<p>I'm currently trying work on a plugin and I'm running into an issue.  Basically, in the plugin options page, I have a form in which the user will input information for an opt-in email.  However, I need different forms for each instance of the email form.  I'm trying to put this together quickly, so rather than rewrite it, I'm merely modifying the code that already exists.</p>

<p>Here's the problem.  I pass the variable for the id of the specific opt-in list to the option form.  My intention is to use it as a suffix for each of the option fields.</p>

<pre><code>    $savedvar1 ='email_capture_signup_';
    $savedvar1 .=$savedformname;
    &lt;input type="text" name="&lt;?php echo $savedvar1;?&gt;" class="regular-text code" value="&lt;?php echo get_option($savedvar1); ?&gt;" /&gt;
</code></pre>

<p>The code works to submit the data, however I can't display the saved value.  Passing the variable through get_option() doesn't seem to work.  I know I'm not too experienced with Wordpress code, but is there any way to be able pass this information through or will I have to do a database query through wpdb.  Unfortunately, the name of the lists has to be dynamic (determined by the user) so I can't just hard code them in there.  Thanks for your help.</p>

## Answers
### Answer ID: 3967676
<p>You might want to try a cleaner way of storing grouped options. get_option and set_option can work with objects and arrays, they're serialized in the database and unserialized upon retrieval.</p>

<p>So the option name itself never changes, but the stuff inside it does. That way you'll not only be able to access your options as an array using functions such as isset, and empty, but you'll also be able to loop through them. Then, in case you need to add an extra field, just add an extra variable to your array and save.</p>


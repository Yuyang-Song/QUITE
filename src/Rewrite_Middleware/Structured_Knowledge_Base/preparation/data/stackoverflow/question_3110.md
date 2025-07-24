# Wordpress: Pass URL parameter to shortcode to create a dynamic page (without editing a template&#39;s functions.php)
[Link to question](https://stackoverflow.com/questions/66965799/wordpress-pass-url-parameter-to-shortcode-to-create-a-dynamic-page-without-edi)
**Creation Date:** 1617700304
**Score:** -1
**Tags:** php, wordpress, shortcode
## Question Body
<p>Before you tell me this question has been asked dozens of times, let me say that I read more than thirty posts on here and elsewhere. Either the explanations are partial and vague, or the proposed code doesn't fit my needs, e.g. the suggestion is to edit the template (which I read wasn't best practice). I'll explain what I want to do and then show the code I already have. My experience with Wordpress is two days long, so bear with me.</p>
<p>I have started writing a plugin (so that I can use it regardless of the theme). I am using a class, not writing the functions directly in the plugin's php file.</p>
<p>The first function I have queries the database to get an array containing a list of translators. Then I pass this array to another function to process the array and make it into a list (with HTML <code>ul</code> and <code>li</code>). I add an anchor tag around the translator's name so that clicking it will open a dynamic page that will show full details about the translator.</p>
<p>To accomplish the above, I have two more functions: one to query the database to get all the relevant details, and another to process the resulting array and apply some basic formatting to it.</p>
<p>All of the above are inside a class. After initiating the class, I add two shortcodes: one is for the formatted translators list, which works as expected. The other one is for the translator details. This is where I can't figure out what to do and how to do it. I did succeed in manually passing the translator's ID to the page but I want to do this dynamically, so that <code>translatorID</code> is passed to the shortcode.</p>
<pre><code>class CT_translator {

private function get_translators_list() {
    global $wpdb;
    return $wpdb-&gt;get_results(
        $wpdb-&gt;prepare(&quot;SELECT * FROM translators_details ORDER BY translatorID ASC&quot;)
    );
}

public function format_translators_list() {
    $results = $this-&gt;get_translators_list();
    $list = &quot;&lt;ul&gt;&quot;;
    foreach($results as $result) {
        $list .= &quot;&lt;li&gt;&lt;a href=\&quot;/prevodach-info/&quot;.$result-&gt;translatorID.&quot;\&quot;&gt;&quot;.$result-&gt;firstName.&quot; &quot;.$result-&gt;paternalName.&quot; &quot;.$result-&gt;familyName.&quot;&lt;/a&gt; &amp;mdash; &quot;.$result-&gt;city.&quot;&lt;/li&gt;&quot;;
    }
    $list .= &quot;&lt;/ul&gt;&quot;;
    return $list;
}

private function get_translator_details($translatorID) {
    global $wpdb;
    return $wpdb-&gt;get_results(
        $wpdb-&gt;prepare(&quot;SELECT * FROM translators_details WHERE translatorID = %s&quot;, $translatorID)
    );
}

public function format_translator_details($translatorID) {
    $results = $this-&gt;get_translator_details($translatorID);
    $list = &quot;&quot;;
    foreach($results as $result) {
        $list .= &quot;&lt;p&gt;&quot;.$result-&gt;firstName.&quot; &quot;.$result-&gt;paternalName.&quot; &quot;.$result-&gt;familyName.&quot; &amp;mdash; &quot;.$result-&gt;city.&quot;&lt;/p&gt;&quot;;
        $list .= &quot;&lt;p&gt;&quot;.$result-&gt;email.&quot;, &quot;.$result-&gt;phone.&quot;, &quot;.$result-&gt;address.&quot;&lt;/p&gt;&quot;;
    }
    return $list;
}
}
</code></pre>
<p>Initiate the class:
$CT_translator = new CT_translator();</p>
<p>Add the two shortcodes:</p>
<pre><code>add_shortcode(&quot;list_translators&quot;, array($CT_translator, 'format_translators_list'));

add_shortcode(&quot;view_translator&quot;, array($CT_translator, 'format_translator_details'));
</code></pre>
<p>This is how I call the translators' list in the page:
[list_translators]</p>
<p>And this is the manual shortcode for viewing a translator's details:
[view_translator translatorID=&quot;1&quot;]</p>
<p>I read that in order for Wordpress to be able to recognise my variables (in this case <code>translatorID</code>), I need a function to add this variable to Wordpress' existing variables, e.g.:</p>
<pre><code>public function add_query_vars($aVars) {
    $aVars[] = &quot;translatorID&quot;;
    return $aVars;
}
</code></pre>
<p>Then I would need to add another function to rewrite the URL so that the last part is understood as a variable:</p>
<pre><code>public function add_rewrite_rules($aRules) {
    $aNewRules = array('prevodach-info/([0-9]+)/?$' =&gt; 'index.php?pagename=prevodach-info&amp;amp;translatorID=$matches[1]');
    $aRules = $aNewRules + $aRules;
    return $aRules;
}
</code></pre>
<p>And when I add the two filters (outside the class):</p>
<pre><code>add_filter('query_vars', 'add_query_vars');
add_filter('rewrite_rules_array', 'add_rewrite_rules');
</code></pre>
<p>everything goes bang! Nothing loads and there's a ton of errors.</p>

## Answers
### Answer ID: 66988807
<p>I received help from someone who is not a member of StackOverflow, and the problemw as solved.</p>
<p>It turns out finding a way to pass the URL parameter to the shortcode, then from the shortcode to the function was not necessary. (Even if possible, I still don't know how it's done.)</p>
<p>All that was necessary was to capture the URL parameter <strong>inside the function</strong> using $_GET or $_REQUEST. From my humble experience writing PHP code, I thought capturing URL parameters <strong>inside</strong> a function was a bad decision.</p>
<p>So, here's what the amended function looks like:</p>
<pre><code>public function format_translator_details($translatorID = &quot;&quot;) {
    if(empty($translatorID)) {
        $translatorID = isset($_GET['translatorID']) ? $_GET['translatorID'] : &quot;&quot;;
    }

    $list = &quot;&quot;;
    if(!empty($translatorID)) {
        $results = $this-&gt;get_translator_details($translatorID);
        foreach($results as $result) {
            $list .= &quot;&lt;p&gt;&quot;.$result-&gt;firstName.&quot; &quot;.$result-&gt;paternalName.&quot; &quot;.$result-&gt;familyName.&quot; &amp;mdash; &quot;.$result-&gt;city.&quot;&lt;/p&gt;&quot;;
            $list .= &quot;&lt;p&gt;Превежда от и на &quot;.$result-&gt;langNameBG.&quot; език.&lt;/p&gt;&quot;;
            $list .= &quot;&lt;p&gt;&quot;.$result-&gt;email.&quot;, &quot;.$result-&gt;phone.&quot;, &quot;.$result-&gt;address.&quot;&lt;/p&gt;&quot;;
        }
    }
    return $list;
}
</code></pre>
<p>And the shortcode is simply <code>[view_translator]</code>.</p>


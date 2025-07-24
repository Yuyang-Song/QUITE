# PHP filter_input_array with FILTER_SANITIZE_STRING allows empty string
[Link to question](https://stackoverflow.com/questions/25252485/php-filter-input-array-with-filter-sanitize-string-allows-empty-string)
**Creation Date:** 1407791450
**Score:** 1
**Tags:** php
## Question Body
<p>I'm using the <code>filter_input_array</code> function to clean <code>$_POST</code> vars submitted from an HTML form.</p>

<p>The problem is that in certain cases I am using the <code>FILTER_SANITIZE_STRING</code> flag and it allows an empty string i.e. <code>$value = ''</code>, but if that form field was left empty, in some cases, it needs to be left as <code>NULL</code>.</p>

<p>The problem occurs when the database query fails due to a foreign key check failing, this happens because the field was submitted as an empty string instead of <code>NULL</code>.</p>

<p>So before I go out rewriting a tonne of queries to make an empty-string check, could anyone tell me how I can configure this <code>filter_input_array</code> input array so that this input string is sanitized and yet either some text value or <code>NULL</code>, but not <code>''</code>.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 69318527
<p>You can use one of the built-in flags called <code>FILTER_FLAG_EMPTY_STRING_NULL</code>. This will replace empty strings with <code>NULL</code>.</p>

### Answer ID: 25252759
<p>You can create a custom filter:</p>

<pre><code>$filter = array('filter' =&gt; FILTER_CALLBACK, 'options' =&gt; function ($input) {
  $filtered = filter_var($input, FILTER_SANITIZE_STRING);
  return $filtered ? $filtered: null;
});
</code></pre>

<p>And then use it in <code>$args</code>:</p>

<pre><code>$args = array(
  'value' =&gt; $filter
);

$inputs = filter_input_array(INPUT_POST, $args);
</code></pre>


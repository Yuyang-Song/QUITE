# How to pass a Future instead of a value as parameter
[Link to question](https://stackoverflow.com/questions/71228381/how-to-pass-a-future-instead-of-a-value-as-parameter)
**Creation Date:** 1645564473
**Score:** 0
**Tags:** flutter, dart, flutter-layout
## Question Body
<p>Suppose I need to create this <strong>Widget()</strong>:</p>
<pre><code>TextButton(
   onPressed: () {},
   child: const Text( myModel.getNameOfCustomer() ),
)
</code></pre>
<p>Currently, my app queries a <strong>EModel</strong> class to obtain the value of nameOfCustomer in a synchronic fashion.  This is due to the fact, that <strong>EModel</strong> maintains its storage fully locally.</p>
<p>Suppose, I want to change <strong>EModel</strong> in such a way, that the class itself queries e.g. a database. Then, <strong>getNameOfCustomer()</strong> needs to return it data asynchronously and this wrapped inside a Future.</p>
<p><strong>Q: How may I pass the <strong>Future&lt;&gt;</strong> as the string parameter for <code>Text()</code>?</strong></p>
<p>Does <code>Text()</code> has a parameter to pass <code>Future&lt;&gt; futureData</code> instead of <code>String data</code> and thus would itself eventually read the value of <code>futureData</code> and set its <code>String data</code>?</p>
<p><strong>In other words...</strong></p>
<p>If my app works synchronously regarding the UI and I switch to an asynchronous data model, do I need to rewrite the whole application?</p>
<p>Does a standard pattern exist, which prepares for such a migration?</p>

## Answers
### Answer ID: 71228443
<p>The thing you are looking for is <a href="https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html" rel="nofollow noreferrer">FutureBuilder</a>.
Wrap your Text widget with this, and you'll be able to wait for that Future, and furthermore, while waiting, you can display something else, like a loading indicator/skeleton.</p>


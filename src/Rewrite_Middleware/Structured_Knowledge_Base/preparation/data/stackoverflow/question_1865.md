# Java + Rails: Invoking some Java code from within a rails app
[Link to question](https://stackoverflow.com/questions/10373524/java-rails-invoking-some-java-code-from-within-a-rails-app)
**Creation Date:** 1335714682
**Score:** 3
**Tags:** java, ruby-on-rails, ruby
## Question Body
<p>I have a rails app. I also wrote a method in Java which constructs a 4 dimensional tree structure. Its for querying my database. The code is relatively complex that i dont want to rewrite it in Ruby again. Is there any way I can use this Java method that I wrote in my rails app. </p>

<p>This would be for a Heroku hosted app.</p>

<p>If so how should I go about learning about how to make this happen? What keywords should I google? Can anyone point me to known good resources ...</p>

<p>Appreciate it.</p>

## Answers
### Answer ID: 10742339
<p>You can expose the Java method to a Ruby client by talking over the network. There are lots of great abstraction layers for exposing Java code via a server.</p>

<p>One such abstraction layer is <a href="http://thrift.apache.org/" rel="nofollow"><code>Thrift</code></a>. You could use Thrift's code generation engine to create a client library for the Ruby side and an interface for your Java server. You can run the Java RPC server anywhere and make calls to it from your Ruby client within your Rails app on Heroku.</p>

<p>Or, if that's too heavy-weight for what you're doing, you could also just shell out to your Java program and have it send the results of the method invocation to STDOUT. In Ruby, you can shell out with backticks (ie <code>`java MyProgram`</code>).</p>


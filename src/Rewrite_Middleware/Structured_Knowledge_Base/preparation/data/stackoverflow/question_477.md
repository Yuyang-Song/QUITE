# Unit testing controllers practices
[Link to question](https://stackoverflow.com/questions/27889392/unit-testing-controllers-practices)
**Creation Date:** 1420993859
**Score:** 0
**Tags:** php, unit-testing, symfony
## Question Body
<p>How should I unit test controllers? First of all, I mock the database results, that's clear. But then what? Should I rewrite the code from controllers, and test all queries against mocks? Or rather call the controller classes, and test the overall result? I mean, for example, having this class:</p>

<pre><code>class User {

   public function foo()
   {
      // query 1
      // query 2
      return $someresults;
   }

}
</code></pre>

<p>Should I test it like that:</p>

<pre><code>class TestUser {

   public testFoo()
   {
      // query1
      // assertions
      // query2
      // assertions
      // results asserions
   }

}
</code></pre>

<p>Or rather like:</p>

<pre><code>class TestUser {

   public function testFoo()
   {
      $user = new User($mockEntityManager);
      // assertions on $user object
   }

}
</code></pre>

<p>What's the proper way to do this? Testing all queries doubles the code, and generates problems with external queries in repository classes (not sure if I can mock that). Testing general results is ok, but methods in controllers return view templates, so I'm not sure how do I test database responses there.</p>

## Answers
### Answer ID: 27893325
<p>You shouldn't unit test controllers, as they do not contain any logic itself. You should need to functional test them, so you can verify it behaves the way you want it.</p>

### Answer ID: 27891028
<p>IMHO the best approach is to define controller as services (as described <a href="http://symfony.com/doc/current/cookbook/controller/service.html" rel="nofollow">here</a>) so you don't need a webcrawler for handling request/response but only interact with his trhow mocked services. </p>

<p>Check <a href="http://php-and-symfony.matthiasnoback.nl/2012/06/symfony2-testing-your-controllers/" rel="nofollow">this article</a> for further detail</p>

<p>Hope this help</p>


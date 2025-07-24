# Angular.js Call $http.get from outside controller
[Link to question](https://stackoverflow.com/questions/24051335/angular-js-call-http-get-from-outside-controller)
**Creation Date:** 1401940172
**Score:** 7
**Tags:** javascript, angularjs, angularjs-scope
## Question Body
<p>I have an HTTP resource that returns a JSON list of top 10 entities from a database.
I call it this way:</p>
<pre><code>var filter= &quot;john&quot;;
var myApp = angular.module('myApp', []);
myApp.controller('SearchController', ['$scope','$http', function ($scope, $http) {
    $http.get('/api/Entity/Find/' + filter). //Get entities filtered
        success(function (data, status, headers, config) {
            $scope.entities = data;
        }).
        error(function () {
        });
    }]);
</code></pre>
<p>It works!</p>
<p>But... how can I change the <code>filter</code> variable in order to change the query?
Should I rewrite the whole controller to get this to work?</p>
<h1>Update</h1>
<p>Sorry for the lack of clarity in my question. When I asked this I couldn't undertand anything of AngularJS.</p>
<p>My original intent was to get the variable <code>$http</code> injected, without relying on creating a controller for that.</p>
<p>Thanks for everyone.</p>

## Answers
### Answer ID: 34779338
<h1>A likely better method</h1>

<p>If you don't want to get it inside a controller, you could have it injected into a recipe (ex, provider, factory, service):
<a href="https://docs.angularjs.org/guide/providers" rel="nofollow noreferrer">https://docs.angularjs.org/guide/providers</a></p>

<pre><code>myApp.factory('getStuff', ['filter', '$http', function (filter, $http) {
    //Blah
}]);
</code></pre>

<h3>If you want to get an instance of $http outside of any angular struct, you can do what's shown below.</h3>

<p>The method given by Dennis works; however, it does not work if called before angular has been bootstrapped.  Also, it seems like Derek has an error with Dennis' method because he does not have jquery.</p>

<p>The solution that Exlord mentioned is better, as it does not have that problem, and is more proper:</p>

<pre><code>$http = angular.injector(["ng"]).get("$http");
</code></pre>

<p><strong>Explained:</strong></p>

<p>The angular injector is an:</p>

<blockquote>
  <p>object that can be used for retrieving services as well as for dependency injection</p>
</blockquote>

<p><a href="https://docs.angularjs.org/api/ng/function/angular.injector" rel="nofollow noreferrer">https://docs.angularjs.org/api/ng/function/angular.injector</a></p>

<p>The function angular.injector takes the modules as a parameter and returns an instance of the injector.</p>

<p>So in this case you retrieve an injector for the ng module (angular's), and then retrieve the service $http.</p>

<p><strong>Note:</strong>
One thing to keep in mind when using injector like this is that in my own findings it seems you need to make sure you include modules in the inject which what you are "getting" will need.  For example:</p>

<pre><code>angular.injector(['ng', 'ngCordova']).get('$cordovaFileTransfer')
</code></pre>

### Answer ID: 24805265
<p>Regarding to your question "... call $http.get from outside controller" you can do the following:</p>

<pre><code>... ANYWHERE IN YOUR CODE

var $http = angular.element('html').injector().get('$http');
$http.get(...).success(...);

ANYWHERE IN YOUR CODE ...
</code></pre>

<p>See official docs from angular: <a href="https://docs.angularjs.org/api/auto/service/$injector">angular $injector docs</a> : 
The <code>get(name);</code> method <code>Returns an instance of the service.</code></p>


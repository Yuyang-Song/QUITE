# How to pass data to angular async function from ng-click
[Link to question](https://stackoverflow.com/questions/47615228/how-to-pass-data-to-angular-async-function-from-ng-click)
**Creation Date:** 1512274995
**Score:** 1
**Tags:** javascript, angularjs, asynchronous
## Question Body
<p>I am trying to use an async function inside a service (so I can acces it from many controllers) and fill an array when I click on an element on the page.</p>

<p>As it is now, the async function will load right after page load. Here is the function ;</p>

<pre><code>   routesApp.factory('angRoutes', function($http) {
    var angRoutes = {
      async: function() {    &lt;----------- How to call this function with params

        var data = $.param({
            query: 'top'         &lt;------------------- HOW TO PASS SOMETHING HERE

        });                         &lt;-- I need to use ng-click="update('top')"

        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
            }
        }

        var promise =   $http.post('../ajax-php.php', data, config)
        .success(function (data, status, headers, config) {

            $('#ajaxLoader').hide(); /// hiding the loading gif

            return data;

       })
        .error(function (data, status, header, config) {
            return data = "Data: " + data +
                "&lt;hr /&gt;status: " + status +
               "&lt;hr /&gt;headers: " + header +
                "&lt;hr /&gt;config: " + config;

        });
        return promise;
      }
    };
    return angRoutes;
  });
</code></pre>

<p>And the controller ;</p>

<pre><code>  routesApp.controller('topRoutesCtrl', function topRoutesCtrl($scope,$http, angRoutes) {
    angRoutes.async().then(function(data) {
        $scope.angRoutes = data;
        console.log(data);
      }); 
});
</code></pre>

<p>I want to update my <code>$scope.angRoutes</code> using the same kind of async function but I need to pass data to the function. For Exemple ;</p>

<pre><code>  &lt;div ng-controller="navRoutesCtrl" class="c prise"&gt;c
        &lt;img ng-click="update()" data-query="top" class= "priseimg" src="../images/prises/c-s.png"&gt; 
     &lt;div class="arrow-all arrow-c"&gt;
          TOP ROUTES
       &lt;/div&gt;
    &lt;/div&gt;
</code></pre>

<p>I use to do it with jquery and I would get the query param for the post from de data-query attribute.</p>

<p>Now I want to turn this into ;</p>

<pre><code> &lt;div ng-controller="navRoutesCtrl" class="c prise"&gt;
  &lt;img ng-click="update('top')" class= "priseimg" src="../images/prises/c-s.png"&gt; 
  &lt;div class="arrow-all arrow-c"&gt;
              TOP ROUTES
           &lt;/div&gt;
        &lt;/div&gt;
</code></pre>

<p>How do I change my service async function and set the .post query to what ever I pass to the update('query').</p>

<p>How do I need to rewrite the function so I can use it with ng-click</p>

<p>I want the exact same thing to happens but from a diffrent controller and a controller that will call the async function with a diffrent query.</p>

<p>Basically I need to call for an async $http function (result come from database and are sent as Json) from a ng-click with at least one param for the query.</p>


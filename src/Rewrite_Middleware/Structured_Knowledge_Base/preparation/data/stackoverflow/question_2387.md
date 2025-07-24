# Angular loads HTML index instead of ng-app.js on refresh
[Link to question](https://stackoverflow.com/questions/32306615/angular-loads-html-index-instead-of-ng-app-js-on-refresh)
**Creation Date:** 1441008508
**Score:** 3
**Tags:** html, angularjs, node.js, angular-ui-router, mean-stack
## Question Body
<p>I am playing around with adding in an Angular-UI router which is working perfectly when I click on links within my application. For example, if I go from <code>/</code> to <code>/feed/9</code> it will load in the <code>/partials/post.html</code> file into the <code>ui-view</code> div and I can then use the '9' held in <code>$stateParams</code> to populate the template with the data from post 9. However if I refresh the page, the site breaks and Angular tries to load index.html as the ng-app.js file? I have no idea what is happening here. I've uploaded some screenshots to demonstrate this and I've included my node server, angular routing and the relevant html partials. I have no idea where this is going wrong so I can provide any additional data and any help would be greatly appreciated!</p>

<p>Working fine when coming from another link on '/'
<a href="https://i.sstatic.net/oNNaL.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/oNNaL.png" alt="Working fine when coming from another link on &#39;/&#39;"></a></p>

<p>On refresh!!
<a href="https://i.sstatic.net/Obnox.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Obnox.png" alt="On refresh"></a></p>

<p>Node - server.js</p>

<pre><code>var = /* Dependencies and vars */;

mongoose.connect(dbConfig.url, dbConfig.options);

app.use(express.static(__dirname + '/public'));
app.use(morgan('dev'));
app.use(bodyParser());
app.use(flash());

require('./routes/api.js')(app);      //For CRUD operations on the database
require('./routes/api_proc.js')(app); //Protected endpoints for CDN
require('./routes/api_ext.js')(app);  //For getting data from GCal, fb, Twitter and Instagram

/* The following code is a url rewrite to pass all
   further get requests that aren't defined in the
   above routing files through the index page and
   hence through the Angular 'frontend' routes */
app.use(function(req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.listen(port);
</code></pre>

<p>Angular ng-app.js</p>

<pre><code>var app = angular.module('app', ['ui.bootstrap', 'ngResource', 'ui.router']);

//Using state ui-router
// ROUTES
app.config(function($stateProvider, $urlRouterProvider, $locationProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider
    .state('home', {
        url : '/',
        templateUrl : 'partials/home.html'
    })

    /* ... */

    .state('feed', {
        url : '/feed',
        templateUrl : 'partials/feed.html'
    })
    .state('post', {
        url : '/feed/{id:.*}',
        templateUrl : 'partials/post.html',
        controller: 'postController'
    })

    $locationProvider.html5Mode(true);

});

app.factory("Feed", function($resource) {
  return $resource("/api/feed/:id", {}, {
      query: {
          isArray: true
      }
  });
});

app.controller("postController", function($scope, Feed, $stateParams) {
    var feed = Feed.query();
    feed.$promise.then(function(promiseData) {
        postArray = promiseData.slice(0,promiseData.length);
        $scope.feed = promiseData;
        $scope.id = $stateParams.id;
    });
});
</code></pre>

<p>index.html</p>

<pre><code>&lt;!DOCTYPE html&gt;
&lt;html ng-app="app"&gt;
    &lt;head&gt;
        &lt;!-- CDN --&gt;
            &lt;!-- Angular, Bootstrap, Angular modules, etc. --&gt;

        &lt;!-- Styles --&gt;

        &lt;!-- Angular Script import --&gt;
            &lt;script type="text/javascript" src="ng-app.js"&gt;&lt;/script&gt;

        &lt;base href="/"&gt;

        &lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;
    &lt;/head&gt;
    &lt;body&gt;     
        &lt;nav&gt;&lt;!--Bootstrap nav--&gt;&lt;/nav&gt;

        &lt;div ui-view&gt;&lt;/div&gt;

        &lt;footer&gt;&lt;/footer&gt;
        &lt;script&gt;
            //For Bootstrap tooltips which are in some of the partials.
            $(document).ready(function(){
                $('[data-toggle="tooltip"]').tooltip(); 
                $('[rel=tooltip]').tooltip();
            });
        &lt;/script&gt;
    &lt;/body&gt;
&lt;/html&gt;
</code></pre>

<p>/partials/post.html</p>

<pre><code>&lt;div class="container-fluid main-content"&gt;         
    &lt;header class="banner" class="row"&gt;
        &lt;h1 class="page-title"&gt;{{id}}&lt;/h1&gt;
    &lt;/header&gt;

    &lt;!-- Main page info --&gt;
&lt;/div&gt;
</code></pre>

## Answers
### Answer ID: 32306721
<p>I think you have relative paths pointing to your css files.
When you load page from <code>/feed/9</code> then links are invalid.
Maybe it happens also for templates referenced from angular.</p>


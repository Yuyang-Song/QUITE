# Migrating to React.js ecosystem from traditional Laravel/Rails app. Need data management on the front-end
[Link to question](https://stackoverflow.com/questions/31630003/migrating-to-react-js-ecosystem-from-traditional-laravel-rails-app-need-data-ma)
**Creation Date:** 1437850393
**Score:** 4
**Tags:** json, node.js, eloquent, reactjs, flux
## Question Body
<p>I have a Laravel app that is in development stage; it's not being relied upon by other people at this point. I've been redesigning the front-end to use React.js as much as possible. I've run into a problem because of the way data needs to be passed to React so that it can be manipulated. Here is an example of the type of problem that is making me rethink how I should be passing data from the back-end to the front-end:</p>

<p>Laravel provides a convenient way to display a link to a route:</p>

<pre><code>link_to_route('users.show', $user-&gt;present()-&gt;name(), $user-&gt;id);
</code></pre>

<p>That code produces the following link:</p>

<pre><code>&lt;a href="http://example.com/users/1"&gt;Jane Austin&lt;/a&gt;
</code></pre>

<p>My thinking was that this sort of functionality (producing links for named routes) was best handled by the back end. However, as I mentioned I'm starting to implement the React.js framework for my views. One of the components I'm started to use is <a href="http://griddlegriddle.github.io/Griddle/index.html" rel="nofollow">Griddle</a>. </p>

<p>First, I set up a Laravel controller to handle the ajax calls:</p>

<pre><code>class AjaxController extends Controller
{
    public function usersIndex()
    {
        $users = Users::orderBy('last')-&gt;get();

        foreach ($users as $user) {
            $user-&gt;displayLink = link_to_route('users.show', $user-&gt;present()-&gt;name(), $user-&gt;id);
            $user-&gt;setVisible(['displayLink']);
        }

        return $users-&gt;toJson();
    }
}
</code></pre>

<p>When the Griddle component calls data from the AjaxController@usersIndex a JSON object is returned:</p>

<pre><code>[
    {
    "displayLink": "&lt;a href=\"http://example.com/users/8\"&gt;Prof. Candelario Q. Abshire&lt;/a&gt;"
    },
    {
    "displayLink": "&lt;a href=\"http://example.com/users/3\"&gt;Prof. Danielle O. Altenwerth IV&lt;/a&gt;"
    },
    {
    "displayLink": "&lt;a href=\"http://example.com/users/18\"&gt;Chelsey J. Bahringer&lt;/a&gt;"
    },
]
</code></pre>

<p>Now, because I'm returning HTML from the back-end instead of the raw data, I have to run the JSON through a custom component to set inner HTML:</p>

<pre><code>var React = require('react');

var DangerouslySetInnerHTML = React.createClass({
    render: function () {
        return (
            &lt;div dangerouslySetInnerHTML={{__html: this.props.data}}&gt;&lt;/div&gt;
        );
    }
});

module.exports = DangerouslySetInnerHTML;
</code></pre>

<p>At first glance, this all appears to be working fine. However, when the Griddle component goes to filter the table or sort the columns it cannot because it can only filter/sort the entire link string instead of just the string that is displayed in the link.</p>

<p>So now obviously I know I'm doing it wrong. I don't know if I need to rewrite a lot of the back end functions (presenters etc) and put them in the front-end somehow or if I need something to manage that data on the front end so that I can combine the raw data from the database and compile links etc. One thing that is clear is that React.js components will need to have access to the raw data before it's combined into larger units like links or fullnames. I imagine that Laravel will basically be relegated to serving up raw JSON objects that mirror closely what is in the database and then I will need to have to write a lot of React.js components to replace the functionality for which Laravel presenters and routers were responsible, e.g, combining small data into larger things like links full names etc. I don't know if there is something out there to help manage that though because I imagine that the complex querying of relations that Eloquent handles purely through JSON is difficult.</p>

<ol>
<li>Is my thinking on this completely wrong?</li>
<li>Is there something similar to Eloquent for the front-end? In other words, are there frameworks out there that manage raw data on the front-end so that you can query relationships similar to what you would do with a Laravel/Rails back-end?</li>
<li>Would there be an advantage to swapping Laravel out for a Node.js back-end like Express.js or a framework like Keystone.js besides the obvious advantage of being able to reuse code due to the fact that it's all JavaScript?</li>
<li>If I am set on using React to handle as much as possible, what are some complementary tools that could help me migrate the functionality that Laravel is currently handling to a React.js ecosystem/environment?</li>
</ol>

## Answers
### Answer ID: 32344917
<p>I understand that this is a complicated area that is changing constantly at the moment. It's been a long time an no answers so I've compiled a list of resources that I've found since asking this question.</p>

<p>First, Relay was just released by the Facebook team and that framework basically solves the problems I've been trying to work around.</p>

<p><a href="https://facebook.github.io/relay/" rel="nofollow">https://facebook.github.io/relay/</a></p>

<p>Second, I found the videos from the React.js Conference 2015 very helpful in helping me to start thinking differently about managing my data.</p>

<p><a href="http://conf.reactjs.com/schedule.html#data-fetching-for-react-applications-at-facebook" rel="nofollow">http://conf.reactjs.com/schedule.html#data-fetching-for-react-applications-at-facebook</a></p>

<p>Particularly this video that introduces Relay was insightful.</p>

<p><a href="http://conf.reactjs.com/schedule.html#data-fetching-for-react-applications-at-facebook" rel="nofollow">http://conf.reactjs.com/schedule.html#data-fetching-for-react-applications-at-facebook</a></p>

<p>Also, this talk by Ryan Florence is right on point with how to go about rewriting an app in React:</p>

<p><a href="https://www.youtube.com/watch?v=BF58ZJ1ZQxY" rel="nofollow">https://www.youtube.com/watch?v=BF58ZJ1ZQxY</a></p>

<p>To answer my own questions: </p>

<p>No, the thinking isn't wrong. A lot of data management is moving from the back end with frameworks like Laravel and Rails to the front end with frameworks like React/Relay. It's a rough transition and a different way of thinking. Backend frameworks can still handle the querying of relationships but should serve up a json/graphql to be managed by the front end. As far as tools that are complementary to React, besides Relay and the awesome dev tools by Dan Abramov (<a href="https://www.youtube.com/watch?v=xsSnOQynTHs" rel="nofollow">https://www.youtube.com/watch?v=xsSnOQynTHs</a>) there are a lot of options popping up. A list of complementary tools is kept up here <a href="https://github.com/facebook/react/wiki/Complementary-Tools" rel="nofollow">https://github.com/facebook/react/wiki/Complementary-Tools</a>.</p>


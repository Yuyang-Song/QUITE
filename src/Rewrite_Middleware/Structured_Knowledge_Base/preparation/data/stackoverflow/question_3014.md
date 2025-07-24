# Trouble understanding the flow of data in a PHP file which uses both server side and client side scripting
[Link to question](https://stackoverflow.com/questions/62371649/trouble-understanding-the-flow-of-data-in-a-php-file-which-uses-both-server-side)
**Creation Date:** 1592132800
**Score:** 0
**Tags:** javascript, php, ajax
## Question Body
<p>I am creating a wordpress plugin where a shortcode can be added to a page which when loaded will display a chart for a chosen user, using that user's data in the wordpress database.</p>

<p>Currently, when the page is loaded, a PHP function executes a couple of SQL queries to create 2 arrays that are then passed as JSON objects to some javascript that dynamically displays two drop-down lists (populated by appropriate data from the arrays). This all works fine and the drop downs display perfectly.</p>

<p>Elsewhere in my PHP file I have php functions that generate charts using charts.js for a given user after it is passed a user ID number. This code also works well when run separately, displaying a graph on the webpage.</p>

<p>My issue is that I need my PHP file to be able to access the user that is chosen from the drop-down list and pass it to another PHP function to generate the graph and display it under the drop-downs.</p>

<p>Now I know JS is client side and PHP is server side. Therefore the only way to pass a JS variable to the PHP is to make an AJAX call. I have this working following the drop-down selection, but the problem is that the PHP file has already been executed. So even though the php file receives the chosen user data in a php variable, which is passed to the graph creation PHP functions, the web page will not update with the graph as the php file has already been executed.</p>

<p>My question is, what possible options do I have here?</p>

<p>My aim is to have a shortcode that displays drop downs and once the user selects a person from the list, the charts for that user are displayed underneath.</p>

<p>Do I need to rewrite my php graph creation functions (that have SQL queries and subsequent PHP calculations) so they are written in pure JS and executed straight after the drop-down select form is submitted (removing the requirement for having the chosen user data in a php variable),  or is there a way that I can still use my graph creating PHP functions that reside in the same PHP file so they display the graph under the drop down once a person is selected from the list?</p>


# nginx : differentiate urls with rewrite rules
[Link to question](https://stackoverflow.com/questions/31288529/nginx-differentiate-urls-with-rewrite-rules)
**Creation Date:** 1436347398
**Score:** 1
**Tags:** php, nginx, url-rewriting
## Question Body
<p>I would like to differentiate urls, the structure is like this :</p>

<pre><code>http://domain/category 1/
             /category n/
             /region 1/
             /region n/
             /city 1/
             /city n/
</code></pre>

<p>the number of different possibilities is minimum 40k, I wondered how to know if the parameter in the url chosen is a city, a region or a category?</p>

<p>Any idea ?
or maybe to get this parameter with a rewrite rule and then to make tests with queries in the database? what is better? how many rewrite rules nginx can support ?</p>

## Answers
### Answer ID: 31290382
<p>I suspect you want something along the lines of:</p>

<pre><code>rewrite ^/(\w+)\%20(\d+)/$ index.php?category=$1&amp;id=$2 last;
</code></pre>

<p>This should rewrite the URL as get parameters on a PHP script. It should be much easier to maintain than 40K of rules.</p>

<p>(note the above is untested, off the top of my head)</p>


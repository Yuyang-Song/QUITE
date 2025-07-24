# Why is this seemingly simple Xpath navigation not working?
[Link to question](https://stackoverflow.com/questions/18363694/why-is-this-seemingly-simple-xpath-navigation-not-working)
**Creation Date:** 1377105121
**Score:** 4
**Tags:** c#, html, xpath
## Question Body
<p>I'm having what seems like a really simple problem. I'm trying to navigate to an element in HTML by Xpath, and can't seem to get it to function properly.</p>

<p>I want to grab a span from the html contents of a page. The page is fairly complex, so I've been using Firebug's "get element by xpath" and pasting the result into my code. I've noticed it's slightly different than the xpath you get from doing the same thing in Chrome, but they both seem to direct to the same place.</p>

<p>The html I'm trying to navigate is <a href="http://nl.newsbank.com/nl-search/we/Archives/?s_siteloc=NL2&amp;p_queryname=4000&amp;p_action=search&amp;p_product=NewsLibrary&amp;p_theme=newslibrary2&amp;s_search_type=customized&amp;d_sources=location&amp;d_place=United%20States&amp;p_nbid=&amp;p_field_psudo-sort-0=psudo-sort&amp;f_multi=&amp;p_multi=&amp;p_widesearch=smart&amp;p_sort=YMD_date:D&amp;p_maxdocs=200&amp;p_perpage=10&amp;p_text_base-0=SEARCHTERM&amp;p_field_base-0=&amp;p_bool_base-1=AND&amp;p_text_base-1=&amp;p_field_base-1=Section&amp;p_bool_base-2=AND&amp;p_text_base-2=&amp;p_field_base-2=&amp;p_text_YMD_date-0=April_1_2001_to_April_1_2012&amp;p_field_YMD_date-0=YMD_date&amp;p_params_YMD_date-0=date:B,E&amp;p_field_YMD_date-3=YMD_date&amp;p_params_YMD_date-3=date:B,E&amp;Search.x=18&amp;Search.y=18" rel="nofollow noreferrer">found here</a>. The field I'm trying to access via xpath is the first "Results 1 - 10 of <em>n</em>".</p>

<p>Based on FireBug's 'inspect element' the xpath should be: <code>/html/body/div/center/table/tbody/tr[6]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/span</code></p>

<p>However when I try to use this xpath to identify the element in a C# codebehind, it gives me a number of errors that that path cannot be found.</p>

<p>Am I doing something wrong here? I've tried a number of permutations of the xpath and I don't understand why this wouldn't be cooperating within code.</p>

<p>Edit: I'm having this problem both in HTMLAgilityPack (but managed to hack out a bad solution using regexes instead) and a SELECT statement modeled after the answer <a href="https://stackoverflow.com/a/18323234/962986">found here</a></p>

<p>Edit 2: I'm trying to figure out this issue using Yahoo's free proxy as shown in the example <a href="https://stackoverflow.com/a/18323234/962986">here</a>:</p>

<pre><code>var query = 'SELECT * FROM html WHERE url="http://mattgemmell.com/2008/12/08/what-have-you-tried/" and xpath="//h1" and class="entry-title"';
var url = "http://query.yahooapis.com/v1/public/yql?q=" + query + "&amp;format=json&amp;callback=??";


$.getJSON(url,function(data){
    alert(data.query.results.h1.content);
})
</code></pre>

<p>I'm having the same problems with HTML agility pack but I'm more interested in getting this part to work. It works for the provided URL that the answerer gave me (seen above). However when I try to use even simple xpath expressions on the <a href="http://nl.newsbank.com" rel="nofollow noreferrer">http://nl.newsbank.com</a> url, I get errors that no object has been retrieved every time, no matter how basic the xpath.</p>

<p>Edit 3: I thought I'd elaborate a little more on the big picture of the larger problem I'm trying to solve of which this problem is a critical component in the hopes that maybe it provides a little more insight.</p>

<p>To learn basic ASP.NET development skills from scratch, I decided to make a simple web application, based around the news archive search at <a href="http://nl.newsbank.com/" rel="nofollow noreferrer">http://nl.newsbank.com/</a>. In its current iteration, it sends a POST request (although I've now learned you can use a GET request and just dump the body at the end of the URL) to send search criteria, as if the user entered criteria in the search bar. It then searches the response (using RegExes, not Xpath because I couldnt get that working) for the "Results 1-<em>n</em> of <em>n</em>" span, extracts <em>n</em>, and dumps it in a table. It's a cool little tool for looking up news occurrence rates over time.</p>

<p>I wanted to add functionality such that you could enter a date range (say May 2002 - June 2010) and run a frequency search for every month / week in that range. This is very easy to implement conceptually. HOWEVER the problem is, right now all this happens server side, and since there's no API, the HTTP response contains the entire page, and is therefore very bandwidth intensive. Sending dozens of queries at once would swallow absolutely unspeakable amounts of bandwidth and wouldn't be even a little scalable.</p>

<p>As a result I tried rewriting the application to work client-side. However because of the <a href="http://en.wikipedia.org/wiki/Same-origin_policy" rel="nofollow noreferrer">same-origin policy</a> I'm not able to send a request to an external host from the client-side. HOWEVER there is a loophole that I can use a free Yahoo proxy that makes the request and converts it to JSON, and then I can use the JSON exception of the Same-Origin Policy to retrieve that data from the proxy.  </p>

<p>Here's where I'm running into these xpath problems specific to <a href="http://nl.newsbank.com" rel="nofollow noreferrer">http://nl.newsbank.com</a>. I'm not able to retrieve html with any xpath, and I'm not sure why or how I can fix it. When debugging in VS2010, I'll receive the error <code>Microsoft JScript runtime error: Unable to get value of the property 'content': object is null or undefined</code></p>

## Answers
### Answer ID: 18536494
<p>As paul t. already mentioned in a comment, the TBODY elements are generated by the webkit engine. The next problem is that the DIV between the BODY and CENTER does not exist on the page by default. It is added by an JS statement on line 119.</p>

<p>After stripping out the DIV and TBODY elements like</p>

<blockquote>
  <p>/html/body/center/table/tr[6]/td/table/tr/td[2]/table/tr/td/table/tr/td/table/tr/td/table/tr/td/span</p>
</blockquote>

<p>i can successfull select a node with the HthmlAgilityPack.</p>

<p>Edit: don't use tools like Firebug for getting an XPath value on a website. Don't even use it if you just want wo look at the source of the page. The problem with Firebug is, that it will show you the <strong>current</strong> DOM document tree which probably on almost every is already (heavily) modified by JS.</p>

### Answer ID: 18442852
<p>Your sample HTML page's elements haven't got many classes to select on, but if you're interested in the first <code>&lt;span&gt;</code> element that contains "Results: 1 - 10 of n", you can use an XPath expression that explicitly targets this textual content.</p>

<p>For example:</p>

<pre><code>//table//span[starts-with(., "Results:")]
</code></pre>

<p>will select all <code>&lt;span&gt;</code> elements, contained in a <code>&lt;table&gt;</code>, and that contain text beginning with "Results:" (the <code>//table</code> is not strictly necessary in your case I think, but might as well restrict a little)</p>

<p>You want the first one of these <code>&lt;span&gt;</code>, so you can use this expression:</p>

<pre><code>(//table//span[starts-with(., "Results:")])[1]
</code></pre>

<p>Note the brackets around the whole previous expression <em>and then</em> <code>[1]</code> to select the first of all the <code>&lt;span&gt;</code> matching the text</p>

### Answer ID: 18411715
<p>It may sound kind of simplistic, but the element you are looking for is the only doc element that is using the css class "basic-text-white". I would think this would be a lot easier to find and extract than a long xpath. Web-scraping is never a stable thing, but I would think this is probably as stable as the xpath. Trying to debug the xpath just about makes my eyes bleed. </p>


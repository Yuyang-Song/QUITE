# Foursquare Venues Search Results Significantly Different
[Link to question](https://stackoverflow.com/questions/32699971/foursquare-venues-search-results-significantly-different)
**Creation Date:** 1442852161
**Score:** 1
**Tags:** foursquare
## Question Body
<p>I am observing the same issues here: 
<a href="https://stackoverflow.com/questions/32697589/foursquare-api-doesnt-work-when-searching-main-categories">Foursquare API doesn&#39;t work when searching main categories</a></p>

<p>and my question relates to this:
<a href="https://stackoverflow.com/questions/32683143/foursquare-api-venues-returning-almost-empty-venues-intent-browse">Foursquare API Venues returning almost empty venues intent=browse</a></p>

<p>But the answer provided (remove the Category ID) has not changed the results. I sent a Tweet to the Foursquare API Twitter account but have not heard a response. The results of my query changed September 18th and have not returned back to normal as of now. </p>

<p>So far I have tried:</p>

<ol>
<li><p>Remove category id (no change).</p></li>
<li><p>Changed version date from a dynamically generated value using PHP
    <code>$version = date('Ymd');</code> to a static string value <code>v=20150918</code> (no change).</p></li>
<li><p>Added <code>query=restaurant</code> which did return results but only items with the query term. For my application this is an incomplete set and unacceptable.</p></li>
<li><p>Removed the <code>query=restaurant</code> and <code>categoryId=4d4b7105d754a06374d81259</code>. This returned all results as expected so for my application which is only concerned with Food this is unacceptable.</p></li>
<li><p>Scrapped the the entire venues search API call and used the venues explore API. This reutrned results similar to the ones I was receiving before September 18th. </p></li>
</ol>

<p>My question:</p>

<p>Does anyone from Foursquare have an explanation about why this is happening and a recommendation on how to resolve? If not, does anyone here on StackOverflow see another option aside from resorting to item 5 of scrapping the venues search API and going with the venues explore API? </p>

<p>I am reluctant to go the way of #5 because:</p>

<ol>
<li><p>The venues search API has seemingly stopped working for no apparent or obvious reason. Will it begin working again and I just need to be patient despite that now my site is giving mixed results at best and no results at worst?</p></li>
<li><p>I would need to rewrite the script that inserts data into my database and also the script that displays the data on the map. </p></li>
</ol>

<p>This is also my first question here. If there are best practices I am not adhering to I would appreciate a heads up. </p>

<p>Thank you.</p>


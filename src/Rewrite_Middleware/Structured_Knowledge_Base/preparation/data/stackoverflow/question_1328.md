# jQuery reorder and structure Ajax data
[Link to question](https://stackoverflow.com/questions/70524830/jquery-reorder-and-structure-ajax-data)
**Creation Date:** 1640810687
**Score:** 0
**Tags:** javascript, php, jquery, mysql, ajax
## Question Body
<p>I have two dimensions of data, one is the purchase itself and the second is the referral reference. Orders are produced with PDO and taken from a MySQL database:</p>
<pre><code>&lt;div rfrnc=&quot;joe&quot; id=&quot;1&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;10.25&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc=&quot;bill&quot; id=&quot;2&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Phone $520&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;10.10&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc=&quot;joe&quot; id=&quot;3&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Headset $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;9.20&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc=&quot;bill&quot; id=&quot;4&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;9.02&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc=&quot;joe&quot; id=&quot;5&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;11.02&lt;/div&gt;&lt;/div&gt;
</code></pre>
<p>Using ajax the above html would be parsed directly into a live feed on my website, sorted desc by orderid or date purchased, through 3 types of api calls of the same function (depending on the parameters to identify each operation):</p>
<ol>
<li><p>initial load (5 entries) &amp; load more button (+5 each time)</p>
<pre><code>$(&quot;.wrapper&quot;).append(html);  
</code></pre>
</li>
<li><p>websocket ping which only triggers the same api call and retrieval from mysql (returning just one order - live feed)</p>
<pre><code>$(&quot;.wrapper&quot;).prepend(html); 
</code></pre>
</li>
<li><p>websocket update when the order is already on the live feed but the status changes</p>
<pre><code>$(&quot;#&quot; + orderid).replaceWith(html);
</code></pre>
</li>
</ol>
<p>The problem I have is how to convert the html divs to display and group it per reference as below.</p>
<pre><code>&lt;div rfrnc=&quot;joe&quot;&gt;
&lt;div id=&quot;5&quot; class=&quot;order&quot;&gt;...&lt;/div&gt;
&lt;div id=&quot;3&quot; class=&quot;order&quot;&gt;...&lt;/div&gt;
&lt;div id=&quot;1&quot; class=&quot;order&quot;&gt;...&lt;/div&gt;
&lt;/div&gt;
&lt;div rfrnc=&quot;bill&quot;&gt;
&lt;div id=&quot;4&quot; class=&quot;order&quot;&gt;...&lt;/div&gt;
&lt;div id=&quot;2&quot; class=&quot;order&quot;&gt;...&lt;/div&gt;
&lt;/div&gt;
</code></pre>
<p>I tried all sort of things, like rewriting the source php html, rewriting the sql query to use group_concat as well as using wrapAll and similar jquery stuff to modify the html after it already comes back from ajax call but no luck. There is further ajax action when clicking on either the order to change the status of it. I need the same on the group level for all the orders having the same reference. Sorry if I did not explain it well.</p>

## Answers
### Answer ID: 70540118
<p>I fully support @firstlast in his comment that sending JSON data and processing it in the front end would be the better solution.</p>
<p>Just in case it is of interest to anyone, here is another way of converting the received html string back to a JavaScript array of arrays:</p>
<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>const html=`&lt;div rfrnc="joe" id="1" class="order"&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class="time"&gt;10.25&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc="bill" id="2" class="order"&gt;&lt;div&gt;1 Phone $520&lt;/div&gt;&lt;div class="time"&gt;10.10&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc="joe" id="3" class="order"&gt;&lt;div&gt;1 Headset $220&lt;/div&gt;&lt;div class="time"&gt;9.20&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc="bill" id="4" class="order"&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class="time"&gt;9.02&lt;/div&gt;&lt;/div&gt;
&lt;div rfrnc="joe" id="5" class="order"&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class="time"&gt;11.02&lt;/div&gt;&lt;/div&gt;`;

const dom=document.createElement("div");
dom.innerHTML=html
  
const data=[...dom.children].map(d=&gt;[d.id,d.getAttribute("rfrnc")].concat([...d.children].flatMap(c=&gt;c.textContent.split(" ")))
);

// show the result:
console.log(["id","rfrnc","qty","descr","price","time"]);
console.log(data);</code></pre>
</div>
</div>
</p>

### Answer ID: 70525292
<p>This <a href="https://jsbin.com/makalufoni/edit?html,js,console,output" rel="nofollow noreferrer">solution</a> loops the existing entries and groups them by the <code>data-rfrnc</code> property:</p>
<pre><code>const people = {};

const html = `&lt;div data-rfrnc=&quot;joe&quot; id=&quot;1&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;10.25&lt;/div&gt;&lt;/div&gt;
&lt;div data-rfrnc=&quot;bill&quot; id=&quot;2&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Phone $520&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;10.10&lt;/div&gt;&lt;/div&gt;
&lt;div data-rfrnc=&quot;joe&quot; id=&quot;3&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Headset $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;9.20&lt;/div&gt;&lt;/div&gt;
&lt;div data-rfrnc=&quot;bill&quot; id=&quot;4&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;9.02&lt;/div&gt;&lt;/div&gt;
&lt;div data-rfrnc=&quot;joe&quot; id=&quot;5&quot; class=&quot;order&quot;&gt;&lt;div&gt;1 Laptop $220&lt;/div&gt;&lt;div class=&quot;time&quot;&gt;11.02&lt;/div&gt;&lt;/div&gt;
`
const domParser = new DOMParser();
const doc = domParser.parseFromString(html, &quot;text/html&quot;)


Array.from(doc.querySelectorAll('body &gt; div')).forEach(div =&gt; {
  const person = div.getAttribute('data-rfrnc');
  if (!people[person]) {
     people[person] = [];
  }
  people[person].push(div)
})


const docFrag = document.createDocumentFragment();
for(let [person, elements] of Object.entries(people)) {
  const personElement = document.createElement('div');
  personElement.setAttribute('data-rfrnc', person);
  elements
    .sort((a,b) =&gt; a.getAttribute('id') &lt; b.getAttribute('id'))
    .forEach(element =&gt; personElement.appendChild(element));
  docFrag.appendChild(personElement);
}

document.body.appendChild(docFrag)
</code></pre>


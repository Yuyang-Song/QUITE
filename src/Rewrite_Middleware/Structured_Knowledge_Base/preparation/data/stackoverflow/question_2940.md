# Javascript: Dynamically set onclick event with different parameters
[Link to question](https://stackoverflow.com/questions/59502939/javascript-dynamically-set-onclick-event-with-different-parameters)
**Creation Date:** 1577461154
**Score:** 0
**Tags:** javascript, jquery, onclick
## Question Body
<p>Trying to rewrite, with minimal functional changes, a program that was written 10+ years ago. Taking it from aspx pages to .NET Core 3.0. For the most part, everything is straight forward. But here's the one problem I'm having - mainly because I'm not great with Javascript (and my searching online has yet to reveal the solution).</p>

<p>In the old system, to search for names, here was the process:</p>

<ol>
<li>Click a letter.</li>
<li>Letter 'link' calls back to code behind.</li>
<li>Code behind appends the new letter to a search string and then queries the database for the values.</li>
<li>Code returns the records to a GridView.</li>
</ol>

<p>So, all 26 letters are displayed in a row and are each a link. Each link gets handled by the same code behind function. To keep minimal functional changes (because the users want the same functionality), I'm going to keep all 26 letter links. However, rather than calling server code, I want to use javascript and ajax calls to accomplish as much as possible. Here's what I currently have:</p>

<p>HTML</p>

<pre><code>&lt;a id="addAToSearch" title="A" accesskey="A" onclick="addClickedLetter('A');"&gt;A&lt;/a&gt;
&lt;a id="addBToSearch" title="B" accesskey="B" onclick="addClickedLetter('B');"&gt;B&lt;/a&gt;
&lt;a id="addCToSearch" title="C" accesskey="C" onclick="addClickedLetter('C');"&gt;C&lt;/a&gt;
&lt;a id="addDToSearch" class="searchLetters" title="D" accesskey="D"&gt;D&lt;/a&gt;
&lt;a id="addEToSearch" class="searchLetters" title="E" accesskey="E"&gt;E&lt;/a&gt;
</code></pre>

<p>Javascript</p>

<pre><code>$(function () {
    var searchLetters = document.getElementsByClassName("searchLetters");
    for (i = 0; i &lt; searchLetters.length; ++i) {
        var letter = searchLetters[i].getAttribute('title');
        searchLetters[i].addEventListener('click', function (letter) {
            addClickedLetter(letter);
        });
    }
});

function addClickedLetter(letter) {
    searchString = $("#txtSearchLastName").val() + letter;
    $("#txtSearchLastName").val(searchString);
};
</code></pre>

<p>For the letters A, B, and C, when I click the links, they append to the string and it shows in the text box. However, rather than assigning the <code>onclick</code> function in the HTML, I'd rather assign it dynamically. That's where D &amp; E come in. I have code that iterates through elements with the <code>searchLetters</code> class and assign their <code>onclick</code> function. And it 'kind of' works. It does assign an <code>onclick</code> function, but unfortunately both D &amp; E do the same value: E. I assume that the code is retaining the last value <code>letter</code> was set to and each <code>onclick</code> that got set all use the same value.</p>

<p>What do I need to do to make sure the onclick function that is set retains the value at the time it was assigned?</p>


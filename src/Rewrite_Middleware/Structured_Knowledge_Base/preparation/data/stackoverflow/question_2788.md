# How to add +1 to a div temporarily until it refreshes, and subtract 1 if clicked a second time (etc etc)?
[Link to question](https://stackoverflow.com/questions/52230258/how-to-add-1-to-a-div-temporarily-until-it-refreshes-and-subtract-1-if-clicked)
**Creation Date:** 1536358877
**Score:** -3
**Tags:** javascript, jquery, html, addition, subtraction
## Question Body
<p>I have a like function on my site. It takes about 1 to 3 seconds (due to unavoidable sql queries for my site - not the best, but it works) to update the new number.</p>

<p>For example, if someone likes it then they click the thumbs up. The div there then updates with the new number.</p>

<p>If it has 3 likes, then when you like, it will have 4 likes. If you click again, it has 3 likes again. Repeat eternally.</p>

<p>The sole purpose of the javascript is to give instant gratification to users who, if not paying attention, may not be sure if it worked, especially during times when it takes longer than 1 second.</p>

<p>My idea is if I can simply do it with jquery to temporarily display the new number until my site rewrites the div to show the updated number, it will serve this function for what I need quite well.</p>

<p>Here is my idea. Please help me to get it working.</p>

<pre><code>var likenum = $(".likenum").val(); // get the number inside the div
var newLikeNum = parseInt(likenum) + 1; // make sure the text is an integer for math functions, then do math and assign to a var
$(".likenum").val(newLikeNum); // refresh div with the new number
</code></pre>

<p>There are a couple problems.</p>

<ol>
<li>how do I run ONCE, and if clicked again, instead, it MINUS? <br>(moreover, some other issues:<br>
It needs to keep original likenum for all future functions, instead of getting a new one. This way if my site refreshes the div, the jquery isn't paying attention to it. It knew the original number and now it ieither +1 or -1 to the original num.</li>
</ol>

<p>So let's take this example for what I want.</p>

<pre><code>&lt;div class="likediv"&gt;3&lt;/div&gt; &lt;!-- original div on page load --&gt;
</code></pre>

<p>x***click***x (pretend I clicked the thumbup)</p>

<pre><code>&lt;div class="likediv"&gt;4&lt;/div&gt; &lt;!-- updated number --&gt;
</code></pre>

<p>x***click***x (pretend I clicked the thumbup again)</p>

<pre><code>&lt;div class="likediv"&gt;3&lt;/div&gt; &lt;!-- updated number --&gt;
</code></pre>

<p>x***click***x (pretend I clicked the thumbup again)</p>

<pre><code>&lt;div class="likediv"&gt;4&lt;/div&gt; &lt;!-- updated number --&gt;
</code></pre>

<p>x***click***x (pretend I clicked the thumbup again)</p>

<pre><code>&lt;div class="likediv"&gt;3&lt;/div&gt; &lt;!-- updated number --&gt;
</code></pre>

<p>x***click***x (pretend I clicked the thumbup again)</p>

<pre><code>&lt;div class="likediv"&gt;4&lt;/div&gt; &lt;!-- updated number --&gt;
</code></pre>

<p>I think you get the point.</p>

<p>So how can I do this? See my starter code above, I think I'm close.</p>

<p>Oh yeah, one more thing. There are many like buttons on the page, not just one. so it would need to store and remember any divs. Because we are liking comments and there are many per page.</p>

<p>For this, only need to use jquery please.</p>

<hr>

<p><strong>EDIT: UPDATE:</strong></p>

<p>So, it wasn't working, @VIDesign's answer, but I see why. In fact, here is what the HTML actually looks like. <em>(Please note I am also including the new working <code>data-value</code> as part of @VIDesign's answer)</em></p>

<pre><code>&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
</code></pre>

<p>Ok so apparently why it didn't work is because when you click, you actually click on <code>.likediv</code>, but the <code>data-value="3"</code> has to go inside the span which is nested inside the div and can't be touched.</p>

<p>So, how to we fire @VIDesign's answer, except the action is triggered when slicking on the div outside the span, when the <code>span</code> is what contains the number and the <code>data-value</code>?</p>

<p>I hope this was clear. Sorry for not specifying this originally, I didn't know until now.</p>

<p>So, we need to change this code below to work with above:</p>

<pre><code>$(".likediv").click(function(){

    // Use the data-value as the constant to calculate with
    const actualValue = $(this).data("value");
    // Set a max value
    const maxValue = actualValue + 1;
    // Get the value the user sees
    const userValue = parseInt($(this).html());

    // create an empty variable for the new value to display
    let newValue;

    // If the value the user sees is equal to the max value
    if(userValue == maxValue){
        // then subtract one
        newValue = maxValue - 1;
    }else{
        // else add one
        newValue = actualValue + 1;
    }
    // Display the new value to the user
    $(this).html(newValue); 

});
</code></pre>

<p>Update 2: I tried this but it didn't work:</p>

<pre><code>$(".likediv").click(function(){

    // Use the data-value as the constant to calculate with
    const actualValue = $(".dynamic-span").data("value");
    // Set a max value
    const maxValue = actualValue + 1;
    // Get the value the user sees
    const userValue = parseInt($(".dynamic-span").html());

    // create an empty variable for the new value to display
    let newValue;

    // If the value the user sees is equal to the max value
    if(userValue == maxValue){
        // then subtract one
        newValue = maxValue - 1;
    }else{
        // else add one
        newValue = actualValue + 1;
    }
    // Display the new value to the user
    $(".dynamic-span").html(newValue); 

});
</code></pre>

<hr>

<p><strong>Note:</strong> The only problem I am having is the <strong><em>speed to which it shows to the user in the front end after they clicked</em></strong>. </p>

<p>I am <em>not</em> trying to do any saving to the database and I do <em>not</em> want to try to get any value from the database, which would be redundant (cause it already happens successfully in other code in the php in the back end). </p>

<p>This is only a quick hack to update the <strong><em>speed at which the number shown is visible</em></strong>. Please be aware that <em>when the php code in the back end updates the div</em> (1 to 3 seconds usually), it will <strong><em>override</em></strong> anything that is in that div currently.</p>

<p>Also, anything done here should be <strong><em>lost on page reload</em></strong> by design. It is only a front-end display hack, not an actual updating of any code on the back end.</p>

## Answers
### Answer ID: 52230591
<p>On the road to freedom, living free of jQuery, lies this answer ..</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>document.querySelectorAll('.likes').forEach(el =&gt;
    el.addEventListener('click', function(){
        let span = this.querySelector('span'),
        now = parseInt(span.innerHTML)

        span.innerHTML = this.dataset.value == now ? ++now : --now
    })
)</code></pre>
<pre class="snippet-code-html lang-html prettyprint-override"><code>&lt;div data-value="3" class="likes"&gt;
    &lt;span&gt;3&lt;/span&gt;
&lt;/div&gt;</code></pre>
</div>
</div>
</p>

### Answer ID: 52230508
<p><strong>Fiddle</strong>
<a href="https://jsfiddle.net/videsignz/n3e5u7bt/34/" rel="nofollow noreferrer">https://jsfiddle.net/videsignz/n3e5u7bt/34/</a>
Here is an example of using the data attribute. The <code>data-value</code> will be loaded from the database and you would end up with this to start.</p>

<pre><code>&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
&lt;div class="likediv"&gt;
    &lt;span class="dynamic-span" data-value="3"&gt;3&lt;/span&gt;
&lt;/div&gt;
</code></pre>

<p>Then handle the restrictions within the click function of the button/div like so...</p>

<pre><code>$(".likediv").on("click", function(){

    const span = $(this).find("span.dynamic-span");
    // Use the data-value as the constant to calculate with
    const actualValue = span.data("value");
    // Set a max value
    const maxValue = actualValue + 1;
    // Get the value the user sees
    const userValue = parseInt(span.html());

    // create an empty variable for the new value to display
    let newValue;

    // If the value the user sees is equal to the max value
    if(userValue == maxValue){
        // then subtract one
        newValue = maxValue - 1;
    }else{
        // else add one
        newValue = actualValue + 1;
    }
    // Display the new value to the user
    span.html(newValue);    

});
</code></pre>

### Answer ID: 52230471
<p>my answer would be to create a global variable <code>dec</code> in the scope that tells if you increment or decrement</p>

<pre><code>var dec = false;
$("#myButton").click(function(){
  dec = !dec;
});
if(!dec)
 $(".likenum").val(parseInt($(".likenum").val()) + 1);
else
  $(".likenum").val(parseInt($(".likenum").val()) - 1);
</code></pre>


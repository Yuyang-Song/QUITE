# My webpage is not updating based on the JSON I import into it
[Link to question](https://stackoverflow.com/questions/71504588/my-webpage-is-not-updating-based-on-the-json-i-import-into-it)
**Creation Date:** 1647466901
**Score:** 0
**Tags:** javascript, html, json
## Question Body
<p>So I have a webpage that is templated so my javascript can access its elements selectively to fill them in. I also have written a small JSON file that I want to import into my javascript and plug in fields from this JSON file into my HTML elements.</p>
<p>HTML:</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;title&gt;Dynamic JSON Events&lt;/title&gt;
    &lt;style&gt;
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville&amp;family=ZCOOL+QingKe+HuangYou&amp;display=swap');

        html, body {
            width: 100%;
            height: 100%;
            background-color: rgb(26, 20, 33, 0.8);
            overflow: hidden;
            margin: 0;
        }

        body {
            display: grid;
            grid-template-areas: 
            'header header header header header'
            'navbar mbody mbody mbody mbody'
            'navbar mbody mbody mbody mbody'
            'navbar mbody mbody mbody mbody'
            'fnotes fnotes fnotes fnotes fnotes';
            gap: 1%;
            padding: 1%;
            width: 100%;
            height: 100%;
        }


        @media screen and (max-width: 800px) {
            html {
                aspect-ratio: 1024/768;
                width: 100%;
                height: 100%;
            }
        }

        @media screen and (max-width: 320px) {
            html {
                aspect-ratio: 375/812;
                width: 100%;
                height: 100%;
            }
        }

        #title {
            grid-area: header;
            font-family:'ZCOOL QingKe HuangYou', cursive;
            color: rgb(233,178,77);
            text-align: center;
            font-size: 48px;;
        }

        #name-color {
            color: rgb(236, 86, 125);
            font-style: normal;
        }

        :hover #title {
            color: rgb(115, 229, 158);
        }

        #site-nav {
            grid-area: navbar;
            display: flex;
            flex-flow: column nowrap;
            width: 100%;
            list-style: none;
        }

        #main {
            grid-area: mbody;
            color:ghostwhite;
            font-family: 'Libre Baskerville';
            font-size: 24px;
            text-align: center;
            width: 100%;
            height: 100%;
            padding: 5%;
        }

        #footer {
            grid-area: fnotes;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1 id=&quot;title&quot;&gt;Hello my name is &lt;em id=&quot;name-color&quot;&gt;Anton&lt;/em&gt;&lt;/h1&gt;
    &lt;time id=&quot;timestamp&quot;&gt;

    &lt;/time&gt;
    &lt;nav role=&quot;navigation&quot; id=&quot;site-nav&quot;&gt;
        &lt;ul id=&quot;sitemap&quot;&gt;

        &lt;/ul&gt;
    &lt;/nav&gt;
    &lt;main role=&quot;main&quot; id=&quot;main&quot;&gt;

    &lt;/main&gt;
    &lt;footer role=&quot;contentinfo&quot; id=&quot;footer&quot;&gt;
        &lt;section id=&quot;content-info&quot; role=&quot;contentinfo&quot;&gt;

        &lt;/section&gt;
        &lt;form id=&quot;contact-form&quot; role=&quot;form&quot;&gt;

        &lt;/form&gt;
    &lt;/footer&gt;
&lt;script src=&quot;./jsofun.js&quot;&gt;
&lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>JSON:</p>
<pre><code>{
    &quot;title&quot; : &quot;First blog post using JSON&quot;,
    &quot;timestamp&quot;: &quot;&quot;,
    &quot;sitemap&quot;: {
        &quot;Homepage&quot;:&quot;../index.html&quot;,
        &quot;Cryptography&quot;: &quot;./Cryptography/index.html&quot;,
        &quot;Homework&quot;: &quot;../cs212/homework/&quot;,
        &quot;Minecraft&quot;: &quot;./minecraft.html&quot;
        },
    &quot;main&quot;: [
        &quot;This was my first attempt at creating a dynamic templated web page which I am going to be&quot;,
        &quot;using to refine and form a blog. This post was parsed entirely from JSON and templated&quot;,
        &quot;into my webpage. I am excited to learn more about how this can play into even more dynamic&quot;,
        &quot;websites and even network driven events when using &lt;em&gt;encoding/json&lt;/em&gt; in my GoLang backend.&quot;
    ],
        &quot;contact_form&quot;: {},
        &quot;content_info&quot;: &quot;&quot;
}
</code></pre>
<p>Javascript:</p>
<pre><code>// import json
require('./post1.json');

// read document elements
var title = window.document.getElementById(&quot;title&quot;);
var timestamp = window.document.getElementById(&quot;timestamp&quot;);
var sitemap = window.document.getElementById(&quot;sitemap&quot;);
var main = window.document.getElementById(&quot;main&quot;);
var contact_form = window.document.getElementById(&quot;contact-form&quot;);
var content_info = window.document.getElementById(&quot;content-info&quot;);

// template in json data
title.textContent = data.title;
timestamp.textContent = String(Date.now());
main.textContent = _main.join();

// log json object for debugging
console.log(data);
</code></pre>
<p>When I test in my terminal using node to see whether my script is importing the JSON correctly with this code:</p>
<pre><code>var data = require('./post1.json');
console.log(data);
</code></pre>
<p>It successfully returns my object how I would expect:</p>
<pre><code>[
  {
    title: 'First blog post using JSON',
    timestamp: '',
    sitemap: {
      Homepage: '../index.html',
      Cryptography: './Cryptography/index.html',
      Homework: '../cs212/homework/',
      Minecraft: './minecraft.html'
    },
    main: [
      'This was my first attempt at creating a dynamic templated web page which I am going to be',
      'using to refine and form a blog. This post was parsed entirely from JSON and templated',
      'into my webpage. I am excited to learn more about how this can play into even more dynamic',
      'websites and even network driven events when using &lt;em&gt;encoding/json&lt;/em&gt; in my GoLang backend.'
    ],
    contact_form: {},
    content_info: ''
  }
]
</code></pre>
<p>However, when I use my full script above to try and then place the object elements into my HTML elements nothing happens or changes on my webpage. I even have tried to completely clear the cache using browser settings and then reloading. One thing I noticed is my browser console tells me require() is not defined; this confuses me because I am testing this locally with the commands <code>npx serve</code> and <code>serve</code> which are both nodejs commands. Node JS is what is supposed to have require defined and able to use so what exactly am I doing wrong here? I use firefox to test this if that changes anything. This is using plain HTML and JavaScript with a node backend, I do not want to use AJAX or any form of XML.</p>
<p>EDIT: Also I want to note, the reason I want to store these objects in external JSON objects is because I would like to use a JSON database which my javascript can dynamically query to form blog posts rather than hardcoding in a JavaScript object into my script for each and every post I want to make. This way I can later make these JSON files locally and add them when I would like without rewriting a webpage every time.</p>
<p><a href="https://i.sstatic.net/KH9tO.png" rel="nofollow noreferrer">errors</a></p>


# Changing colour of substring in Thymeleaf table cell not working
[Link to question](https://stackoverflow.com/questions/65392248/changing-colour-of-substring-in-thymeleaf-table-cell-not-working)
**Creation Date:** 1608551374
**Score:** 0
**Tags:** java, html, spring-boot, thymeleaf
## Question Body
<p>I am rewriting old legacy system written in PHP/HTML into Java/SpringBoot/Thymeleaf. In the old system, there is table displaying search result. In the column &quot;Sentence&quot; I call this function in order to highlight search keywords inside the sentence string.</p>
<pre><code>function highlightKeywords($sentence, $keywords_array){
$resultSentence = &quot;&quot;;
$sentenceArray = explode(&quot; &quot;, $sentence);

for($i = 0; $i &lt; count($sentenceArray); $i++){    
        $token = $sentenceArray[$i];
        if(containsToken($token, $keywords_array)){
        $token = &quot;&lt;mark&gt;&quot;.$token.&quot;&lt;/mark&gt;&quot;;
        }
        $resultSentence = $resultSentence.&quot; &quot;.$token;
    }
return $resultSentence;
}
</code></pre>
<p>Example: seach keyword is &quot;Macron&quot; and the sentence queried from database is <em>&quot;Emmanuel Macron meets Angela Merkel on Friday to discuss refugee crisis.&quot;</em> So &quot;Macron&quot; substring of the sentence has yellow colour.</p>
<p>Now I am trying to do the same thing in Thymeleaf so I wrote this Java method:</p>
<pre><code>public static String highlightSearchParams(String sentence, String keyword) {
        StringBuilder stringBuilder = new StringBuilder();
        String[] tokens = sentence.split(&quot; &quot;);
        for (String token : tokens) {
            if (keyword.equals(token)) {
                token = &quot;&lt;mark class=\&quot;red\&quot;&gt;&quot; + token + &quot;&lt;/mark&gt;&quot;;
            }
            stringBuilder.append(token);
            stringBuilder.append(&quot; &quot;);
        }
        return stringBuilder.toString();
    }
</code></pre>
<p>In my Thymeleaf template I call the method:</p>
<pre><code>&lt;td th:text=&quot;${T(util.DataRepresentationUtils).highlightSearchParams(result.sentence, keywords)}&quot;&gt;...&lt;/td&gt;
        
</code></pre>
<p>And to CSS, I added the style:</p>
<pre><code>mark.red {
    color:#ff0000;
    background: none;
}
</code></pre>
<p>But it does not work. Colour of the substring is not changed though tag was added to the substring. Does anybody knows what the problem is please?</p>
<p>Thank you</p>
<hr />
<p>EDIT:</p>
<p>I changed my style to:</p>
<pre><code>.keyword {
  color: black;
}
</code></pre>
<p>and Java method to:</p>
<pre><code>public static String highlightSearchParams(String sentence, String keywordsString) {
        StringBuilder stringBuilder = new StringBuilder();
        String[] tokens = sentence.split(&quot; &quot;);
        String[] keywords = keywordsString.split(&quot; &quot;);
        for (String token : tokens) {
            for (String keyword : keywords) {
                if (!&quot;&quot;.equals(keyword) &amp;&amp; !&quot; &quot;.equals(keyword) &amp;&amp; keyword.equals(token) || token.contains(keyword)) {
                    token = &quot;&lt;mark class=\&quot;keyword\&quot;&gt;&quot; + token + &quot;&lt;/mark&gt;&quot;;
                }
            }
            stringBuilder.append(token);
            stringBuilder.append(&quot; &quot;);
        }
        return stringBuilder.toString();
    }
</code></pre>
<hr />
<p>EDIT 2:</p>
<p>I realized that I don't need CSS style at all as I want my characters to have black colour. So I changed my Java method to:</p>
<pre><code>public static String highlightSearchParams(String sentence, String keywordsString) {
        StringBuilder stringBuilder = new StringBuilder();
        String[] tokens = sentence.split(&quot; &quot;);
        String[] keywords = keywordsString.split(&quot; &quot;);
        for (String token : tokens) {
            for (String keyword : keywords) {
                if (!&quot;&quot;.equals(keyword) &amp;&amp; !&quot; &quot;.equals(keyword) &amp;&amp; keyword.equals(token) || token.contains(keyword)) {
                    token = &quot;&lt;mark&gt;&quot; + token + &quot;&lt;/mark&gt;&quot;;
                }
            }
            stringBuilder.append(token);
            stringBuilder.append(&quot; &quot;);
        }
        return stringBuilder.toString();
    }
</code></pre>
<p>But if you want to change characters colour, use the approach from the first EDIT section.</p>

## Answers
### Answer ID: 65392552
<p>I tried out your case and it works fine for me in both Chrome and Firefox. I think we need to elaborate your CSS. If the mark is indeed added to the html content of the td then something is going on with your CSS. You may have a look in the developer tools of your browser. (Usually invoked via F12) Find the misbehaving mark in your td and Elaborate the Style-Sheet attributes that actually are applied. Maybe some !important attribute elsewhere in the code overrides your settings.</p>
<pre><code>&lt;html&gt;
&lt;head&gt;
    &lt;style&gt;
        mark.red {
            color:#ff0000;
            background: none;
        }
        table, tr  {
            border: 1px solid black;
        }
        th  {
            border-top: 1px solid black;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;table&gt;

    &lt;tr&gt;
        &lt;th&gt;
            ID
        &lt;/th&gt;
        &lt;th&gt;
            Sentence
        &lt;/th&gt;
        &lt;th&gt;
            Other Column
        &lt;/th&gt;
    &lt;/tr&gt;


    &lt;tr&gt;
        &lt;th&gt;
            1
        &lt;/th&gt;
        &lt;th&gt;
            Hello World
        &lt;/th&gt;
        &lt;th&gt;
            Today
        &lt;/th&gt;
    &lt;/tr&gt;
    
    &lt;tr&gt;
        &lt;th&gt;
            1
        &lt;/th&gt;
        &lt;th&gt;
            Emmanuel &lt;mark class=&quot;red&quot;&gt;Macron&lt;/mark&gt; meets Angela Merkel on Friday to discuss refugee crisis.
        &lt;/th&gt;
        &lt;th&gt;
            Today
        &lt;/th&gt;
    &lt;/tr&gt;

&lt;/table&gt;

&lt;/body&gt;
&lt;/html&gt;
</code></pre>


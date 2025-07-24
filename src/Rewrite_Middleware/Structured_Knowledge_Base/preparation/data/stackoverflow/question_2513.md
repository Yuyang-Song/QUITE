# order divs in columns and prevent vertical free space
[Link to question](https://stackoverflow.com/questions/37888487/order-divs-in-columns-and-prevent-vertical-free-space)
**Creation Date:** 1466189550
**Score:** 2
**Tags:** javascript, php, html, mysql, css
## Question Body
<p>Let's say, we have a website, which contains 5 columns: "Daily", "Weekly1", "Weekly2", "Monthly1", "Monthly2".</p>

<p>Now there is a script, which gets data from a MySQL Database in an unsorted sequence <em>(there is no way to sort by query I think)</em> and these Datasets ("cards" with specific height) should be shown in the dataset-corresponding column.</p>

<p>How to achieve this?</p>

<p>What I have is that the "cards" are placed in right column, but there is vertical blank space between the cards, if another card was placed in another column before.</p>

<p>Is there a way to achieve this in css or do I have to do a workaround in php or JavaScript?</p>

<p><b>-edit-</b> Very minimal and not 100% working, but my actual test-file :)    </p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true">
<div class="snippet-code">
<pre class="snippet-code-html lang-html prettyprint-override"><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Title&lt;/title&gt;

    &lt;style&gt;
        body{
            width:100vh;
            background-color: darkolivegreen;
        }
        .spalte1{
            position:absolute;
            width: 20%;
            left: 0%;
            height: 80vh;
            background-color: aqua;
            border: solid 1px;
        }

        .spalte2{
            position:absolute;
            left: 20%;
            width: 20%;
            height: 80vh;
            background-color: yellow;
            border: solid 1px;
        }
        .spalte3{
            position:absolute;
            left: 40%;
            width: 20%;
            height: 80vh;
            background-color: green;
            border: solid 1px;
        }
        .spalte4{
            position:absolute;
            left: 60%;
            width: 20%;
            height: 80vh;
            background-color: gray;
            border: solid 1px;
        }
        .spalte5{
            position:absolute;
            left: 80%;
            width: 20%;
            height: 80vh;
            background-color: deeppink;
            border: solid 1px;
        }

        .card{
            position: relative;
            background-color: bisque;
            border: solid 1px;
            height: 7vh;
        }

    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div class="spalte1"&gt;spalte1&lt;/div&gt;
&lt;div class="spalte2"&gt;spalte2&lt;/div&gt;
&lt;div class="spalte3"&gt;spalte3&lt;/div&gt;
&lt;div class="spalte4"&gt;spalte4&lt;/div&gt;
&lt;div class="spalte5"&gt;spalte5&lt;/div&gt;

&lt;div class="spalte3 card"&gt;Karte1&lt;/div&gt;
&lt;div class="spalte1 card"&gt;Karte2&lt;/div&gt;
&lt;div class="spalte5 card"&gt;Karte3&lt;/div&gt;
&lt;div class="spalte4 card"&gt;Karte4&lt;/div&gt;
&lt;div class="spalte1 card"&gt;Karte5&lt;/div&gt;


&lt;/body&gt;
&lt;/html&gt;</code></pre>
</div>
</div>
</p>

<p><b>-edit-</b> actually, i can't provide php, because i am rewriting my code and add the ordering on the page as a "feature". my actual code is just writing the cards in a table from left to right :)</p>

<p>sql:</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true">
<div class="snippet-code">
<pre class="snippet-code-html lang-html prettyprint-override"><code>CREATE TABLE `tkarten` (
  `id` int(11) NOT NULL,
  `Kartennummer` int(11) NOT NULL,
  `Beschreibung` text NOT NULL,
  `erledigt` tinyint(1) NOT NULL,
  `inBearbeitung` tinyint(1) NOT NULL,
  `wann` enum('daily','weekly','monthly','') NOT NULL,
  `fmn` enum('f','m','n') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Daten für Tabelle `tkarten`
--

INSERT INTO `tkarten` (`id`, `Kartennummer`, `Beschreibung`, `erledigt`, `inBearbeitung`, `wann`, `fmn`) VALUES
(1, 1, 'Karte 1 mach irgendwas hauptsache hier steht was', 0, 0, 'daily', 'm'),
(3, 2, 'Karte 2 macht auch irgendwas ... hauptsache hier steht was', 1, 0, 'weekly', 'n'),
(4, 3, 'Auch bei der dritten Karte haben wir arbeit', 0, 0, 'weekly', 'n'),
(5, 4, 'Die vierte Karte ist nicht so wichtig', 0, 0, 'monthly', 'm'),
(6, 5, 'Wir haben 5 voll... jetzt kann schon einer gegen sich selbst poker spielen', 0, 0, 'weekly', 'm'),
(7, 6, 'noch ne sechste Karte, weils so sch&amp;ouml;n war.', 0, 0, 'monthly', 'f');</code></pre>
</div>
</div>
</p>

<p>column "wann" = daily, weekly or monthly
column "fmn" = weekly1 or 2 and monthly 1 or 2</p>

## Answers
### Answer ID: 37889186
<p>Here's a simple solution for columns with cards in it:</p>

<pre><code>//css

.columns {
  list-style-type: none;
  //width: 100%;
  padding: 0;
  margin: 0;
}
.column {
  display: inline-block;
  border: 1px solid #aaa;
  padding: 10px;
  width: 100px; 
  vertical-align: top;
}
.cards {
  list-style-type: none;
  padding: 0;

}

.card {
  border: 1px solid #ededff;
  background: #ededed;
  margin-top: 2px;
  padding: 5px;
}


// html
&lt;ul class="columns"&gt;

&lt;li class="column"&gt;
  &lt;ul class="cards"&gt;
    &lt;li class="card"&gt;card1&lt;/li&gt;
    &lt;li class="card"&gt;card4&lt;/li&gt;
  &lt;/ul&gt;
&lt;/li&gt;

&lt;li class="column"&gt;
  &lt;ul class="cards"&gt;
    &lt;li class="card"&gt;card2&lt;/li&gt;
  &lt;/ul&gt;
&lt;/li&gt;

&lt;li class="column"&gt;
  &lt;ul class="cards"&gt;
    &lt;li class="card"&gt;card3&lt;/li&gt;
    &lt;li class="card"&gt;card5&lt;/li&gt;
    &lt;li class="card"&gt;card6&lt;/li&gt;
  &lt;/ul&gt;
&lt;/li&gt;

&lt;/ul&gt;
</code></pre>

<p>This approach is easier than trying to position (absolute) several divs depending on it's content above some other divs...</p>

<p>For the php-part I can't give an answer yet, as there is no php-code yet to look at... </p>


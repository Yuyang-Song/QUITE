# How to convert perl hash of hash of hash to php
[Link to question](https://stackoverflow.com/questions/36312579/how-to-convert-perl-hash-of-hash-of-hash-to-php)
**Creation Date:** 1459349829
**Score:** 0
**Tags:** php, perl, hash
## Question Body
<p>I am currently looking a rewriting some perl cgi scripts into php, mainly in order so I can learn php. Everything is going well, except I can't get my head round how to convert a perl hash of hash of hash into a php array.
Take this scenario (not real, but the idea is the same)
I have 5 network nodes called A,B,C,D,E.
Each node is actually a stack of 3 switches called TOP, MIDDLE, BOTTOM
Each switch has 10 interfaces called 1 to 10.</p>

<p>I have a script that polls round every interface and record the input bytes in a database like this:-</p>

<pre><code>node   switch   interface  bytes
 A      TOP       1         999
 B     MIDDLE     1         999
 A     MIDDLE     2         999
</code></pre>

<p>etc</p>

<p>I can read the database in php, but then I come unstuck. In perl I just read the data and store it in a hash of hashes by looping though the query of the database</p>

<pre><code>`While $ref fetchrow_hashref() {
    $hash{$ref{'NODE'}}{$ref{'Switch'}}{$ref{'Interface'}=$ref{'Bytes'}
}`
</code></pre>

<p>So now I can access any value in my cgi code using the names
<code>$hash{A}{Top}{1}</code> would return 999</p>

<p>But when I try and do something similar in php with associative array of arrays, it go wrong. I've used</p>

<pre><code>$hash[]=[$ref["NODE"}=&gt;
    [$ref["Switch"]=&gt;
        [$ref["Interface"]=&gt;
            $ref["Bytes"]
        ]
    ]
];
</code></pre>

<p>A var_dump of the hash looks correct, but I don't appear to be able to print a value out of the array using
<code>print $hash[A][TOP][1];</code></p>

<p>Please can I have pointers to my mistakes</p>

## Answers
### Answer ID: 36313313
<p>That would be </p>

<pre><code>while( $ref=somefetchingfunction_or_method() ) {
    $hash[$ref['NODE']][$ref['Switch']][$ref['Interface']]=$ref['Bytes'];
</code></pre>

<p>(i.e. just replacing all <code>{</code> by <code>[</code>, <code>}</code> by <code>]</code> and fixing the missing last <code>]</code>.)</p>

<p>edit: <a href="http://sscce.org/" rel="nofollow">sscce</a>:</p>

<pre><code>&lt;?php
$hash = [];
foreach( gen_fetch() as $ref ) {
    $hash[$ref['NODE']][$ref['Switch']][$ref['Interface']]=$ref['Bytes'];
}
echo $hash['A']['TOP'][1];

// generator requires php version &gt;= 5.5, see http://php.net/language.generators.overview
function gen_fetch() {
    $keys = ['NODE','Switch','Interface','Bytes'];
    foreach( [['A','TOP',1,997],['B','MIDDLE',1,998],['A','MIDDLE',2,999]] as $r) {
        yield array_combine($keys,$r);
    }
}
</code></pre>

<p>prints <code>997</code>.</p>


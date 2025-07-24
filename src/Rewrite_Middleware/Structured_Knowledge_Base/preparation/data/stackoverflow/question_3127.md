# Prolog - How would I recursively build a list?
[Link to question](https://stackoverflow.com/questions/67747443/prolog-how-would-i-recursively-build-a-list)
**Creation Date:** 1622258582
**Score:** 0
**Tags:** list, prolog, logic, predicate
## Question Body
<p>I'm working through the exercises on <a href="http://www.let.rug.nl/bos/lpn//lpnpage.php?pagetype=html&amp;pageid=lpn-htmlse12" rel="nofollow noreferrer">Learn Prolog Now!</a> and I'm stumped on the very last question. Given the following facts:</p>
<pre><code>   byCar(auckland,hamilton).
   byCar(hamilton,raglan).
   byCar(valmont,saarbruecken).
   byCar(valmont,metz).
   byTrain(metz,frankfurt).
   byTrain(saarbruecken,frankfurt).
   byTrain(metz,paris).
   byTrain(saarbruecken,paris).
   
   byPlane(frankfurt,bangkok).
   byPlane(frankfurt,singapore).
   byPlane(paris,losAngeles).
   byPlane(bangkok,auckland).
   byPlane(singapore,auckland).
   byPlane(losAngeles,auckland).
</code></pre>
<blockquote>
<p>Write a predicate travel/2 which determines whether it is possible to travel from one place to another by chaining together car, train,
and plane journeys. For example, your program should answer yes to the
query travel(valmont,raglan) .</p>
<p>So, by using travel/2 to query the above database, you can find out
that it is possible to go from Valmont to Raglan. If you are planning
such a voyage, that’s already something useful to know, but you would
probably prefer to have the precise route from Valmont to Raglan.
Write a predicate travel/3 which tells you which route to take when
travelling from one place to another. For example, the program should
respond    X  =  go(valmont,metz,
go(metz,paris,
go(paris,losAngeles))) to the query travel(valmont,losAngeles,X) .</p>
</blockquote>
<p>here's my go functors:</p>
<pre><code>go(X).
go(X,Y).
</code></pre>
<p>Here's my travel/2 predicate:</p>
<pre><code>travel(X,Y) :- byCar(X,Y).
travel(X,Y) :- byCar(X,Z), travel(Z,Y).

travel(X,Y) :- byTrain(X,Y).
travel(X,Y) :- byTrain(X,Z), travel(Z,Y).

travel(X,Y) :- byPlane(X,Y).
travel(X,Y) :- byPlane(X,Z), travel(Z,Y).
</code></pre>
<p>However, I'm having trouble with my travel/3 predicate:</p>
<pre><code>travel(X,Y,G) :- byCar(X,Y),   G = go(X, Y).
travel(X,Y,G) :- byCar(X,Z),   travel(Z,Y,G).

travel(X,Y,G) :- byTrain(X,Y), G = go(X, Y).       
travel(X,Y,G) :- byTrain(X,Z), travel(Z,Y,G).

travel(X,Y,G) :- byPlane(X,Y), G = go(X, Y).       
travel(X,Y,G) :- byPlane(X,Z), travel(Z,Y,G).
</code></pre>
<p>When I run the predicate in the question, I get:</p>
<pre><code>?- travel(valmont,losAngeles,X).
X = go(paris, losAngeles) .
</code></pre>
<p>But it's not an entire list like the question needs. I'm not really sure how to accomplish that; whether I need to rewrite my predicates or not. Any help you could offer to help me learn what I'm doing wrong is super appreciated!</p>

## Answers
### Answer ID: 67747538
<p>Your are not changing <code>G</code> appropriately in the <code>travel/3</code> predicate.</p>
<pre><code>travel(X,Y, go(X, Y)) :- byCar(X,Y).
travel(X,Y, go(X, Y)) :- byTrain(X,Y).
travel(X,Y, go(X, Y)) :- byPlane(X,Y).

travel(X,Y, go(X, Z, G)) :- byCar(X,Z), travel(Z,Y, G).
travel(X,Y, go(X, Z, G)) :- byTrain(X,Z), travel(Z,Y, G).
travel(X,Y, go(X, Z, G)) :- byPlane(X,Z), travel(Z,Y, G).
</code></pre>
<p>You get:</p>
<pre><code>| ?- travel(valmont, losAngeles, G).
G = go(valmont,saarbruecken,go(saarbruecken,paris,go(paris,losAngeles))) ? ;
G = go(valmont,metz,go(metz,paris,go(paris,losAngeles))) ? ;
no
</code></pre>
<p>As a bonus you can just embed the type of travel too:</p>
<pre><code>travel_(X,Y, car(X, Y)) :- byCar(X,Y).
travel_(X,Y, train(X, Y)) :- byTrain(X,Y).
travel_(X,Y, plane(X, Y)) :- byPlane(X,Y).
      
travel_(X,Y, car(X, Z, G)) :- byCar(X,Z), travel_(Z,Y, G).
travel_(X,Y, train(X, Z, G)) :- byTrain(X,Z), travel_(Z,Y, G).
travel_(X,Y, plane(X, Z, G)) :- byPlane(X,Z), travel_(Z,Y, G).
</code></pre>
<p>Now you get:</p>
<pre><code>| ?- travel_(valmont, losAngeles, G).
G = car(valmont,saarbruecken,train(saarbruecken,paris,plane(paris,losAngeles))) ? ;
G = car(valmont,metz,train(metz,paris,plane(paris,losAngeles))) ? ;
no
</code></pre>


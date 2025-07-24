# Convert string to name of object (casting)
[Link to question](https://stackoverflow.com/questions/26570698/convert-string-to-name-of-object-casting)
**Creation Date:** 1414307813
**Score:** 0
**Tags:** javascript, string, object, casting
## Question Body
<p>I want to cast a string to an existing object. 
Background: I am using only JS, no libraries and no server side code. I have existing objects with elements I wish to display. I pass the name of the object using a query string so it arrives as a string. Example <code>?Room=Cube</code> and what I wind up with is </p>

<pre><code>nextRoom = getQueryString();  // which returns a string
</code></pre>

<p>and I want to display the Cube object. However nextRoom contains "Cube" and JS is not helpful, if I call a display function: </p>

<pre><code>display(nextRoom)
</code></pre>

<p>Javascript treats it as a string and fails. Currently I fake it out with the object:</p>

<pre><code>castToObj{"Cube":Cube, "Other":Other, "Etc":Etc, ........}
  .....  
room = castToObj[nextRoom];    // accessing the object returns the room Object
</code></pre>

<p>then I can display the room by calling:</p>

<pre><code>display(room);  // now JS treats the parameter as an object
</code></pre>

<p>But this requires me to rewrite code to modify the <code>castToObj{}</code> contents every time I add a room. I would like a way to turn "Cube" into Cube, in other words turn a string into an object. I have tried many variations but have been unsuccessful. I could list ways I have tried but that seems senseless because they were all failures.
HELP! PLEASE!</p>

<p>P.S I retired about twenty years ago before learning C++, OOP, etcetera so my javascript skills are just my "C" programming experience expanded.</p>

## Answers
### Answer ID: 26571654
<p>First create an empty container object:</p>

<pre><code>myElements = {};
</code></pre>

<p>Then change your code wherever you define an element, from</p>

<pre><code>Cube =  ... whatever ...
</code></pre>

<p>to </p>

<pre><code>myElements.Cube = ... whatever ....
</code></pre>

<p>for all of your elements (Other, Etc ...).</p>

<p>After this, you simply use</p>

<pre><code>nextRoom = getQueryString(); 
display(myElements[nextRoom]);
</code></pre>

### Answer ID: 26570907
<p>You can use java script eval function but depending on the situation it might open your program to XSS attack. You should use it carefully. </p>


# Is it recommended to keep a program sources (as opposed to lib sources) in a single file?
[Link to question](https://stackoverflow.com/questions/23469962/is-it-recommended-to-keep-a-program-sources-as-opposed-to-lib-sources-in-a-sin)
**Creation Date:** 1399284737
**Score:** 5
**Tags:** go
## Question Body
<p>I am making my first steps into Go and obviously am reasoning from what I'm used to in other languages rather than understanding go specificity and styles yet.</p>

<p>I've decided to rewrite a ruby background job I have that takes ages to execute. It iterates over a huge table in my database and process data individually for each row, so it's a good candidate for parallelization.</p>

<p>Coming from a ruby on rails task and using ORM, this was meant to be, as I thought of it, a quite simple two files program: one that would contain a struct type and its methods to represent and work with a row and the main file to operate the database query and loop on rows (maybe a third file to abstract database access logic if it gets too heavy in my main file). This file separation as I intended it was meant for codebase clarity more than having any relevance in the final binary.</p>

<p>I've <a href="http://golang.org/doc/code.html" rel="nofollow noreferrer">read</a> and <a href="https://www.youtube.com/watch?v=XCsL89YtqCs" rel="nofollow noreferrer">seen</a> several things on the topic, including questions and answers here, and it always tends to resolve into writing code as libraries, installing them and then using them into a single file source (in package main) program.</p>

<p>I've read that one may pass multiple files to go build/run, but it complains if there is several package name (so basically, everything should be in <code>main</code>) and it doesn't seem that common.</p>

<p>So, my questions are :</p>

<ul>
<li>did I get it right, and having code mostly as a library with a single file program importing it the way to go?</li>
<li>if so, how do you deal with having to build libraries repeatedly? Do you build/install on each change in library codebase before executing (which is way less convenient that what <code>go run</code> promise to be) or is there something common I don't know of to execute library dependent program quick and fast while working on those libraries code?</li>
</ul>

## Answers
### Answer ID: 23471099
<p>No.</p>

<p>Go and the <code>go</code> tool works on packages only (just <code>go run</code> works on files, but that is a different story): You should not think about files when organizing Go code but packages. A package may be split into several files, but that is used for keeping test code separated and limiting file size or
grouping types, methods, functions, etc.</p>

<p>Your questions:</p>

<blockquote>
  <p>did I get it right, and having code mostly as a library with a single file program
  importing it the way to go?</p>
</blockquote>

<p>No. Sometimes this has advantages, sometimes not. Sometimes a split may be one lib + one short main,
in other cases, just one large main might be better.  Again: It is all about packages and never about files. There is nothing wrong with a single 12 file main package if this is a real standalone program. But maybe extracting some stuff into one or a few other packages might result in more readable code. It all depends.</p>

<blockquote>
  <p>if so, how do you deal with having to build libraries repeatedly? Do you build/install on each change in library codebase before executing (which is way less convenient that what go run promise to be) or is there something common I don't know of to execute library dependent program quick and fast while working on those libraries code?</p>
</blockquote>

<p>The <code>go</code> tool tracks the dependencies and recompiles whatever is necessary. Say you have a package main in <code>main.go</code> which imports a package foo. If you execute <code>go run main.go</code> it will recompile package foo transparently iff needed. So for quick hacks: No need for a two-step  <code>go install foo; go run main</code>.  Once you extract code into three packages foo, bar, and waz it might be a bit faster to install foo, bar and waz.</p>

### Answer ID: 23470769
<p>No. Look at the Go commands and Go standard packages for exemplars of good programming style.</p>

<p><a href="https://code.google.com/p/go/wiki/Source" rel="nofollow">Go Source Code</a> </p>


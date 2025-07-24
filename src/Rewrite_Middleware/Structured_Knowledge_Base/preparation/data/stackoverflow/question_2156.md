# Using PHP Classes for Device Objects
[Link to question](https://stackoverflow.com/questions/21174458/using-php-classes-for-device-objects)
**Creation Date:** 1389912245
**Score:** 0
**Tags:** php, mysql, class, oop, project-management
## Question Body
<p>I have developed a Web Interface for managing our devices (Dedicated Servers/Switches/etc) at work, however with my basic PHP knowledge, I ignored OOP completely. In the current state it just queries the MYSQL Database and populates the tables. Functions are all stored in a Functions.php file and called as needed.</p>

<p>As the project is functional and used now, I would like to rewrite this to be more efficient as it will be used among our other brands. I am having trouble applying the concept of classes to this project though (I use them all the time in C#/C++).</p>

<p>The way I see it, each Device be it a server, switch, etc. could be a part of a Device class that keeps properties like Datacenter, Name, etc. and methods such as Update, Delete, etc. I suppose I could additionally have a base Device class, then subsequent classes such as Server/Switch/etc. which inherit from that.</p>

<p>My question then is how is this more efficient? Each time the page loads I am still going to have to generate each instance of Device and then populate it from the Database, why I don't really see how this is better than the current implementation.</p>

<p>Thanks for any insight!</p>

## Answers
### Answer ID: 21174583
<p>Using OOP is mostly unrelated to performance or efficiency. However, it allows you to organize your code in a modular fashion, and encourage code reuse.</p>

<p>A better webpage to explain can be found <a href="http://felixgers.de/teaching/oop/oop_intro.html" rel="nofollow">here</a>.</p>


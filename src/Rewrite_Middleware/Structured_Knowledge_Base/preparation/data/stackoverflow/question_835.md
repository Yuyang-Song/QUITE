# Handling big arrays in PHP
[Link to question](https://stackoverflow.com/questions/44813388/handling-big-arrays-in-php)
**Creation Date:** 1498688067
**Score:** 1
**Tags:** php, mysql, arrays, json, memory
## Question Body
<p>The application i am working on needs to obtain dataset of around 10mb maximum two times a hour. We use that dataset to display paginated results on the site also simple search by one of the object properties should also be possible.</p>

<p>Currently we are thinking about 2 different ways to implement this</p>

<p>1.) Store the json dataset in the database or a file in the file system, read that and loop over to display results whenever we need.</p>

<p>2.) Store the json dataset in relational MySQL table and query the results and loop over whenever we need to display them.</p>

<p>Replacing/Refreshing the results has to be done multiple times per hour as i said.</p>

<p>Both ways have cons. I am trying to choose a good way which is less evil overall. Reading 10 MB in memory is not a lot and on the other hand rewriting a table few times a hour could produce conflicts in my opinion.</p>

<p>My concern regarding 1.) is how safe the app will be if we read 10mb in the memory all the time? What will happen if multiple users do this at some point of time, is this something to worry about or PHP is able to handle this in background?</p>

<p>What do you think it will be best for this use case?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 44813889
<p>When php runs on a web server (as it usually does) the server starts new php processes on demand when they're needed to handle concurrent requests. A powerful web server may allow fifty or so php processes. If each of them is handling this large data set, you'll need to have enough RAM for fifty copies.   And, you'll need to load that data somehow for each new request.  Reading 10mb from a file is not an overwhelming burden unless you have some sort of parsing to do. But it is a burden.  </p>

<p>As it starts to handle each request, php offers a clean context to the programming environment. php is not good at maintaining in-RAM context from one request to the next.  You may be able to figure out how to do it, but it's a dodgy solution. If you're running on a server that's shared with other web applications -- especially applications you don't trust -- you should not attempt to do this; the other applications will have access to your in-RAM data.</p>

<p>You can control the concurrent processes with Apache or nginx configuration settings, and  restrict it to five or ten copies of php. But if you have a lot of incoming requests, those requests  get serialized and they will slow down.</p>

<p>Will this application need to scale up? Will you eventually need a pool of web servers to handle all your requests? If so, the in-RAM solution looks worse.</p>

<p>Does your json data look like a big array of objects? Do most of the objects in that array have the same elements as each other?  If so, that's conformable to a SQL table? You can make a table in which the columns correspond to the elements of your object.  Then you can use SQL to avoid touching every row -- every element of each array -- every time you display or update data.</p>

<p>(The same sort of logic applies to Mongo, Redis, and other ways of storing your data.)</p>


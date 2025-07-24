# Where to start? Java application with multiple front ends
[Link to question](https://stackoverflow.com/questions/595416/where-to-start-java-application-with-multiple-front-ends)
**Creation Date:** 1235751316
**Score:** 0
**Tags:** java
## Question Body
<p>I've got an application here that I wrote many years ago that consists of a heavy-weight front end that directly queries a database server.  This application runs on about 7 dedicated workstations.  There is also a web-based front-end that I whipped up that shares the same feature set, and a web-based administration too for managing and reporting on the data -- they all just hit the database directly.</p>

<p>The application is quite simple and I understand the problem it solves very well.  It could use an update, and I don't even have access to the tools necessary to work on the GUI anymore.  I've been getting into Java lately, and it seems like a rewrite of this app would be a good project to get started with.</p>

<p>So my question then is this:</p>

<p>The application will require a non-web GUI, I suppose in Swing.  This is necessary for very particular reasons.  The application will also require a web-based GUI with the same exact features as the Swing front that will probably be deployed as a JSR-168 portlet, and a web-based administration tool (portlet also).  With my previous design I ended up with a lot of duplicate code because each component had its own code base, and I foolishly used stored procedures to help to ensure that critical calculations were at least consistent.</p>

<p>Where should I start?  I'm having such a hard time wrapping my mind around how this should all work in the Java world.  I guess what I'm having the hardest time with is how do I create an application that can have both a Swing (or whatever) front-end and a web-based front end with as little duplication as possible?</p>

<p>Edit: I know conceptually how this <em>can</em> work.  What I'm asking is for advice specifically related to Java technologies.  Which frameworks to consider, etc. </p>

## Answers
### Answer ID: 595502
<p>Build a Core that contains the business logic. Use JDepend or a similar tool to ensure that it nowhere references anything swing or anything web/jsp/servlet. </p>

<p>Build the two UIs: For the web version pick a webframework of your choice and call your business logic from there.</p>

<p>For the Swing framework you have two options: access the businesslogic through webservices (you could use RMI or whatever, but I wouldn't), i.e. the logic is on the same webserver that serves the webapp (I'd probably prefer that). The alternative is to ship the weblogic with a swing GUI. Makes the coding and debugging easier, but now you have multiple points that access the db which causes headaches when you want to use caching</p>

<p>In any case you should only duplicate the gui stuff, once in html/css/javascript and once in swing.</p>

<p>Congrats on that project it will teach you tons about design and software architecture</p>

### Answer ID: 595439
<p>Use a middle tier server.</p>

<hr>

<p>Swing Client -> middle-server with spring-remoting -> database</p>

<p>Web Client -> middle-server with spring-remoting -> database</p>

<hr>

<p>Web Client write once any MVC framework will work stripes, struts, even grails if you are brave rememder to keep it thin....</p>

<hr>

<p>Swing Client write once using miglayout, and glazelist.</p>

<p><strong><a href="http://www.miglayout.com/" rel="nofollow noreferrer">http://www.miglayout.com/</a></strong></p>

<p><strong><a href="http://publicobject.com/glazedlists/glazedlists-1.8.0/" rel="nofollow noreferrer">http://publicobject.com/glazedlists/glazedlists-1.8.0/</a></strong></p>

<p>take a look at this posting.....</p>

<p><strong><a href="https://stackoverflow.com/questions/458817/java-swing-libraries-tools-layout-managers">Java Swing: Libraries, Tools, Layout Managers</a></strong></p>

<hr>

<p>Middle-server write once using jdbc cause you have the db already..</p>

<p><strong><a href="http://www.springsource.org/" rel="nofollow noreferrer">http://www.springsource.org/</a></strong></p>

<hr>

<p>database write once using whatever you like. It seems already have this....</p>

### Answer ID: 595483
<p>Obviously start with a unified code base. You might also want to consider whether you really do need multiple interfaces.</p>

<p>You want to make sure that your code does not have unnecessary dependencies. For instance, make you UI as shallow as possible, rather than the usual ball of mud. Avoid singletons, as they cause dependency hell.</p>

<p>It may seem very enterprisey to have a middle tier, but it also adds a lot of work. For a small group it is entirely pointless.</p>

### Answer ID: 595445
<p>You should have a project with all business logic.</p>

<p>Then, 2 separated projects, 1 for the web access, and 1 for the Swing application. those projects both calling the business logic API.
in these 2 projects, have only presentation code</p>


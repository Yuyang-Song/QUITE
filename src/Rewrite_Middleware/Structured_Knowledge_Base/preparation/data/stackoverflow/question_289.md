# Python, PyTables, Java - tying all together
[Link to question](https://stackoverflow.com/questions/1953731/python-pytables-java-tying-all-together)
**Creation Date:** 1261584852
**Score:** 26
**Tags:** java, python, architecture, hdf5, pytables
## Question Body
<h1>Question in nutshell</h1>
What is the best way to get Python and Java to play nice with each other?
<h1>More detailed explanation</h1>
<p>I have a somewhat complicated situation.  I'll try my best to explain both in pictures and words.  Here's the current system architecture:</p>
<p><a href="https://i.sstatic.net/N4P37.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/N4P37.png" alt="Current system architecture" /></a></p>

<p>We have an agent-based modeling simulation written in Java.  It has options of either writing locally to CSV files, or remotely via a connection to a Java server to an <a href="https://www.hdfgroup.org/solutions/hdf5/" rel="nofollow noreferrer">HDF5</a> file.  Each simulation run spits out over a gigabyte of data, and we run the simulation dozens of times.  We need to be able to aggregate over multiple runs of the same scenario (with different random seeds) in order to see some trends (e.g. min, max, median, mean).  As you can imagine, trying to move around all these CSV files is a nightmare; there are multiple files produced per run, and like I said some of them are enormous.  That's the reason we've been trying to move towards an HDF5 solution, where all the data for a study is stored in one place, rather than scattered across dozens of plain text files.  Furthermore, since it is a binary file format, it should be able to get significant space savings as compared to uncompressed CSVS.</p>
<p>As the diagram shows, the current post-processing we do of the raw output data from simulation also takes place in Java, and reads in the CSV files produced by local output.  This post-processing module uses JFreeChart to create some charts and graphs related to the simulation.</p>
<h2> The Problem </h2>
As I alluded to earlier, the CSVs are really untenable and are not scaling well as we generate more and more data from simulation.  Furthermore, the post-processing code is doing more than it should have to do, essentially performing the work of a very, very poor man's relational database (making joins across 'tables' (csv files) based on foreign keys (the unique agent IDs).  It is also difficult in this system to visualize the data in other ways (e.g. Prefuse, Processing, JMonkeyEngine getting some subset of the raw data to play with in MatLab or SPSS).
<h2> Solution? </h2>
My group decided we really need a way of filtering and querying the data we have, as well as performing cross table joins.  Given this is a write-once, read-many situation, we really don't need the overhead of a real relational database; instead we just need some way to put a nicer front end on the HDF5 files.  I found a few papers about this, such as one describing how to use [XQuery as the query language on HDF5 files][3], but the paper describes having to write a compiler to convert from XQuery/XPath into the native HDF5 calls, way beyond our needs.
Enter [PyTables][4].  It seems to do exactly what we need (provides two different ways of querying data, either through Python list comprehension or through [in-kernel (C level) searches][5].
<p>The proposed architecture I envision is this:
<a href="https://i.sstatic.net/Q8QzN.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Q8QzN.png" alt="Envisioned architecture" /></a></p>

<p>What I'm not really sure how to do is to link together the python code that will be written for querying, with the Java code that serves up the HDF5 files, and the Java code that does the post processing of the data.  Obviously I will want to rewrite much of the post-processing code that is implicitly doing queries and instead let the excellent PyTables do this much more elegantly.</p>
<h2> Java/Python options</h2>
A simple google search turns up a few options for [communicating between Java and Python][7], but I am so new to the topic that I'm looking for some actual expertise and criticism of the proposed architecture.  It seems like the Python process should be running on same machine as the Datahose so that the large .h5 files do not have to be transferred over the network, but rather the much smaller, filtered views of it would be transmitted to the clients.  [Pyro][8] seems to be an interesting choice - does anyone have experience with that?

## Answers
### Answer ID: 3539368
<p>Not sure if this is good etiquette.  I couldn't fit all my comments into a normal comment, and the post has no activity for 8 months. </p>

<p>Just wanted to see how this was going for you?  We have a very very very similar situation where I work - only the simulation is written in C and the storage format is binary files.  Every time a boss wants a different summary we have to make/modify handwritten code to do summaries.  Our binary files are about 10 GB in size and there is one of these for every year of the simulation, so as you can imagine, things get hairy when we want to run it with different seeds and such.  </p>

<p>I've just discovered pyTables and had a similar idea to yours.  I was hoping to change our storage format to hdf5 and then run our summary reports/queries using pytables.  Part of this involves joining tables from each year.  Have you had much luck doing these types of "joins" using pytables?</p>

### Answer ID: 1954175
<p>This is an epic question, and there are lots of considerations.  Since you didn't mention any specific performance or architectural constraints, I'll try and offer the best well-rounded suggestions.</p>

<p>The initial plan of using PyTables as an intermediary layer between your other elements and the datafiles seems solid.  However, one design constraint that wasn't mentioned is one of the most critical of all data processing:  Which of these data processing tasks can be done in batch processing style and which data processing tasks are more of a live stream.</p>

<p>This differentiation between "we know exactly our input and output and can just do the processing" (batch) and "we know our input and what needs to be available for something else to ask" (live) makes all the difference to an architectural question.  Looking at your diagram, there are several relationships that imply the different processing styles.</p>

<p>Additionally, on your diagram you have components of different types all using the same symbols.  It makes it a little bit difficult to analyze the expected performance and efficiency.</p>

<p>Another contraint that's significant is your IT infrastructure.  Do you have high speed network available storage?  If you do, intermediary files become a brilliant, simple, and fast way of sharing data between the elements of your infrastructure for all batch processing needs.  You mentioned running your PyTables-using-application on the same server that's running the Java simulation.  However, that means that server will experience load for both writing and reading the data.  (That is to say, the simulation environment could be affected by the needs of unrelated software when they query the data.)</p>

<p>To answer your questions directly:</p>

<ul>
<li>PyTables looks like a nice match.</li>
<li>There are many ways for Python and Java to communicate, but consider a language agnostic communication method so these components can be changed later if necessarily.  This is just as simple as finding libraries that support both Java and Python and trying them.  The API you choose to implement with whatever library should be the same anyway. (XML-RPC would be fine for prototyping, as it's in the standard library, Google's Protocol Buffers or Facebook's Thrift make good production choices.  But don't underestimate how great and simple just "writing things to intermediary files" can be if data is predictable and batchable.</li>
</ul>

<p>To help with the design process more and flesh out your needs:</p>

<p>It's easy to look at a small piece of the puzzle, make some reasonable assumptions, and jump into solution evaluation.  But it's even better to look at the problem holistically with a clear understanding of your constraints.  May I suggest this process:</p>

<ul>
<li>Create two diagrams of your current architecture, physical and logical.

<ul>
<li>On the physical diagram, create boxes for each physical server and diagram the physical connections between each.

<ul>
<li>Be certain to label the resources available to each server and the type and resources available to each connection.</li>
<li>Include physical hardware that isn't involved in your current setup if it might be useful.  (If you have a SAN available, but aren't using it, include it in case the solution might want to.)</li>
</ul></li>
<li>On the logical diagram, create boxes for every <em>application</em> that is running in your current architecture.

<ul>
<li>Include relevant libraries as boxes <em>inside</em> the application boxes.  (This is important, because your future solution diagram currently has PyTables as a box, but it's just a library and can't do anything on it's own.)</li>
<li>Draw on disk resources (like the HDF5 and CSV files) as cylinders.</li>
<li>Connect the applications with arrows to other applications and resources as necessary.  Always draw the arrow <em>from</em> the "actor" <em>to</em> the "target".  So if an app writes and HDF5 file, they arrow goes from the app to the file.  If an app reads a CSV file, the arrow goes from the app to the file.</li>
<li>Every arrow must be labeled with the communication mechanism.  Unlabeled arrows show a relationship, but they don't show <em>what</em> relationship and so they won't help you make decisions or communicate constraints.</li>
</ul></li>
</ul></li>
</ul>

<p>Once you've got these diagrams done, make a few copies of them, and then right on top of them start to do data-flow doodles.  With a copy of the diagram for each "end point" application that needs your original data, start at the simulation and end at the end point with a pretty much solid flowing arrow.  Any time your data arrow flows across a communication/protocol arrow, make notes of how the data changes (if any).</p>

<p>At this point, if you and your team all agree on what's on paper, then you've explained your current architecture in a manner that should be easily communicable to anyone.  (Not just helpers here on stackoverflow, but also to bosses and project managers and other purse holders.)</p>

<p>To start planning your solution, look at your dataflow diagrams and work your way backwards from endpoint to startpoint and create a nested list that contains every app and intermediary format on the way back to the start.  Then, list requirements for every application.  Be sure to feature:</p>

<ul>
<li>What data formats or methods can this application use to communicate.</li>
<li>What data does it actually want. (Is this always the same or does it change on a whim depending on other requirements?)</li>
<li>How often does it need it.</li>
<li>Approximately how much resources does the application need.</li>
<li>What does the application do now that it doesn't do that well.</li>
<li>What can this application do now that would help, but it isn't doing.</li>
</ul>

<p>If you do a good job with this list, you can see how this will help define what protocols and solutions you choose.  You look at the situations where the data crosses a communication line, and you compare the requirements list for <em>both sides</em> of the communication.</p>

<p>You've already described one particular situation where you have quite a bit of java post-processing code that is doing "joins" on tables of data in CSV files, thats a "do now but doesn't do that well".  So you look at the other side of that communication to see if the other side can do that thing well.  At this point, the other side is the CSV file and before that, the simulation, so no, there's nothing that can do that better in the current architecture.</p>

<p>So you've proposed a new Python application that uses the PyTables library to make that process better.  Sounds good so far!  But in your next diagram, you added a bunch of other things that talk to "PyTables".  Now we've extended past the understanding of the group here at StackOverflow, because we don't know the requirements of those other applications.  But if you make the requirements list like mentioned above, you'll know exactly what to consider.  Maybe your Python application using PyTables to provide querying on the HDF5 files can support all of these applications.  Maybe it will only support one or two of them.  Maybe it will provide live querying to the post-processor, but periodically write intermediary files for the other applications.  We can't tell, but with planning, you can.</p>

<p>Some final guidelines:</p>

<ul>
<li><strong>Keep things simple!</strong> The enemy here is complexity.  The more complex your solution, the more difficult the solution to implement and the more likely it is to fail.  Use the least number operations, use the least complex operations.  Sometimes just one application to handle the queries for all the other parts of your architecture is the simplest.  Sometimes an application to handle "live" queries and a separate application to handle "batch requests" is better.</li>
<li><strong>Keep things simple!</strong>  It's a big deal!  Don't write anything that can already be done for you.  (This is why intermediary files can be so great, the OS handles all the difficult parts.)  Also, you mention that a relational database is too much overhead, but consider that a relational database also comes with a very expressive and well-known query language, the network communication protocol that goes with it, <em>and</em> you don't have to develop anything to use it!  Whatever solution you come up with has to be <em>better</em> than using the off-the-shelf solution that's going to work, for certain, very well, or it's not the best solution.</li>
<li><strong>Refer to your physical layer documentation frequently</strong> so you understand the resource use of your considerations.  A slow network link or putting too much on one server can both rule out otherwise good solutions.</li>
<li><strong>Save those docs.</strong> Whatever you decide, the documentation you generated in the process is valuable.  Wiki-them or file them away so you can whip them out again when the topic come s up.</li>
</ul>

<p>And the answer to the direct question, "How to get Python and Java to play nice together?" is simply "use a language agnostic communication method."  The truth of the matter is that Python and Java are both not important to your describe problem-set.  What's important is the data that's flowing through it.  Anything that can easily and effectively share data is going to be just fine.</p>

### Answer ID: 1953842
<p>Do not make this more complex than it needs to be.</p>

<p>Your Java process can -- simply -- spawn a separate subprocess to run your PyTables queries.  Let the Operating System do what OS's do best.</p>

<p>Your Java application can simply fork a process which has the necessary parameters as command-line options.  Then your Java can move on to the next thing while Python runs in the background.</p>

<p>This has HUGE advantages in terms of concurrent performance.  Your Python "backend" runs concurrently with your Java simulation "front end".</p>

### Answer ID: 1953764
<p>You could try <a href="http://wiki.python.org/jython/WhyJython" rel="nofollow noreferrer">Jython</a>, a Python interpreter for the JVM which can <code>import</code> Java classes.</p>

<p><strong><a href="http://www.jython.org/" rel="nofollow noreferrer">Jython project homepage</a></strong></p>

<p><sup>Unfortunately, that's all I know on the subject.</sup></p>


# How to read data from a collection of HTML fragment files?
[Link to question](https://stackoverflow.com/questions/13652884/how-to-read-data-from-a-collection-of-html-fragment-files)
**Creation Date:** 1354308243
**Score:** 2
**Tags:** jquery, html, sql, parsing, text
## Question Body
<p>I've inherited a project that has a very odd quirk I'd like to fix.  The project has a web form where user's key in data and then click a "Submit" button.  Given that we have a SQL database in our office, I expected that each value would be read from the form and saved in a SQL table.</p>

<p>However, this is not the case.  Some values are saved in SQL, but some are not.  How are the values looked up that aren't saved in SQL?  Simple Answer: the Javascript in the form is written so that when the user clicks submit, the mark-up of the entire form is sent to the server and saved in a text file.  Then, when an authorized user wants to see how the user filled out the form, the mark-up is retrieved from the text file and sent down the wire to the browser.</p>

<p>This is clearly not the best way of doing this because it is wasteful of disk space and is not readily queryable.</p>

<p>That's why I'm rewriting the code so that future entries in the web form will be saved entirely in SQL.</p>

<p>In the meantime, I have tens of thousands of text files containing HTML fragments that need to be imported into SQL.  My idea is to write a utility program to parse the files, one-by-one, and save the field values in SQL.</p>

<p>I wanted to ask for advice about the best way to do this.  Normally, I use jQuery to read values from HTML, but I don't know of a practical way to do this with so many files.  I also have Visual Studio 2010 at my disposal.</p>

<p>What tools and techniques would be best to accomplish this task?</p>

## Answers
### Answer ID: 13654004
<p>If you are on a Windows machine, I'd start by using windows script host to make a list of the files you need to process. If you copy the code below into a js file, save that js file into the directory containing thousands of files, then double-click the js file in Windows (to run it in wscript), it will save an array listing the thousands of files you need to check.</p>

<pre><code>var io, here, fileToWrite, files;

io   =  new ActiveXObject('Scripting.FileSystemObject');
here = unescape(io.GetParentFolderName(WScript.ScriptFullName) + "\\");

fileToWrite = io.OpenTextFile(here + "\\filelist.js", 2, true);
fileToWrite.writeLine("filelist=[");

for (files = new Enumerator(io.GetFolder(here).files); !files.atEnd(); files.moveNext()) {
  var file = files.item();
  fileToWrite.writeLine('"' + file.Name + '",');
}

fileToWrite.writeLine("]");
fileToWrite.Close();
WScript.Echo("Process Complete - an array of files has been created");
</code></pre>

<p>You could then create a browser-based jQuery script that would load each file in sequentially, extract the information however you would normally, then save it into a more consumable format such as a text file using the FileSystemObject. (You must use IE for this.)</p>

<p>If you run into security issues trying to create a FileSystemObject in IE, just rename your html file with the "hta" extension - that will create an html application with the rights to do this. </p>


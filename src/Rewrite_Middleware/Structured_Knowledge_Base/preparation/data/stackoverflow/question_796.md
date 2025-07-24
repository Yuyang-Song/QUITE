# Attempting to load a DLL on Windows using LoadLibrary when a dependent DLL is missing
[Link to question](https://stackoverflow.com/questions/4265874/attempting-to-load-a-dll-on-windows-using-loadlibrary-when-a-dependent-dll-is-mi)
**Creation Date:** 1290595399
**Score:** 11
**Tags:** c, windows
## Question Body
<p>I have an application that uses LoadLibrary on Windows to dynamically load plugins. However some of the plugins have other dependent DLLs, such as database client DLLs. 
When you attempt to load such a DLL and one of the dependent DLLs doesn't exist you get a nasty Windows dialog:</p>

<p>"The program can't start because xxx.ddl is missing from your computer. Try reinstalling the program to fix this problem."</p>

<p>Is there any easy way to avoid this dialog? I was hoping one could use LoadLibraryEx and pass a flag that says "don't give me that annoying dialog", but it doesn't seem like it.</p>

<p>What I'd like is for the application to handle that error, rather than Windows handling it for me, especially as the text of the message is incorrect (the problem isn't that the program can't start, the program is running quite happily, it just can't load this plugin).</p>

<p>What I'd like to avoid is having to rewrite the plugins that have these external dependencies to make them themselves do a dynamic load of any dependent modules and then query for any entry points. </p>

<p>Anyway, any suggestions would be gratefully received.</p>

## Answers
### Answer ID: 4265916
<p>Use <a href="http://msdn.microsoft.com/en-us/library/ms680621(VS.85).aspx" rel="noreferrer">SetErrorMode()</a>. Use it with <code>SEM_NOOPENFILEERRORBOX | SEM_FAILCRITICALERRORS</code> before you load the DLL and with <code>0</code> right after.</p>

### Answer ID: 4265910
<p>From MSDN:</p>

<blockquote>
  <p>To enable or disable error messages displayed by the loader during DLL loads, use the SetErrorMode function.</p>
</blockquote>

<p><a href="http://msdn.microsoft.com/en-us/library/ms684175%28VS.85%29.aspx" rel="nofollow">Link here</a></p>


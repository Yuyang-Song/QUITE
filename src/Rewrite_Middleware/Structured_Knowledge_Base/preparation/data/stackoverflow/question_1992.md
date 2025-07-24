# &quot;Access violation&quot; Error on displaying string of simple Oracle Query (VS10 Exp C++)
[Link to question](https://stackoverflow.com/questions/14885487/access-violation-error-on-displaying-string-of-simple-oracle-query-vs10-exp-c)
**Creation Date:** 1360882055
**Score:** 1
**Tags:** c++, oracle-database, database-connection, resultset, occi
## Question Body
<p>I am struggling with an issue regarding running a SQL statement to an Oracle database through C++, using occi.  My code is as follows: </p>

<pre><code>#include &lt;iostream&gt;
#include "occi.h"

namespace oc = oracle::occi;

int main() {
    std::cout &lt;&lt; "Setting up environment...\n";
    oc::Environment * env = oc::Environment::createEnvironment();

    std::cout &lt;&lt; "Setting up connection...\n";
    oc::Connection * conn = env-&gt;createConnection("user","pass","server");

    std::cout &lt;&lt; "Creating statement...\n";
    //Very simply query... 
    oc::Statement * stmt = conn-&gt;createStatement("SELECT '1' FROM dual");

    std::cout &lt;&lt; "Executing query...\n";
    oc::ResultSet * rs = stmt-&gt;executeQuery();

    while(rs-&gt;next()) {
            std::cout &lt;&lt; rs-&gt;getString(1) &lt;&lt; std::endl; //Error is thrown at this line, but after printing since I can see '1' on the console.
    }


    stmt-&gt;closeResultSet(rs);
    conn-&gt;terminateStatement(stmt);
    env-&gt;terminateConnection(conn);
    oc::Environment::terminateEnvironment(env);

    return 0;
}
</code></pre>

<p>The error that is shown is: </p>

<blockquote>
  <p>Unhandled exception at 0x1048ad7a (msvcp100d.dll) in MyDatabaseApp.exe: 0xC0000005: Access violation reading location 0xccccccd0.</p>
</blockquote>

<p>My program stops inside 'xstring' at the following line of code: </p>

<pre><code>    #if _ITERATOR_DEBUG_LEVEL == 0

    ....

    #else /* _ITERATOR_DEBUG_LEVEL == 0 */
    typedef typename _Alloc::template rebind&lt;_Elem&gt;::other _Alty;

    _String_val(_Alty _Al = _Alty())
            : _Alval(_Al)
            {   // construct allocator from _Al
            ....
            }

    ~_String_val()
            {   // destroy the object
            typename _Alloc::template rebind&lt;_Container_proxy&gt;::other
                    _Alproxy(_Alval);  

            this-&gt;_Orphan_all(); //&lt;----------------------Code stops here

            _Dest_val(_Alproxy, this-&gt;_Myproxy);
            _Alproxy.deallocate(this-&gt;_Myproxy, 1);
            this-&gt;_Myproxy = 0;
            }
    #endif /* _ITERATOR_DEBUG_LEVEL == 0 */
</code></pre>

<p>If I change my query to:</p>

<pre><code>oc::Statement * stmt = conn-&gt;createStatement("SELECT 1 FROM dual"); 
</code></pre>

<p>and the loop statement to:</p>

<pre><code>std::cout &lt;&lt; rs-&gt;getInt(1) &lt;&lt; std::endl;
</code></pre>

<p>It works fine with no errors. I think this is because getting an integer simply returns a primitive, but when an object is being returned it is blowing up (I think on a destructor, but I'm not sure why...)</p>

<p>I have been playing around with this for hours today, and I am pretty stuck.</p>

<p>Some information about my system: </p>

<ul>
<li>OS - Windows XP</li>
<li>Oracle Version - 10g</li>
<li>IDE - Microsoft Visual Studio 2010 Express C++</li>
</ul>

<p>My project properties are as follows: </p>

<ul>
<li>C/C++ - General - Additional Include Directories = C:\oracle\product\10.2.0\client_1\oci\include;%(AdditionalIncludeDirectories)</li>
<li>C/C++ - Code Generation - Multi-threaded Debug DLL (/MDd)</li>
<li>Linker - General - Additional Library Directories = C:\oracle\product\10.2.0\client_1\oci\lib\msvc\vc8;%(AdditionalLibraryDirectories)</li>
<li>Linked - Input - Additional Dependencies = oraocci10.lib;oraocci10d.lib;%(AdditionalDependencies)</li>
</ul>

<p>I hope I haven't been confusing with too much info... Any help or insight would be great, Thanks in advance!</p>

<p><b>EDIT</b> If I rewrite my loop, storing the value in a local variable, the error is thrown at the end of the loop: </p>

<pre><code>while(rs-&gt;next()) {
    std::string s = rs-&gt;getString(1); //s is equal to "1" as expected
    std::cout &lt;&lt; s &lt;&lt; std::endl; //This is executed successfully
} //Error is thrown here
</code></pre>

## Answers
### Answer ID: 17428959
<p>I revisited this issue about a month ago and I found that the MSVC2010 occi library was built for Oracle 11g. We are running Oracle 10g, so I had to use the MSVC2005 library. So I installed the outdated IDE and loaded the Debug library and it worked (for some reason the release version wouldn't work though). </p>

<p><b>EDIT</b></p>

<p>For anyone who is having the same problem I was, if downgrading the IDE from MSVC2010 to MSVC2005 with the appropriate libraries doesn't work, you could try upgrading the Oracle client from 10g to 11g and use the MSVC2010 library, as suggested by harvyS. In retrospect this would've probably been the better solution.</p>

### Answer ID: 17424650
<p>Usually such kind of problems come from differences in build environments (IDE) of end user and provider.</p>

<p>Check <a href="http://support.microsoft.com/kb/168958" rel="nofollow noreferrer">this</a>.</p>

<p>Related problems:</p>

<ul>
<li><a href="https://stackoverflow.com/questions/4241882/unhandled-exception-at-0x523d14cf-msvcr100d-dll">Unhandled exception at 0x523d14cf (msvcr100d.dll)?</a></li>
<li><a href="https://stackoverflow.com/questions/2322095/why-does-this-program-crash-passing-of-stdstring-between-dlls">Why does this program crash: passing of std::string between DLLs</a></li>
</ul>

<p>First try to use correct lib and dll. If compiled in debug mode then all libs and dlls must be debug. Use VC++ Modules view to be sure that proper DLL loaded.</p>

<p>I was lucky with my application to have all libs compiled for MSVC2010. So I just check debug and release mode DLLs and got working application.</p>


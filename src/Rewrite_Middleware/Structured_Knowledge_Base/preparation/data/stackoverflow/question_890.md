# Does it make sense to rewrite Perl and shell scripts in java?
[Link to question](https://stackoverflow.com/questions/484355/does-it-make-sense-to-rewrite-perl-and-shell-scripts-in-java)
**Creation Date:** 1233077299
**Score:** 16
**Tags:** java, perl, shell
## Question Body
<p>I have a bunch of scripts - some in perl and some in bash - which are used for:</p>

<ul>
<li>Creating a database (tables, indexes,
constraints, views)</li>
<li>Parsing spreadsheets and loading the data into the database</li>
<li>Getting info about a bunch of files and loading that into the<br>
database.</li>
</ul>

<p>These scripts are used in conjunction with a much larger application that is written in java, and my manager has requested that I rewrite the scripts in java.  His reasoning is that it is easier to work with, port, manage, understand, and support if it's all in one language, and that too many separate pieces is a design issue.</p>

<p>My initial reaction is that this is a bad idea.  The scripts are beautifully concise and fast, and tasks that are trivial in the scripts - such as using regexs to find and replace invalid values - will be so much more verbose and very likely slower when done in java.</p>

<p>The one drawback of the scripts is that when they run on windows they require cygwin in order to run.  Therefore I would like to give a counter proposition that I port all the bash scripts to perl so that they can run on windows without cygwin, and that I spend time organizing and documenting the scripts.</p>

<p>The problem is that a "gut reaction" type of response is not going to be enough to convince my manager.  I come from a linux background, he from Windows, and we have some of the classic linux vs. windows differences in approaches.</p>

<p>So I have two questions:</p>

<ol>
<li>Is my "gut reaction" correct?  Is java slower, more verbose, and harder to maintain for database management, spreadsheet parsing, &amp; file processing tasks?</li>
<li>If the answer to the first question is yes, what is the best way to present my case?</li>
</ol>

<hr>

<p>EDIT:  Thanks everyone for the insights.  I'd like to make one clarification: the scripts are not full-blown apps hidden away in obfuscated scripts.  They are, for the most part, tasks that had been done manually that I automated via scripts and later embellished as the requirements developed.  And the reason I used a scripting language instead of java to start with is because these tasks were <i>so</i> much easier to do in scripts.  For example, one script runs a bunch of queries, formats the results, and outputs them to a file.  How many LOC do you think it would take to do that in java?</p>

## Answers
### Answer ID: 45255573
<p>This is now many years later, but I just went through converting bash scripts with some Perl scripts. I rewrote a system to a Java app, and I also added Groovy. Java and Groovy work well together. </p>

<ul>
<li>groovy runs plain java code.</li>
<li>I can access and manipulate all my java objects/structures/data in groovy. I call groovy scripts that manipulate data in my running java program.</li>
<li>groovy has some nice short-hand syntax. I can easily open a file and write to it with one liners.</li>
<li>groovy also has some short regex syntax as well.</li>
<li>groovy script files are intrepreted at runtime so while my java program is still running, I can change my groovy script code and the next time the files are called it uses the new code.</li>
</ul>

### Answer ID: 4260068
<p>"For manipulating files and moving stuff around, you want the OS on your side"</p>

<p>Be careful following this advice without understanding the proper context!</p>

<p>The OS supports programming API like man (2) and (3) and user commands man (1).</p>

<p>Having a Perl script for example drive a sequence of man(1) is not going to run as fast
as a JVM effectively issue a sequence of man(2) or man(3).</p>

<p>Consider this example:</p>

<p>At the company I joined I found they had a Perl module calling Java utility in a loop - part of a make/perl/java hybrid build contraption.</p>

<p>On the surface, it must have seemed reasonable to have the perl read in metadata and exec/call into a JVM to do the heavy lifting (a proprietary form of file merging in a perl loop).</p>

<p>The overhead (setup/teardown) of this multi-process approach was significant and was especially bad under Windows OS.</p>

<p>The perf issue had to be addressed.</p>

<p>The teams dealt with the perf issue by "reusing" the java program by
hosting it in a servlet and creating a protocol to send commands from the perl to the java servlet. Now the iterative JVM setup/teardown in a loop was reduced an everyone was happy until there were edge use cases like timeout issues where the team added sleeps into the mix.</p>

<p>The culture encourages tool teams to use perl and the service team to use Java.
The best approach of replacing the perl with Java and eliminate all the overhead either was lost to everyone or political forces influenced the rube-goldberg solution...</p>

<p>Doing the build in a JVM language like ANT or Maven avoids all this.</p>

<p>Again, be warned :-)</p>

### Answer ID: 3819347
<p>Remember Java isn't the only JVM language - perhaps something like <a href="http://groovy.codehaus.org/" rel="nofollow">Groovy</a> or <a href="http://www.jython.org/" rel="nofollow">Jython</a> would be a compromise that would keep everyone happy. </p>

### Answer ID: 2396276
<p>On a project in the past Perl code was ported to Java resulting in significant speed increase. The company had mostly Java programmers and our tools Eclipse, Ant, JUnit and Maven were not suited for Perl development. I have seen Perl code in lots of companies, but most of the time it was only meant as temporary solution, quick fix, prototype, demo etc .. It makes sense to rewrite, but you should look at it on a case by case business, sometimes time or manpower would not allow it.</p>

### Answer ID: 488495
<h2>Convert to all <code>Perl</code></h2>

<p>Your right to think that <code>Java</code>'s <code>Regexp</code> is slower. <code>Perl</code>'s <code>Regexp</code> variant has undergone many changes to make sure that it is as fast as possible.</p>

<p>Converting from <code>BASH</code> to <code>Perl</code> should prove easy to accomplish, <code>Perl</code> can easily do what you are doing in <code>BASH</code>.</p>

<p>By getting rid of the <code>BASH</code> files, you can also get rid of Cygwin.</p>

### Answer ID: 491964
<p><strong>Just do as you said: convert your shell to Perl and document it</strong></p>

<p>The code you mention seems not to be part of the application, it seems to be "setup" code or "maintenance" code. As one answer notice, "one job = one tool":</p>

<ul>
<li>for your app, it's Java,</li>
<li>for packaging your app, it's ant or maven or make,</li>
<li>for setting up environment, fill in the db, making reports from logs, it's a scripting language (Perl, Python, shell).</li>
</ul>

<p>To convince your boss:</p>

<ol>
<li><a href="http://en.wikipedia.org/wiki/Golden_hammer" rel="nofollow noreferrer">http://en.wikipedia.org/wiki/Golden_hammer</a> </li>
<li>migrate from one language to another is risky: you'll have to spend lot of time to check for regression errors</li>
<li>In my experience, one line of Perl = 20 lines of Java (give a try: migrate one of your Perl script). So the codebase will be multiplied by 20, and more code to maintain is more headakes</li>
<li><p>Perl maintain all its modules and doc in the same place (cpan.org). For Java, there is no "reference point". You'll have to waste time on the net to make a choice between java spreadsheet parsers, learn to use it (hope the doc will be ok), and make some java-cryptic-glue-code:</p>

<p>SheetHolder = ParserFactory
                  .newInstance(Configuration.asProperties())
                      .parse(SheetReader.asStream());</p></li>
</ol>

### Answer ID: 484382
<p>The trouble is, your Gut reaction might be right, but that doesn't mean your manager is necessarily wrong - he probably has very good reasons for wanting it all done in java. Not least, if you fall under a bus, finding a replacement who knows java, perl and bash is going to be a lot harder than finding someone who knows java. And that's leaving aside the "they can only be run on a PC with cygwin installed" issue. And in all likelihood, performance isn't as big an issue as you think it is.</p>

<p>Having said that, your best bet is to spend a bit of time estimating the time it will take to port them all to java, so he can make an informed decision. And while you're at it, estimate how long it would take to port the bash scripts to perl <strong>and</strong> document them. Then let him decide. Remember - he doesn't get to spend the majority of his time coding, like you do, so it's only fair that he gets to make some decisions instead.</p>

<p>If he decides to proceed with the java option, port one of the scripts as well as you can, then report back with the two versions and, if you're right about the concision of the perl/bash scripts, you should be able to get some mileage from examining the two versions side by side.</p>

<p><strong>EDIT:</strong> MCS, to be honest, it sounds to me as if those scripts are better implemented in perl and/or bash, rather than java, but that's not really the point - the point is how do you demonstrate that to your manager. If you address that, you address both the "gut reaction" question (btw, here's a tip - start referring to your gut reactions as "judgement, based on experience") and the "best way to present my case" question.</p>

<p>Now, the first thing you have to realise is that your manager is (probably) not going down this path just to piss you off. He almost certainly has genuine concerns about these scripts. Given that they're probably genuine concerns (and there's no point in going any further if they're not - if he's made his mind up to do this  thing for some political reason then you're not going to change his mind, no matter what, so just get on with it and add it to your CV) it follows that you need to provide him with information that addresses his concerns if you're going to get anywhere. If you can do that then you're more than halfway to getting your own way.</p>

<p>So, what are his concerns? Based on your post, and on my judgement and experience :-) I'd say they are:  </p>

<ul>
<li>maintainability</li>
<li>that's it, just maintainability</li>
</ul>

<p>I would also guess that his concerns are <strong>not</strong>:  </p>

<ul>
<li>performance</li>
</ul>

<p>I might be wrong about this last one, of course; in the last place I worked we had a SQL Server performance problem to do with replication that impacted the business's ability to provide customer support, so performance was an issue, so we addressed it. But generally speaking performance isn't as much of an issue as programmers think. If he's actually told you that performance is an issue, then factor it in. But if he hasn't mentioned it, forget it - it's probably only you that thinks the fact that these scripts run faster in perl/bash than they probably will in java matters at all.</p>

<p>So, maintainability. This comes down to answering the question "who will maintain these scripts if MCS falls under a bus?" and the supplementary question "will that cause me (i.e. your manager) problems?" (Aside: don't get hung up on the whole bus thing. "Falling under a bus" is a useful and diplomatic shorthand for all sorts of risks, e.g. "what happens if someone lures him away with a salary my company can't match?", "what happens if he decides to emigrate to Bermuda?", "what happens if I want to fire him?", "what happens if I want to promote him?", and, of course, "what happens if just he stops turning up for work one day for some unknown, possibly bus-related, reason?")</p>

<p>Remember, it's your manager's job to consider and mitigate these risks.</p>

<p>So, how to do that?</p>

<p>First, demonstrate how maintainable these scripts actually are. Or at least how maintainable they can be. Document them (in proper documents, not in the code). Train a colleague to maintain them (pick someone who would like to acquire/improve their perl and bash skills, and who your manager trusts). Refactor them to make them more readable (sacrificing performance and clever scripting tricks if necessary). If you want to continue using bash, create a document that provides step-by-step instructions for installing cygwin and bash. Regardless, document the process of installing perl, and running the scripts.</p>

<p>Second, pick one of the scripts and port it to java. Feel free to pick the script that best demonstrates the advantages of perl/bash over java, but <strong>do the best job you can of porting it.</strong> Use java.util.regex to do the same clever things you do in your perl. Document it to the standard that other in-house java utilities are documented. If performance is actually a factor, measure its performance relative to the perl/bash script.</p>

<p>Third, having been through that exercise, be honest with yourself about their relative maintainability. Ask the guy you trained what he thinks. If you still think the perl/bash scripts are more or less as maintainable as java versions would be, estimate the work involved in porting the remaining scripts to java as accurately as you can (you'll be able to do this pretty accurately now, because you'll have actually ported one). Then take the comparative scripts and the documentation and the estimates (and the performance figures, if appropriate) to your manager and go through them with him. Present your counter-proposals (a. leave them in perl and bash but document them and train a colleague, and b. port the bash scripts to perl, document them and train a colleague).</p>

<p>Finally, let your manager weigh up all the information and decide, and abide by his decision. In fact, don't just abide by his decision, accept the fact that he might be right. Just because you know more about perl/bash/java than him doesn't mean you necessarily know more about managing the team/department than he does. And if his decision is to stick with perl/bash, or port to perl, rejoice! Because you have not only got your own way, you have gone up in your manager's estimation and learned an invaluable lesson along the way.</p>

### Answer ID: 486908
<p>Have you considered Ant? I have to admit I never tried, but always wanted to port my scripts to Ant. File operations are easy and there are even tasks to create SQL statements. Of course if your scripts are more like programs, i.e. many loop constructs, then this is not the way to go. Just a suggestion. </p>

### Answer ID: 485805
<p>If you build a shed and use a hammer 80-90% of the time, does it follow that you should use only hammers to build sheds? No, you use the most appropriate tools for each part of the job, just as you have done!</p>

<p>Also the average skills/experience level of the IT work-force has increased in recent years. E.g. This <a href="https://stackoverflow.com/questions/327973/how-old-are-you-and-how-old-were-you-when-you-started-coding-closed">SO Poll</a> showed the medium SO programmer is in their 30's with over 10 years experience.</p>

<p>You boss will have no problem recruiting programmers with a broad mix of skills and experience.</p>

### Answer ID: 484703
<p>It depends. I've found that text processing in Java can take up to 8 or 9 times the amount of code as in Perl. If these scripts need to be tightly integrated into the application then I would agree with your manager but if there just background tasks I'd look into using ActiveState on windows and rewriting the bash scripts in Perl.</p>

### Answer ID: 484657
<p>Just one point.  In many ways, he has a point, but...</p>

<p>Perl (or bash scripting) is a glue language.  It is one of the best languages out there for sticking to systems and making them work better.  Perl is a fully-interpreted language, which affords it significant power for run-time-code-rewrite and more dynamic programming styles.  You can pass perl code blocks around as data, and modify them up until the moment you call "eval" on the string.  Whether or not there's native java functionality to embed perl, you can easily create such embedding yourself, making for an immensely powerful system.</p>

<p>You might want to make clear to your supervisor what potential you will lose if you remove the perl.  At my last job, two of the developers got IronPython added to our "legal language list" so that we could implement libraries and trivially pass them through the database for a massive-scale automation project that turned into a very simple, very tiny project, with a bunch of python code gluing and being glued to compiled modules.</p>

<p>All in all, there are times when a million lines of Java cannot do what 10 lines of Bash script does.  That's when you want to use it.  The rest of the time, your boss is right, so long as you're afforded the time to do it.</p>

### Answer ID: 484611
<p>In general, I understand your manager's desire to minimize and standardize on the different languages/platforms used in your environment.</p>

<p>However, there <em>are</em> certain tasks for which a scripting language is much better suited than a language like Java.  If you feel that's the case with the scripts you're being asked to rewrite, maybe rather than proposing using Perl as a one-off language for this particular task, you could propose adopting Perl (or another scripting language if you think you'd get better buy-in) as the "supported" language for scripting tasks.</p>

<p>That said, depending on what you mean by "used in conjunction with" (that is, how tightly coupled the different bits are), it may simply be the case that these tasks would make more sense written as Java libraries to be called by the rest of the application.</p>

### Answer ID: 484579
<p>From my own experience (which includes mixing Java and Perl in a single system), I'd suggest the following:</p>

<p>1) "Java is slower" is not necessarily true, but also isn't relevant (even if true) unless the additional run time interferes with some time-critical workflow.</p>

<p>2) Long-term maintainability is a legitimate issue. Having e.g. a single DAO layer that doesn't have to be maintained in two languages can pay back in the long haul. How much of your Java code and current scriptage would have to be modified (twice) to cover a refactoring in the database?</p>

<p>3) If you really have a preference for lighter-weight notation, but your manager wants Java, could you compromise on Java libraries (from previous point) combined with one of the interoperable scripting-like languages that runs on the JVM and could share use of the standard libs you write for e.g. database access? I'm thinking of something in the JRuby-Groovy-Scala-Jython spectrum.</p>

### Answer ID: 484412
<p>I certainly agree that it is easier for everyone if you work with a set of tools that most of you know. However, since you have both Java and Perl code I am assuming that at least some of you know both, and as such I honestly do not see the big problem with having both Java and Perl code. </p>

<p>If the Perl scripts work as expected and can be maintained I would not spend time rewriting them in Java. Scripting is a lot easier in Perl than it is in Java imo, so unless you really need to convert, I don't see the point. I would prefer to spend the hours on something that actually adds value to whatever you're doing. </p>

<p>You say that the scripts need cygwin to run. I have done a lot of Perl on both Unix/Linux and Windows, and unless you're doing a lot of specific Unix stuff my experience is that scripts can easily be converted to run under a Windows Perl like ActiveState. Maybe that could be an option in your case. </p>

### Answer ID: 484549
<p>I think your first reaction is right. One argument is <em>If it works, don't 'fix' it.</em> Another argument is that one developer can write almost same amount of SLOC independently of language which used. It sounds strange if you know how is Java verbose but think about how carefully you must design your Java code to get same result using perl features as closures, dynamic generated code, instant regexps and other. And now when Java to Perl SLOC ratio to same result is more than 10:1. Each line of code you must read, understand and maintain. Java is faster. Yes. Java is faster for some thinks as number crunching and some sort of text processing. Perl is faster for regexps and some other text processing and far far more productive than Java generally. Perl is worse maintainable if compared by SLOC but same or better than Java if compared by feature. If Perl is written using best practices and keep coding style than can beat Java in maintainability especially if used for short scripts.</p>

### Answer ID: 484454
<p>I can see what you are saying, but being short and concise isn't always maintainable--sometimes verbose and explicit is maintainable.</p>

<p>Also, once it's all in Java, you'll be more likely to have a UI/Control Console feel which might be an improvement.</p>

<p>If you really like the scripting language feel, maybe you could counter-propose groovy.  It's syntax is very easy for Java programmers to pick up and it's 100% java compatible (including extending java classes in groovy and the like), yet it's a scripting language--as powerful as any--with all the power and lack of compiling that implies.</p>

<p>By the way, Java handles regular expressions fine.</p>

<p>Also by the way, If you wrote all these scripts and are the only one familiar with them, you might want to start looking around for a new job.  Sorry to say it, but asking you to make your "Special little tricks" documented and maintainable is often something they don't think about until just before a layoff.</p>

### Answer ID: 484439
<p>For me, it depends on how badly written the Perl is (I've never seen Perl that I would say was "WELL" written), and whether you'll ever need to READ the Perl. </p>

<p>Perl is often a Write Once, Read Never language. If it all works, and you're not likely to need to alter it, I would say don't touch it.</p>

### Answer ID: 484421
<p>Should they be rewritten?  That depends.  The strongest argument that your boss has is that the rest of the application is written in Java and sounds like that might be the way the organization is headed.  Reducing the number of different langues that must be supported by the organization is actually a pretty smart long term decision.  I know, I know, right tool for the right job, but from a cost perspective,it is entirely possible that it will cost the organization more money to hire someone who knows both PERL and JAVA than just Java.  Even if the scripts are beautiful they still have to be supported, and that means he has to keep at least one person on staff who knows how to do that.  It's another thing that he (and the organization) has to worry about at the end of the day.</p>

### Answer ID: 484406
<p>Personally I find db, file management harder to do with java, but it may be easier to maintain once they are written. </p>

<p>But is it worth it? If it works, don't 'fix' it.</p>

<p>Personally I don't care - If I get work to do, I debate pros and cons with my manager and if she insists, I do it and get payed. Usually she comes to her senses though, and gives me more important work to do.</p>

### Answer ID: 484374
<blockquote>
  <p>Is my "gut reaction" correct? Is java
  slower, more verbose, and harder to
  maintain for database management,
  spreadsheet parsing, &amp; file processing
  tasks?</p>
</blockquote>

<p>No.  </p>

<p>It seems like your manager is tasking the wrong person to do this.  Its clear that you're not comfortable writing Java and that you shouldn't be doing so.  Why doesn't one of the developers from the "java side" help you out?</p>


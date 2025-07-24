# refactor old webapp to gain speed
[Link to question](https://stackoverflow.com/questions/7488971/refactor-old-webapp-to-gain-speed)
**Creation Date:** 1316538578
**Score:** -1
**Tags:** url-rewriting, upgrade, legacy-app
## Question Body
<p>4 years ago, I've built a webapp which is still used by some friends. the problem with that app, is that now it has a huge database, and it loads very slow. I know that is just my fault, mysql queries are mixted all over the places(even in the layout generation time). </p>

<p>ATM I know some about OO. I'll like to use this knowledge in my old app, but I don't know how to do it without rewriting all the from the beginning. Using MVC for my app, is very difficult at this moment.</p>

<p>If you were in my place, or if you will had the task to improve the speed of my old app, how you will do it? Do you have any tips for me? Any working scenarios?</p>

## Answers
### Answer ID: 7489485
<p>It all depends on context. The best would be to change the entire application, introducing best practices and standards at once. But perhaps would be better to adopt an evolutionary approach:</p>

<p>1- Identify the major bottlenecks in the application using a profiling tool or load test.</p>

<p>2 - Estimate the effort required to refactoring each item.</p>

<p>3 - Identify the pages for which performance is more sensitive to the end user.</p>

<p>4 - Based on the information identified create a task list and set the priority of each item.</p>

<p>Attack one prolem at a time, making small increments. Always trying to spend 80% of your time solving the 20% more critical problems.</p>

### Answer ID: 7489110
<p>Hard to give specific advice without a specific question, but here are some general optimization/organization techniques:  </p>

<ol>
<li>Profile to find hot spots in your code</li>
<li>you mention mysql queries being slow to load, try to optimize them</li>
<li>possibly move data base access to stored procedures to help modularize your code</li>
<li>look for repeated code and try to move it to objects one piece at a time</li>
</ol>


# Upgrading a .NET application data layer
[Link to question](https://stackoverflow.com/questions/7914891/upgrading-a-net-application-data-layer)
**Creation Date:** 1319713006
**Score:** 3
**Tags:** .net, entity-framework, data-layer
## Question Body
<p>I work for a company that develops a very large scale data based application. The application was first created around ten years ago and as such, is in desperate need of an upgrade. I have been given the task of investigating and implementing the data layer upgrade.</p>

<p>At present, it uses a system with business objects that are all based on/extend <code>DataRow</code> objects, that is - each object more or less relates to one row in a database. The application is NOT currently object oriented, but this causes many problems and we want to move in the OO direction.</p>

<p>So we are looking to start using the .NET `Entity Framework' and create an .edmx file. The idea is simply to drag all of the SQL database tables onto the .edmx designer and let it create its related data objects.</p>

<p>Now in my mind (as an OO developer), I was planning to manually create new business objects and populate them from the .edmx generated data objects returned from queries in the new data layer. This would allow the simple separation of the various layers using an interface.</p>

<p>The problem is that the boss says that there is not enough time to rewrite the hundred or so business object classes and he suggests using the .edmx generated data objects throughout the whole application. </p>

<p>Every thought in my mind says 'no... don't create that coupling between the data layer and the whole system', but the boss says that he has seen articles online promoting this.</p>

<p>So my questions for you guys are these: (please provide valid reasons for your answers to 1 and 2)</p>

<ol>
<li><p>Is this a viable solution (even short term)? </p></li>
<li><p>Is there a better/alternative solution to creating separate business objects from the generated data objects?</p></li>
<li><p>Is there a better/easier way to create separate business objects from the generated data objects rather than manually copying and pasting?</p></li>
</ol>

<p>I understand that these questions are somewhat subjective, but I've provided as much specific information as possible and I could really do with some advice on the subject.</p>

## Answers
### Answer ID: 7915426
<blockquote>
  <p>The problem is that the boss says that there is not enough time to
  rewrite the hundred or so business object classes and he suggests
  using the .edmx generated data objects throughout the whole
  application.</p>
</blockquote>

<ol>
<li>Is this a viable solution (even short term)?
&amp;</li>
<li>Is there a better/alternative solution to creating separate business objects from the generated data objects?
&amp;</li>
<li>Is there a better/easier way to create separate business objects from the generated data objects rather than manually copying and pasting?</li>
</ol>

<p><strong>ANS:</strong> You could try <a href="http://www.sybase.com/products/modelingdevelopment/powerdesigner" rel="nofollow">Sybase PowerDesigner</a> that can reverse engineer and generate C# code for you.
Or you could try <a href="http://www.codesmithtools.com/product/frameworks" rel="nofollow">CodeSmith</a>  to generate the code for you.These tools save your time.</p>

<p>There are other frameworks like <a href="http://www.devexpress.com/products/NET/ORM/" rel="nofollow">Developer Express XPO</a> and <a href="http://dataobjects.net/" rel="nofollow">DataObjects.Net</a> etc... or <a href="http://www.llblgen.com/" rel="nofollow">LLBLGen Pro</a> you could try.These can separate your concern.</p>

### Answer ID: 7915182
<p>This is one common issue happens to probably every legacy system people try to upgrade.</p>

<p>I don't see any point that you create "hundreds" of business objects and copy data from EF data objects to yours? You are still coupling with a EF and your business objects! </p>

<p>To get passed with coupling <code>IoC</code> should be used where you can consider keeping the separation from your data access layer from your business layer. And definitely you can switch ORM with very little cost/time. This is the beauty of <code>separation of concern</code>.</p>

<p>In software industry, if you want to cut down the cost now, you probably have to pay more in the long run (if you need to change or ORM once again).</p>

<p>Try to negotiate with your boss in terms of quality, which maybe a bit costly now but definitely be gaining in the long run.</p>

<p>And in your case, you may consider <code>EF Code First</code>. This will definitely give you a better grip than "Database first" on your data access layer design.</p>

<p>You may also code generators to generate your data access layer like the way you want which will save hundreds of man hour, plus you can get a better implementation of your module. I would suggest you to go for CodeSmith Generator. There's a bit of learning curve, but it's worth it.</p>

<p>Please keep in mind separating the data access is not the solution to upgrade a legacy system. I have seen in many cases where upgrading and maintaining the core functionality becomes the hardest job in the world. And there's nothing much to do unless the business people decides for a real upgrade when they face loses.</p>

<p>Try to identify the core components and DAL must be one of then to be upgraded.</p>

### Answer ID: 7915011
<p>When I started developing my current application, I chose to use Code First, so as not to create a gigantic edmx. I read that they're making improvements to that designer (splitting it up etc.) but as it was, I didn't want to try and use the edmx because of the 100+ objects we have to create. </p>

<p>I developed a small application to read the table and create POCO objects for code-first (I think there are tools to do this now), then create a class representing the context containinig DbSet for all these objects. </p>

<p>What I found when I tried to use these objects right up into an MVC application on the front end was that I got serialization problems trying to put them into grids (heavy use of json serialization) with circular reference problems. So, I chose to create ViewModels and in cases where I don't need the speed, use a tool like AutoMapper to map Table &lt;-> ViewModel. In cases where I do need the speed (like listing screens), I wrote the actual linq query to translate the results into the view model object. The only issue I find with this is that the viewmodels have to be very flat.</p>

<p>Not really an answer for you, but some experience from going through this. </p>


# Navigation properties not being loaded after upgrading EF 4.1 to 6.1.2
[Link to question](https://stackoverflow.com/questions/43063257/navigation-properties-not-being-loaded-after-upgrading-ef-4-1-to-6-1-2)
**Creation Date:** 1490686291
**Score:** 1
**Tags:** c#, entity-framework
## Question Body
<p>I've recently upgraded Entity Framework version 4.1 to 6.1.2 targeting .Net framework 4.0. It has database first approach. </p>

<p>The problem I am facing is, before upgrading all navigation properties are loaded correctly but after upgradation it returns always Null.</p>

<p>Here is the current configuration after upgradation which exact same as before.</p>

<ol>
<li>lazy loading is enabled.</li>
<li>Proxy is enabled.</li>
<li>I've deleted previously created entities and regenerated DBContext and all entity classes using EF 6.1 code generator (T4 templates)</li>
<li>All other things are working fine. Just navigation properties are not working.</li>
</ol>

<p>As an example, this below is working fine before upgradation.</p>

<pre><code>var listResult = entities.sampleEntity.where(c=&gt;c.active).ToList();
var result = listResult.navigationProperty1.navigationCollection1.select(c=&gt;c.active).firstOrDefault().Id;
</code></pre>

<p>Am I missing any configuration after upgrading EF? As of now I've following two solution to try out.</p>

<ol>
<li>Rewrite all queries to load related entities. This has risk of changing many number of queries.</li>
<li>Once again upgrade EF 6.1.2 with DataContext code generator. This has risk as it is not going to supported from EF 7 i guess. And it is recommended to use DBContext.</li>
</ol>

<p>EDIT:</p>

<p>I've used EF 6.x EntityObject Generator to use ObjectContext API with EF 6. Everything is working fine same as before upgrading the version. </p>

<p>Thanks,
Fenil</p>


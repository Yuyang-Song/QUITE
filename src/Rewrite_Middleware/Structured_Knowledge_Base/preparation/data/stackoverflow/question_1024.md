# Avoiding or fixing namespace pollution in .Net Core
[Link to question](https://stackoverflow.com/questions/55424655/avoiding-or-fixing-namespace-pollution-in-net-core)
**Creation Date:** 1553889153
**Score:** 3
**Tags:** c#, asp.net-core
## Question Body
<h1>Summary</h1>

<p>For my CS capstone project we are encountering an issue with a class name existing in two different dependencies.  Specifically, we are using a dependency for using MySQL with Entity Frame and one for just connected and executing MySQL queries directly.  </p>

<h2>Background</h2>

<p>The non-EF is owned by a component outside of the project, and this database is one of our main ways of interacting with the database.  It has been requested by the client/mentor that any additions or changes we need be made to a separate database, which is the database EF is connecting to.</p>

<h1>The question</h1>

<p>My question is essentially about how do I fix error <code>the type &lt;class-name&gt; exists in both...</code>, but I'm more wondering about the root problem of namespace pollution in .Net Core and the courses of action we can take.  I have looked into the error and the initial results described a fix that is only applicable in .Net not .Net Core and an explanation that .Net Core does not support aliasing.  </p>

<h2>Potential fixes</h2>

<ul>
<li><p><strong>Separate projects</strong> - I have asked someone I know who has more experience with .Net, and he suggest making separate projects.  While that would obviously work in terms of getting rid of a build error, I do not know how we could make use of one in the main ASP.Net app.  I am assuming either both need to be apps or making one into a library.  I am also assuming that if it is a separate library it will have the same problem we are having now.</p></li>
<li><p><strong>Removing one dependency</strong> - I am currently considering that the less than ideal solution is rewriting the code that relies on EF to use the direct MySQL connection dependency.  There is less code relying on that EF database, so it would be simpler to rewrite that and some SQL.</p></li>
<li><p><strong>Aliasing or full reference</strong> - The results I have found that seem to only be applicable to .Net describe using an alias or referencing the full path of the decency in the type.  From what I have read, this is not currently supported in .Net Core.  If it is, how may I go about it?</p></li>
</ul>

<pre class="lang-cs prettyprint-override"><code>using System;
using System.Collections.Generic;
using MySql.Data.MySqlClient;

namespace OVD.API.GuacamoleDatabaseConnectors
{
    public class GuacamoleDatabaseConnector : IDisposable
    {

        private MySqlConnection connection;
...
</code></pre>

<p>The error is on the MySqlConnection type and is, in full: <code>GuacamoleDatabaseConnectors/GuacamoleDatabaseConnector.cs(81,16): error CS0433: The type 'MySqlConnection' exists in both 'MySql.Data, Version=8.0.15.0, Culture=neutral, PublicKeyToken=c5687fc88969c44d' and 'MySqlConnector, Version=0.49.2.0, Culture=neutral, PublicKeyToken=d33d3e53aa5f8c92' [/Users/markbeussink/Action/OVD/OVD.API/OVD.API.csproj]</code></p>

<p>Here is the <code>.cs.proj</code></p>

<pre class="lang-xml prettyprint-override"><code>&lt;Project Sdk="Microsoft.NET.Sdk.Web"&gt;
  &lt;PropertyGroup&gt;
    &lt;TargetFramework&gt;netcoreapp2.2&lt;/TargetFramework&gt;
    &lt;AspNetCoreHostingModel&gt;InProcess&lt;/AspNetCoreHostingModel&gt;
  &lt;/PropertyGroup&gt;
  &lt;ItemGroup&gt;
    &lt;PackageReference Include="Microsoft.AspNetCore.App"/&gt;
    &lt;PackageReference Include="Microsoft.AspNetCore.Razor.Design" Version="2.2.0" PrivateAssets="All"/&gt;
    &lt;PackageReference Include="Ldap.NETStandard" Version="1.0.3"/&gt;
    &lt;PackageReference Include="MySql.Data" Version="8.0.15"/&gt;
    &lt;PackageReference Include="Pomelo.EntityFrameworkCore.MySql" Version="2.2.0"/&gt;
  &lt;/ItemGroup&gt;
&lt;/Project&gt;
</code></pre>

## Answers
### Answer ID: 55425929
<p>It's really bad form for two separate projects to have a type with the same namespace and the same name, for the reason you've just discovered.   It is not at all normal or expected that you would run into such a conflict, and you may well never encounter it again in your career.</p>

<p>It looks like this project: </p>

<p><a href="https://www.nuget.org/packages/MySqlConnector/" rel="nofollow noreferrer">https://www.nuget.org/packages/MySqlConnector/</a></p>

<p>decided to clobber the namespace of the more official ADO.NET provider for MySQL:</p>

<p><a href="https://www.nuget.org/packages/MySql.Data" rel="nofollow noreferrer">https://www.nuget.org/packages/MySql.Data</a></p>

<p>by defining a type called: <code>MySql.Data.MySqlClient.MySqlConnection</code>, instead of using <code>MySqlConnector.MySqlClient.MySqlConnection</code>, or somesuch.  </p>

<p>The best way forward is to exclude one of these from your projects, and use just the other.  Here the obvious choice would be to switch from</p>

<p><a href="https://www.nuget.org/packages/Pomelo.EntityFrameworkCore.MySql/" rel="nofollow noreferrer">https://www.nuget.org/packages/Pomelo.EntityFrameworkCore.MySql/</a></p>

<p>to </p>

<p><a href="https://www.nuget.org/packages/MySql.Data.EntityFrameworkCore/" rel="nofollow noreferrer">https://www.nuget.org/packages/MySql.Data.EntityFrameworkCore/</a></p>

<p>But I don't have any opinion on the relative merits of these libraries.</p>

<p>If you can't do this, C# provides a <a href="https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/reference-compiler-option" rel="nofollow noreferrer">compiler directive</a> for you to alias one of the assemblies with a different namespace.  See <a href="https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/cs0433" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/cs0433</a></p>

<p>This will in effect add a new outermost namespace level to the offending assembly, so the <em>other</em> MySqlConnection would be known (only in your code) as <code>SomeAlias.MySql.Data.MySqlClient.MySqlConnection</code>.</p>

### Answer ID: 55424854
<p>Just create a new project "class library" and inside this project, you can create an interface which gives you access to a method from one of your component (you need to implement your "component" and its method inside this project). Something like in facade pattern. Then in the rest of your solution, you will use a newly created project reference only. This solution allows you define your own namespace name</p>


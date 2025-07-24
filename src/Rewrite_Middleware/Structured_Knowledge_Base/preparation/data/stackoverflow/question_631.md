# DbGeography Alternative for C# POCO
[Link to question](https://stackoverflow.com/questions/34211759/dbgeography-alternative-for-c-poco)
**Creation Date:** 1449781706
**Score:** 5
**Tags:** c#, entity-framework, spatial
## Question Body
<p>I'm writing an application where I need to query for a records within a radius of some position.  I started out with just a lat / long pair of properties on my PCO but realised that spatial searches in SQL are done against a column type of geography which translates down to DbGeography in the POCO (referenced in another SO post and also using EF Powertools Reverse Engineer POCO).</p>

<p>So, the problem I'm seeing is that I keep my POCOS as clean as possible leaving out all references / dependencies to entity framework and the persistence store as possible.  I have my POCOS in a model/Domain assembly which should never have any references to EF.  Only my Repository classes and DataStore for DbContext subclass and Fluent Configuration projects know about EF. I also stay away from DataAnnotation attributes using fluent configuration. As soon as you put DbGeography you need 'using System.Data.Entity.Spatial' and 'EF' which breaks the persistence agnostic approach, at least for the <strong>"Plain" Old C# Object</strong>.</p>

<p>With so many database platforms around and to make this system as future proof as possible with minimal effort to rewrite the data store code in the event I want to switch to another persistence store it's very important to keep my domain code as clean as possible.  I find it odd that EF fluent code based config was introduced and allowed us to not have to use DataAnnotations attributes therefore keeping System.Data.Entity out of the mix, yet with spatial they break the pattern.</p>

<p>Does anyone know how to approach what I'm trying to do?</p>

<p>--Update after Scott's Comment:
So there is a slight issue still.
I have the reference to System.Data.Entity and I have this on my model: 
<strong>public System.Data.Spatial.DbGeography GeoLocation { get; set; }</strong></p>

<p>I have this in my configuration class:
<strong>this.Property(t => t.GeoLocation).HasColumnName("GeoLocation").HasColumnType("geography");</strong></p>

<p>The this.Property gets underlined and I get this compile error:
<strong>Severity  Code    Description Project File    Line    Suppression State
Error   CS0453  The type 'DbGeography' must be a non-nullable value type in order to use it as parameter 'T' in the generic type or method 'StructuralTypeConfiguration.Property(Expression>)'   FoodRadar.DataStore C:\Developer\SrcSt\FoodRadar\FoodRadar.DataStore\Configuration\VendorConfiguration.cs   66  Active</strong></p>

<p>I tried another reverse poco generator which uses a t4 template and it generates using System.Data.Entity.Spatial.DbGeography but that requires a reference to EntityFramework still.</p>

<p>How am I supposed to specify the mapping?</p>

## Answers
### Answer ID: 34211927
<p>As of .NET 4.5 they realized the need to have <code>DbGeography</code> as part of the core .NET Framework and moved it <a href="https://msdn.microsoft.com/en-us/library/system.data.entity.spatial.dbgeography(v=vs.113).aspx" rel="noreferrer">out of EntityFramework.dll</a> and into <a href="https://msdn.microsoft.com/en-us/library/system.data.spatial.dbgeography(v=vs.110).aspx" rel="noreferrer">System.Data.Entity.dll</a>, which is the ORM Agnostic API they now provide so that EF and any other ORM can build against it.</p>


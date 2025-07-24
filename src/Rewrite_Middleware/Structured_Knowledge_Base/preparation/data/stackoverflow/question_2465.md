# serialized property to complex type in dto with linq and automapper
[Link to question](https://stackoverflow.com/questions/35602996/serialized-property-to-complex-type-in-dto-with-linq-and-automapper)
**Creation Date:** 1456318993
**Score:** 2
**Tags:** c#, linq, serialization, automapper, azure-mobile-services
## Question Body
<p>I'm having a hard time figuring something out that seems as a "easy" problem. 
I'm working with Microsoft Azure mobile apps .Net backend, a MSSQL database, Entity Framework code-first and AutoMapper. 
So i have the following objects:</p>

<pre><code>public class Route
{
    public string Id { get; set; }
    [...] //some other properties
    public string SerializedGoogleRoute { get; set; }
}

public class DtoRoute
{
    public string Id { get; set; }
    [...]
    public DtoGoogleRoute GoogleRoute { get; set; }
}

public class DtoGoogleRoute
{
    [...] //only strings, ints,... 
}
</code></pre>

<p>So what I want to do is: In the database save the GoogleRoute as a serialized string because it consists of many properties and I don't need them in different columns - I just want it as a serialized string in one column on the route entity. 
When the Route object is projected to the DtoRoute object I want the GoogleRoute to be serialized and vice versa. </p>

<p>Because I'm working with LINQ / queryables I am limited to a few AutoMapper mapping options (see <a href="https://github.com/AutoMapper/AutoMapper/wiki/Queryable-Extensions" rel="nofollow noreferrer">AutoMapper wiki</a>). And with none of these I can't get it to work. </p>

<p>The problems I'm facing/what I tried: 
I can't serialize/deserialize the string to the DtoGoogleRoute on mapping (with MapFrom or ConstructProjectionUsing) because LINQ obviously cannot transform the JsonConvert.Serialize/Deserialize methods to SQL statements. </p>

<p>I tried having a DtoGoogleRoute property in the Route object and a string property in the DtoRoute object with getters/setters doing the (de)serialization. This works almost perfectly in a custom API controller but because of the OData query filter the azure mobile app .Net backend uses in the tablecontrollers again only the serialized string property gets returned to the client (because OData/LINQ does not know of the other property). </p>

<p>Another option was making a complex type out of DtoGoogleRoute with Entity Framework - this works fine but not with AutoMapper because AutoMapper can't handle complex types. </p>

<p>For now I'm working with a custom API controller and this works. But it would be better to use the tablecontrollers because they support offline sync. </p>

<p>I can't imagine such a simple thing (at least I thought it was a simple thing) can't be done or is so hard to do. But maybe the problem is all the components (tablecontroller, OData, LINQ, EF, AutoMapper) involved. </p>

<p>I would really be thankful if someone could help.</p>

<p>[EDIT]: I think the fact that it works with a normal api controller and not with a tablecontroller has something to do with OData. I tried putting the same code in a tablecontroller method and in an API controller method. when calling the API controller method I can see on the server that it just calls this function and returns all the right properties to the client (checked with fiddler). But when calling the tablecontroller method the tablecontroller method "rewrites" the URL to a OData URL --> I think this is because of some of the EnableQuery or other OData attributes. Because <a href="https://github.com/azzlack/Microsoft.AspNet.OData.Extensions.ODataQueryMapper" rel="nofollow noreferrer">here</a> (although not AutoMapper but it seems like a similar project from Microsoft) it says that the EnableQuery attribute is called twice - also when the request leaves the server. And I think it cuts of the GoogleRoute property because it does not know about this property in the OData metadata or something like that. </p>

## Answers
### Answer ID: 35603875
<p>You can achieve it like this -</p>

<pre><code>internal class RouteToDtoConverter : TypeConverter&lt;Route, DtoRoute&gt;
{
    protected override DtoRoute ConvertCore(Route source)
    {
        return new DtoRoute
        {
            Id = source.Id,
            GoogleRoute = JsonConvert.DeserializeObject&lt;DtoGoogleRoute&gt;(source.SerializedGoogleRoute)
        };
    }
}

internal class DtoToRouteConverter : TypeConverter&lt;DtoRoute, Route&gt;
{
    protected override Route ConvertCore(DtoRoute source)
    {
        return new Route
        {
            Id = source.Id,
            SerializedGoogleRoute = JsonConvert.SerializeObject(source.GoogleRoute)
        };
    }
}

public class Route
{
    public string Id { get; set; }

    public string SerializedGoogleRoute { get; set; }
}

public class DtoRoute
{
    public string Id { get; set; }

    public DtoGoogleRoute GoogleRoute { get; set; }
}

public class DtoGoogleRoute
{
    public int MyProperty { get; set; }
    public int MyProperty2 { get; set; }
}


AutoMapper.Mapper.CreateMap&lt;Route, DtoRoute&gt;()
            .ConvertUsing(new RouteToDtoConverter());

AutoMapper.Mapper.CreateMap&lt;DtoRoute, Route&gt;()
            .ConvertUsing(new DtoToRouteConverter());

var res = Mapper.Map&lt;DtoRoute&gt;(new Route
        {
            Id = "101",
            SerializedGoogleRoute = "{'MyProperty':'90','MyProperty2':'09'}"
        });

var org = Mapper.Map&lt;Route&gt;(res);  //pass
</code></pre>


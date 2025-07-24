# Recreating this SQL to LINQ (C#, NET 4.5)
[Link to question](https://stackoverflow.com/questions/28698415/recreating-this-sql-to-linq-c-net-4-5)
**Creation Date:** 1424788205
**Score:** -1
**Tags:** c#, mysql, .net, sql-server, linq
## Question Body
<p>I have to query the database and to do so requires that I do quite a few inner joins and a couple of left outer joins. I've generated the SQL in a view but I am now having a bit of difficulty rewriting it to LINQ in my applications data layer.</p>

<pre><code>FROM            dbo.Organisation 
INNER JOIN
                         dbo.EducationCourseVenue
 INNER JOIN
                         dbo.EducationCourseVenueLocation ON dbo.EducationCourseVenue.Id = dbo.EducationCourseVenueLocation.EducationCourseVenueId ON 
                         dbo.Organisation.GlobalEntityGUID = dbo.EducationCourseVenue.GlobalEntityGUID
 INNER JOIN
                         dbo.CommunicationType
 INNER JOIN
                         dbo.CommunicationTypeGlobalEntityMap ON dbo.CommunicationType.Id = dbo.CommunicationTypeGlobalEntityMap.CommunicationTypeId ON 
                         dbo.EducationCourseVenue.GlobalEntityGUID = dbo.CommunicationTypeGlobalEntityMap.GlobalEntityGUID 
INNER JOIN
                         dbo.Country 
INNER JOIN
                         dbo.Address ON dbo.Country.Id = dbo.Address.CountryId 
INNER JOIN
                         dbo.CountryRegion ON dbo.Country.RegionId = dbo.CountryRegion.Id ON 
                         dbo.CommunicationTypeGlobalEntityMap.CommunicationTypeItemId = dbo.Address.Id 
LEFT OUTER JOIN
                         dbo.AddressPostalDistrictMap 
INNER JOIN
                         dbo.RegionItemDistrictMap ON dbo.AddressPostalDistrictMap.Id = dbo.RegionItemDistrictMap.Id
 INNER JOIN
                         dbo.RegionTypeItem ON dbo.RegionItemDistrictMap.RegionTypeItemId = dbo.RegionTypeItem.Id ON 
                         dbo.Address.Id = dbo.AddressPostalDistrictMap.AddressId 
LEFT OUTER JOIN
                         dbo.RHSGarden
 INNER JOIN
                         dbo.AddressGeographics ON dbo.RHSGarden.Id = dbo.AddressGeographics.NearestRHSGardenId ON dbo.Address.Id = dbo.AddressGeographics.AddressId
WHERE        (dbo.CommunicationType.Code = 'AD')
</code></pre>

<p>This particular line of SQL is a problem for in LINQ</p>

<pre><code>FROM            dbo.Organisation 
    INNER JOIN
                             dbo.EducationCourseVenue
     INNER JOIN
                             dbo.EducationCourseVenueLocation ON dbo.EducationCourseVenue.Id = dbo.EducationCourseVenueLocation.EducationCourseVenueId ON 
                             dbo.Organisation.GlobalEntityGUID = dbo.EducationCourseVenue.GlobalEntityGUID
</code></pre>

<p>I don't know how to do a join in LINQ without specifying key joins and then doing another join below that. </p>

<p>Any ideas?</p>

## Answers
### Answer ID: 28699373
<pre><code>var q = from o in context.Organisation
        join v in context.EducationCourseVenue on o.GlobalEntityGUID equals v.GlobalEntityGUID
        join l in context.EducationCourseVenueLocation on v.Id equals l.EducationCouseVenueId
</code></pre>

<p>Is how i think of it, since your:</p>

<pre><code>FROM            dbo.Organisation 
    INNER JOIN
                             dbo.EducationCourseVenue
     INNER JOIN
                             dbo.EducationCourseVenueLocation ON dbo.EducationCourseVenue.Id = dbo.EducationCourseVenueLocation.EducationCourseVenueId ON 
                             dbo.Organisation.GlobalEntityGUID = dbo.EducationCourseVenue.GlobalEntityGUID
</code></pre>

<p>Corresponds to:</p>

<pre><code>FROM dbo.Organisation as o
    INNER JOIN dbo.EducationCourseVenue as v ON o.GlobalEntityGUID = v.GlobalEntityGUID
    INNER JOIN dbo.EducationCourseVenueLocation as l ON v.Id = l.EducationCourseVenueId
</code></pre>


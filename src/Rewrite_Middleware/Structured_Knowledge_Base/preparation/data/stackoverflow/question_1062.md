# org.postgresql.util.PSQLException: ERROR: function st_dwithin(geometry, double precision, double precision) does not exist
[Link to question](https://stackoverflow.com/questions/57176354/org-postgresql-util-psqlexception-error-function-st-dwithingeometry-double-p)
**Creation Date:** 1563948862
**Score:** 2
**Tags:** java, postgresql, spring-boot, postgis
## Question Body
<p>I would like to get all stores near a specific location however it seems that I am having a problem with the query string. I have checked the version of postgis is <em>postgis 2.5.2_2</em>. I have also checked to see if longitude and latitude have double precision.</p>

<p>My database has the following structure:
<a href="https://i.sstatic.net/oLwdI.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/oLwdI.png" alt="enter image description here"></a></p>

<p>I have tried to rewrite the query Into a different query string but I still get the same error.</p>

<p>My Entity:</p>

<pre><code>@Entity
@Table(name = "seller_geolocation_ms")
public class Seller_Geolocation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private static final long serialVersionUID = 2L;

    private double latitude;
    private double longitude;
    private String country;
    private String cityName;
    private String zipCode;
    private String town;
    private String address;
    private Long sellerId;

    @JsonIgnore
    @Column(columnDefinition = "geometry")
    private com.vividsolutions.jts.geom.Point location;

}

</code></pre>

<p>My RepositoryInterface: </p>

<pre><code>@Repository
public interface SellerGeolocationRepository extends CrudRepository&lt;Seller_Geolocation, Long&gt; {

    @Query(value="SELECT * FROM seller_geolocation_ms WHERE ST_DWithin(location,?1,?2) = true", nativeQuery = true)
    public Set&lt;Seller_Geolocation&gt; findAllSellersInRange(double longitude, double latitude);

}
</code></pre>

<p>My Service Class I have this function :</p>

<pre><code>    public Set&lt;Seller_Geolocation&gt; getAllSellersInLocation(Double longitude, Double latitude) {
        return sellerRepository.findAllSellersInRange(longitude, latitude);
    }

</code></pre>

<p>I get the following error : </p>

<blockquote>
  <p>ERROR: function st_dwithin(geometry, double precision, double
  precision) does not exist Hint: No function matches the given name and
  argument types. You might need to add explicit type casts.</p>
</blockquote>

<p><strong>UPDATE :</strong> </p>

<p>The query string :</p>

<pre><code>SELECT * 
FROM seller_geolocation_ms 
WHERE ST_DWithin(location::geography, ST_SetSRID(ST_Point(59.393181, 5.286147), 4326), 30000);
</code></pre>

<p>works in the postgres database but in the java app it returns an error:</p>

<blockquote>
  <p>org.postgresql.util.PSQLException: ERROR: syntax error at or near ":"</p>
</blockquote>

## Answers
### Answer ID: 57183350
<p><a href="https://postgis.net/docs/ST_DWithin.html" rel="nofollow noreferrer">ST_DWithin</a> checks if two geometries are within a given distance of each others. It takes 2 geometries and a distance as parameters.</p>

<p>The row SQL would be</p>

<pre class="lang-sql prettyprint-override"><code>SELECT * 
FROM myTable
WHERE ST_DWithin(mytable.geom,ST_SetSRID(ST_Point(longitude,latitude),4326), distance_degrees);
</code></pre>

<p>Now this would take a distance in degrees. To use a distance in meters you can either reproject to a CRS whose unit is meter, or cast to geography</p>

<pre class="lang-sql prettyprint-override"><code>SELECT * 
FROM myTable
WHERE ST_DWithin(mytable.geom::geography,ST_SetSRID(ST_Point(longitude,latitude),4326)::geography, distance_meters);
</code></pre>

<p>Or using a different way of casting to geography:</p>

<pre class="lang-sql prettyprint-override"><code>SELECT * 
FROM myTable
WHERE ST_DWithin(cast(mytable.geom as geography),ST_SetSRID(ST_Point(longitude,latitude),4326)::geography, distance_meters);
</code></pre>


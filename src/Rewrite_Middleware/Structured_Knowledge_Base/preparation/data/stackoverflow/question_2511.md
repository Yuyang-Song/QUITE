# Joins with CakePHP 3 Query Builder Not Returning Data
[Link to question](https://stackoverflow.com/questions/37863461/joins-with-cakephp-3-query-builder-not-returning-data)
**Creation Date:** 1466090972
**Score:** 0
**Tags:** cakephp, orm, cakephp-3.0
## Question Body
<p>Query is executing just fine but Cakes query builder is not adding the joined fields to the SELECT. What am I missing here? Cake 3.2.10, MySQL, Ubuntu.</p>

<pre><code>        $data = $this-&gt;Property-&gt;find()
        -&gt;hydrate(false)
        -&gt;join([
            'PublisherProperty' =&gt; [
                'table' =&gt; 'publisher_property', 'type' =&gt; 'inner', 
                'conditions' =&gt; "PublisherProperty.property_id = Property.id AND PublisherProperty.publisher_id = " . $this-&gt;Publisher-&gt;id
            ],
            'PhysicalAddress' =&gt; [
                'table' =&gt; 'property_address', 'type' =&gt; 'inner', 
                'conditions' =&gt; "PhysicalAddress.property_id = Property.id AND PhysicalAddress.type = 'physical'"
            ],
            'CheckinAddress' =&gt; [
                'table' =&gt; 'property_address', 'type' =&gt; 'left', 
                'conditions' =&gt; "CheckinAddress.property_id = Property.id AND CheckinAddress.type = 'checkin'"
            ],
            'MainTelephone' =&gt; [
                'table' =&gt; 'property_telephone', 'type' =&gt; 'inner', 
                'conditions' =&gt; "MainTelephone.property_id = Property.id AND MainTelephone.type = 'main'"
            ],
            'ReservationTelephone' =&gt; [
                'table' =&gt; 'property_telephone', 'type' =&gt; 'left', 
                'conditions' =&gt; "ReservationTelephone.property_id = Property.id AND ReservationTelephone.type = 'reservation'"
            ],
            'PropertyDescription' =&gt; [
                'table' =&gt; 'property_description', 'type' =&gt; 'left', 
                'conditions' =&gt; "PropertyDescription.property_id = Property.id AND PropertyDescription.publisher_id IN (" . implode(',',$publishers) . ")",
            ],
        ])
        -&gt;where([
            'Property.id' =&gt; 1111, //$request-&gt;property_id,
            'Property.status' =&gt; 'ready',
        ])-&gt;first();
</code></pre>

<p>This is what the Query Builder ends up executing:</p>

<pre><code>SELECT 
  Property.id AS `Property__id`, 
  Property.property_type_id AS `Property__property_type_id`, 
  Property.name AS `Property__name`, 
  Property.parent_company AS `Property__parent_company`, 
  Property.short_name AS `Property__short_name`, 
  Property.url AS `Property__url`, 
  Property.checkin_time AS `Property__checkin_time`, 
  Property.checkout_time AS `Property__checkout_time`, 
  Property.cutoff_days AS `Property__cutoff_days`, 
  Property.cutoff_time AS `Property__cutoff_time`, 
  Property.desk_open_time AS `Property__desk_open_time`, 
  Property.desk_close_time AS `Property__desk_close_time`, 
  Property.checkin_policy AS `Property__checkin_policy`, 
  Property.room_tax AS `Property__room_tax`, 
  Property.commission_rate AS `Property__commission_rate`, 
  Property.status AS `Property__status`, 
  Property.tripadvisor_location_id AS `Property__tripadvisor_location_id`, 
  Property.created AS `Property__created`, 
  Property.modified AS `Property__modified` 
FROM 
  property Property 
  inner JOIN publisher_property PublisherProperty ON PublisherProperty.property_id = Property.id 
  AND PublisherProperty.publisher_id = 2 
  inner JOIN property_address PhysicalAddress ON PhysicalAddress.property_id = Property.id 
  AND PhysicalAddress.type = 'physical' 
  left JOIN property_address CheckinAddress ON CheckinAddress.property_id = Property.id 
  AND CheckinAddress.type = 'checkin' 
  inner JOIN property_telephone MainTelephone ON MainTelephone.property_id = Property.id 
  AND MainTelephone.type = 'main' 
  left JOIN property_telephone ReservationTelephone ON ReservationTelephone.property_id = Property.id 
  AND ReservationTelephone.type = 'reservation' 
  left JOIN property_description PropertyDescription ON PropertyDescription.property_id = Property.id 
  AND PropertyDescription.publisher_id IN (2, NULL) 
WHERE 
  (
    Property.id = 1111 
    AND Property.status = 'ready'
  ) 
LIMIT 
  1
</code></pre>

<p>Edit: To avoid any "why are you doing it this way" stuff. I am rewriting a legacy application in which the database naming conventions do not fit neatly with cakes naming conventions and the relations are a bit complex. I would use ORM if contain was efficiently querying the database, its not.</p>

## Answers
### Answer ID: 37864757
<p>Figured this one out go into the Table model and add alias relations so you don't have to custom write queries and can use contains. Example for PhysicalAddress above go into PropertyTable and add the following</p>

<pre><code>    $this-&gt;hasOne('PhysicalAddress', [
        'className' =&gt; 'PropertyAddress',
        'foreignKey' =&gt; 'property_id',
        'conditions' =&gt; ['PhysicalAddress.type'=&gt;'physical']
    ]);
</code></pre>

<p>Then in your find just do contain('PhysicalAddress')</p>


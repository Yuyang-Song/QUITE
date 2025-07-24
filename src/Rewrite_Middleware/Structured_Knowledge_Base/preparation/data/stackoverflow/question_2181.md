# Neo4j Cypher query fails and return with an Unknown Error
[Link to question](https://stackoverflow.com/questions/22396082/neo4j-cypher-query-fails-and-return-with-an-unknown-error)
**Creation Date:** 1394771061
**Score:** 0
**Tags:** neo4j, cypher
## Question Body
<p>I'm trying to build a Cypher query to test if a specific structure exists so I can relate dates to it. </p>

<p>Running Neo4j 2.1.0-M01 on a Linux server, but the same issue occurred with Neo4j 2.0.1</p>

<p>We're starting with a clean database, 0 nodes.</p>

<p>First I'm running this MATCH query to prove that it runs. 
Obviously this query is not going to return any nodes. But after creating the nodes, it will 
fail with an 'unknown error'. 
It seems like a bug to me, since a query with fewer nodes will return. Does anyone have suggestions how to rewrite this query for now?</p>

<p>Sorry for the large amount of code in this post.</p>

<p>Thanks,</p>

<p>-Edwin</p>

<p>Cypher Query: </p>

<p><code>MATCH (c:Cluster{cluster_name:'mycluster',cluster_uuid:'7bd4f66d-5faf-11db-8d0d-000e0cba569c'})
,(sc1:Controller{serialnumber:'7000610071',system_id:'1873784171',hostname:'node01',node_uuid:'7cd70205-66ae-11e0-a4a9-0deba859517d'})
,(sc1)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc2:Controller{serialnumber:'7000606111',system_id:'1873778118',hostname:'node02',node_uuid:'b954f0a1-6682-11e0-b8a0-517da924923d'})
,(sc2)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc3:Controller{serialnumber:'7000561878',system_id:'1873772083',hostname:'node03',node_uuid:'ac293586-6690-11e0-b8a0-517da924923d'})
,(sc3)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc4:Controller{serialnumber:'800000075807',system_id:'1873784143',hostname:'node04',node_uuid:'e8d6c7e5-663e-11e0-b8a0-517da924923d'})
,(sc4)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc5:Controller{serialnumber:'7000477261',system_id:'1873745662',hostname:'node05',node_uuid:'1d1ecc64-728c-11e0-bf0e-3d25383f7ed3'})
,(sc5)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc6:Controller{serialnumber:'7000477273',system_id:'1873745654',hostname:'node06',node_uuid:'140fb0f9-728c-11e0-afeb-49fcf0b6e6c3'})
,(sc6)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc7:Controller{serialnumber:'7000474908',system_id:'1873745665',hostname:'node07',node_uuid:'edbf9c62-728b-11e0-bf0e-3d25383f7ed3'})
,(sc7)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc8:Controller{serialnumber:'7000474910',system_id:'1873745695',hostname:'node08',node_uuid:'20dbfe67-7832-11e0-afeb-49fcf0b6e6c3'})
,(sc8)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc9:Controller{serialnumber:'7000609864',system_id:'1873802756',hostname:'node09',node_uuid:'a8b75397-6690-11e0-b8a0-517da924923d'})
,(sc9)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc10:Controller{serialnumber:'7000610021',system_id:'1873791030',hostname:'node10',node_uuid:'f6cf0705-6670-11e0-b8a0-517da924923d'})
,(sc10)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc11:Controller{serialnumber:'7000610057',system_id:'1873784128',hostname:'node11',node_uuid:'551b1bf8-663d-11e0-b8a0-517da924923d'})
,(sc11)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc12:Controller{serialnumber:'7000609981',system_id:'1873778164',hostname:'node12',node_uuid:'f6062d6c-663e-11e0-9b53-cd0ece6aa2ce'})
,(sc12)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc13:Controller{serialnumber:'7000610033',system_id:'1873778186',hostname:'node13',node_uuid:'ed0e61c5-6670-11e0-b07f-933da0385fdc'})
,(sc13)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc14:Controller{serialnumber:'7000610069',system_id:'1873784175',hostname:'node14',node_uuid:'8623ea28-66ae-11e0-ab9d-5fdc7f30dee7'})
,(sc14)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc15:Controller{serialnumber:'7000606109',system_id:'1873778197',hostname:'node15',node_uuid:'b4349a83-6682-11e0-ab9d-5fdc7f30dee7'})
,(sc15)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc16:Controller{serialnumber:'7000610045',system_id:'1873784157',hostname:'node16',node_uuid:'67d80db8-663d-11e0-9b53-cd0ece6aa2ce'})
,(sc16)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc17:Controller{serialnumber:'7001246085',system_id:'2014175904',hostname:'node19',node_uuid:'1c792588-ff4e-11db-94fe-3b91dd7dd242'})
,(sc17)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc18:Controller{serialnumber:'7001246097',system_id:'2014176797',hostname:'node20',node_uuid:'3ae9e7ae-ff44-11db-864d-af2af862bba3'})
,(sc18)-[:IS_PART_OF_CLUSTER]-&gt;(c)
RETURN c,sc1,sc2,sc3,sc4,sc5,sc6,sc7,sc8,sc9,sc10,sc11,sc12,sc13,sc14,sc15,sc16,sc17,sc18
</code>
<b>Rows returned: 0</b></p>

<p>Cypher Query for creating the nodes:</p>

<p><code>CREATE (c:Cluster{cluster_name:'mycluster',cluster_uuid:'7bd4f66d-5faf-11db-8d0d-000e0cba569c'})
,(sc1:Controller{serialnumber:'7000610071',system_id:'1873784171',hostname:'node01',node_uuid:'7cd70205-66ae-11e0-a4a9-0deba859517d'})
,(sc1)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc2:Controller{serialnumber:'7000606111',system_id:'1873778118',hostname:'node02',node_uuid:'b954f0a1-6682-11e0-b8a0-517da924923d'})
,(sc2)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc3:Controller{serialnumber:'7000561878',system_id:'1873772083',hostname:'node03',node_uuid:'ac293586-6690-11e0-b8a0-517da924923d'})
,(sc3)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc4:Controller{serialnumber:'800000075807',system_id:'1873784143',hostname:'node04',node_uuid:'e8d6c7e5-663e-11e0-b8a0-517da924923d'})
,(sc4)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc5:Controller{serialnumber:'7000477261',system_id:'1873745662',hostname:'node05',node_uuid:'1d1ecc64-728c-11e0-bf0e-3d25383f7ed3'})
,(sc5)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc6:Controller{serialnumber:'7000477273',system_id:'1873745654',hostname:'node06',node_uuid:'140fb0f9-728c-11e0-afeb-49fcf0b6e6c3'})
,(sc6)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc7:Controller{serialnumber:'7000474908',system_id:'1873745665',hostname:'node07',node_uuid:'edbf9c62-728b-11e0-bf0e-3d25383f7ed3'})
,(sc7)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc8:Controller{serialnumber:'7000474910',system_id:'1873745695',hostname:'node08',node_uuid:'20dbfe67-7832-11e0-afeb-49fcf0b6e6c3'})
,(sc8)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc9:Controller{serialnumber:'7000609864',system_id:'1873802756',hostname:'node09',node_uuid:'a8b75397-6690-11e0-b8a0-517da924923d'})
,(sc9)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc10:Controller{serialnumber:'7000610021',system_id:'1873791030',hostname:'node10',node_uuid:'f6cf0705-6670-11e0-b8a0-517da924923d'})
,(sc10)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc11:Controller{serialnumber:'7000610057',system_id:'1873784128',hostname:'node11',node_uuid:'551b1bf8-663d-11e0-b8a0-517da924923d'})
,(sc11)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc12:Controller{serialnumber:'7000609981',system_id:'1873778164',hostname:'node12',node_uuid:'f6062d6c-663e-11e0-9b53-cd0ece6aa2ce'})
,(sc12)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc13:Controller{serialnumber:'7000610033',system_id:'1873778186',hostname:'node13',node_uuid:'ed0e61c5-6670-11e0-b07f-933da0385fdc'})
,(sc13)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc14:Controller{serialnumber:'7000610069',system_id:'1873784175',hostname:'node14',node_uuid:'8623ea28-66ae-11e0-ab9d-5fdc7f30dee7'})
,(sc14)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc15:Controller{serialnumber:'7000606109',system_id:'1873778197',hostname:'node15',node_uuid:'b4349a83-6682-11e0-ab9d-5fdc7f30dee7'})
,(sc15)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc16:Controller{serialnumber:'7000610045',system_id:'1873784157',hostname:'node16',node_uuid:'67d80db8-663d-11e0-9b53-cd0ece6aa2ce'})
,(sc16)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc17:Controller{serialnumber:'7001246085',system_id:'2014175904',hostname:'node19',node_uuid:'1c792588-ff4e-11db-94fe-3b91dd7dd242'})
,(sc17)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc18:Controller{serialnumber:'7001246097',system_id:'2014176797',hostname:'node20',node_uuid:'3ae9e7ae-ff44-11db-864d-af2af862bba3'})
,(sc18)-[:IS_PART_OF_CLUSTER]-&gt;(c)
RETURN c,sc1,sc2,sc3,sc4,sc5,sc6,sc7,sc8,sc9,sc10,sc11,sc12,sc13,sc14,sc15,sc16,sc17,sc18</code></p>

<p><b>19 nodes created, 18 relationships. </b></p>

<p>Now when I run the first query again, it takes one minute  and will eventually return with 'Unknown error'.</p>

<p>Cypher Query:  </p>

<p><code>MATCH (c:Cluster{cluster_name:'mycluster',cluster_uuid:'7bd4f66d-5faf-11db-8d0d-000e0cba569c'})
,(sc1:Controller{serialnumber:'7000610071',system_id:'1873784171',hostname:'node01',node_uuid:'7cd70205-66ae-11e0-a4a9-0deba859517d'})
,(sc1)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc2:Controller{serialnumber:'7000606111',system_id:'1873778118',hostname:'node02',node_uuid:'b954f0a1-6682-11e0-b8a0-517da924923d'})
,(sc2)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc3:Controller{serialnumber:'7000561878',system_id:'1873772083',hostname:'node03',node_uuid:'ac293586-6690-11e0-b8a0-517da924923d'})
,(sc3)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc4:Controller{serialnumber:'800000075807',system_id:'1873784143',hostname:'node04',node_uuid:'e8d6c7e5-663e-11e0-b8a0-517da924923d'})
,(sc4)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc5:Controller{serialnumber:'7000477261',system_id:'1873745662',hostname:'node05',node_uuid:'1d1ecc64-728c-11e0-bf0e-3d25383f7ed3'})
,(sc5)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc6:Controller{serialnumber:'7000477273',system_id:'1873745654',hostname:'node06',node_uuid:'140fb0f9-728c-11e0-afeb-49fcf0b6e6c3'})
,(sc6)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc7:Controller{serialnumber:'7000474908',system_id:'1873745665',hostname:'node07',node_uuid:'edbf9c62-728b-11e0-bf0e-3d25383f7ed3'})
,(sc7)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc8:Controller{serialnumber:'7000474910',system_id:'1873745695',hostname:'node08',node_uuid:'20dbfe67-7832-11e0-afeb-49fcf0b6e6c3'})
,(sc8)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc9:Controller{serialnumber:'7000609864',system_id:'1873802756',hostname:'node09',node_uuid:'a8b75397-6690-11e0-b8a0-517da924923d'})
,(sc9)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc10:Controller{serialnumber:'7000610021',system_id:'1873791030',hostname:'node10',node_uuid:'f6cf0705-6670-11e0-b8a0-517da924923d'})
,(sc10)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc11:Controller{serialnumber:'7000610057',system_id:'1873784128',hostname:'node11',node_uuid:'551b1bf8-663d-11e0-b8a0-517da924923d'})
,(sc11)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc12:Controller{serialnumber:'7000609981',system_id:'1873778164',hostname:'node12',node_uuid:'f6062d6c-663e-11e0-9b53-cd0ece6aa2ce'})
,(sc12)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc13:Controller{serialnumber:'7000610033',system_id:'1873778186',hostname:'node13',node_uuid:'ed0e61c5-6670-11e0-b07f-933da0385fdc'})
,(sc13)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc14:Controller{serialnumber:'7000610069',system_id:'1873784175',hostname:'node14',node_uuid:'8623ea28-66ae-11e0-ab9d-5fdc7f30dee7'})
,(sc14)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc15:Controller{serialnumber:'7000606109',system_id:'1873778197',hostname:'node15',node_uuid:'b4349a83-6682-11e0-ab9d-5fdc7f30dee7'})
,(sc15)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc16:Controller{serialnumber:'7000610045',system_id:'1873784157',hostname:'node16',node_uuid:'67d80db8-663d-11e0-9b53-cd0ece6aa2ce'})
,(sc16)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc17:Controller{serialnumber:'7001246085',system_id:'2014175904',hostname:'node19',node_uuid:'1c792588-ff4e-11db-94fe-3b91dd7dd242'})
,(sc17)-[:IS_PART_OF_CLUSTER]-&gt;(c)
,(sc18:Controller{serialnumber:'7001246097',system_id:'2014176797',hostname:'node20',node_uuid:'3ae9e7ae-ff44-11db-864d-af2af862bba3'})
,(sc18)-[:IS_PART_OF_CLUSTER]-&gt;(c)
RETURN c,sc1,sc2,sc3,sc4,sc5,sc6,sc7,sc8,sc9,sc10,sc11,sc12,sc13,sc14,sc15,sc16,sc17,sc18</code></p>

<p><b>Returns <code>Unknown Error</code></b></p>

## Answers
### Answer ID: 22400796
<p>Your MATCH query is way to complicated. There's no need to specify every node. The following query returns the cluster and its related controllers:</p>

<pre><code>MATCH (c:Cluster{cluster_name:'mycluster',cluster_uuid:'7bd4f66d-5faf-11db-8d0d-000e0cba569c'})&lt;-[:IS_PART_OF_CLUSTER]-(sc:Controller) 
WITH c, collect(sc) as controllers 
RETURN c as cluster, controllers
</code></pre>


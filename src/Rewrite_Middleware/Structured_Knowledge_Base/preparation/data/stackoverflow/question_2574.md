# Combining Bind variables for webpage lookup
[Link to question](https://stackoverflow.com/questions/41149594/combining-bind-variables-for-webpage-lookup)
**Creation Date:** 1481740092
**Score:** 1
**Tags:** oracle-database, bind-variables
## Question Body
<p>I have this sql that uses the same variable (:Item) for 3 different tables in the where clause. It runs fine in Oracle SQL developer. It pops up and asks for the Item and returns the correct data.<br>
I want to create a web page using this sql to allow the user to lookup the Item. This is querying against an Oracle database. 
Is there a way to rewrite this so it combines the 3 :Items into 1?<br>
Then I would use that as my search field for the web page.<br>
I'm new to this so be kind.   </p>

<pre><code>SELECT ITEM_C.SEGMENT1 "Chain (Top) Item",
  ITEM_C.DESCRIPTION,
  ITEM_F.SEGMENT1 "Newer Item",
  ITEM_F.DESCRIPTION,
  item_t.SEGMENT1 "Older Item",
  item_t.DESCRIPTION "Older Description",
  ITEM_C.ITEM_TYPE TOP_ITEM_TYPE,
  ITEM_F.ITEM_TYPE NEWER_ITEM_TYPE,
  item_t.ITEM_TYPE Older_Item_Type,
  DOF.LINK_NUMBER,
  DOF.SUPERCESSION_TYPE,
  (SELECT fu.USER_NAME
  FROM apps.fnd_user fu
  WHERE fu.USER_ID = DOF.CREATED_BY
  ) "DOF Created By",
  DOF.CREATION_DATE "DOF Created",
  DOF.LAST_UPDATE_DATE "DOF Updated",
  item_t.CREATION_DATE "Older Created",
  item_t.LAST_UPDATE_DATE "Older Updated",
  ITEM_C.CREATION_DATE "Top Created",
  TRUNC(ITEM_C.CREATION_DATE - DOF.CREATION_DATE, 1) "Chain Lag",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Top in P01",
  DECODE(
  (SELECT 1 FROM INV.MTL_SYSTEM_ITEMS_B a WHERE a.INVENTORY_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Top in FTE",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Newest in P01",
  DECODE(
  (SELECT 1 FROM INV.MTL_SYSTEM_ITEMS_B a WHERE a.INVENTORY_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Newest in FTE",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = item_t.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Oldest in P01",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = item_t.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Oldest in FTE",
  ITEM_C.PURCHASING_ENABLED_FLAG "Top Purchasing Enabled",
  ITEM_F.PURCHASING_ENABLED_FLAG "Newer Purchasing Enabled",
  item_t.PURCHASING_ENABLED_FLAG "Older Purchasing Enabled",
  ITEM_C.FIXED_LOT_MULTIPLIER CHAIN_FLM,
  ITEM_F.FIXED_LOT_MULTIPLIER NEWER_FLM,
  item_t.FIXED_LOT_MULTIPLIER Older_FLM,
  SysDate "Current Date"
FROM IKNDOF.IKN_DOF_ITEM_CHAINS DOF
LEFT OUTER JOIN INV.MTL_SYSTEM_ITEMS_B ITEM_F
ON DOF.FROM_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
AND ITEM_F.ORGANIZATION_ID = 86
LEFT OUTER JOIN INV.MTL_SYSTEM_ITEMS_B ITEM_C
ON DOF.CHAIN_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
AND ITEM_C.ORGANIZATION_ID = 86
LEFT OUTER JOIN inv.mtl_system_items_b item_t
ON DOF.TO_ITEM_ID = item_t.INVENTORY_ITEM_ID
AND item_t.ORGANIZATION_ID = 86
WHERE 1 = 1
AND DOF.CHAIN_ITEM_ID     IN
  (SELECT DISTINCT df.CHAIN_ITEM_ID
  FROM inv.mtl_system_items_b topi,
    inv.mtl_system_items_b fri,
    inv.mtl_system_items_b toi,
    ikndof.ikn_dof_item_chains df
  WHERE df.FROM_ITEM_ID    = fri.INVENTORY_ITEM_ID(+)
  AND df.TO_ITEM_ID        = toi.INVENTORY_ITEM_ID(+)
  AND df.CHAIN_ITEM_ID     = topi.INVENTORY_ITEM_ID(+)
  AND fri.ORGANIZATION_ID  = 86
  AND toi.ORGANIZATION_ID  = 86
  AND topi.ORGANIZATION_ID = 86
  AND (fri.SEGMENT1 LIKE :Item
  OR toi.SEGMENT1 LIKE :Item
  OR topi.SEGMENT1 LIKE :Item)
  )
ORDER BY "Chain (Top) Item",
  DOF.LINK_NUMBER
</code></pre>

<p>Thanks,   Scott</p>

## Answers
### Answer ID: 41150074
<p>You have 2 options here - </p>

<p>Option 1. put this query in your web page using the syntax according to the scripting language you use. This option is not recommended.</p>

<p>Option 2. Create Stored Procedure (SP) in Oracle and call it in your webpage. This is much better option because </p>

<p>a.) SP is compiled hence runs faster </p>

<p>b.) it can be re-used by multiple pages/clients.</p>

<p>c.) if the query changes you only need to change it in one place - SP. </p>

<p>Below is the Stored Procedure I put together for you, it should compile in your IDE, hopefully without modifications. </p>

<pre><code>CREATE OR REPLACE PROCEDURE yourdb.yourproc
(
        i_search            IN varchar2,
        o_return_cursor     OUT  GLOBAL.GenericCursorType
) AS
BEGIN


    OPEN o_return_cursor FOR 
SELECT ITEM_C.SEGMENT1 "Chain (Top) Item",
  ITEM_C.DESCRIPTION,
  ITEM_F.SEGMENT1 "Newer Item",
  ITEM_F.DESCRIPTION,
  item_t.SEGMENT1 "Older Item",
  item_t.DESCRIPTION "Older Description",
  ITEM_C.ITEM_TYPE TOP_ITEM_TYPE,
  ITEM_F.ITEM_TYPE NEWER_ITEM_TYPE,
  item_t.ITEM_TYPE Older_Item_Type,
  DOF.LINK_NUMBER,
  DOF.SUPERCESSION_TYPE,
  (SELECT fu.USER_NAME
  FROM apps.fnd_user fu
  WHERE fu.USER_ID = DOF.CREATED_BY
  ) "DOF Created By",
  DOF.CREATION_DATE "DOF Created",
  DOF.LAST_UPDATE_DATE "DOF Updated",
  item_t.CREATION_DATE "Older Created",
  item_t.LAST_UPDATE_DATE "Older Updated",
  ITEM_C.CREATION_DATE "Top Created",
  TRUNC(ITEM_C.CREATION_DATE - DOF.CREATION_DATE, 1) "Chain Lag",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Top in P01",
  DECODE(
  (SELECT 1 FROM INV.MTL_SYSTEM_ITEMS_B a WHERE a.INVENTORY_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Top in FTE",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Newest in P01",
  DECODE(
  (SELECT 1 FROM INV.MTL_SYSTEM_ITEMS_B a WHERE a.INVENTORY_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Newest in FTE",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = item_t.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 2470383
  ), NULL, 'No', 'Yes') "Oldest in P01",
  DECODE(
  (SELECT 1 FROM inv.mtl_system_items_b a WHERE a.INVENTORY_ITEM_ID = item_t.INVENTORY_ITEM_ID
  AND a.ORGANIZATION_ID = 98
  ), NULL, 'No', 'Yes') "Oldest in FTE",
  ITEM_C.PURCHASING_ENABLED_FLAG "Top Purchasing Enabled",
  ITEM_F.PURCHASING_ENABLED_FLAG "Newer Purchasing Enabled",
  item_t.PURCHASING_ENABLED_FLAG "Older Purchasing Enabled",
  ITEM_C.FIXED_LOT_MULTIPLIER CHAIN_FLM,
  ITEM_F.FIXED_LOT_MULTIPLIER NEWER_FLM,
  item_t.FIXED_LOT_MULTIPLIER Older_FLM,
  SysDate "Current Date"
FROM IKNDOF.IKN_DOF_ITEM_CHAINS DOF
LEFT OUTER JOIN INV.MTL_SYSTEM_ITEMS_B ITEM_F
ON DOF.FROM_ITEM_ID = ITEM_F.INVENTORY_ITEM_ID
AND ITEM_F.ORGANIZATION_ID = 86
LEFT OUTER JOIN INV.MTL_SYSTEM_ITEMS_B ITEM_C
ON DOF.CHAIN_ITEM_ID = ITEM_C.INVENTORY_ITEM_ID
AND ITEM_C.ORGANIZATION_ID = 86
LEFT OUTER JOIN inv.mtl_system_items_b item_t
ON DOF.TO_ITEM_ID = item_t.INVENTORY_ITEM_ID
AND item_t.ORGANIZATION_ID = 86
WHERE 1 = 1
AND DOF.CHAIN_ITEM_ID     IN
  (SELECT DISTINCT df.CHAIN_ITEM_ID
  FROM inv.mtl_system_items_b topi,
    inv.mtl_system_items_b fri,
    inv.mtl_system_items_b toi,
    ikndof.ikn_dof_item_chains df
  WHERE df.FROM_ITEM_ID    = fri.INVENTORY_ITEM_ID(+)
  AND df.TO_ITEM_ID        = toi.INVENTORY_ITEM_ID(+)
  AND df.CHAIN_ITEM_ID     = topi.INVENTORY_ITEM_ID(+)
  AND fri.ORGANIZATION_ID  = 86
  AND toi.ORGANIZATION_ID  = 86
  AND topi.ORGANIZATION_ID = 86
  AND (fri.SEGMENT1 LIKE i_search
  OR toi.SEGMENT1 LIKE i_search
  OR topi.SEGMENT1 LIKE i_search)
  )
ORDER BY "Chain (Top) Item",
  DOF.LINK_NUMBER ;


EXCEPTION
    WHEN  OTHERS THEN 

  DBMS_OUTPUT.PUT_LINE(TO_CHAR(SQLCODE)||'  yourproc WHEN OTHERS  '); 
END; -- Procedure 
/
</code></pre>


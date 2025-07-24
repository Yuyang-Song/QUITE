# Refactoring SQL queries run within Qlik not write data on db using temp tables
[Link to question](https://stackoverflow.com/questions/76528651/refactoring-sql-queries-run-within-qlik-not-write-data-on-db-using-temp-tables)
**Creation Date:** 1687408881
**Score:** 0
**Tags:** sql, database, common-table-expression, qliksense
## Question Body
<p>There are a number of SQL queries that run within Qlik that use temporary tables.  Temp tables write back to the database and as a reporting tool and i dont want Qlik to be writing to a database.  I need to rewrite these queries without using temp tables.  I tried using CTEs but not sure why it is not working, need help please.</p>
<pre><code>SELECT 
    req_item.number AS RITM_SnowCloudReq,
    'https://xxxxxxx.xxxxxxxx.com/sc_req_item.do?sys_id=' + req_item.sys_id + '&amp;sysparm_view=' AS URL_SnowCloudReq,
    req_item.active AS Active_SnowCloudReq,
    req_item.dv_cat_item AS Item_SnowCloudReq,
    req_item.dv_state AS State_SnowCloudReq,
    req_item.dv_stage AS Stage_SnowCloudReq,
    req_item.dv_approval AS Approval_SnowCloudReq,
    req_item.opened_at AS Opened_At_SnowCloudReq,
    req_item.closed_at AS Closed_At_SnowCloudReq,
    req_item.dv_parent AS Parent_SnowCloudReq,
    req_item.sys_id AS Sys_Id_SnowCloudReq,
    req_item.dv_requested_for AS Requested_For_SnowCloudReq,
    task1.number AS Task1_Number_SnowCloudReq,
    task1.dv_state AS Task1_State_SnowCloudReq,
    task1.dv_approval AS Task1_Approval_SnowCloudReq,
    task1.dv_assignment_group AS Task1_Assignment_Group_SnowCloudReq,
    task1.dv_assigned_to AS Task1_Assignee_SnowCloudReq,
    task1.short_description AS Task1_Short_Description_SnowCloudReq,
    task1.dv_opened_by AS Task1_Opened_By_SnowCloudReq,
    task1.opened_at AS Task1_Opened_At_SnowCloudReq,
    task1.dv_closed_by AS Task1_Closed_By_SnowCloudReq,
    task1.closed_at AS Task1_Closed_At_SnowCloudReq,
    task2.number AS Task2_Number_SnowCloudReq,
    task2.dv_state AS Task2_State_SnowCloudReq,
    task2.dv_approval AS Task2_Approval_SnowCloudReq,
    task2.dv_assignment_group AS Task2_Assignment_Group_SnowCloudReq,
    task2.dv_assigned_to AS Task2_Assignee_SnowCloudReq,
    task2.short_description AS Task2_Short_Description_SnowCloudReq,
    task2.dv_opened_by AS Task2_Opened_By_SnowCloudReq,
    task2.opened_at AS Task2_Opened_At_SnowCloudReq,
    task2.dv_closed_by AS Task2_Closed_By_SnowCloudReq,
    task2.closed_at AS Task2_Closed_At_SnowCloudReq,
    (OpUser.first_name + ' ' + OpUser.last_name) AS Opened_By_SnowCloudReq,
    (ClUser.first_name + ' ' + ClUser.last_name) AS Closed_By_SnowCloudReq,
    MAX(CASE 
        WHEN var.[dv_item_option_new] = 'Requested For' THEN [value] END) Requestor_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Release Number' THEN [value] END) AS Release_Number_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Cloud Initiative Name' THEN [value] END) AS Cloud_Initiative_Name_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Business Application' THEN [value] END) AS Business_Application_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'APM ID' THEN [value] END) AS APM_ID_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Initiative Description' THEN [value] END) AS Initiative_Description_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'What system does this replace ?' THEN [value] END) AS What_System_Does_This_Replace_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'What is the business benefit ?' THEN [value] END) AS What_Is_The_Business_Benefit_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Who is responsible for the change and by when ?' THEN [value] END) AS Responsible_And_When_SnowCloudReq, 
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Location of service being used' THEN [value] END) AS Location_Service_Used_SnowCloudReq,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Other Countries' THEN [value] END) AS Countries_id,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Asset Criticality' THEN [value] END) AS Asset_Criticality_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Data Confidentiality Rating' THEN [value] END) AS Data_Confidentiality_Rating_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Data Integrity Rating' THEN [value] END) AS Data_Integrity_Rating_SnowCloudReq,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Service Model' THEN [value] END) AS Service_Model_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Service Provider' THEN [value] END) AS Service_Provider_id,
    MAX(CASE 
        WHEN var.[dv_item_option_new] = 'Hosting Provider' THEN [value] END) AS Hosting_Provider,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Hosting Country' THEN [value] END) AS Hosting_Country_id,  
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Contain Customer Data ?' THEN [value] END) AS Contain_Customer_Data_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Single Signon (SSO) ?' THEN [value] END) AS Single_Signon_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Accessible via the internet ?' THEN [value] END) AS Accessible_Via_The_Internet_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'URL Address' THEN [value] END) AS URL_Address_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Fast Track Request' THEN [value] END) AS Fast_Track_Request_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Technology Domain' THEN [value] END) AS Technology_Domain_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Domain Approvers ' THEN [value] END) AS Domain_Approvers_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Asset Owner' THEN [value] END) AS Asset_Owner_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Tech Area Architect' THEN [value] END) AS Tech_Area_Architect_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Additional Approval' THEN [value] END) AS Additional_Approval_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Check Stage' THEN [value] END) AS Check_Stage_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Bulk Upload' THEN [value] END) AS Bulk_Upload_SnowCloudReq
INTO #tmp_1 -- inserting in to temp table that can be used to pivot

FROM [SnowMirror].[dbo].[sc_req_item] req_item

    LEFT JOIN
    (
    SELECT 
        request_item,
        number,
        dv_state,
        dv_approval,
        dv_assignment_group,
        dv_assigned_to,
        short_description,
        dv_opened_by,
        opened_at,
        dv_closed_by,
        closed_at
    FROM 
        (
        Select *,
            ROW_NUMBER() OVER 
            (
            PARTITION BY request_item
            ORDER BY opened_at Asc
            ) AS row_number
        FROM [SnowMirror].[dbo].[sc_task]
        ) AS numbered_tasks
        WHERE numbered_tasks.row_number = 1
    ) AS task1
    ON req_item.sys_id = task1.request_item

    LEFT JOIN
    (
    SELECT 
        request_item,
        number,
        dv_state,
        dv_approval,
        dv_assignment_group,
        dv_assigned_to,
        short_description,
        dv_opened_by,
        opened_at,
        dv_closed_by,
        closed_at
    FROM 
        (
        Select *,
            ROW_NUMBER() OVER 
            (
            PARTITION BY request_item
            ORDER BY opened_at Asc
            ) AS row_number
        FROM [SnowMirror].[dbo].[sc_task]
        ) AS numbered_tasks
        WHERE numbered_tasks.row_number = 2
    ) AS task2
    ON req_item.sys_id = task2.request_item

    LEFT JOIN [SnowMirror].[dbo].[sc_item_option_mtom] mtom
        ON req_item.sys_id = mtom.request_item
        
    LEFT JOIN [SnowMirror].[dbo].[sc_item_option] var
        ON mtom.sc_item_option = var.sys_id
        
    LEFT JOIN
        (
        SELECT 
            sys_id, 
            first_name, 
            last_name 
        FROM [SnowMirror].[dbo].[sys_user]
        ) OpUser 
        ON OpUser.sys_id = req_item.opened_by
        
    LEFT JOIN 
        (
        SELECT 
            sys_id,
            first_name,
            last_name 
        FROM [SnowMirror].[dbo].[sys_user]
        ) ClUser 
        ON ClUser.sys_id = req_item.closed_by
WHERE req_item.dv_cat_item = 'Cloud Request Form'
GROUP BY 
    req_item.number,
    ('https://xxxxxxxxxxxxxxxxxxxx.com/sc_req_item.do?sys_id=' + req_item.sys_id + '&amp;sysparm_view='),
    req_item.active,
    req_item.dv_cat_item,
    req_item.dv_state,
    req_item.dv_stage,
    req_item.dv_approval,
    req_item.dv_requested_for,
    req_item.opened_at,
    req_item.closed_at,
    req_item.dv_parent,
    req_item.sys_id,
    task1.number,
    task1.dv_state,
    task1.dv_approval,
    task1.dv_assignment_group,
    task1.dv_assigned_to,
    task1.short_description,
    task1.dv_opened_by,
    task1.opened_at,
    task1.dv_closed_by,
    task1.closed_at,
    task2.number,
    task2.dv_state,
    task2.dv_approval,
    task2.dv_assignment_group,
    task2.dv_assigned_to,
    task2.short_description,
    task2.dv_opened_by,
    task2.opened_at,
    task2.dv_closed_by,
    task2.closed_at,
    (OpUser.first_name + ' ' + OpUser.last_name),
    (ClUser.first_name + ' ' + ClUser.last_name)

SELECT 
    temp.*,
    (ISNULL(OpUser.first_name,'') + ' ' + ISNULL(OpUser.last_name,'')) AS Requestor_SnowCloudReq, 
    OpUser.email AS Requestor_Email_SnowCloudReq,
    rls.sys_id AS rls_sys_id, 
    rls.number AS Release_Number_SnowCloudReq,
    APM.name AS Business_Application_SnowCloudReq,
    value,
    country1.name AS Country_name,
    comp1.name AS Service_Provider_SnowCloudReq,
    CASE
        WHEN Hosting_Provider IN ('AWS','GCP','VMC','Azure','AWS and GCP') 
        THEN Hosting_Provider
        ELSE comp2.name
    END AS Hosting_Provider_SnowCloudReq,
    country2.name AS Hosting_Country_SnowCloudReq,
    (ISNULL(ClUser.first_name,'') + ' ' + ISNULL(ClUser.last_name,'')) AS Asset_Owner_SnowCloudReq,
    (ISNULL(TAAUser.first_name,'') + ' ' + ISNULL(TAAUser.last_name,'')) AS Tech_Area_Architect_SnowCloudReq,
    (ISNULL(AAUser.first_name,'') + ' ' + ISNULL(AAUser.last_name,'')) AS Additional_Approval_SnowCloudReq
INTO #tmp_2 -- inserting in to temp table that can be used to pivot
FROM #tmp_1 temp
    LEFT JOIN [SnowMirror].[dbo].[sys_user] OpUser 
        ON OpUser.sys_id = Requestor_id
        
    LEFT JOIN [SnowMirror].[dbo].[rm_release] rls
        ON rls.sys_id = Release_Number_id
        
    LEFT JOIN [SnowMirror].[dbo].[cmdb_ci_business_app] APM
        ON APM.sys_id = Business_Application_id
    CROSS APPLY STRING_SPLIT(ISNULL(Countries_id,''), ',')
    
    LEFT JOIN [SnowMirror].[dbo].[core_country] country1
        ON country1.sys_id = value
        
    LEFT JOIN [SnowMirror].[dbo].[core_company] comp1
        ON comp1.sys_id = Service_Provider_id
        
    LEFT JOIN [SnowMirror].[dbo].[core_company] comp2
        ON comp2.sys_id = Hosting_Provider
        
    LEFT JOIN [SnowMirror].[dbo].[core_country] country2
        ON country2.sys_id = Hosting_Country_id
        
    LEFT JOIN [SnowMirror].[dbo].[sys_user] ClUser
        ON ClUser.sys_id = Asset_Owner_id
        
    LEFT JOIN [SnowMirror].[dbo].[sys_user] TAAUser
        ON TAAUser.sys_id = Tech_Area_Architect_id
        
    LEFT JOIN [SnowMirror].[dbo].[sys_user] AAUser
        ON AAUser.sys_id = Additional_Approval_id

DROP TABLE #tmp_1 -- Remove temp table;


SELECT DISTINCT 
    RITM_SnowCloudReq,
    URL_SnowCloudReq,
    Active_SnowCloudReq,
    Item_SnowCloudReq,
    State_SnowCloudReq,
    Stage_SnowCloudReq,
    Approval_SnowCloudReq,
    Opened_At_SnowCloudReq,
    Closed_At_SnowCloudReq,
    Requested_For_SnowCloudReq,
    Opened_By_SnowCloudReq,
    Closed_By_SnowCloudReq,
    Requestor_SnowCloudReq,
    Requestor_Email_SnowCloudReq,
    Parent_SnowCloudReq,
    Sys_Id_SnowCloudReq,
    Release_Number_SnowCloudReq,
    Cloud_Initiative_Name_SnowCloudReq,
    Business_Application_SnowCloudReq,
    APM_ID_SnowCloudReq,
    Initiative_Description_SnowCloudReq,
    What_System_Does_This_Replace_SnowCloudReq,
    What_Is_The_Business_Benefit_SnowCloudReq,
    Responsible_And_When_SnowCloudReq,
    Location_Service_Used_SnowCloudReq,
    SUBSTRING(
        (
            SELECT ',' + Country_name AS [text()]
            FROM #tmp_2 t
            WHERE tmp.RITM_SnowCloudReq = t.RITM_SnowCloudReq
            ORDER BY Country_name
            FOR XML PATH(''), TYPE      
        ).value('text()[1]','nvarchar(max)'), 2, 1000) AS Countries_SnowCloudReq,
    Asset_Criticality_SnowCloudReq,
    Data_Confidentiality_Rating_SnowCloudReq,
    Data_Integrity_Rating_SnowCloudReq,
    Service_Model_SnowCloudReq,
    Service_Provider_SnowCloudReq,
    Hosting_Provider_SnowCloudReq,
    Hosting_Country_SnowCloudReq,
    Contain_Customer_Data_SnowCloudReq,
    Single_Signon_SnowCloudReq,
    Accessible_Via_The_Internet_SnowCloudReq,
    URL_Address_SnowCloudReq,
    Fast_Track_Request_SnowCloudReq,
    Technology_Domain_SnowCloudReq,
    Domain_Approvers_SnowCloudReq,
    Asset_Owner_SnowCloudReq,
    Tech_Area_Architect_SnowCloudReq,
    Additional_Approval_SnowCloudReq,
    Check_Stage_SnowCloudReq,
    Bulk_Upload_SnowCloudReq,
    Task1_Number_SnowCloudReq,
    Task1_State_SnowCloudReq,
    Task1_Approval_SnowCloudReq
    Task1_Assignment_Group_SnowCloudReq,
    Task1_Assignee_SnowCloudReq,
    Task1_Short_Description_SnowCloudReq,
    Task1_Opened_By_SnowCloudReq,
    Task1_Opened_At_SnowCloudReq,
    Task1_Closed_By_SnowCloudReq,
    Task1_Closed_At_SnowCloudReq,
    Task2_Number_SnowCloudReq,
    Task2_State_SnowCloudReq,
    Task2_Approval_SnowCloudReq
    Task2_Assignment_Group_SnowCloudReq,
    Task2_Assignee_SnowCloudReq,
    Task2_Short_Description_SnowCloudReq,
    Task2_Opened_By_SnowCloudReq,
    Task2_Opened_At_SnowCloudReq,
    Task2_Closed_By_SnowCloudReq,
    Task2_Closed_At_SnowCloudReq
FROM #tmp_2 tmp
ORDER BY RITM_SnowCloudReq DESC

DROP TABLE #tmp_2 -- Remove temp table;
</code></pre>
<blockquote>
<p>**I used the below CTE query and i am struck with the Joins after this, request your help and also let me know if this is the best alternative for the temp tables writing on the DB?
**</p>
</blockquote>
<pre><code>WITH cte AS (
    SELECT 
        req_item.number AS RITM_SnowCloudReq,
        'https://xxxxxxxxxxxxxxxxxxxx.com/sc_req_item.do?sys_id=' + req_item.sys_id + '&amp;sysparm_view=' AS URL_SnowCloudReq,
        req_item.active AS Active_SnowCloudReq,
        req_item.dv_cat_item AS Item_SnowCloudReq,
        req_item.dv_state AS State_SnowCloudReq,
        req_item.dv_stage AS Stage_SnowCloudReq,
        req_item.dv_approval AS Approval_SnowCloudReq,
        req_item.opened_at AS Opened_At_SnowCloudReq,
        req_item.closed_at AS Closed_At_SnowCloudReq,
        req_item.dv_parent AS Parent_SnowCloudReq,
        req_item.sys_id AS Sys_Id_SnowCloudReq,
        req_item.dv_requested_for AS Requested_For_SnowCloudReq,
        task1.number AS Task1_Number_SnowCloudReq,
        task1.dv_state AS Task1_State_SnowCloudReq,
        task1.dv_approval AS Task1_Approval_SnowCloudReq,
        task1.dv_assignment_group AS Task1_Assignment_Group_SnowCloudReq,
        task1.dv_assigned_to AS Task1_Assignee_SnowCloudReq,
        task1.short_description AS Task1_Short_Description_SnowCloudReq,
        task1.dv_opened_by AS Task1_Opened_By_SnowCloudReq,
        task1.opened_at AS Task1_Opened_At_SnowCloudReq,
        task1.dv_closed_by AS Task1_Closed_By_SnowCloudReq,
        task1.closed_at AS Task1_Closed_At_SnowCloudReq,
        task2.number AS Task2_Number_SnowCloudReq,
        task2.dv_state AS Task2_State_SnowCloudReq,
        task2.dv_approval AS Task2_Approval_SnowCloudReq,
        task2.dv_assignment_group AS Task2_Assignment_Group_SnowCloudReq,
        task2.dv_assigned_to AS Task2_Assignee_SnowCloudReq,
        task2.short_description AS Task2_Short_Description_SnowCloudReq,
        task2.dv_opened_by AS Task2_Opened_By_SnowCloudReq,
        task2.opened_at AS Task2_Opened_At_SnowCloudReq,
        task2.dv_closed_by AS Task2_Closed_By_SnowCloudReq,
        task2.closed_at AS Task2_Closed_At_SnowCloudReq,
        (OpUser.first_name + ' ' + OpUser.last_name) AS Opened_By_SnowCloudReq,
        (ClUser.first_name + ' ' + ClUser.last_name) AS Closed_By_SnowCloudReq,
            MAX(CASE 
        WHEN var.[dv_item_option_new] = 'Requested For' THEN [value] END) Requestor_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Release Number' THEN [value] END) AS Release_Number_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Cloud Initiative Name' THEN [value] END) AS Cloud_Initiative_Name_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Business Application' THEN [value] END) AS Business_Application_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'APM ID' THEN [value] END) AS APM_ID_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Initiative Description' THEN [value] END) AS Initiative_Description_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'What system does this replace ?' THEN [value] END) AS What_System_Does_This_Replace_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'What is the business benefit ?' THEN [value] END) AS What_Is_The_Business_Benefit_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Who is responsible for the change and by when ?' THEN [value] END) AS Responsible_And_When_SnowCloudReq, 
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Location of service being used' THEN [value] END) AS Location_Service_Used_SnowCloudReq,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Other Countries' THEN [value] END) AS Countries_id,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Asset Criticality' THEN [value] END) AS Asset_Criticality_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Data Confidentiality Rating' THEN [value] END) AS Data_Confidentiality_Rating_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Data Integrity Rating' THEN [value] END) AS Data_Integrity_Rating_SnowCloudReq,
    MAX(CASE    
        WHEN var.[dv_item_option_new] = 'Service Model' THEN [value] END) AS Service_Model_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Service Provider' THEN [value] END) AS Service_Provider_id,
    MAX(CASE 
        WHEN var.[dv_item_option_new] = 'Hosting Provider' THEN [value] END) AS Hosting_Provider,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Hosting Country' THEN [value] END) AS Hosting_Country_id,  
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Contain Customer Data ?' THEN [value] END) AS Contain_Customer_Data_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Single Signon (SSO) ?' THEN [value] END) AS Single_Signon_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Accessible via the internet ?' THEN [value] END) AS Accessible_Via_The_Internet_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'URL Address' THEN [value] END) AS URL_Address_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Fast Track Request' THEN [value] END) AS Fast_Track_Request_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Technology Domain' THEN [value] END) AS Technology_Domain_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Domain Approvers ' THEN [value] END) AS Domain_Approvers_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Asset Owner' THEN [value] END) AS Asset_Owner_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Tech Area Architect' THEN [value] END) AS Tech_Area_Architect_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Additional Approval' THEN [value] END) AS Additional_Approval_id,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Check Stage' THEN [value] END) AS Check_Stage_SnowCloudReq,
    MAX(CASE
        WHEN var.[dv_item_option_new] = 'Bulk Upload' THEN [value] END) AS Bulk_Upload_SnowCloudReq
</code></pre>
<p>Thanks in Advance</p>
<p>I tried with the CTE query which will avoid writing data on the DB using Temp Tables, however i am struck at a point where i am not able to proceed beyond this query.</p>
<p>I need help in letting me know if the CTE is the right approach and help in the continuation of the query.</p>

## Answers
### Answer ID: 76671624
<p>To avoid using temporary tables in your SQL queries, you should use <a href="https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Scripting/load-data-from-previously-loaded-table.htm" rel="nofollow noreferrer">Resident and Preceding Load prefixes</a> in Qlik. The basic idea is that you would use <code>[Table A]: SELECT ... FROM [SQL Table]</code> with your SQL database, then perform your needed joins and transformations on that table using <code>[Table B]: LOAD ... RESIDENT [Table A]</code>, after which you would <code>DROP TABLE [Table A]</code>.</p>
<p><a href="https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Tutorials/transforming-data.htm" rel="nofollow noreferrer">This Qlik Help article</a> also explains how you can achieve this.</p>


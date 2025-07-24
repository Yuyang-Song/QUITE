# Performance issue with MDX query
[Link to question](https://stackoverflow.com/questions/36352939/performance-issue-with-mdx-query)
**Creation Date:** 1459503684
**Score:** 0
**Tags:** mdx, olap-cube, mondrian, olap4j
## Question Body
<p>I'm trying to get top 5 records from MySQL database based on some filters using below MDX query and cube definition.But, this query takes more time for execution and this works fine when we have less no.of FILE_NUM's in where condition. Please suggest how to rewrite this query to gain performance.</p>

<p><strong><em>MDX Query</em></strong>: </p>

<blockquote>
  <p>SELECT {[Measures].[BBLSOIL_TOTAL], [Measures].[MCF_PROD_TOTAL],
  [Measures].[AVG.DAYS]} ON COLUMNS,
  {TOPCOUNT(FILTER([WELL_ID].[WellIds].MEMBERS, [WELL_ID].CurrentMember </p>
  
  <blockquote>
    <p>0),5,[Measures].[BBLSOIL_TOTAL])} ON ROWS FROM [MON_KPI_CHARTS] WHERE({[Date].&amp;[2015-09-01
    00:00:00.0]}*{[FILE_NUM].[1],[FILE_NUM].[10],[FILE_NUM].[18],[FILE_NUM].[47],[FILE_NUM].[52],[FILE_NUM].[105],[FILE_NUM].[126],[FILE_NUM].[392],[FILE_NUM].[588],[FILE_NUM].[656],[FILE_NUM].[995],[FILE_NUM].[1005],[FILE_NUM].[1010],[FILE_NUM].[1061],[FILE_NUM].[1128],[FILE_NUM].[1137],[FILE_NUM].[1138],[FILE_NUM].[1337],[FILE_NUM].[1340],[FILE_NUM].[1410],[FILE_NUM].[1438],[FILE_NUM].[1503],[FILE_NUM].[1628],[FILE_NUM].[1698],[FILE_NUM].[1801],[FILE_NUM].[1808],[FILE_NUM].[1843],[FILE_NUM].[1876],[FILE_NUM].[1885],[FILE_NUM].[2017],[FILE_NUM].[2051],[FILE_NUM].[2053],[FILE_NUM].[2134],[FILE_NUM].[2929],[FILE_NUM].[2930],[FILE_NUM].[2931],[FILE_NUM].[2946],[FILE_NUM].[2979],[FILE_NUM].[3039],[FILE_NUM].[3080],[FILE_NUM].[3087],[FILE_NUM].[3124],[FILE_NUM].[3125],[FILE_NUM].[3165],[FILE_NUM].[3166],[FILE_NUM].[3237],[FILE_NUM].[3256],[FILE_NUM].[3314],[FILE_NUM].[3421],[FILE_NUM].[3445],[FILE_NUM].[3485],[FILE_NUM].[3493],[FILE_NUM].[3501],[FILE_NUM].[3552],[FILE_NUM].[3557],[FILE_NUM].[3622],[FILE_NUM].[3795],[FILE_NUM].[3812],[FILE_NUM].[3824],[FILE_NUM].[3837],[FILE_NUM].[3858],[FILE_NUM].[3884],[FILE_NUM].[3952],[FILE_NUM].[3963],[FILE_NUM].[3984],[FILE_NUM].[3995],[FILE_NUM].[4021],[FILE_NUM].[4030],[FILE_NUM].[4097],[FILE_NUM].[4117],[FILE_NUM].[4142],[FILE_NUM].[4145],[FILE_NUM].[4153],[FILE_NUM].[4155],[FILE_NUM].[4159],[FILE_NUM].[4161],[FILE_NUM].[4190],[FILE_NUM].[4209],[FILE_NUM].[4216],[FILE_NUM].[4223],[FILE_NUM].[4251],[FILE_NUM].[4255],[FILE_NUM].[4303],[FILE_NUM].[4313],[FILE_NUM].[4315],[FILE_NUM].[4329],[FILE_NUM].[4343],[FILE_NUM].[4346],[FILE_NUM].[4356],[FILE_NUM].[4366],[FILE_NUM].[4372],[FILE_NUM].[4400],[FILE_NUM].[4401],[FILE_NUM].[4409],[FILE_NUM].[4422],[FILE_NUM].[4443],[FILE_NUM].[4484],[FILE_NUM].[4501],[FILE_NUM].[4539],[FILE_NUM].[4569],[FILE_NUM].[4630],[FILE_NUM].[4638],[FILE_NUM].[4639],[FILE_NUM].[4658],[FILE_NUM].[4686],[FILE_NUM].[4698],[FILE_NUM].[4699],[FILE_NUM].[4768],[FILE_NUM].[4775],[FILE_NUM].[4794],[FILE_NUM].[4799],[FILE_NUM].[4803],[FILE_NUM].[4805],[FILE_NUM].[4835],[FILE_NUM].[4891],[FILE_NUM].[4923],[FILE_NUM].[4925],[FILE_NUM].[4929],[FILE_NUM].[4950],[FILE_NUM].[4956],[FILE_NUM].[4961],[FILE_NUM].[4978],[FILE_NUM].[4987],[FILE_NUM].[4990],[FILE_NUM].[4992],[FILE_NUM].[4996],[FILE_NUM].[5020],[FILE_NUM].[5025],[FILE_NUM].[5026],[FILE_NUM].[5048],[FILE_NUM].[5057],[FILE_NUM].[5058],[FILE_NUM].[5067],[FILE_NUM].[5074],[FILE_NUM].[5075],[FILE_NUM].[5077],[FILE_NUM].[5079],[FILE_NUM].[5080],[FILE_NUM].[5090],[FILE_NUM].[5095],[FILE_NUM].[5096],[FILE_NUM].[5098],[FILE_NUM].[5103],[FILE_NUM].[5105],[FILE_NUM].[5139],[FILE_NUM].[5149],[FILE_NUM].[5154],[FILE_NUM].[5158],[FILE_NUM].[5165],[FILE_NUM].[5180],[FILE_NUM].[5198],[FILE_NUM].[5199],[FILE_NUM].[5207],[FILE_NUM].[5215],[FILE_NUM].[5219],[FILE_NUM].[5223],[FILE_NUM].[5236],[FILE_NUM].[5242],[FILE_NUM].[5275],[FILE_NUM].[5300],[FILE_NUM].[5304],[FILE_NUM].[5313],[FILE_NUM].[5321],[FILE_NUM].[5356],[FILE_NUM].[5368],[FILE_NUM].[5389],[FILE_NUM].[5401],[FILE_NUM].[5444],[FILE_NUM].[5457],[FILE_NUM].[5467],[FILE_NUM].[5468],[FILE_NUM].[5498],[FILE_NUM].[5519],[FILE_NUM].[5520],[FILE_NUM].[5531],[FILE_NUM].[5539],[FILE_NUM].[5542],[FILE_NUM].[5563],[FILE_NUM].[5578],[FILE_NUM].[5707],[FILE_NUM].[5723],[FILE_NUM].[5761],[FILE_NUM].[5785],[FILE_NUM].[5795],[FILE_NUM].[5809],[FILE_NUM].[5830],[FILE_NUM].[5860],[FILE_NUM].[5903],[FILE_NUM].[5923],[FILE_NUM].[5962],[FILE_NUM].[5966],[FILE_NUM].[5970],[FILE_NUM].[5996],[FILE_NUM].[6005],[FILE_NUM].[6006],[FILE_NUM].[6008],[FILE_NUM].[6012],[FILE_NUM].[6023],[FILE_NUM].[6032],[FILE_NUM].[6041],[FILE_NUM].[6043],[FILE_NUM].[6073],[FILE_NUM].[6100],[FILE_NUM].[6150],[FILE_NUM].[6201],[FILE_NUM].[6223],[FILE_NUM].[6271],[FILE_NUM].[6295],[FILE_NUM].[6314],[FILE_NUM].[6404],[FILE_NUM].[6440],[FILE_NUM].[6459],[FILE_NUM].[6482],[FILE_NUM].[6486],[FILE_NUM].[6502],[FILE_NUM].[6540],[FILE_NUM].[6588],[FILE_NUM].[6610],[FILE_NUM].[6637],[FILE_NUM].[6653],[FILE_NUM].[6664],[FILE_NUM].[6725],[FILE_NUM].[6819],[FILE_NUM].[6871],[FILE_NUM].[6932],[FILE_NUM].[6934],[FILE_NUM].[6978],[FILE_NUM].[7009],[FILE_NUM].[7042],[FILE_NUM].[7043],[FILE_NUM].[7055],[FILE_NUM].[7493],[FILE_NUM].[7547],[FILE_NUM].[7554],[FILE_NUM].[7612],[FILE_NUM].[7624],[FILE_NUM].[7638],[FILE_NUM].[7646],[FILE_NUM].[7671],[FILE_NUM].[7693],[FILE_NUM].[7695],[FILE_NUM].[7696],[FILE_NUM].[7697],[FILE_NUM].[7698],[FILE_NUM].[7708],[FILE_NUM].[7710],[FILE_NUM].[7711],[FILE_NUM].[7862],[FILE_NUM].[7910],[FILE_NUM].[7927],[FILE_NUM].[7960],[FILE_NUM].[7962],[FILE_NUM].[8009],[FILE_NUM].[8033],[FILE_NUM].[8056],[FILE_NUM].[8057],[FILE_NUM].[8104],[FILE_NUM].[8109],[FILE_NUM].[8170],[FILE_NUM].[8177],[FILE_NUM].[8181],[FILE_NUM].[8211],[FILE_NUM].[8323],[FILE_NUM].[8376],[FILE_NUM].[8412],[FILE_NUM].[8475],[FILE_NUM].[8541],[FILE_NUM].[8547],[FILE_NUM].[8578],[FILE_NUM].[8654],[FILE_NUM].[8691],[FILE_NUM].[8697],[FILE_NUM].[8699],[FILE_NUM].[8749],[FILE_NUM].[8763],[FILE_NUM].[8790],[FILE_NUM].[8840],[FILE_NUM].[8870],[FILE_NUM].[8939],[FILE_NUM].[9036],[FILE_NUM].[9077],[FILE_NUM].[9094],[FILE_NUM].[9107],[FILE_NUM].[9149],[FILE_NUM].[9150],[FILE_NUM].[9293],[FILE_NUM].[9429],[FILE_NUM].[9499],[FILE_NUM].[9550],[FILE_NUM].[9571],[FILE_NUM].[9579],[FILE_NUM].[9752],[FILE_NUM].[9910],[FILE_NUM].[9953],[FILE_NUM].[10270],[FILE_NUM].[10271],[FILE_NUM].[10272],[FILE_NUM].[10273],[FILE_NUM].[10274],[FILE_NUM].[10275],[FILE_NUM].[10309],[FILE_NUM].[10326],[FILE_NUM].[10403],[FILE_NUM].[10408],[FILE_NUM].[10471],[FILE_NUM].[10491],[FILE_NUM].[10496],[FILE_NUM].[10505],[FILE_NUM].[10551],[FILE_NUM].[10572],[FILE_NUM].[10601],[FILE_NUM].[10615],[FILE_NUM].[10679],[FILE_NUM].[10725],[FILE_NUM].[10778],[FILE_NUM].[10819],[FILE_NUM].[11002],[FILE_NUM].[11042],[FILE_NUM].[11055],[FILE_NUM].[11076],[FILE_NUM].[11095],[FILE_NUM].[11112],[FILE_NUM].[11213],[FILE_NUM].[11249],[FILE_NUM].[11308],[FILE_NUM].[11311],[FILE_NUM].[11486],[FILE_NUM].[11555]})</p>
  </blockquote>
</blockquote>

<p><strong><em>Cube Definition</em></strong>:</p>

<pre><code>&lt;Schema name="ONG" description="Schema for RIAB"&gt;
    &lt;Dimension type="StandardDimension" visible="true" highCardinality="false" name="Location"&gt;
        &lt;Hierarchy name="LOCATION_HIR" visible="true" hasAll="true" allMemberName="AllLocations" primaryKey="FILE_NO"&gt;
            &lt;Table name="mas_well_spatial_dim"&gt;
            &lt;/Table&gt;
            &lt;Level name="Township" visible="true" column="TOWNSHIP" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="Range" visible="true" column="RANGE" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="Section" visible="true" column="SECTION" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="CountyName" visible="true" column="COUNTY_NAME" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="FieldName" visible="true" column="FIELD_NAME" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
        &lt;/Hierarchy&gt;
    &lt;/Dimension&gt;
    &lt;Dimension type="StandardDimension" visible="true" highCardinality="false" name="WellIndex"&gt;
        &lt;Hierarchy name="WellIndex_HIR" visible="true" hasAll="true" allMemberName="AllWellIndexes" primaryKey="FILE_NO"&gt;
            &lt;Table name="mas_well_index"&gt;
            &lt;/Table&gt;
            &lt;Level name="Wellbore" visible="true" column="WELL_BORE" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="TotalDepth" visible="true" column="TOTAL_DEPTH" type="Integer" internalType="int" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="CurrentOperator" visible="true" column="CURRENT_OPERATOR" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="OriginalOperator" visible="true" column="ORIGINAL_OPERATOR" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="SpudDate" visible="true" column="SPUD_DATE" type="Date" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="WellStatus" visible="true" column="WELL_STATUS" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
            &lt;Level name="WellType" visible="true" column="WELL_TYPE" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
        &lt;/Hierarchy&gt;
    &lt;/Dimension&gt;
    &lt;Dimension type="StandardDimension" visible="true" name="FIELD_NAME"&gt;
        &lt;Hierarchy name="FIELD_NAME_HIR" visible="true" hasAll="true" allMemberName="AllFieldNames" primaryKey="FILE_NO"&gt;
            &lt;Table name="mas_well_spatial_dim"&gt;
            &lt;/Table&gt;
            &lt;Level name="FIELD_NAME" visible="true" column="FIELD_NAME" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
        &lt;/Hierarchy&gt;
    &lt;/Dimension&gt;
    &lt;Dimension type="StandardDimension" visible="true" highCardinality="false" name="FILE_NUM"&gt;
        &lt;Hierarchy name="FILE_NUM_HIR" visible="true" hasAll="true" allMemberName="AllFileNos" primaryKey="FILE_NO"&gt;
            &lt;Table name="mas_well_index"&gt;
            &lt;/Table&gt;
            &lt;Level name="FileNos" visible="true" column="FILE_NO" type="Numeric" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
            &lt;/Level&gt;
        &lt;/Hierarchy&gt;
    &lt;/Dimension&gt;
    &lt;Cube name="MON_KPI_CHARTS" visible="true" cache="true" enabled="true"&gt;
        &lt;Table name="prd_well_production_monthly"&gt;
        &lt;/Table&gt;
        &lt;Dimension type="TimeDimension" visible="true" foreignKey="DATE_ID" highCardinality="false" name="TIME"&gt;
            &lt;Hierarchy name="Quaterly" visible="true" hasAll="true" primaryKey="DATE_ID"&gt;
                &lt;Table name="mas_date_temporal_dim"&gt;
                &lt;/Table&gt;
                &lt;Level name="Year" visible="true" table="mas_date_temporal_dim" column="YEAR" type="Integer" uniqueMembers="true" levelType="TimeYears" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
                &lt;Level name="Quarter" visible="true" table="mas_date_temporal_dim" column="QUARTER" type="String" uniqueMembers="false" levelType="TimeQuarters" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
                &lt;Level name="Month" visible="true" table="mas_date_temporal_dim" column="MONTH" type="String" uniqueMembers="false" levelType="TimeMonths" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
            &lt;Hierarchy name="Monthly" visible="true" hasAll="true" primaryKey="DATE_ID"&gt;
                &lt;Table name="mas_date_temporal_dim"&gt;
                &lt;/Table&gt;
                &lt;Level name="Year" visible="true" table="mas_date_temporal_dim" column="YEAR" type="Integer" uniqueMembers="true" levelType="TimeYears" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
                &lt;Level name="Month" visible="true" table="mas_date_temporal_dim" column="MONTH" type="String" uniqueMembers="false" levelType="TimeMonths" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
                &lt;Level name="Day" visible="true" table="mas_date_temporal_dim" column="DAY" type="Integer" uniqueMembers="false" levelType="TimeDays" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;Dimension type="StandardDimension" visible="true" foreignKey="FILE_NO" highCardinality="false" name="WELL_ID"&gt;
            &lt;Hierarchy name="WELL_ID_HIR" visible="true" hasAll="true" allMemberName="AllWells" primaryKey="FILE_NO"&gt;
                &lt;Table name="mas_well_index"&gt;
                &lt;/Table&gt;
                &lt;Level name="WellIds" visible="true" column="API_NO" type="Numeric" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
         &lt;Dimension type="StandardDimension" visible="true" foreignKey="FILE_NO" highCardinality="false" name="CURRENT_OPTR"&gt;
            &lt;Hierarchy name="CURRENT_OPTR_HIR" visible="true" hasAll="true" allMemberName="AllWells" primaryKey="FILE_NO"&gt;
                &lt;Table name="mas_well_index"&gt;
                &lt;/Table&gt;
                &lt;Level name="CurrentOperator" visible="true" column="CURRENT_OPERATOR" type="String" internalType="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;DimensionUsage source="FILE_NUM" name="FILE_NUM" visible="true" foreignKey="FILE_NO"&gt;
        &lt;/DimensionUsage&gt;
        &lt;DimensionUsage source="Location" name="LOCATION" visible="true" foreignKey="FILE_NO" highCardinality="false"&gt;
        &lt;/DimensionUsage&gt;
        &lt;DimensionUsage source="WellIndex" name="WELL_INDEX" visible="true" foreignKey="FILE_NO" highCardinality="false"&gt;
        &lt;/DimensionUsage&gt;
        &lt;Dimension type="StandardDimension" visible="true" foreignKey="DATE_ID" highCardinality="false" name="MON_KPI_DATE"&gt;
            &lt;Hierarchy name="DATE_HIR" visible="true" hasAll="true" allMemberName="AllDateValues" primaryKey="DATE_ID"&gt;
                &lt;Table name="mas_date_temporal_dim"&gt;
                &lt;/Table&gt;
                &lt;Level name="DATE" visible="true" table="mas_date_temporal_dim" column="DATE_VALUE" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;Dimension type="StandardDimension" visible="true" highCardinality="false" name="DATE_VALUE"&gt;
            &lt;Hierarchy name="DATE_VALUE_HIR" visible="true" hasAll="true" allMemberName="AllDateValues" primaryKey="FILE_NO"&gt;
                &lt;Level name="DATE" visible="true" column="DATE" type="Timestamp" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;Dimension type="StandardDimension" visible="true" foreignKey="FILE_NO" highCardinality="false" name="COUNTY"&gt;
            &lt;Hierarchy name="COUNTY_HIR" visible="true" hasAll="true" allMemberName="AllCounties" primaryKey="FILE_NO"&gt;
                &lt;Table name="mas_well_spatial_dim"&gt;
                &lt;/Table&gt;
                &lt;Level name="CountyName" visible="true" column="COUNTY_NAME" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;DimensionUsage source="FIELD_NAME" name="FIELDNAME" visible="true" foreignKey="FILE_NO"&gt;
        &lt;/DimensionUsage&gt;
        &lt;Measure name="BBLSOIL_TOTAL" column="OIL_PROD_BBLS" datatype="Numeric" formatString="Standard" aggregator="sum" visible="true"&gt;
        &lt;/Measure&gt;
        &lt;Measure name="VENT_FLARE_TOTAL" column="GAS_VENT_MCF" datatype="Numeric" formatString="Standard" aggregator="sum" visible="true"&gt;
        &lt;/Measure&gt;
        &lt;Measure name="BBLSWATER_TOTAL" column="WATER_PROD_BBLS" datatype="Numeric" formatString="Standard" aggregator="sum" visible="true"&gt;
        &lt;/Measure&gt;
        &lt;Measure name="MCF_PROD_TOTAL" column="GAS_PROD_MCF" datatype="Numeric" formatString="Standard" aggregator="sum" visible="true"&gt;
        &lt;/Measure&gt;
        &lt;Measure name="AVG.DAYS" column="DAYS_IN_PROD" datatype="Numeric" formatString="###.####" aggregator="avg" visible="true"&gt;
        &lt;/Measure&gt;
    &lt;/Cube&gt;
    &lt;Cube name="SPUD_KPI_CHART" visible="true" cache="true" enabled="true"&gt;
        &lt;Table name="mas_well_spatial_dim"&gt;
        &lt;/Table&gt;
        &lt;Dimension type="StandardDimension" visible="true" foreignKey="FILE_NO" highCardinality="false" name="WELL_ID"&gt;
            &lt;Hierarchy name="WELL_ID_HIR" visible="true" hasAll="true" allMemberName="AllWellIDs" primaryKey="FILE_NO"&gt;
                &lt;Table name="mas_well_index"&gt;
                &lt;/Table&gt;
                &lt;Level name="WellIDs" visible="true" column="API_NO" type="Numeric" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;DimensionUsage source="FILE_NUM" name="FILE_NUM" visible="true" foreignKey="FILE_NO"&gt;
        &lt;/DimensionUsage&gt;
        &lt;DimensionUsage source="FIELD_NAME" name="FIELDNAME" visible="true" foreignKey="FILE_NO"&gt;
        &lt;/DimensionUsage&gt;
        &lt;Dimension type="StandardDimension" visible="true" foreignKey="FILE_NO" name="SPUDDATE"&gt;
            &lt;Hierarchy name="SPUDDATE_HIR" visible="true" hasAll="true" allMemberName="AllDates" primaryKey="FILE_NO"&gt;
                &lt;Table name="mas_well_index"&gt;
                &lt;/Table&gt;
                &lt;Level name="SPUD_DATE" visible="true" column="SPUD_DATE" type="String" uniqueMembers="true" levelType="Regular" hideMemberIf="Never"&gt;
                &lt;/Level&gt;
            &lt;/Hierarchy&gt;
        &lt;/Dimension&gt;
        &lt;Measure name="NewWells" column="FIELD_NAME" datatype="Integer" formatString="Standard" aggregator="count" visible="true"&gt;
        &lt;/Measure&gt;
    &lt;/Cube&gt;
&lt;/Schema&gt;
</code></pre>

## Answers
### Answer ID: 39989054
<p>Since Mondrian is a ROLAP engine ultimately the MDX getting converted in to SQL and that SQL runs on the DB. So all RDBMS factors like number of rows, table size and indexes are matters for performance. You may enable the Mondiran SQL logs at <code>WEB-INF/classes/log4j.xml</code> and see the corresponding SQL. You may have to do some optimisations to DB as well.  </p>


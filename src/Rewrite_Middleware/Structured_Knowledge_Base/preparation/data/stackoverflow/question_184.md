# Slow query - suggestions for rewrite with focus on where clause (or whatever else makes sense)
[Link to question](https://stackoverflow.com/questions/16015833/slow-query-suggestions-for-rewrite-with-focus-on-where-clause-or-whatever-els)
**Creation Date:** 1366030904
**Score:** 0
**Tags:** sql-server
## Question Body
<p>Database: sqlserver 2008.
The following query is extremely slow.  I'm looking to get this beast to run faster, rewrite the query, but I'm stumped.  I can comment out all the sum case statements and group by clauses to leave just the shell of a query with the select sum(0) and the where clause and the performance doesn't change much.  So I'm pretty sure the problem is with the where clause.  But, I'm not sure how to rewrite this one to try any other alternatives.</p>

<p>Anyone want to test their SQL-fu on this one?
Any help is much appreciated.  Thanks!</p>

<pre><code>    INSERT INTO [_SOC_Reviews]
DECLARE
    @LocationID         Int=NULL,
    @FromDate           DateTime=NULL,
    @ToDate             DateTime=NULL,
    @DateType           Int=0,
    @OfficeID           Int=NULL,
    @QCType             Int=NULL,
    @ProgramTypeID      Int=NULL,
    @SupervisorID       varchar(100)=NULL,
    @SpecialistID       varchar(100)=NULL,
    @ReviewerID         varchar(100)=NULL,
    @PrincipalActionID  Int=NULL,
    @DepartmentID       Int=NULL,
    @Group1             Int=1,
    @Group2             Int=1,
    @ReportName         VarChar(100)='rptQC',
    @UserName           varchar(30)=NULL

select 
    @LocationID=NULL,
    @FromDate='2012-05-01 00:00:00',
    @ToDate='2012-06-01',
    @OfficeID=NULL,
    @ProgramTypeID=NULL,
    @SupervisorID=NULL,
    @SpecialistID=NULL,
    @PrincipalActionID=NULL,
    @QCType=NULL,
    @Group1=1,
    @Group2=NULL,
    @UserName=N'joeblow',
    @DepartmentID=NULL,
    @ReviewerID=NULL

IF OBJECT_ID('dbo.[_SOC_Reviews]', 'U') IS NOT NULL
  DROP TABLE dbo.[_SOC_Reviews]
CREATE TABLE [_SOC_Reviews] (
    IsReviewed                  int,
    Group1                      Varchar(100),
    Group2                      Varchar(100),
    NumFilesAssigned            int,
    NumFilesInProgress          int,
    TotalNumFiles               int,
    PendingCorrections          int,
    PendingCorrGT30             int
    )


select SUM(0),
        CASE 
            WHEN @Group1 = 1 THEN CONVERT(Varchar(100), R.LocationID)
            WHEN @Group1 = 2 THEN CONVERT(Varchar(100), R.SubLocation)
            WHEN @Group1 = 3 THEN CONVERT(Varchar(100), R.ProgramTypeID)
            WHEN @Group1 = 4 THEN CONVERT(Varchar(100), RS.SupervisorID)
            WHEN @Group1 = 5 THEN CONVERT(Varchar(100), R.TransactionTypeId)
            WHEN @Group1 = 6 THEN CONVERT(Varchar(100), RS.SpecialistID)
            WHEN @Group1 = 7 THEN CONVERT(Varchar(100), R.ChecklistTypeId)
            WHEN @Group1 = 8 THEN CONVERT(Varchar(100), RS.DepartmentID)
            WHEN @Group1 = 9 THEN CONVERT(Varchar(2), DATEPART(MONTH,R.EffectiveActionDate)) + '/' + CONVERT(VARCHAR(4),DATEPART(YEAR,R.EffectiveActionDate))
            WHEN @Group1 = 10 THEN CONVERT(Varchar(100), R.ReviewedBy)
        END,
        CASE 
            WHEN @Group2 = 1 THEN CONVERT(Varchar(100), R.SubLocation)
            WHEN @Group2 = 2 THEN CONVERT(Varchar(100), R.ProgramTypeID)
            WHEN @Group2 = 3 THEN CONVERT(Varchar(100), RS.SupervisorID)
            WHEN @Group2 = 4 THEN CONVERT(Varchar(100), RS.SpecialistID) 
            WHEN @Group2 = 5 THEN CONVERT(Varchar(100), R.TransactionTypeId)
            WHEN @Group2 = 6 THEN CONVERT(Varchar(100), R.LocationID)
            WHEN @Group2 = 7 THEN CONVERT(Varchar(100), R.ChecklistTypeId)
            WHEN @Group2 = 8 THEN CONVERT(Varchar(100), RS.DepartmentID)
            WHEN @Group2 = 9 THEN CONVERT(Varchar(2), DATEPART(MONTH,R.EffectiveActionDate)) + '/' + CONVERT(VARCHAR(4),DATEPART(YEAR,R.EffectiveActionDate))
            WHEN @Group2 = 10 THEN CONVERT(Varchar(100), R.ReviewedBy) 
            ELSE NULL
        END,
    SUM(CASE WHEN R.ReviewStatusId = 7 AND (R.ReviewStatusModified BETWEEN @FromDate AND @ToDate) THEN 1 ELSE 0 END) AS NumberOfFilesAssigned,
    SUM(CASE WHEN R.ReviewStatusId = 1 AND (R.ReviewStatusModified BETWEEN @FromDate AND @ToDate) THEN 1 ELSE 0 END) as NumberOfFilesInProgress,
    SUM(CASE WHEN (R.ReviewStatusModified BETWEEN @FromDate AND @ToDate) THEN 1 ELSE 0 END) AS TotalNumFiles,
    SUM(CASE WHEN R.ReviewStatusId IN (10,12,14,16) THEN 1 ELSE 0 END),
    SUM(CASE WHEN R.ReviewStatusId IN (10,12,14,16) AND DATEDIFF(DAY, R.InitialCompletionDate, GETDATE()) &gt; 30  THEN 1 ELSE 0 END)

from Review R 
LEFT JOIN   dbo.fnu_ReviewSpecialists2_TEST(@SpecialistID,@SupervisorID,@DepartmentID) RS
    ON  R.Id = RS.ReviewId
    LEFT JOIN Location L
    ON R.LocationId = L.Id
    INNER JOIN  [_SOC_USER] U
    ON R.LocationID = U.LocationID
where 
    ((R.LocationID = @LocationID AND @LocationID IS NOT NULL) OR (@LocationID IS NULL))
    AND ((R.SubLocation = @OfficeID AND @OfficeID IS NOT NULL) or (@OfficeID IS NULL))
    AND ((R.ProgramTypeID = @ProgramTypeID AND @ProgramTypeID IS NOT NULL) or (@ProgramTypeID IS NULL))
    AND ((R.TransactionTypeId = @PrincipalActionID AND @PrincipalActionID IS NOT NULL) or (@PrincipalActionID IS NULL))
    AND ((R.ChecklistTypeId = @QCType AND @QCType IS NOT NULL) OR (@QCType IS NULL))
    AND ((R.ReviewedBy = @ReviewerID AND @ReviewerID IS NOT NULL) or (@ReviewerID IS NULL))
    AND ((RS.SupervisorId = @SupervisorID AND @SupervisorID IS NOT NULL) or (@SupervisorID IS NULL))
    AND ((RS.SpecialistId = @SpecialistID AND @SpecialistID IS NOT NULL) or (@SpecialistID IS NULL))
    AND ((RS.DepartmentId = @DepartmentID AND @DepartmentID IS NOT NULL) or (@DepartmentID IS NULL))
    AND (@LocationID is NOT NULL OR L.IsConsulting = 0)
    AND L.IsActive = 1

GROUP BY  
        CASE
            WHEN @Group1 = 1 THEN CONVERT(Varchar(100), R.LocationID)
            WHEN @Group1 = 2 THEN CONVERT(Varchar(100), R.SubLocation)
            WHEN @Group1 = 3 THEN CONVERT(Varchar(100), R.ProgramTypeID)
            WHEN @Group1 = 4 THEN CONVERT(Varchar(100), RS.SupervisorID)
            WHEN @Group1 = 5 THEN CONVERT(Varchar(100), R.TransactionTypeId)
            WHEN @Group1 = 6 THEN CONVERT(Varchar(100), RS.SpecialistID)
            WHEN @Group1 = 7 THEN CONVERT(Varchar(100), R.ChecklistTypeID)
            WHEN @Group1 = 8 THEN CONVERT(Varchar(100), RS.DepartmentID)
            WHEN @Group1 = 9 THEN CONVERT(Varchar(2), DATEPART(MONTH,R.EffectiveActionDate)) + '/' + CONVERT(VARCHAR(4),DATEPART(YEAR,R.EffectiveActionDate))
            WHEN @Group1 = 10 THEN CONVERT(Varchar(100), R.ReviewedBy)          
        END,
        CASE 
            WHEN @Group2 = 1 THEN CONVERT(Varchar(100), R.SubLocation)
            WHEN @Group2 = 2 THEN CONVERT(Varchar(100), R.ProgramTypeID)
            WHEN @Group2 = 3 THEN CONVERT(Varchar(100), RS.SupervisorID)
            WHEN @Group2 = 4 THEN CONVERT(Varchar(100), RS.SpecialistID) 
            WHEN @Group2 = 5 THEN CONVERT(Varchar(100), R.TransactionTypeId)
            WHEN @Group2 = 6 THEN CONVERT(Varchar(100), R.LocationID)
            WHEN @Group2 = 7 THEN CONVERT(Varchar(100), R.ChecklistTypeId)
            WHEN @Group2 = 8 THEN CONVERT(Varchar(100), RS.DepartmentID)
            WHEN @Group2 = 9 THEN CONVERT(Varchar(2), DATEPART(MONTH,R.EffectiveActionDate)) + '/' + CONVERT(VARCHAR(4),DATEPART(YEAR,R.EffectiveActionDate))
            WHEN @Group2 = 10 THEN CONVERT(Varchar(100), R.ReviewedBy)          
            ELSE NULL
        END 
</code></pre>

<p>Here is the explain plan:</p>

<pre><code>      |--Stream Aggregate(GROUP BY:([Expr1015], [Expr1014]) DEFINE:([Expr1016]=SUM((0)), [Expr1017]=SUM(CASE WHEN [_DatabaseTesta].[dbo].[Review].[ReviewStatusId] as [R].[ReviewStatusId]=(7) AND [_DatabaseTesta].[dbo].[Review].[ReviewStatusModified] as [R].[Re 3           4           3           Stream Aggregate              
       |--Sort(ORDER BY:([Expr1015] ASC, [Expr1014] ASC))                                                                                                                                                                                                        3           5           4           Sort                          
            |--Compute Scalar(DEFINE:([Expr1014]=CASE WHEN [@Group1]=(1) THEN CONVERT(varchar(100),[_DatabaseTesta].[dbo].[Review].[LocationId] as [R].[LocationId],0) ELSE CASE WHEN [@Group1]=(10) THEN CONVERT(varchar(100),[_DatabaseTesta].[dbo].[Review].[ 3           6           5           Compute Scalar                
                 |--Filter(WHERE:(([_DatabaseTesta].[dbo].[ReviewSpecialist].[SupervisorId]=CONVERT_IMPLICIT(uniqueidentifier,[@SupervisorID],0) AND [@SupervisorID] IS NOT NULL OR [@SupervisorID] IS NULL) AND ([_DatabaseTesta].[dbo].[ReviewSpecialist].[Spe 3           7           6           Filter                        
                      |--Nested Loops(Left Outer Join, OUTER REFERENCES:([R].[Id]))                                                                                                                                                                              3           8           7           Nested Loops                  
                           |--Nested Loops(Inner Join, OUTER REFERENCES:([U].[locationID]))                                                                                                                                                                      3           9           8           Nested Loops                  
                           |    |--Nested Loops(Inner Join, WHERE:([_DatabaseTesta].[dbo].[Review].[LocationId] as [R].[LocationId]=[_DatabaseTesta].[dbo].[_SOC_USER].[locationID] as [U].[locationID]))                                                        3           10          9           Nested Loops                  
                           |    |    |--Sort(ORDER BY:([R].[Id] ASC))                                                                                                                                                                                            3           11          10          Sort                          
                           |    |    |    |--Compute Scalar(DEFINE:([Expr1047]=CASE WHEN [_DatabaseTesta].[dbo].[Review].[ReviewStatusId] as [R].[ReviewStatusId]=(16) OR [_DatabaseTesta].[dbo].[Review].[ReviewStatusId] as [R].[ReviewStatusId]=(14) OR [Qual 3           12          11          Compute Scalar                
                           |    |    |         |--Nested Loops(Inner Join, OUTER REFERENCES:([R].[Id], [Expr1056]) WITH UNORDERED PREFETCH)                                                                                                                      3           13          12          Nested Loops                  
                           |    |    |              |--Hash Match(Inner Join, HASH:([R].[Id])=([R].[Id]))                                                                                                                                                        3           16          13          Hash Match                    
                           |    |    |              |    |--Index Scan(OBJECT:([_DatabaseTesta].[dbo].[Review].[idxReview_Status_Loc] AS [R]),  WHERE:(([_DatabaseTesta].[dbo].[Review].[LocationId] as [R].[LocationId]=[@LocationID] AND [@LocationID] IS NOT  3           17          16          Index Scan                    
                           |    |    |              |    |--Index Scan(OBJECT:([_DatabaseTesta].[dbo].[Review].[idx_Review_TenantID_QCType] AS [R]),  WHERE:([_DatabaseTesta].[dbo].[Review].[ChecklistTypeId] as [R].[ChecklistTypeId]=[@QCType] AND [@QCType]  3           18          16          Index Scan                    
                           |    |    |              |--Clustered Index Seek(OBJECT:([_DatabaseTesta].[dbo].[Review].[PK_Review] AS [R]), SEEK:([R].[Id]=[_DatabaseTesta].[dbo].[Review].[Id] as [R].[Id]),  WHERE:([_DatabaseTesta].[dbo].[Review].[SubLocation] 3           32          13          Clustered Index Seek          
                           |    |    |--Table Scan(OBJECT:([_DatabaseTesta].[dbo].[_SOC_USER] AS [U]))                                                                                                                                                           3           41          10          Table Scan                    
                           |    |--Clustered Index Seek(OBJECT:([_DatabaseTesta].[dbo].[Location].[PK_Location] AS [L]), SEEK:([L].[Id]=[_DatabaseTesta].[dbo].[_SOC_USER].[locationID] as [U].[locationID]),  WHERE:([_DatabaseTesta].[dbo].[Location].[IsActiv 3           43          9           Clustered Index Seek          
                           |--Nested Loops(Left Semi Join, WHERE:([_DatabaseTesta].[dbo].[ReviewSpecialist].[Id]=[Expr1008]))                                                                                                                                    3           44          8           Nested Loops                  
                                |--Nested Loops(Inner Join, OUTER REFERENCES:([_DatabaseTesta].[dbo].[ReviewSpecialist].[Id]))                                                                                                                                   3           45          44          Nested Loops                  
                                |    |--Index Seek(OBJECT:([_DatabaseTesta].[dbo].[ReviewSpecialist].[idxReviewSpecialist_ReviewID]), SEEK:([_DatabaseTesta].[dbo].[ReviewSpecialist].[ReviewId]=[_DatabaseTesta].[dbo].[Review].[Id] as [R].[Id]) ORDERED FORWA 3           46          45          Index Seek                    
                                |    |--Clustered Index Seek(OBJECT:([_DatabaseTesta].[dbo].[ReviewSpecialist].[PK_ReviewSpecialist]), SEEK:([_DatabaseTesta].[dbo].[ReviewSpecialist].[Id]=[_DatabaseTesta].[dbo].[ReviewSpecialist].[Id]) LOOKUP ORDERED FORWA 3           48          45          Clustered Index Seek          
                                |--Table Spool                                                                                                                                                                                                                   3           56          44          Table Spool                   
                                     |--Stream Aggregate(GROUP BY:([_DatabaseTesta].[dbo].[ReviewSpecialist].[ReviewId]) DEFINE:([Expr1008]=MIN([_DatabaseTesta].[dbo].[ReviewSpecialist].[Id])))                                                                3           57          56          Stream Aggregate              
                                          |--Sort(ORDER BY:([_DatabaseTesta].[dbo].[ReviewSpecialist].[ReviewId] ASC))                                                                                                                                           3           58          57          Sort                          
                                               |--Clustered Index Scan(OBJECT:([_DatabaseTesta].[dbo].[ReviewSpecialist].[PK_ReviewSpecialist]), WHERE:([_DatabaseTesta].[dbo].[ReviewSpecialist].[SpecialistId]=isnull(CONVERT_IMPLICIT(uniqueidentifier,[@Spec 3           59          58          Clustered Index Scan          
</code></pre>

## Answers
### Answer ID: 16016133
<p>Add at the end of the query hint - <code>option(recompile)</code></p>


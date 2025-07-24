# SQL Server 2008: Using Multiple dts Ranges to Build a Set of Dates
[Link to question](https://stackoverflow.com/questions/2687655/sql-server-2008-using-multiple-dts-ranges-to-build-a-set-of-dates)
**Creation Date:** 1271899248
**Score:** 0
**Tags:** sql, sql-server, sql-server-2008
## Question Body
<p>I'm trying to build a query for a medical database that counts the number of patients that were on at least one medication from a class of medications (the medications listed below in the FAST_MEDS CTE) and had either:
1) A diagnosis of myopathy (the list of diagnoses in the FAST_DX CTE)
2) A CPK lab value above 1000 (the lab value in the FAST_LABS CTE)
and this diagnosis or lab happened AFTER a patient was on a statin.</p>

<p>The query I've included below does that under the assumption that once a patient is on a statin, they're on a statin forever. The first CTE collects the ids of patients that were on a statin along with the first date of their diagnosis, the second those with a diagnosis, and the third those with a high lab value. After this I count those that match the above criteria.</p>

<p>What I would like to do is drop the assumption that once a patient is on a statin, they're on it for life. The table edw_dm.patient_medications has a column called start_dts and end_dts. This table has one row for each prescription written, with start_dts and end_dts denoting the start and end date of the prescription. End_dts could be null, which I'll take to assume that the patient is currently on this medication (it could be a missing record, but I can't do anything about this). If a patient is on two different statins, the start and ends dates can overlap, and there may be multiple records of the same medication for a patient, as in a record showing 3-11-2000 to 4-5-2003 and another for the same patient showing 5-6-2007 to 7-8-2009.</p>

<p>I would like to use these two columns to build a query where I'm only counting the patients that had a lab value or diagnosis done during a time when they were already on a statin, or in the first n (say 3) months after they stopped taking a statin. I'm really not sure how to go about rewriting the first CTE to get this information and how to do the comparison after the CTEs are built. I know this is a vague question, but I'm really stumped. Any ideas?</p>

<p>As always, thank you in advance.</p>

<p>Here's the current query:</p>

<pre><code>    WITH FAST_MEDS AS
    (
    select distinct
     statins.mrd_pt_id, min(year(statins.order_dts)) as statin_yr
     from
      edw_dm.patient_medications as statins
      inner join mrd.medications as mrd
        on statins.mrd_med_id = mrd.mrd_med_id
        WHERE mrd.generic_nm in (
           'Lovastatin (9664708500)',
           'lovastatin-niacin',
           'Lovastatin/Niacin',
           'Lovastatin',
           'Simvastatin (9678583966)',
           'ezetimibe-simvastatin',
           'niacin-simvastatin',
           'ezetimibe/Simvastatin',
           'Niacin/Simvastatin',
           'Simvastatin',
           'Aspirin Buffered-Pravastatin',
           'aspirin-pravastatin',
           'Aspirin/Pravastatin',
           'Pravastatin',
           'amlodipine-atorvastatin',
           'Amlodipine/atorvastatin',
           'atorvastatin',
           'fluvastatin',
           'rosuvastatin'
            )
        and YEAR(statins.order_dts) IS NOT NULL
        and statins.mrd_pt_id IS NOT NULL
     group by statins.mrd_pt_id
    )

    select *
    into #meds
    from FAST_MEDS
    ;

    --return patients who had a diagnosis in the list and the year that
    --diagnosis was given
    with
    FAST_DX AS
    (
     SELECT pd.mrd_pt_id, YEAR(pd.init_noted_dts) as init_yr
      FROM edw_dm.patient_diagnoses as pd
        inner join mrd.diagnoses as mrd
          on pd.mrd_dx_id = mrd.mrd_dx_id
          and mrd.icd9_cd in
    ('728.89','729.1','710.4','728.3','729.0','728.81','781.0','791.3')
    )
    select *
    into #dx
    from FAST_DX;

    --return patients who had a high cpk value along with the year the cpk
    --value was taken
    with
    FAST_LABS AS
    (
     SELECT
      pl.mrd_pt_id, YEAR(pl.order_dts) as lab_yr
     FROM
      edw_dm.patient_labs as pl
      inner join mrd.labs as mrd
        on pl.mrd_lab_id = mrd.mrd_lab_id
        and mrd.lab_nm = 'CK (CPK)'
     WHERE
       pl.lab_val between 1000 AND 999998
    )
    select *
    into #labs
    from FAST_LABS;

    -- count the number of patients who had a lab value or a medication
    -- value taken sometime AFTER their initial statin diagnosis
    select
     count(distinct p.mrd_pt_id) as ct
    from
     mrd.patient_demographics as p
     join #meds as m
      on p.mrd_pt_id = m.mrd_pt_id
     AND 
     (
       EXISTS (
             SELECT 'A' FROM #labs l WHERE p.mrd_pt_id = l.mrd_pt_id
             and l.lab_yr &gt;= m.statin_yr
       ) 
       OR
       EXISTS(
           SELECT 'A' FROM #dx d WHERE p.mrd_pt_id = d.mrd_pt_id
           AND d.init_yr &gt;= m.statin_yr
       )
     )
</code></pre>

## Answers
### Answer ID: 2687725
<p>You probably don't need to select all of your CTE defined queries into temp tables.</p>

<p>I think that the query you're after has the form:</p>

<pre><code>WITH FAST_MEDS(PatientID, StartDate, EndDate) AS
(
    --your query for patients on statins, projecting the patient ID and the start/end date for the medication
),
FAST_DX(PatientID, Date) AS
(
    --your query for patients with certain diagnosis, projecting the patient ID and the date
),
FAST_LABS(PatientID, Date) AS
(
    --your query for patients with certain labs, projecting the patient ID and the date
)
SELECT PatientID
FROM FAST_MEDS
WHERE PatientID IN (SELECT PatientID FROM FAST_DX WHERE Date BETWEEN StartDate AND EndDate OR EndDate IS NULL AND StartDate &lt; Date)
  OR  PatientID IN (SELECT PatientID FROM FAST_LABS WHERE Date BETWEEN StartDate AND EndDate OR EndDate IS NULL AND StartDate &lt; Date)
</code></pre>


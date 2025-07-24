# Subqueries in Linq when attempting to get counts
[Link to question](https://stackoverflow.com/questions/63144446/subqueries-in-linq-when-attempting-to-get-counts)
**Creation Date:** 1595980915
**Score:** 0
**Tags:** linq, .net-core
## Question Body
<p>I'm trying to get some subqueries to work in a call of mine. I am trying to make this call one trip to the database but cannot for the life of me solve how.  The query breaks on the GoodSections portion.  I have tried many different methods of doing this.  I keep getting this message:</p>
<blockquote>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()</p>
</blockquote>
<p>Can someone help me?</p>
<pre><code>var test = context.UserAssessments.Include(n =&gt; n.Assessment).Include(n =&gt; n.UserSections).ThenInclude(userSection =&gt; userSection.Section)
                .OrderBy(n =&gt; n.StartDateTime);

            MyAssessments = await test.Select(assessment =&gt; new MyAssessmentVM()
            {
                Assessment = assessment.Assessment.Name,
                CompletedDateTime = assessment.CompletedDateTime,
                StartedDateTime = assessment.StartDateTime,
                UserAssessmentID = assessment.ID,
                GoodSections = assessment.UserSections.Where(userSection =&gt; userSection.Section.SectionType != SectionTypeEnum.Reading)
                            .Count(n =&gt; n.Percentage &lt; n.Section.ReadinessRangeHigh &amp;&amp; n.Percentage &gt; n.Section.ReadinessRangeLow)
            }).ToListAsync();
</code></pre>

## Answers
### Answer ID: 63227513
<p>Your code:</p>
<pre><code> GoodSections = assessment.UserSections
    .Where(userSection =&gt; userSection.Section.SectionType != SectionTypeEnum.Reading)

    // End of Where!

    .Count(n =&gt; n.Percentage &lt; n.Section.ReadinessRangeHigh 
             &amp;&amp; n.Percentage &gt; n.Section.ReadinessRangeLow)
</code></pre>
<p>Apparently, every Assesment has a sequence of zero or more UserSections. It seems to me that every UserSection has a Percentage and exactly one Section.</p>
<p>You use Include to access the values of this Section, so I assume that Section is in a different table, with a one-to-many relation: every Section is the section of zero or more UserSections; every UserSection belongs to exaclty one Section, namely the one that the foreign key refers to.</p>
<p>First, try to simplify your Count, if that does not help, consider to GroupJoin.</p>
<pre><code>GoodSections = assessment.UserSections
    .Where(userSection =&gt; userSection.Section.SectionType != SectionTypeEnum.Reading
                       &amp;&amp; userSection.Percentage &lt; userSection.Section.ReadinessRangeHigh 
                       &amp;&amp; userSection.Percentage &gt; userSection.Section.ReadinessRangeLow)
    .Count(),
</code></pre>
<p>Do the GroupJoin yourself:</p>
<pre><code>var test = dbContext.UserAssessments.GroupJoin(
    dbContext.UserSections,

    userAssessment =&gt; userAssesment.Id      // from every Assessment take the primary key
    userSection =&gt; userSection.AssesmentId, // from every UserSection take the foreign key

    // parameter resultSelector: from every UserAssesment, with all its UserSections
    // make one new
    (userAssessment, userSectionsOfThisAssessment) =&gt; new
    {
        UserAssessmentID = userAssessment.ID,
        StartedDateTime = userAssessment.StartDateTime,
        CompletedDateTime = userAssessment.CompletedDateTime,

        // To get the name, we need to get the Assesment that my foreign key refers to
        AssessmentName = dbContext.Assessments
             .Where(assessment =&gt; assessment.AssessmentId == userAssesment.Id)
             .Select(assessment =&gt; assessment.Name)
             .FirstOrDefault(),

        GoodSections = ... // TODO
    });
</code></pre>
<p>I'm not sure, but it seems to me that there is a oney-to-many relation between Sections and UserSections: every Section has zero or more UserSections; every UserSection belongs to exactly one Section, namely the Section that the foreign key refers to.</p>
<p>So for every userSectionOfThisAssessment we need to get the Section that the foreign key refers to: a standard inner join</p>
<pre><code>GoodSections = userSectionsOfThisAssessment.Join(
    dbContext.Sections

    userSection =&gt; userSection.SectionId,    // take the foreign key to the section
    section =&gt; section.Id,                   // take the sections's primary key

    (userSection, section) =&gt; new
    {
        SectionType = section.SectionType,

        Percentage = userSection.Percentage,
        MaxPercentage = section.ReadinessRangeHigh,
        MinPercentage = section.ReadinessRangeLow,
    })
    .Where(joinResult =&gt; joinResult.SectionType != SectionTypeEnum.Reading
                      &amp;&amp; joinResult.Percentage &lt; MaxPercentage
                      &amp;&amp; joinResult.Percentage &gt; MinPercentage)
    .Count(),
    
</code></pre>
<p>For the GoodSections, we need to GroupJoin the <code>userSectionsOfThisAssessment</code> with all Sections. I'm not sure if this is a one-to-many relation, or a man</p>
<pre><code>        MyAssessments = await test.Select(assessment =&gt; new MyAssessmentVM()
        {
            Assessment = assessment.Assessment.Name,
            CompletedDateTime = assessment.CompletedDateTime,
            StartedDateTime = assessment.StartDateTime,
            UserAssessmentID = assessment.ID,
            GoodSections = assessment.UserSections.Where(userSection =&gt; userSection.Section.SectionType != SectionTypeEnum.Reading)
                        .Count(n =&gt; n.Percentage &lt; n.Section.ReadinessRangeHigh &amp;&amp; n.Percentage &gt; n.Section.ReadinessRangeLow)
        }).ToListAsync();
</code></pre>


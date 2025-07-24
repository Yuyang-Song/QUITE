# Receiving the LINQ expression x could not be translated error when using a properly loaded list object
[Link to question](https://stackoverflow.com/questions/67554907/receiving-the-linq-expression-x-could-not-be-translated-error-when-using-a-prope)
**Creation Date:** 1621156697
**Score:** 0
**Tags:** c#, entity-framework, linq, entity-framework-core
## Question Body
<p>I have the following <code>List</code> object which is properly loaded with valid values from the database:</p>
<pre><code>  List&lt;AssessmentItem&gt; assessmentItems = 
      _context.AssessmentItems
              .Include(ai =&gt; ai.Assessment).ThenInclude(assess =&gt; assess.Evaluator)
              .Where(ai =&gt; ai.IsActive &amp;&amp;
                           ai.Assessment.SubmissionId == submissionId &amp;&amp;
                           ai.Assessment.RubricId == rubricId)
              .ToList();
</code></pre>
<p>Then I need to use this <code>assessmentItems</code> list object inside another LINQ statement. I provide the partial code below where <code>assessmentItems</code> is used.</p>
<pre><code>   ....
   Description = ri.Description,
   Abbreviation = ri.Abbreviation,
   RubricId = ri.RubricId,
   RubricItemCategoryId = ri.RubricItemCategoryId,
   CurrentScores = assessmentItems
                         .Where(aitem =&gt; aitem.RubricItemId == ri.Id)
                         .Select(aitem =&gt; new AssessmentItemDTO
                         {
                             Id = aitem.Id,
                             EvaluatorName = aitem.Assessment.Evaluator.FirstName + &quot; &quot; + aitem.Assessment.Evaluator.LastName,
                             EvaluatorId = aitem.Assessment.EvaluatorId,
                             CurrentScore = aitem.CurrentScore
                         }).ToList(),
</code></pre>
<p>For some reason I receive the following error:</p>
<blockquote>
<p>The LINQ expression <code>'aitem'</code> could not be translated. Either rewrite
the query in a form that can be translated, or switch to client
evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'</p>
</blockquote>
<p>I checked other related posts in SO however I could not find a solution for my case. I am using the latest version of EF Core. Any help?</p>


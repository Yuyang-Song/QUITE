# Design of an Aggregate Root with a large collection of children
[Link to question](https://stackoverflow.com/questions/49230940/design-of-an-aggregate-root-with-a-large-collection-of-children)
**Creation Date:** 1520843442
**Score:** 1
**Tags:** c#, entity-framework, domain-driven-design
## Question Body
<p>I started a new project (rewrite an existing solution) and wanted to use and explore DDD. It was very hard to at the beginning to ignore the Entity Framework during designing my domain model. It worked very well for smaller aggregates that only have small child collections or that where only CRUD based. Now i am at a point, where i have an aggregate with a large collection and i get crazy about that.</p>

<p><strong>Domain Overview</strong></p>

<ul>
<li>In my domain model, there is an called <strong>Protocol</strong> (Aggregate Root).</li>
<li>A <strong>Protocol</strong> has children called <strong>Protocol Entries</strong>. </li>
<li><strong>Protocol Entries</strong> have a specific type (<em>Default</em>, <em>Monthly</em> and <em>Yearly</em>). As for now, there are no more requirements other than to know what type they are - they are all the same and behave the same but may have different types (read on to find out why).</li>
<li>Now during the month, there are added several <strong>Protocol Entries</strong> (Type: Default) to a specific <strong>Protocol</strong>. Its not possible to set or define the date(time) of a <strong>Protocol Entry</strong> - its added/created with "now".</li>
<li>At the <strong>end of every month</strong> (except at December, see next), there is the requirement, that a <strong>Protocol Entry</strong> (Type: Monthly) is created/added, before any other <strong>Protocol Entry</strong> can be added again.</li>
<li>At the <strong>end of every year</strong>, there is the requirement, that a <strong>Protocol Entry</strong> (Type: Yearly) is created/added, before any other <strong>Protocol Entry</strong> can be added again. At the end of the year, the <em>Monthly</em> entry is not required, because there is already the yearly.</li>
</ul>

<p>That may reads sick, but at the end may be looks like a really simple problem to solve. It is/was except with the following thing i want to achieve. I don't know and event cant find anything related that gives me the answer, if i am thinking again to much about persistence/performance when i should not as much during domain design. Or my it is not solvable that way.</p>

<p><strong>Futher Information</strong></p>

<p>Since the <em>Monthly</em> and <em>Yearly</em> <strong>Protocol Entries</strong> are created from the system itself (background job/service), the users won't event care about that. Maybe there will be an transient and short error when adding an <strong>Protocol Entry</strong> at the beginning of a new month/year at 00:00 because the background job/service has not the completed the <em>Monthly</em> or <em>Yearly</em> entry for the current <strong>Protocol</strong> yet - its ok!</p>

<p>The <strong>Protocol Entry</strong> in the old solution had two fields called <em>NextMonthlyEntry</em> and <em>NextYearlyEntry</em> (DataType: DateTime). With those, it is easy and feels very natural to ask the Aggregate questions like "protocol.IsYearlyOverdue()" and it also helps during the background job/service to query for all protocols that are "overdue" and process the <em>Monthly</em> or <em>Yearly</em> entry. I reused those fields in the new solution.</p>

<p>Because the <strong>Protocol</strong> can have thousands of <strong>Protocol Entries</strong> during a month and even more during a year, i can not load all of those in the Aggregate root every time i load the <strong>Protocol</strong> which seems to be ok (i read that in some other posts etc.) as long as the <strong>Protocol</strong> has no requirement on those (Like a Customer AR must not have all Orders all the time, if there is no requirement that a Customer is not allowed to have only 5 Orders at a time for example).</p>

<p><strong>Problem</strong></p>

<p>How is it possible to don't load all that entries with every protocol and keep the behavior like checking if its allowed to add the entry to the protocol (which i am sure its related to the protocol) because it must update the (row) version of the protocol and also the Next(Monthly|Yearly)Entry fields when an entry is added to ensure consistency and be aware of concurrency issues.</p>

<p>When my <strong>Protocol</strong> gets a private field called <strong>AddedEntries</strong> which gets populated with new entries. Since entries are never edited/deleted its ok to only track those. So i can add one or more entries and ensure consistency and validate rules. Seems good and ok for me from the Domain and DDD side, but now at persistence, how to add those <em>new</em> entries to the database? I cannot just update the protocol with the collection, because that will delete existing entries that are not in the collection (EF). Is it the responsibility of the repository (ProtocolRepository.Update(protocol)) to add entries to the depending table if there are any entries?</p>

<p>Sorry for the long question and may be not perfect title (didn't know how to summarize that in a few words). I am new with DDD and that problem makes me crazy and i am also sorry if not everything is totally correct - i am still learning. Thank you all in advance for your time care and thinking about my problem!</p>

## Answers
### Answer ID: 49235441
<p>Before going to actual implementation, you need to think about the invariants and shape your model accordingly.</p>

<ul>
<li><p>Identify which data is needed to enforce invariants when adding an <code>Entry</code> and find a meaningful name for it in your Ubiquitous Language (is it <code>MonthlyProtocolEntry</code>?)</p></li>
<li><p>Can you load that thing as part of the Aggregate without performance problems?</p>

<ul>
<li>Yes: make it an Entity in the Aggregate.</li>
<li>No: see with your domain expert if you can use Eventual Consistency to enforce the rule and make it a separate Aggregate.</li>
</ul></li>
</ul>

<p>Your problem here might be overgeneralization - seeing everything as just another <code>ProtocolEntry</code> prevents you from thinking about all possible designs, especially ones with more specialized, fine-grained parts.</p>

### Answer ID: 49232902
<p>If you want to work with a lot of children, check the work of Vaughn Vernon and particularly his work on Calendar and CalendarEntry. Its in Java but looks very similar to you:</p>

<p><a href="https://github.com/VaughnVernon/IDDD_Samples/tree/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar" rel="nofollow noreferrer">https://github.com/VaughnVernon/IDDD_Samples/tree/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar</a></p>

<p>Notice how the relation is made, Calendar never own any CalendarEntry, instead the CalendarEntry references the CalendarId.</p>

<p><a href="https://github.com/VaughnVernon/IDDD_Samples/blob/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar/Calendar.java" rel="nofollow noreferrer">https://github.com/VaughnVernon/IDDD_Samples/blob/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar/Calendar.java</a></p>

<p><a href="https://github.com/VaughnVernon/IDDD_Samples/blob/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar/CalendarEntry.java" rel="nofollow noreferrer">https://github.com/VaughnVernon/IDDD_Samples/blob/master/iddd_collaboration/src/main/java/com/saasovation/collaboration/domain/model/calendar/CalendarEntry.java</a></p>

<p>When you work on the Calendar or CalendarEntry, the application service is responsible of loading the set you want to work on, make the object interact, and persist them. That way, you have more control over granularity, if you need only the subset of entry for the current month, there is no need of loading the full aggregate, improving performances and memory footprint.</p>

<p>Remember DDD is all about tailor made.</p>

<p>So in your repository, you might have methods such as: </p>

<ul>
<li>(load)entriesForCurrentMonth</li>
<li>(load)entriesForNextMonth</li>
</ul>

<p>And work with them, then save them.</p>


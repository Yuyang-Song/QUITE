# Possible issue with fetchLimit and fetchOffset in a Core Data query
[Link to question](https://stackoverflow.com/questions/10725252/possible-issue-with-fetchlimit-and-fetchoffset-in-a-core-data-query)
**Creation Date:** 1337795409
**Score:** 11
**Tags:** objective-c, ios, core-data
## Question Body
<p>I have a very sporadic bug with a Core Data query containing fetchLimit and fetchOffset. Once in a long while (I've seen it happen once, as has another tester), the fetchOffset seems to be ignored. The query looks like this: </p>

<pre><code>NSFetchRequest *fetch = [[NSFetchRequest alloc] initWithEntityName:@"MyEntity"];
NSSortDescriptor *dateDescriptor = [[NSSortDescriptor alloc] initWithKey:@"timestamp" ascending:NO];
NSArray *sortDescriptors = [NSArray arrayWithObject:dateDescriptor];
[fetch setSortDescriptors:sortDescriptors];

fetch.fetchOffset = 500;
fetch.fetchLimit = 1;

NSError *error = nil;
NSArray *objects = [self.managedObjectContext executeFetchRequest:fetch error:&amp;error];
if (objects.count) {
    MyEntity *objectAtLimit = [objects objectAtIndex:0];
}
</code></pre>

<p>This almost always returns the 501st object as desired, but on those two occasions where it broke it returned the first object. </p>

<p>The query is never run unless there are >500 rows in the database. I'm using iOS5. The managedObjectContext has a mainQueueConcurrencyType. </p>

<p>It seems to be the same behavior as reported in this question: <a href="https://stackoverflow.com/questions/7955486/paging-results-from-core-data-requests">Paging results from Core Data requests</a>, which was never resolved (or at least not on list.) In that case the fetchOffset appeared to be either ignored or respected based on the data model being tested against. </p>

<p>I'm probably going to rewrite the query without the fetchOffset, just in case that is the problem, since the performance shouldn't be an issue. But I'm wondering if anyone has thoughts about where the bug might be here. </p>

## Answers
### Answer ID: 66843162
<p>The problem indeed seems the be connected with unsaved changes in the NSManagedObjectContext. If you set the <a href="https://developer.apple.com/documentation/coredata/nsfetchrequest/1506724-includespendingchanges" rel="nofollow noreferrer">includesPendingChanges</a> property to <code>false</code> the NSFetchRequest with limit + offset will work as expected.</p>
<pre><code>fetchRequest.includesPendingChanges = false
</code></pre>

### Answer ID: 15681043
<p>Ran across a similar problem this morning and noticed if my NSManagedObjectContext has unsaved changes that the fetchOffset may be ignored for whatever reason. After saving the context the fetchOffset is interpreted correctly.</p>


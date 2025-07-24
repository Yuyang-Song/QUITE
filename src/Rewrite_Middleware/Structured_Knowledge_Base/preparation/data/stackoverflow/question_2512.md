# hooks causing issues with insert using subqueries
[Link to question](https://stackoverflow.com/questions/37882485/hooks-causing-issues-with-insert-using-subqueries)
**Creation Date:** 1466169117
**Score:** 0
**Tags:** orientdb
## Question Body
<p>I'm not sure why this is causing me an issue, but I'm using Orient 2.1.19, found this in 2.1.12 as well.  We are building some hooks to implement a method of encryption.  I know 2.2 implements some encryption, but we had some further requirements.  </p>

<p>Anyway, we have hooks for onRecordAfterRead, onRecordBeforeCreate and onRecordBeforeUpdate.  It works for most statements fine, but with the hook in place, running a query that sets a link property using a subquery in an insert fails. Here's an example query:</p>

<pre><code>create EDGE eThisEdge from (select from vVertex where thisproperty = 'this') to (select from vVertex where thatProperty = 'that' ) set current = (select from lookupCurrent where displayCurrentPast = 'Current');
</code></pre>

<p>Runnning this query gives me the error:</p>

<p>com.orientechnologies.orient.core.exception.OValidationException: The field 'eThisEdge.current' has been declared as LINK but the value is not a record or a record-id.</p>

<p>It's some issue with the way a subquery is ran during just an insert though, because if I run the insert without setting any properties, then run an update to set the properties, that works.  I'd hate to have to rewrite all of our inserts for our base data and our coding just as a work around for this, and it seems like I'm just missing something here.  </p>

<p>Has anyone seen this kind of issue with hooks as well?</p>

<p>The biggest issue seems to be surrounding the onRecordBeforeCreate code.  We are trying to have a generic hook that encrypts strings in our database.  Here's the basics of the onRecordBeforeCreate method:</p>

<pre><code>    public RESULT onRecordBeforeCreate( ODocument oDocument) {

    RESULT changed = RESULT.RECORD_NOT_CHANGED;
    try {
        if(classIsCipherable(oDocument)) {
            for (String field : oDocument.fieldNames()) {
                if (oDocument.fieldType(field) != null &amp;&amp; oDocument.fieldType(field) == OType.STRING &amp;&amp; oDocument.field(field) != null) {
                    oDocument.field(field, crypto.encrypt(oDocument.field(field).toString()));
                    changed = RESULT.RECORD_CHANGED;
                }
            }
        }
        return changed;
    } catch (Exception e) {
        throw new RuntimeException( e );
    }
</code></pre>

<p>Is there anything there that looks obvious that I'd have issues with running a create edge statement that sets properties with a property that is a link?  </p>

## Answers
### Answer ID: 37882940
<p>The query <code>select from lookupCurrent where displayCurrentPast = "Current"</code> return more than one element, you must use a LinkList or a LinkSet</p>


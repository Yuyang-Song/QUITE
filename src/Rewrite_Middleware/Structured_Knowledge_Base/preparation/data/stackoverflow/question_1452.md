# Replicating PostgreSQL manually: can I ensure a user&#39;s queries are always deterministic?
[Link to question](https://stackoverflow.com/questions/76920584/replicating-postgresql-manually-can-i-ensure-a-users-queries-are-always-determ)
**Creation Date:** 1692267470
**Score:** -1
**Tags:** postgresql, distributed-system
## Question Body
<p>I'm wondering whether it's feasible to run several PostgreSQL database instances, initialized from an empty state, and manually keep them in sync by applying the same sequence of queries on them. Basically, my question is: what is the (inherent) level of non-determinism in queries, and is there a way to restrict that?</p>
<p>One obvious source of non-determinism are functions such as RANDOM() or datetime functions that access the current system time. Would I be able to restrict a user from executing those built-in functions?</p>
<p>PostgreSQL already has the concept of <a href="https://www.postgresql.org/docs/current/xfunc-volatility.html" rel="nofollow noreferrer">VOLATILE functions</a>. Does this also apply to built-ins, and can I revoke access based on that pattern?</p>
<p>For context, I'm trying to build something like <a href="https://github.com/rqlite/rqlite" rel="nofollow noreferrer">rqlite</a>, which implements SQLite on top of the Raft consensus protocol. They rewrite queries such that the output of a RANDOM() call will be manually synchronized between the servers. For my purposes, I don't need that type of mechanism (I suspect it'd be a lot more complex in PostgreSQL anyway), and I'd rather just get rid of all non-deterministic functions.</p>

## Answers
### Answer ID: 76920800
<p>Broadly speaking, you would want to have an allowed list of operations and functions rather than trying to exclude them. As you spotted this rules out anything that accesses the environment (time, randomness etc) unless you also sync that environment. Consider also any per-session/user <code>SET</code> options.</p>
<p>You will also need to disallow any queries that don't have a fully-specified sort order. If you are processing the &quot;first N people by name&quot; and two people have the same name two instances could return differing results. This applies to any sub-queries too of course.</p>
<p>Finally you will need very precise control over concurrency. You can't reproduce a set of queries on multiple nodes without knowing what order they started and finished in.</p>
<p>If you allow installation of extensions or custom functions you will want to audit those too.</p>
<p>You may want to lean on the two-phase-commit protocol to try and ensure all servers commit or rollback.</p>
<p><a href="https://www.postgresql.org/docs/16/two-phase.html" rel="nofollow noreferrer">https://www.postgresql.org/docs/16/two-phase.html</a></p>


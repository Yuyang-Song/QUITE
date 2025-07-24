# How to refresh data in the Prism Framework
[Link to question](https://stackoverflow.com/questions/13847658/how-to-refresh-data-in-the-prism-framework)
**Creation Date:** 1355342585
**Score:** 1
**Tags:** .net, wpf, mvvm, prism, design-patterns
## Question Body
<p>I'm rewriting an app to be based on Prism. It was based on WAF, and it uses the Entity Framework to access data via the unit of work / repository pattern.</p>

<p>I'm intending to use the event aggregator to inform my view models when a new unit of work is available (eg, after a save). They can then replace the model objects they are presenting with the new equivalents from the new unit of work.</p>

<p>1.) Is this a reasonable idea? How else could I inform my view models that they are showing out of date information?</p>

<p>I only want to have the view models that are visible re-query the database. ViewModels that are not currently shown can delay their refresh until they are shown (I'm planning to do this using the INavigationAware interface).</p>

<p>2.) Again, is this a reasonable way to proceed? How can I distinguish between view models that are currently visible to the user, and those that are not?</p>

<p>As an alternative solution to 2.), I'm considering creating views only as needed, and destroying them immediately when they are hidden. This would solve the "which view models are visible" question, but seems very expensive.</p>

<p>3.) Is Prism intended to be used in this manner?</p>

## Answers
### Answer ID: 13847961
<blockquote>
  <p>1.) Is this a reasonable idea? How else could I inform my view models that they are showing out of date information?</p>
</blockquote>

<p>This boils down to dealing with dirty data be it needing <em>saved</em> or needing <em>refreshed</em>. One way to solve this is that the ViewModel pulls its data from a Service, which would allow the data to get refreshed on demand.</p>

<blockquote>
  <p>2.) Again, is this a reasonable way to proceed? How can I distinguish between view models that are currently visible to the user, and those
  that are not?</p>
</blockquote>

<p>If you are going to also leverage IoC and DI via CI, the ViewModel should exist as needed and get injected into the View at runtime upon construction. To manage state and persistence of data, you should leverage the a Service for that. </p>

<blockquote>
  <p>3.) Is Prism intended to be used in this manner?</p>
</blockquote>

<p>Prism is a buffet of services; Prism is not a single offering. The <code>EventAggregator</code> is to be used for cross module communication. If your communication is spanning modules, yes this would serve well to use. If the communication is internal, simple eventing would suffice.</p>

<p>The concept of visible will depend on your application. <code>IActiveAware</code> is simply an interface, not the implementation. If your application was structured in a tabular manner, <code>IActiveAware</code> would serve well in that environment. Again, implementation details are important in how you use the interface but are driven by application structure.</p>

### Answer ID: 13847866
<p>Ah, sorry - I think I've found a large part of the answer to my question.</p>

<p>I didn't know about the IActiveAware interface (http://compositewpf.codeplex.com/discussions/277463) which seems to quite nicely solve the problem of determining which view models are visible.</p>

<p>I'm still interested in how to inform them that new data is available, but I'd understand if the question doesn't have enough left anymore and needs deleting.</p>


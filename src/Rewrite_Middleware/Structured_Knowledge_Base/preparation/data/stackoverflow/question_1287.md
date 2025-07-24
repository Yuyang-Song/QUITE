# Grails 4 Testing: Implementing ServiceUnitTest &amp; DataTest on the same Spock Specification
[Link to question](https://stackoverflow.com/questions/68350695/grails-4-testing-implementing-serviceunittest-datatest-on-the-same-spock-spec)
**Creation Date:** 1626106667
**Score:** 0
**Tags:** grails, grails-orm, spock
## Question Body
<p>I'm upgrading a Grails 2.4.4 application, and some of the unit tests use database interactions that rely on <code>{DomainObject}.save(validate: false)</code> (to avoid creating all the domain object's required associations). In some cases, rewriting the test will not be possible.</p>
<p>Implementing <code>ServiceUnitTest</code> alone didn't allow me to call <code>mockDomain</code> because <code>ServiceUnitTest</code> doesn't implement <code>DataTest</code>, so I implemented <code>DataTest</code> as well.</p>
<p>My questions are:</p>
<ol>
<li><strong>Short term:</strong> Are there any foreseeable problems with implementing <code>ServiceUnitTest</code> and <code>DataTest</code> on the same Spec?</li>
<li><strong>Long term:</strong> Is the general best practice to replace dynamic finders and criteria queries in the services and controllers with calls to GORM data services, which look like they can be mocked using convention Spock mocking?</li>
</ol>

## Answers
### Answer ID: 68352259
<blockquote>
<p>Are there any foreseeable problems with implementing ServiceUnitTest
and DataTest on the same Spec?</p>
</blockquote>
<p>No.  We designed the traits to work together like that.</p>
<blockquote>
<p>Is the general best practice to replace dynamic finders and criteria
queries in the services and controllers with calls to GORM data
services, which look like they can be mocked using convention Spock
mocking?</p>
</blockquote>
<p>Yes.  Most dynamic finder and criteria queries would be better suited to be implemented as GORM Data Service instances.</p>


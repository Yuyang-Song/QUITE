# Is there a way to add a where clause on a Select within a Select - I need to reduce the amount of JSON returned
[Link to question](https://stackoverflow.com/questions/56107241/is-there-a-way-to-add-a-where-clause-on-a-select-within-a-select-i-need-to-red)
**Creation Date:** 1557731072
**Score:** 1
**Tags:** c#, entity-framework, lambda
## Question Body
<p>This question is about trying to make my code return a smaller amount of results to make the solution more efficient by adding a where on my Selects or rewriting the query entirely.</p>

<p>N.B. This is using C# .NET Framework 4.7.2. (We haven't moved to Core yet).</p>

<p>I have the following entities: PERSON, PERSON_TYPE, COINS &amp; FINANCIAL_YEAR.</p>

<ul>
<li>A PERSON has a PERSON_TYPE (One to Many),   </li>
<li>A PERSON has Many COINS (Left side of Many-to-Many),   </li>
<li>COINS has Many FINANCIAL_YEARS (Right Side of Many to Many)</li>
</ul>

<p>(A person can also have one or more offices which I have left in for completeness).</p>

<p>E.g. A Person can have a set of coins 10 for 2016, 29 for 2017, 37 for 2018 etc</p>

<p>I get results returned but in trying to filter the results for a specific year, I get all COINS returned but with only the 'FINANCIAL YEAR' I want lazy loaded.</p>

<p>I have tried the following code query</p>

<pre><code>    var persons = appCoreDBContext.PersonRepository.GetAll()
                  .Where(p =&gt; p.Active.Equals(true))
                  .Select(pl =&gt; new
                  {
                     pl,
                     PersonLocs = pl.PersonLocations.Where(ed =&gt; ed.EndDate != null)
                     .Select(o =&gt; new
                     {
                         o,
                         office = o.Office
                     }),
                     PersonType = pl.PersonType,
                     PersonCoins = pl.PersonCoins
                     .Select(yr =&gt; new
                     {
                         yr,
                         finYear = yr.FinancialYear
                     })
                     .Where(ee =&gt; ee.finYear.StartDate.Year == DateTime.Now.Year)
                  })
                  .AsEnumerable()
                  .Select(x =&gt; x.pl);
</code></pre>

<p>So this returns the following results in JSON</p>

<pre><code>[
  {
    "id": 1,
    "lastModifiedDate": "2019-05-09T11:47:10.193",
    "active": true,
    "firstName": "Fred",
    "lastName": "Flintstone",
    "title": "Mr",
    "email": "fred.flintstone@slaterockandgravel.com",    
    "personTypeId": 2,
    "personType": {
      "id": 2,
      "name": "Blue-Collar"
    },
    "personCoins": [
      {
        "id": 118,
        "lastModifiedDate": "2019-05-12T23:01:33.1566667",
        "active": true,
        "fullYearValue": 102.0,        
        "personId": 1,        
        "financialYearId": 19,
        "financialYear": {
          "id": 19,
          "lastModifiedDate": "2019-04-30T15:33:20.05",
          "active": true,
          "startDate": "2019-05-01T00:00:01",
          "endDate": "2020-04-30T00:00:00",
          "label": "FY 2019/2020"
        }
      },
      {
        "id": 1,
        "lastModifiedDate": "2019-04-29T07:49:41.367",
        "active": true,
        "fullYearValue": 85.0,        
        "personId": 1,        
        "financialYearId": 3,
        "financialYear": null
      },
      {
        "id": 2,
        "lastModifiedDate": "2019-04-29T07:50:14.747",
        "active": true,
        "fullYearValue": 65.0,        
        "personId": 1,        
        "financialYearId": 2,
        "financialYear": null
      },
      {
        "id": 3,
        "lastModifiedDate": "2019-04-29T07:50:41.307",
        "active": true,
        "fullYearValue": 45.0,        
        "personId": 1,        
        "financialYearId": 1,
        "financialYear": null
      },
      {
        "id": 109,
        "lastModifiedDate": "2019-05-09T18:02:34.52",
        "active": true,
        "fullYearValue": 100.0,        
        "personId": 1,        
        "financialYearId": 20,
        "financialYear": null
      },
      {
        "id": 112,
        "lastModifiedDate": "2019-05-09T19:00:09.787",
        "active": true,
        "fullYearValue": 101.0,        
        "personId": 1,       
        "financialYearId": 21,
        "financialYear": null
      },
      {
        "id": 115,
        "lastModifiedDate": "2019-05-09T19:04:15.853",
        "active": true,
        "fullYearValue": 101.0,        
        "personId": 1,       
        "financialYearId": 22,
        "financialYear": null
      }
    ],
    "personLocations": [
      {
        "id": 1,
        "lastModifiedDate": "2019-04-25T10:19:07.193",
        "active": true,
        "startDate": "2018-10-29T09:00:00",
        "endDate": null,
        "office": {
          "id": 2,
          "lastModifiedDate": "2019-04-25T10:16:37.9533333",
          "active": true,
          "name": "Bedrock",
          "address1": "The Quarry",
          "address2": "Bedrock",
          "address3": "Prehistorica",
          "zipcode": "YabbaDabbaDoo",
          "openingDate": "1992-06-01T09:00:00",
          "closingDate": null,
          "officialCurrencyId": 1,
          "officialCurrency": null,
          "countryId": 1,
          "country": null
        }
      }
    ]
  }
]

</code></pre>

<p>As you can see above, I do get the financial year information for the year I want 2019, but I also get all other COIN data for the other financial years that I don't want which makes the response larger. </p>

<p>What I want, so I can make this result set more efficient, is that my returning results look like</p>

<pre><code>    [
  {
    "id": 1,
    "lastModifiedDate": "2019-05-09T11:47:10.193",
    "active": true,
    "firstName": "Fred",
    "lastName": "Flintstone",
    "title": "Mr",
    "email": "fred.flintstone@slaterockandgravel.com",    
    "personTypeId": 2,
    "personType": {
      "id": 2,
      "name": "Blue-Collar"
    },
    "personCoins": [
      {
        "id": 118,
        "lastModifiedDate": "2019-05-12T23:01:33.1566667",
        "active": true,
        "fullYearValue": 102.0,        
        "personId": 1,        
        "financialYearId": 19,
        "financialYear": {
          "id": 19,
          "lastModifiedDate": "2019-04-30T15:33:20.05",
          "active": true,
          "startDate": "2019-05-01T00:00:01",
          "endDate": "2020-04-30T00:00:00",
          "label": "FY 2019/2020"
        }
      }
    ],
    "personLocations": [
      {
        "id": 1,
        "lastModifiedDate": "2019-04-25T10:19:07.193",
        "active": true,
        "startDate": "2018-10-29T09:00:00",
        "endDate": null,
        "office": {
          "id": 2,
          "lastModifiedDate": "2019-04-25T10:16:37.9533333",
          "active": true,
          "name": "Bedrock",
          "address1": "The Quarry",
          "address2": "Bedrock",
          "address3": "Prehistorica",
          "zipcode": "YabbaDabbaDoo",
          "openingDate": "1992-06-01T09:00:00",
          "closingDate": null,
          "officialCurrencyId": 1,
          "officialCurrency": null,
          "countryId": 1,
          "country": null
        }
      }
    ]
  }
]

</code></pre>

<p>E.G. It 'just' returns the Coin data for the specified year.</p>

<p>As I am displaying this data in a paginated JQuery Datatable I get all the results back at once and I have 5000 people in the database which therefore returns a really large JSON file. </p>

<p>Is there a way in which I can add a Where clause on this query within the sub selects, or another way of getting the data out which will be more efficient. </p>

<p>Any help gratefully received.</p>

## Answers
### Answer ID: 56123235
<p>The issue is that you are trying to sub-filter data, but then at the end you are selecting, and serializing the complete Person entity and all of it's related entities using the <code>.Select(x =&gt; x.pl)</code></p>

<p>Give this a try:</p>

<pre><code>.Select(pl =&gt; new PersonViewModel
{
    pl.id,
    pl.lastModifiedDate,
    pl.active,
    pl.firstName,
    pl.lastName,
    pl.email,
    pl.personType.Select(pt =&gt; new PersonTypeViewModel
    {
       pt.id,
       pt.name
    }),             
    personLocs = pl.PersonLocations.Where(ed =&gt; ed.EndDate != null)
        .Select(o =&gt; new PersonLocationViewModel
        {
           id = o.OfficeId,
           office = o.Office
        }),
    personCoins = pl.PersonCoins
       .Select(yr =&gt; new PersonCoinViewModel
       {
           finYear = yr.FinancialYear
       })
       .Where(ee =&gt; ee.finYear.StartDate.Year == DateTime.Now.Year)
 }).AsEnumerable();
</code></pre>

<p>You will need to define view models for the data structure you want to send back since I don't believe you can return/serialize anonymous types.</p>

<p>Essentially just select the fields and related data that you want <em>without</em> selecting the entities. You should avoid returning entities, including referencing entities inside a returned DTO/ViewModel because this will include serializing all data and related data available in the entity. This can trigger lazy loads (performance issues) and sends far more data to the client than you need to, or would wish to expose to potentially malicious users.  </p>

### Answer ID: 56108905
<p>At a quick glance, you could just add a where clause to the financial year section:</p>

<pre><code>var persons = appCoreDBContext.PersonRepository.GetAll()
              .Where(p =&gt; p.Active.Equals(true))
              .Select(pl =&gt; new
              {
                 pl,
                 PersonLocs = pl.PersonLocations.Where(ed =&gt; ed.EndDate != null)
                 .Select(o =&gt; new
                 {
                     o,
                     office = o.Office
                 }),
                 PersonType = pl.PersonType,
                 PersonCoins = pl.PersonCoins
                 .Where(yr =&gt; yr.FinancialYear != null)
                 .Select(yr =&gt; new
                 {
                     yr,
                     finYear = yr.FinancialYear
                 })
                 .Where(ee =&gt; ee.finYear.StartDate.Year == DateTime.Now.Year)
              })
              .AsEnumerable()
              .Select(x =&gt; x.pl);
</code></pre>


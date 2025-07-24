# Why is Filterrific Search in Production on Heroku add-on db not working?
[Link to question](https://stackoverflow.com/questions/77059919/why-is-filterrific-search-in-production-on-heroku-add-on-db-not-working)
**Creation Date:** 1694092194
**Score:** 0
**Tags:** ruby-on-rails, ruby, heroku-postgres, filterrific
## Question Body
<p>I use the filterrific gem (currently 5.2.3) a lot for my Rails apps and love it. I have run into a weird problem. I have a secondary Postgres database for my dev team to write to as an additional add-on in Heroku. My filterrific setup works great for all my scope filters in production but the search returns errors. Everything works perfectly in Development with my SQL seed data.</p>
<p><strong>Model.rb</strong></p>
<pre><code>filterrific(
   default_filter_params: { },
   available_filters: [
     :sorted_by,
     :with_search_please,
     :with_manufacturer,
     :with_boot_type,
     :with_firm,
     :with_monitor_count,
     :with_ethernet_count,
   ],
 )

scope :with_search_please, -&gt;(search_string) {
  return nil  if search_string.blank?
  terms = search_string.to_s.downcase.split(/\s+/)
  terms = terms.map { |e|
      #('%' + e + '%').gsub(/%+/, '%')
      ('%' + e.gsub('*', '%') + '%').gsub(/%+/, '%')
    }
  num_or_conds = 6
  self.where(
      terms.map { |term|
        &quot;(
        LOWER(Terminals.Model) LIKE ?
        OR LOWER(Terminals.TermcapModel) LIKE ?
        OR LOWER(Manufacturers.Name) LIKE ?
        OR LOWER(TerminalType.Type) LIKE ?
        OR LOWER(Note.Description) LIKE ?
        OR LOWER(FirmwarePackage.Version) LIKE ?
        )&quot;
      }.join(' AND '),
      *terms.map { |e| [e] * num_or_conds }.flatten
    )
    .joins(:Manufacturers).references(:ManufacturerIds)
    .joins(:TerminalType).references(:TypeIds)
    .includes(:Notes).references(:TerminalIds)
    .joins(:FirmwarePackages).references(:TerminalFirmwarePackages)
}
</code></pre>
<p><strong>Log Error</strong></p>
<pre><code>Completed 500 Internal Server Error in 15ms (ActiveRecord: 3.2ms | Allocations: 6057)
2023-09-07T12:56:11.955033+00:00 app[web.1]: F, [2023-09-07T12:56:11.954949 #2] FATAL -- : [9e6cf5c0-457c-47aa-9099-a5923e41b1ce]
2023-09-07T12:56:11.955035+00:00 app[web.1]: [9e6cf5c0-457c-47aa-9099-a5923e41b1ce] ActionView::Template::Error (PG::UndefinedTable: ERROR:  missing FROM-clause entry for table &quot;terminals&quot;
2023-09-07T12:56:11.955035+00:00 app[web.1]: LINE 2:         LOWER(Terminals.Model) LIKE '%a%'
2023-09-07T12:56:11.955036+00:00 app[web.1]: ^
</code></pre>
<p>I have tried several ways of rewriting the search query, stripping out conditions and even just a straight SQL query.  This is particularly difficult as everything works flawlessly in Development and all the filtering scopes work in Production. I know it must have to do with the secondary add-on db as I have never run in to this before.</p>

## Answers
### Answer ID: 77061151
<p>Your issue is that the &quot;terminals&quot; table is not part of the query.</p>
<p>Also please note Postgres double quoted identifiers are case sensitive e.g. &quot;Terminals&quot; v &quot;terminals&quot;.</p>
<p>If you post the entire query as well as some context as to where this code block is defined we may be able to assist with that.</p>
<p>All that being said I would also like to take the opportunity to help you clean up that query a bit as it seems very awkward, IMO.</p>
<p>From the post it appears that your intent is to find: &quot;A Record where every word in the search string is contained in one of the following columns Terminals.Model, Terminals.TermcapModel, Manufacturers.Name, TerminalType.Type, Note.Description, FirmwarePackage.Version&quot;.</p>
<p>We can achieve this in a simpler fashion (and possibly solve your issue in the process) as follows:</p>
<pre><code>scope :with_search_please, -&gt;(search_string) {
  return none if search_string.blank? # A scope should not return nil

  search_columns = [
    Terminal.arel_table[:Model],
    Terminal.arel_table[:TermcapModel],
    Manufacturer.arel_table[:Name],
    TerminalType.arel_table[:Type],
    Note.arel_table[:Description],
    FirmwarePackage.arel_table[:Version]
  ]

  terms = search_string.to_s
          .gsub(&quot;*&quot;,&quot;%&quot;)
          .split
          .map {|term| &quot;%#{term}%&quot;}

  where(search_columns.map {|c| c.matches_any(terms)}.reduce(:and))
    .joins(:Manufacturers)
    .joins(:TerminalType)
    .left_joins(:Notes)
    .joins(:FirmwarePackages)
}
</code></pre>
<p>As an example, with a search_string of &quot;A Sun*ny Day&quot; this will result in a WHERE CLAUSE similar to</p>
<pre><code>(Terminals.Model ILIKE '%A%' OR Terminals.Model ILIKE '%Sun%ny%' OR Terminals.Model ILIKE '%Day%') AND 
(Terminals.TermcapModel ILIKE '%A%' OR Terminals.TermcapModel ILIKE '%Sun%ny%' OR Terminals.TermcapModel ILIKE '%Day%') AND 
(Manufacturers.Name ILIKE '%A%' OR Manufacturers.Name ILIKE '%Sun%ny%' OR Manufacturers.Name ILIKE '%Day%') AND 
(TerminalType.Type ILIKE '%A%' OR TerminalType.Type ILIKE '%Sun%ny%' OR TerminalType.Type ILIKE '%Day%') AND 
(Note.Description ILIKE '%A%' OR Note.Description ILIKE '%Sun%ny%' OR Note.Description ILIKE '%Day%') AND 
(FirmwarePackage.Version ILIKE '%A%' OR FirmwarePackage.Version ILIKE '%Sun%ny%' OR FirmwarePackage.Version ILIKE '%Day%')
</code></pre>
<p>We could take this a bit further with Full Text Search as well.</p>


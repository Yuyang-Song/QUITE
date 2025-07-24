# Displaying entity-attribute-value data in JTable?
[Link to question](https://stackoverflow.com/questions/1039694/displaying-entity-attribute-value-data-in-jtable)
**Creation Date:** 1245863293
**Score:** 1
**Tags:** java, swing, jdbc, jtable
## Question Body
<p>How can I use a JTable to display &amp; edit attribute properties for entities retrieved from an entity,attribute,value (EAV) store (a relational DBMS)? </p>

<p>I know this is a question with a lot of possible answers, so PLEASE <strong>look at the requirements I have below before answering.</strong>  </p>

<p>I promise to vote up answers that show you've read &amp; understand the whole thing (as long as they aren't totally silly).  </p>

<hr>

<p><strong>The user needs to be able to:</strong></p>

<ol>
<li><p>Filter/Search entities by their attributes</p></li>
<li><p>Choose which attributes to show (as columns)</p></li>
<li><p>Sort entities by chosen attributes</p></li>
<li><p>Edit attribute values </p></li>
<li><p>Do operations on selected entities</p></li>
<li><p><em>(Optional)</em> Ability to save view for later use.</p></li>
</ol>

<hr>

<p><strong>System Requirements:</strong></p>

<ol>
<li><p>Number of entities: needs to scale up to 100K+ unique entities</p></li>
<li><p>Attributes: user can add and define new attributes, system should be able to handle this</p></li>
<li><p>Underlying Storage: H2 Database (already designed), communicating by JDBC</p></li>
<li><p>Memory: not everything will fit, so somehow needs to pull from DBMS queries</p></li>
<li><p>Performance: should minimize number of queries needed to DBMS (one query per attribute OK, and I have a form with 1 query per table view, but it sucks).</p></li>
<li><p>Queries: ONE query should be required to generate list of entities matching a search/filter.  Otherwise massive performance suck.</p></li>
<li><p>Reusing data: shouldn't have to re-query or re-sort the entire list when column is added.  </p></li>
</ol>

<hr>

<p><strong>Things I've looked at:</strong></p>

<ol>
<li><p>Glazed Lists library </p>

<ul>
<li><p>Pros:</p>

<ul>
<li>Flexible about column handling</li>
<li>Easy to implement sort/filter of entities</li>
<li>Flexible about column display format &amp; editing</li>
</ul></li>
<li><p>Cons:</p>

<ul>
<li>One object per entity (if objects are complex, memory overhead becomes a serious memory problem!)</li>
<li>Object responsible for all functionality... but objects should be simple for memory reasons</li>
<li>How do I support user-selectable columns without a HashMap for EVERY entity object?</li>
</ul></li>
</ul></li>
<li><p>Extending AbstractTableModel to map data from a JDBC ResultSet to rows,columns</p>

<ul>
<li>Pros:

<ul>
<li>Paging of results avoids memory problem</li>
<li>Searching/Filtering is directly in SQL</li>
<li>Memory-friendly, doesn't have to make an object per-row</li>
</ul></li>
<li>Cons:

<ul>
<li>Implementing custom columns &amp; sorting is a pain (table header renderer, managing sort columns and order, etc)!</li>
<li>Probably have to write custom JTableColumnModel too, and this gets messy!</li>
<li>Has to manipulate SQL a lot, so if DB schema changes, have to rewrite multiple pieces of code!</li>
<li>Hard to maintain entity ID info</li>
</ul></li>
</ul></li>
<li><p>ORM</p>

<ul>
<li>Pros:

<ul>
<li>Designed to map DB rows to objects</li>
<li>Provides object management</li>
</ul></li>
<li>Cons:

<ul>
<li>WORST POSSIBLE solution for entity-attribute-value model</li>
<li>Have to learn &amp; write ORM code in addition to DBMS &amp; Java code!</li>
<li>Entities can have <em>any</em> number of attributes, ORM is only good with static, limited object attributes</li>
<li>Lose flexibility/speed of custom SQL</li>
</ul></li>
</ul></li>
</ol>

<hr>

<p><strong>Is there a better option that I missed, or some clever way to make Glazed Lists or custom Table Model easier?</strong></p>

<p>I've totally discarded ORM as an option already, because of how badly matched it is to EAV storage.  </p>

## Answers
### Answer ID: 1039766
<p>I think your best option is to go with 'Extending AbstractTableModel with form map data from a JDBC ResultSet' because</p>

<ul>
<li>Java 6 JTable has built in sorting support so you don't really need to implement that.</li>
<li>If you design your model carefully, you could survive some schema changes. Code clearly to allow yourself to make changes easier if you need.</li>
<li>You'll have to write back changes anyway. Use a 'Save' button and batch update might even help your performance.</li>
<li>You can override TableCellEditor to supply combobox instead of the default text editor.</li>
<li>Don't try to do all edit in one table. Have separated means for entry creation etc.</li>
<li>You can add/remove columns to JTable at runtime. Just fireTableModelChanged() and the new column becomes visible</li>
</ul>

<p><strong>Edit:</strong> One crazy thing I would do to create a custom component and do all rendering myself and perform the edit operations with well placed JTextField and JComboBox.</p>

<p><strong>Edit2:</strong> Based on your comment.
Save the position of the selected item before you do the fire...() call. Btw, I don't think the call resets the sorting or the selection - had no problem with that. </p>

<p>If you add a column, you could just fetch the key field and the values for the new column only. Display them in the column. Then do a hidden complete reload in the background and swap the model to that when it is finished. This is practically working from multiple ResultSets at the same time in one table.</p>

<p>Removing is easy as you don't show the values for that column. </p>

<p><strong>Edit3:</strong></p>

<p>DefaultRowSorter isn't that deep. It maintains a reindexing table for your records. So when JTable asks for the 10th row, the rowsorter checks its 10th entry of the index table and retrieves that indexth element from your actual model. </p>

<p>Also if you have lots of identical strings in your model use a simple Map of String to String cache when you query the data from the database. This way the tons of redundant String objects can be GC-d right away.</p>

<p><strong>Edit4:</strong></p>

<p>I would query the new field into a Map of key to value and have my primary model contain a list of map of key to value. Then I would use a getValue() implementation which returns the value from either the primary data source of from these additional maps on demand. I would lookup the row's key from the primary model and use that to retrieve the actual value from the additional maps. (Btw. Reputation gained from accepted answers are not subject to the daily limit.)</p>


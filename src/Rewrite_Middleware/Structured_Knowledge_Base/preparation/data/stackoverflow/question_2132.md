# Liquibase, create foreign keys in Oracle, preconditions
[Link to question](https://stackoverflow.com/questions/20148318/liquibase-create-foreign-keys-in-oracle-preconditions)
**Creation Date:** 1385133617
**Score:** 2
**Tags:** java, sql, database, oracle-database, liquibase
## Question Body
<p>I have a production and a QA instance of my application into which I'm integrating Liquibase. This means DDL and data already exists (or not if on development box). I have to create a changeLog which records everything as RAN on the non-empty DBs but execute actually on empty DBs.
I'm on a good way but I'm a bit stuck with creating the foreign keys. (the database is Oracle).</p>

<p>(In general I'm creating preconditions which expects various objects to NOT exists and on fail MARK_RAN the change).</p>

<p>I find difficulties writing a correct precondition when I don't know the exact name of foreign keys, which may or may not exist.
There is <code>&lt;foreignKeyConstraintExists&gt;</code> tag in liquibase (precondition) but it takes only <code>schemaName</code> and <code>foreignKeyName</code> attributes (and they are required). I don't know the foreign key names for sure in these instances as they are out of my control.</p>

<p>You can write custom SQL in preconditions like:</p>

<pre><code>&lt;changeSet id="1" author="bob"&gt;
    &lt;preConditions onFail="WARN"&gt;
        &lt;sqlCheck expectedResult="0"&gt;select count(*) from oldtable&lt;/sqlCheck&gt;
    &lt;/preConditions&gt;
    &lt;dropTable tableName="oldtable"/&gt;
&lt;/changeSet&gt;
</code></pre>

<p>So I only have to create a custom SQL query which can check if a column on table <code>A</code> has foreign key referencing table <code>B</code> and use the result as a precondition.
This is where my problem is because you can do it in Oracle but it's quite bloat:</p>

<pre><code>SELECT a.table_name, a.column_name, a.constraint_name, c.owner, 
       c.r_owner, c_pk.table_name r_table_name
  FROM all_cons_columns a
  JOIN all_constraints c ON a.owner = c.owner
                        AND a.constraint_name = c.constraint_name
  JOIN all_constraints c_pk ON c.r_owner = c_pk.owner
                        AND c.r_constraint_name = c_pk.constraint_name
  WHERE c.constraint_type = 'R' AND a.table_name = 'MY_TABLE'
  AND a.column_name = 'MY_COLUMN'
  AND c_pk.table_name = 'MY_OTHER_TABLE';
</code></pre>

<p>This prints a row if a foreign key exists on <code>MY_COLUMN</code> of <code>MY_TABLE</code> which references to <code>MY_OTHER_TABLE</code>. After rewriting it to COUNT you can check if there's foreign key without knowing it's name.</p>

<p><strong>My question:</strong>
I have dozens of foreign keys, do I really have to write this big SQL such dozens of times? Any suggestions, like outsourcing this to some function? Thanks!</p>

<p>Would it worth asking Liquibase developers to make <code>&lt;foreignKeyConstraintExists&gt;</code> 's name attribute optional and introduce the referenced table attribute alogn with local column name?</p>

## Answers
### Answer ID: 20189952
<p>There is one more possibility: implementing the interface <a href="http://www.liquibase.org/javadoc/liquibase/precondition/CustomPrecondition.html" rel="nofollow">http://www.liquibase.org/javadoc/liquibase/precondition/CustomPrecondition.html</a> and use it as a custom precondition. More info: <a href="http://www.liquibase.org/documentation/preconditions.html" rel="nofollow">http://www.liquibase.org/documentation/preconditions.html</a></p>

<p>Here is the implementation (verified):</p>

<pre><code>import liquibase.database.Database;
import liquibase.exception.CustomPreconditionErrorException;
import liquibase.exception.CustomPreconditionFailedException;
import liquibase.precondition.CustomPrecondition;
import liquibase.snapshot.SnapshotGeneratorFactory;
import liquibase.structure.core.ForeignKey;
import liquibase.structure.core.Schema;
import liquibase.structure.core.Table;
import liquibase.util.StringUtils;

/**
 * {@link CustomPrecondition} implementation that checks if a column on a table
 * has a foreign key constraint for some other table.
 */
public final class CheckForeignKey implements CustomPrecondition {

    /**
     * Schema.
     */
    private String schemaName;

    /**
     * Table name (that has the column).
     */
    private String tableName;

    /**
     * Column (that might have the foreign key).
     */
    private String columnName;

    /**
     * Referenced table of the foreign key.
     */
    private String foreignTableName;

    @Override
    public void check(final Database db)
            throws CustomPreconditionFailedException,
            CustomPreconditionErrorException {

        try {
            // The fkey we are looking for
            final ForeignKey fKey = new ForeignKey();

            // Schema, base table
            fKey.setForeignKeyTable(new Table());
            if (StringUtils.trimToNull(getTableName()) != null) {
                fKey.getForeignKeyTable().setName(getTableName());
            }

            final Schema schema = new Schema();
            schema.setName(getSchemaName());
            fKey.getForeignKeyTable().setSchema(schema);

            // Base column
            fKey.addForeignKeyColumn(getColumnName());

            // Referenced table
            fKey.setPrimaryKeyTable(new Table());
            if (StringUtils.trimToNull(getForeignTableName()) != null) {
                fKey.getPrimaryKeyTable().setName(getForeignTableName());
            }

            if (!SnapshotGeneratorFactory.getInstance().has(fKey, db)) {
                throw new CustomPreconditionFailedException(
                        String.format(
                                "Error fkey not found schema %s table %s column %s ftable %s",
                                getSchemaName(), getTableName(),
                                getColumnName(), getForeignTableName()));
            }
        } catch (final CustomPreconditionFailedException e) {
            throw e;
        } catch (final Exception e) {
            throw new CustomPreconditionErrorException("Error", e);
        }
    }

    public String getSchemaName() {
        return schemaName;
    }

    public void setSchemaName(final String schemaName) {
        this.schemaName = schemaName;
    }

    public String getTableName() {
        return tableName;
    }

    public void setTableName(final String tableName) {
        this.tableName = tableName;
    }

    public String getColumnName() {
        return columnName;
    }

    public void setColumnName(final String columnName) {
        this.columnName = columnName;
    }

    public String getForeignTableName() {
        return foreignTableName;
    }

    public void setForeignTableName(final String foreignTableName) {
        this.foreignTableName = foreignTableName;
    }
}
</code></pre>

### Answer ID: 20150040
<p>I think that you have to do it like you suggested if you dont know foreign key constraint names.</p>

<p>But if you can modify database then you could prepare sql script which prepare another sql script which renames all FK to well known names. Something like that:</p>

<pre><code>BEGIN

FOR cur IN (
    SELECT 
      c_list.CONSTRAINT_NAME as FK_NAME,
      'FK_' || c_dest.TABLE_NAME || '_' || substr(c_dest.COLUMN_NAME, 1, 20) as NEW_FK_NAME,
      c_src.TABLE_NAME as SRC_TABLE,
      c_src.COLUMN_NAME as SRC_COLUMN,
      c_dest.TABLE_NAME as DEST_TABLE,
      c_dest.COLUMN_NAME as DEST_COLUMN
    FROM ALL_CONSTRAINTS c_list, ALL_CONS_COLUMNS c_src, ALL_CONS_COLUMNS c_dest
    WHERE c_list.CONSTRAINT_NAME = c_src.CONSTRAINT_NAME
    AND c_list.R_CONSTRAINT_NAME = c_dest.CONSTRAINT_NAME
    AND c_list.CONSTRAINT_TYPE = 'R'
    AND c_src.TABLE_NAME IN ('&lt;your-tables-here&gt;')
    GROUP BY c_list.CONSTRAINT_NAME, c_src.TABLE_NAME, c_src.COLUMN_NAME, c_dest.TABLE_NAME, c_dest.COLUMN_NAME;
) LOOP

    -- Generate here SQL commands (by string concatenation) something like:
    -- alter table SRC_TABLE rename constraint FK_NAME to NEW_FK_NAME;
    -- then paste this sql commands to some other script and run it

END LOOP;

END;
</code></pre>

<p>This is one time migration.</p>

<p>After this migration you know whats your FK constraint names are and you can use &lt;foreignKeyConstraintExists&gt; precondition in your changesets.</p>


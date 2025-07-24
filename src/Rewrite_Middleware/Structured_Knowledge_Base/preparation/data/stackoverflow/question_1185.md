# Rewrite Do-Block to trigger function in PostgreSQL/plpgsql
[Link to question](https://stackoverflow.com/questions/62452522/rewrite-do-block-to-trigger-function-in-postgresql-plpgsql)
**Creation Date:** 1592491022
**Score:** -1
**Tags:** postgresql
## Question Body
<p>I created a script to update multiple columns of a table in my database . Originally I run this manually but I'd like to apply some automatization with the help of a <code>TRIGGER</code> function. Basically I have an empty table where I <code>INSERT</code> values. Based on this <code>INSERT</code> i'd like to update the same table afterwards.</p>

<p>Thats my old code:</p>

<pre><code>-- Create example table
    CREATE TABLE table1(
                        column1 INTEGER,
                        column2 INTEGER,
                        column3 INTEGER,
                        column4 INTEGER);

-- Insert example values        
    INSERT INTO table1 (column1, column2, column3)
    VALUES
        (1,2,3),
        (4,5,6),
        (7,8,9),
        (10,11,12);         

-- Update the table

    DO $$
        DECLARE

            b INTEGER := 5;
            c INTEGER := 11;

        BEGIN

        UPDATE table1
        SET column2 = column1 + b;

        UPDATE table1
        SET column3 = column2 - c;

        UPDATE table1
        SET column4 = column1 + column2 +column3;

    END $$ language plpgsql;
</code></pre>

<p>I tried to rewrite it in this form:</p>

<pre><code>--Create Trigger function
    CREATE OR REPLACE FUNCTION example_trigger() 
    RETURNS TRIGGER AS
    $func$
        DECLARE

            b INTEGER := 5;
            c INTEGER := 11;

        BEGIN

        UPDATE table1
        SET column2 = column1 + b;

        UPDATE table1
        SET column3 = column2 - c;

        UPDATE table1
        SET column4 = column1 + column2 +column3;

    END $func$ language plpgsql;

-- Create Trigger  
    CREATE TRIGGER atest AFTER INSERT ON table1
    EXECUTE PROCEDURE example_trigger();

        -- DELETE FROM table1

    --INSERT values in the hope to trigger "example_trigger"
    INSERT INTO table1 (column1, column2, column3)
        VALUES
            (1,2,3),
            (4,5,6),
            (7,8,9),
            (10,11,12);  
</code></pre>

<p>But I get </p>

<pre><code>ERROR:  control reached end of trigger procedure without RETURN
CONTEXT:  PL/pgSQL function example_trigger()
SQL state: 2F005
</code></pre>

<p>How is <code>RETURN</code> causing problems in my query? Additionally I'd like to know if the <code>UPDATE</code> statements in the <code>DO</code> Blocks are working row-wise or column wise.</p>

## Answers
### Answer ID: 62452619
<p>In a PostgreSQL trigger function <a href="https://www.postgresql.org/docs/12/plpgsql-trigger.html" rel="nofollow noreferrer">you need to use RETURN statement:</a></p>

<blockquote>
  <p>A trigger function must return either NULL or a record/row value
  having exactly the structure of the table the trigger was fired for.</p>
  
  <p>Row-level triggers fired BEFORE can return null to signal the trigger
  manager to skip the rest of the operation for this row (i.e.,
  subsequent triggers are not fired, and the INSERT/UPDATE/DELETE does
  not occur for this row). If a nonnull value is returned then the
  operation proceeds with that row value. Returning a row value
  different from the original value of NEW alters the row that will be
  inserted or updated. Thus, if the trigger function wants the
  triggering action to succeed normally without altering the row value,
  NEW (or a value equal thereto) has to be returned. To alter the row to
  be stored, it is possible to replace single values directly in NEW and
  return the modified NEW, or to build a complete new record/row to
  return. In the case of a before-trigger on DELETE, the returned value
  has no direct effect, but it has to be nonnull to allow the trigger
  action to proceed. Note that NEW is null in DELETE triggers, so
  returning that is usually not sensible. The usual idiom in DELETE
  triggers is to return OLD.</p>
  
  <p>INSTEAD OF triggers (which are always row-level triggers, and may only
  be used on views) can return null to signal that they did not perform
  any updates, and that the rest of the operation for this row should be
  skipped (i.e., subsequent triggers are not fired, and the row is not
  counted in the rows-affected status for the surrounding
  INSERT/UPDATE/DELETE). Otherwise a nonnull value should be returned,
  to signal that the trigger performed the requested operation. For
  INSERT and UPDATE operations, the return value should be NEW, which
  the trigger function may modify to support INSERT RETURNING and UPDATE
  RETURNING (this will also affect the row value passed to any
  subsequent triggers, or passed to a special EXCLUDED alias reference
  within an INSERT statement with an ON CONFLICT DO UPDATE clause). For
  DELETE operations, the return value should be OLD.</p>
  
  <p>The return value of a row-level trigger fired AFTER or a
  statement-level trigger fired BEFORE or AFTER is always ignored; it
  might as well be null. However, any of these types of triggers might
  still abort the entire operation by raising an error.</p>
</blockquote>


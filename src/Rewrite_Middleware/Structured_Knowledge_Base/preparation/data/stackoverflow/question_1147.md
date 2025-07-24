# Hashaggregate on postgres relation table is slow
[Link to question](https://stackoverflow.com/questions/61004733/hashaggregate-on-postgres-relation-table-is-slow)
**Creation Date:** 1585885057
**Score:** 0
**Tags:** sql, postgresql, query-performance
## Question Body
<p>I have the following scenario: I have a postgres database with several card records and also several deck records (it is a card game information system). In this case, I have an association table between decks and cards, called <code>deck_cards</code>, which has approximately 6 million rows and is growing. Database schema looks like this:</p>

<pre><code>decks(id,name)
cards(id,name,extra) -- extra is a varchar field to store general information
deck_cards(id,id_card,id_deck)

cards indexes:
    "Cards_pkey" PRIMARY KEY, btree (id)

deck indexes:
    "Decks_pkey" PRIMARY KEY, btree (id)

deck_cards indexes:
    "deck_cards_pkey" PRIMARY KEY, btree (id)
    "deck_cards_card_id" btree (card_id)
    "deck_cards_deck_id" btree (deck_id)
    "deck_cards_deck_id_card_id" btree (deck_id, card_id) CLUSTER
    "deck_cards_extra_card_id" btree (extra, card_id)
</code></pre>

<p>Having this structure, I tried to build a query that would return the most used cards on decks that have an X card. The problem is that the query is very slow to be executed, and I can't imagine if the problem is my schema, my query, or if it’s something else.</p>

<p>My attempts were:</p>

<pre><code>EXPLAIN ANALYZE
WITH d AS (
  SELECT deck_id FROM deck_cards
  WHERE extra IS NULL AND card_id = 'XXX'
)
SELECT COUNT(*) AS count, card_id
FROM deck_cards
WHERE
  card_id &lt;&gt; 'XXX'
  AND deck_id IN (SELECT * FROM d)
GROUP BY card_id
ORDER BY count DESC
LIMIT 200;
</code></pre>

<p>The result obtained was:</p>

<pre><code>Limit  (cost=54567.65..54568.15 rows=200 width=24) (actual time=4951.567..4951.611 rows=200 loops=1)
   CTE d
     -&gt;  HashAggregate  (cost=16666.74..16937.95 rows=27121 width=16) (actual time=381.594..395.473 rows=43256 loops=1)
           Group Key: deck_cards_1.deck_id
           -&gt;  Index Scan using deck_cards_extra_card_id on deck_cards deck_cards_1  (cost=0.56..16550.34 rows=46560 width=16) (actual time=0.038..350.081 rows=43258 loops=1)
                 Index Cond: ((extra IS NULL) AND (card_id = 'dc87938d-6df8-4acc-bfd0-3cbb58066057'::uuid))
   -&gt;  Sort  (cost=37629.70..37649.11 rows=7766 width=24) (actual time=4951.565..4951.586 rows=200 loops=1)
         Sort Key: (count(*)) DESC
         Sort Method: top-N heapsort  Memory: 50kB
         -&gt;  HashAggregate  (cost=37216.40..37294.06 rows=7766 width=24) (actual time=4942.328..4947.457 rows=17035 loops=1)
               Group Key: deck_cards.card_id
               -&gt;  Nested Loop  (cost=610.65..24198.67 rows=2603546 width=16) (actual time=439.553..3568.086 rows=3518996 loops=1)
                     -&gt;  HashAggregate  (cost=610.22..612.22 rows=200 width=16) (actual time=439.466..454.442 rows=43256 loops=1)
                           Group Key: d.deck_id
                           -&gt;  CTE Scan on d  (cost=0.00..542.42 rows=27121 width=16) (actual time=381.598..416.827 rows=43256 loops=1)
                     -&gt;  Index Scan using deck_cards_deck_id on deck_cards  (cost=0.43..116.58 rows=135 width=32) (actual time=0.026..0.061 rows=81 loops=43256)
                           Index Cond: (deck_id = d.deck_id)
                           Filter: (card_id &lt;&gt; 'dc87938d-6df8-4acc-bfd0-3cbb58066057'::uuid)
                           Rows Removed by Filter: 1
 Planning time: 0.484 ms
 Execution time: 4952.303 ms
</code></pre>

<p>I also tried to rewrite without using <code>WITH</code>, but I also didn't get a good result.</p>

<pre><code>EXPLAIN ANALYZE
SELECT COUNT(*) AS count, card_id
FROM deck_cards
WHERE card_id &lt;&gt; 'dc87938d-6df8-4acc-bfd0-3cbb58066057' AND deck_id IN (
  SELECT DISTINCT deck_id FROM deck_cards
  WHERE extra IS NULL AND card_id = 'dc87938d-6df8-4acc-bfd0-3cbb58066057'
)
GROUP BY card_id
ORDER BY count DESC
LIMIT 200;
</code></pre>

<p>The result obtained was similar to the previous one in terms of performance:</p>

<pre><code>Limit  (cost=127334.18..127334.68 rows=200 width=24) (actual time=5098.815..5098.982 rows=200 loops=1)
   -&gt;  Sort  (cost=127334.18..127353.59 rows=7766 width=24) (actual time=5098.813..5098.834 rows=200 loops=1)
         Sort Key: (count(*)) DESC
         Sort Method: top-N heapsort  Memory: 52kB
         -&gt;  Finalize GroupAggregate  (cost=126804.38..126998.53 rows=7766 width=24) (actual time=5081.173..5095.062 rows=17035 loops=1)
               Group Key: deck_cards.card_id
               -&gt;  Sort  (cost=126804.38..126843.21 rows=15532 width=24) (actual time=5081.164..5086.096 rows=44616 loops=1)
                     Sort Key: deck_cards.card_id
                     Sort Method: external merge  Disk: 1488kB
                     -&gt;  Gather  (cost=124092.27..125723.13 rows=15532 width=24) (actual time=4964.087..5039.956 rows=44616 loops=1)
                           Workers Planned: 2
                           Workers Launched: 2
                           -&gt;  Partial HashAggregate  (cost=123092.27..123169.93 rows=7766 width=24) (actual time=4889.013..4909.163 rows=14872 loops=3)
                                 Group Key: deck_cards.card_id
                                 -&gt;  Hash Join  (cost=17548.17..115477.70 rows=1522913 width=16) (actual time=1058.268..3482.032 rows=1172999 loops=3)
                                       Hash Cond: (deck_cards.deck_id = deck_cards_1.deck_id)
                                       -&gt;  Parallel Seq Scan on deck_cards  (cost=0.00..92233.65 rows=2169622 width=32) (actual time=0.053..1233.727 rows=1736981 loops=3)
                                             Filter: (card_id &lt;&gt; 'dc87938d-6df8-4acc-bfd0-3cbb58066057'::uuid)
                                             Rows Removed by Filter: 14421
                                       -&gt;  Hash  (cost=17209.16..17209.16 rows=27121 width=16) (actual time=1057.194..1057.194 rows=43256 loops=3)
                                             Buckets: 65536 (originally 32768)  Batches: 1 (originally 1)  Memory Usage: 2540kB
                                             -&gt;  HashAggregate  (cost=16666.74..16937.95 rows=27121 width=16) (actual time=942.447..988.024 rows=43256 loops=3)
                                                   Group Key: deck_cards_1.deck_id
                                                   -&gt;  Index Scan using deck_cards_extra_card_id on deck_cards deck_cards_1  (cost=0.56..16550.34 rows=46560 width=16) (actual time=0.077..855.472 rows=43258 loops=3)
                                                         Index Cond: ((extra IS NULL) AND (card_id = 'dc87938d-6df8-4acc-bfd0-3cbb58066057'::uuid))
 Planning time: 0.373 ms
 Execution time: 5099.848 ms
</code></pre>

<p>Can anyone tell me if I am doing something wrong, if there is a better way to consult this type of data, or if I am stuck in this problem and should I look for a solution to respond to my API requests using only a cache?</p>

<p>[EDIT]</p>

<p>Exemplifying: I want to get a count of cards that share a deck_id with a card <code>A</code> when it has NULL in the extra field on that deck. Only:</p>

<pre><code>(card_id, deck_id, extra)
(A, 1, NULL)
(C, 1, NULL)
(A, 2,NULL)
(C, 2,NULL)
(Y, 2,NULL)
(A,3,'foo')
(C,3,NULL)

- The response I want is looking for card = 'A' AND extra IS NULL:
(C, 2)
(Y, 1)
</code></pre>

## Answers
### Answer ID: 61017681
<pre><code>\i tmp.sql

        -- make some usable data
        -- UUID --&gt; bigint
CREATE TABLE decks
        ( id bigserial NOT NULL PRIMARY KEY
        , name text
        );
CREATE TABLE cards
        ( id bigserial NOT NULL PRIMARY KEY
        , name text
        , extra text
        );

CREATE TABLE deck_cards
        ( id_card  bigint NOT NULL REFERENCES cards(id)
        , id_deck bigint NOT NULL REFERENCES decks(id)
        , PRIMARY KEY (id_card,id_deck)
        , UNIQUE (id_deck, id_card)
        );

INSERT INTO cards(name, extra)
SELECT 'name_' || gs::text
        , NULLIF(gs%41,0)::text
FROM generate_series(1,1000) gs
        ;

INSERT INTO decks(name)
SELECT 'deck_' || gs::text
FROM generate_series(1,1000) gs
        ;
INSERT INTO deck_cards(id_card, id_deck)
SELECT c.id, d.id
FROM cards c
JOIN decks d ON random() &lt; 0.1
        ;
VACUUM ANALYZE decks;
VACUUM ANALYZE cards;
VACUUM ANALYZE deck_cards;
        -- do the query
EXPLAIN ANALYZE
SELECT dc.id_card
        , COUNT(*) AS cnt
FROM deck_cards dc
WHERE dc.id_card &lt;&gt; 123
AND EXISTS ( -- select all decks that have an X card
         SELECT *
        FROM deck_cards xdc
        JOIN cards x ON x.id = xdc.id_card
        WHERE xdc.id_card = 123 -- deck must have an X-card
        AND x.extra IS NULL
        AND xdc.id_deck = dc.id_deck  -- same deck as outer query
        )
GROUP BY id_card
        ;
</code></pre>

<hr>

<p>Resulting plan:</p>

<hr>

<pre><code>                                                                                  QUERY PLAN                                                                              
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=486.80..496.80 rows=1000 width=16) (actual time=7.198..7.428 rows=999 loops=1)
   Group Key: dc.id_card
   -&gt;  Nested Loop  (cost=7.70..430.26 rows=11307 width=8) (actual time=0.227..4.757 rows=11078 loops=1)
         -&gt;  HashAggregate  (cost=7.28..8.22 rows=94 width=8) (actual time=0.199..0.234 rows=111 loops=1)
               Group Key: xdc.id_deck
               -&gt;  Nested Loop  (cost=0.69..7.03 rows=99 width=8) (actual time=0.127..0.165 rows=111 loops=1)
                     -&gt;  Index Scan using cards_pkey on cards x  (cost=0.28..2.69 rows=1 width=8) (actual time=0.068..0.069 rows=1 loops=1)
                           Index Cond: (id = 123)
                           Filter: (extra IS NULL)
                     -&gt;  Index Only Scan using deck_cards_pkey on deck_cards xdc  (cost=0.42..3.35 rows=99 width=16) (actual time=0.057..0.082 rows=111 loops=1)
                           Index Cond: (id_card = 123)
                           Heap Fetches: 0
         -&gt;  Index Only Scan using deck_cards_id_deck_id_card_key on deck_cards dc  (cost=0.42..3.49 rows=100 width=16) (actual time=0.013..0.030 rows=100 loops=111)
               Index Cond: (id_deck = xdc.id_deck)
               Filter: (id_card &lt;&gt; 123)
               Rows Removed by Filter: 1
               Heap Fetches: 0
 Planning Time: 0.988 ms
 Execution Time: 7.621 ms
(19 rows)
</code></pre>

### Answer ID: 61011564
<p>You can just use a window function and aggregation:</p>

<pre><code>SELECT COUNT(*) AS count,
       card_id
FROM (SELECT dc.*, COUNT(*) FILTER (WHERE card_id = 'A' and extra IS NULL) OVER (PARTITION BY deck_id) as cnt
      FROM deck_cards dc
     ) dc
WHERE cnt &gt; 0 AND card_id &lt;&gt; 'A'
GROUP BY card_id
ORDER BY count DESC;
</code></pre>

<p><a href="https://dbfiddle.uk/?rdbms=postgres_12&amp;fiddle=b6a6e7ae45c35162e923d175b799798c" rel="nofollow noreferrer">Here</a> is a db&lt;>fiddle.</p>

<p>This might have better performance than your version.</p>


# How to rewrite kafka connect jdbc driver select current_timestamp method?
[Link to question](https://stackoverflow.com/questions/78477330/how-to-rewrite-kafka-connect-jdbc-driver-select-current-timestamp-method)
**Creation Date:** 1715681365
**Score:** 0
**Tags:** jdbc, apache-kafka, apache-kafka-connect, jaybird
## Question Body
<p>I am trying to use Kafka connect with jaybird to retrieve data from firebird tables using timestamp.
Jaybird version is 5.0.4. Kafka connect failed with 'failed to get current time from db using generic and query' error. The correct way to get timestamp is
SELECT CURRENT_TIMESTAMP from rdb$database;</p>
<p>How can I rewrite default jaybird timestamp query?</p>
<p>Using this <a href="https://stackoverflow.com/questions/56218720/getting-exception-failed-to-get-current-time-from-db-using-query-valuescurrent">Getting exception ,Failed to get current time from DB using query values(CURRENT_TIMESTAMP) on database DB2</a> I updated jaybird driver to latest version but it did not help.</p>
<p>Dockerfile is</p>
<pre><code>ARG image
FROM ${image}

## Install connectors
RUN echo &quot;\nInstalling all required connectors...\n&quot; &amp;&amp; \
confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:latest &amp;&amp; \
confluent-hub install --no-prompt debezium/debezium-connector-postgresql:latest &amp;&amp; \
confluent-hub install --no-prompt jcustenborder/kafka-connect-transform-common:latest

COPY fb_driver/jaybird-5.0.4.java11.jar /usr/share/confluent-hub-components/confluentinc-kafka-connect-jdbc/lib/jaybird-5.0.4.java11.jar
</code></pre>


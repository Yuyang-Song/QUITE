# Indexing irregular String Data with special characters(;+) into Solr using Apache Nifi
[Link to question](https://stackoverflow.com/questions/77043171/indexing-irregular-string-data-with-special-characters-into-solr-using-apach)
**Creation Date:** 1693904855
**Score:** 0
**Tags:** solr, full-text-search, apache-nifi, dataimporthandler
## Question Body
<p>Im new to Apache Nifi, im try to implement it as a replacement for Solr Native Data Import Handler(DIH) which is now deprecated in Solr vr.9.
Concrete here is the problem: I can import all other fields from Oracle database except data in this field that gives the following error:Error adding field 'FIELD_NAME'='77777383;+4377777383' msg=For input string: &quot;77777383;
I suspect the problem lies with the special characters &quot;;+&quot; included in the string</p>
<p>The nifi-app log looks like this:</p>
<blockquote>
<p>org.apache.solr.client.solrj.impl.HttpSolrClient$RemoteSolrException: Error from server at https://servername:9999/solr/core: ERROR: [doc=4241b407-c29b-40c2-ad46-2dae92fb3694] Error adding field 'FIELD_NAME'='77777383;+4377777383' msg=For input string: &quot;77777383;+4940866485409&quot;
at org.apache.solr.client.solrj.impl.HttpSolrClient.executeMethod(HttpSolrClient.java:681)
at org.apache.solr.client.solrj.impl.HttpSolrClient.request(HttpSolrClient.java:266)
at org.apache.solr.client.solrj.impl.HttpSolrClient.request(HttpSolrClient.java:248)
at org.apache.solr.client.solrj.SolrRequest.process(SolrRequest.java:214)
at org.apache.solr.client.solrj.SolrRequest.process(SolrRequest.java:231)
at org.apache.nifi.processors.solr.PutSolrRecord.index(PutSolrRecord.java:325)
at org.apache.nifi.processors.solr.PutSolrRecord.doOnTrigger(PutSolrRecord.java:251)
at org.apache.nifi.processors.solr.SolrProcessor.onTrigger(SolrProcessor.java:132)
at org.apache.nifi.processor.AbstractProcessor.onTrigger(AbstractProcessor.java:27)
at org.apache.nifi.controller.StandardProcessorNode.onTrigger(StandardProcessorNode.java:1360)
at org.apache.nifi.controller.tasks.ConnectableTask.invoke(ConnectableTask.java:246)
at org.apache.nifi.controller.scheduling.AbstractTimeBasedSchedulingAgent.lambda$doScheduleOnce$0(AbstractTimeBasedSchedulingAgent.java:59)
at org.apache.nifi.engine.FlowEngine$2.run(FlowEngine.java:110)
at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Unknown Source)
at java.base/java.util.concurrent.FutureTask.run(Unknown Source)
at java.base/java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(Unknown Source)
at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
at java.base/java.lang.Thread.run(Unknown Source)</p>
</blockquote>
<p>Here is the solr definition of the field in schema.xml:</p>
<pre><code>&lt;fieldType name=&quot;tele_1&quot; class=&quot;solr.TextField&quot; multiValued=&quot;true&quot;&gt;
&lt;analyzer type=&quot;index&quot;&gt;
&lt;tokenizer class=&quot;solr.StandardTokenizerFactory&quot; maxTokenLength=&quot;255&quot;/&gt;
&lt;filter class=&quot;solr.ReversedWildcardFilterFactory&quot; maxPosAsterisk=&quot;3&quot; withOriginal=&quot;true&quot; maxPosQuestion=&quot;2&quot; maxFractionAsterisk=&quot;0.33&quot;/&gt;
&lt;filter class=&quot;solr.RemoveDuplicatesTokenFilterFactory&quot;/&gt;
&lt;/analyzer&gt;
&lt;analyzer type=&quot;query&quot;&gt;
&lt;tokenizer class=&quot;solr.StandardTokenizerFactory&quot; maxTokenLength=&quot;255&quot;/&gt;
&lt;filter class=&quot;solr.ReversedWildcardFilterFactory&quot; maxPosAsterisk=&quot;3&quot; withOriginal=&quot;true&quot; maxPosQuestion=&quot;2&quot; maxFractionAsterisk=&quot;0.33&quot;/&gt;
&lt;/analyzer&gt;
&lt;/fieldType&gt;
</code></pre>
<h2>And Solr.log:</h2>
<blockquote>
<p>2023-09-08 05:52:48.348 ERROR (qtp1345265484-63) [ x:vdb]
o.a.s.h.RequestHandlerBase org.apache.solr.common.SolrException:
ERROR: [doc=2d74b84a-33c2-488e-8331-eee4a2c6120e] Error adding field
'FAX_OLZ'=''77777383;+4377777383'' msg=For input string:
&quot;'77777383;+4377777383'&quot; =&gt; org.apache.solr.common.SolrException:
ERROR: [doc=2d74b84a-33c2-488e-8331-eee4a2c6120e] Error adding field
'FAX_OLZ'='7313 2592;+49 431 71745 2592' msg=For input string:
&quot;'77777383;+4377777383'&quot;  at
org.apache.solr.update.DocumentBuilder.toDocument(DocumentBuilder.java:258)
org.apache.solr.common.SolrException: ERROR:
[doc=2d74b84a-33c2-488e-8331-eee4a2c6120e] Error adding field
'FAX_OLZ'='77777383;+4377777383' msg=For input string:
&quot;'77777383;+4377777383'&quot;  at
org.apache.solr.update.DocumentBuilder.toDocument(DocumentBuilder.java:258)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DocumentBuilder.toDocument(DocumentBuilder.java:100)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.AddUpdateCommand.lambda$makeLuceneDocs$0(AddUpdateCommand.java:233)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
java.util.stream.ReferencePipeline$3$1.accept(Unknown Source) ~[?:?]
at java.util.ArrayList$ArrayListSpliterator.tryAdvance(Unknown
Source) ~[?:?]    at
java.util.stream.StreamSpliterators$WrappingSpliterator.lambda$initPartialTraversalState$0(Unknown
Source) ~[?:?]    at
java.util.stream.StreamSpliterators$AbstractWrappingSpliterator.fillBuffer(Unknown
Source) ~[?:?]    at
java.util.stream.StreamSpliterators$AbstractWrappingSpliterator.doAdvance(Unknown
Source) ~[?:?]    at
java.util.stream.StreamSpliterators$WrappingSpliterator.tryAdvance(Unknown
Source) ~[?:?]    at java.util.Spliterators$1Adapter.hasNext(Unknown
Source) ~[?:?]    at
org.apache.lucene.index.DocumentsWriterPerThread.updateDocuments(DocumentsWriterPerThread.java:232)
~[lucene-core-9.3.0.jar:9.3.0 d25cebcef7a80369f4dfb9285ca7360a810b75dc</p>
<ul>
<li>ivera - 2022-07-25 12:30:23]    at org.apache.lucene.index.DocumentsWriter.updateDocuments(DocumentsWriter.java:432)
~[lucene-core-9.3.0.jar:9.3.0 d25cebcef7a80369f4dfb9285ca7360a810b75dc</li>
<li>ivera - 2022-07-25 12:30:23]    at org.apache.lucene.index.IndexWriter.updateDocuments(IndexWriter.java:1532)
~[lucene-core-9.3.0.jar:9.3.0 d25cebcef7a80369f4dfb9285ca7360a810b75dc</li>
<li>ivera - 2022-07-25 12:30:23]    at org.apache.lucene.index.IndexWriter.updateDocuments(IndexWriter.java:1521)
~[lucene-core-9.3.0.jar:9.3.0 d25cebcef7a80369f4dfb9285ca7360a810b75dc</li>
<li>ivera - 2022-07-25 12:30:23]    at org.apache.solr.update.DirectUpdateHandler2.updateDocOrDocValues(DirectUpdateHandler2.java:1048)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DirectUpdateHandler2.doNormalUpdate(DirectUpdateHandler2.java:416)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DirectUpdateHandler2.addDoc0(DirectUpdateHandler2.java:369)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DirectUpdateHandler2.addDoc(DirectUpdateHandler2.java:300)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.RunUpdateProcessorFactory$RunUpdateProcessor.processAdd(RunUpdateProcessorFactory.java:76)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.NestedUpdateProcessorFactory$NestedUpdateProcessor.processAdd(NestedUpdateProcessorFactory.java:78)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.DistributedUpdateProcessor.doLocalAdd(DistributedUpdateProcessor.java:269)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.DistributedUpdateProcessor.doVersionAdd(DistributedUpdateProcessor.java:544)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.DistributedUpdateProcessor.lambda$versionAdd$0(DistributedUpdateProcessor.java:356)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.VersionBucket.runWithLock(VersionBucket.java:51)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.DistributedUpdateProcessor.versionAdd(DistributedUpdateProcessor.java:353)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.DistributedUpdateProcessor.processAdd(DistributedUpdateProcessor.java:235)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.LogUpdateProcessorFactory$LogUpdateProcessor.processAdd(LogUpdateProcessorFactory.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.AddSchemaFieldsUpdateProcessorFactory$AddSchemaFieldsUpdateProcessor.processAdd(AddSchemaFieldsUpdateProcessorFactory.java:535)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldMutatingUpdateProcessor.processAdd(FieldMutatingUpdateProcessor.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldMutatingUpdateProcessor.processAdd(FieldMutatingUpdateProcessor.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldMutatingUpdateProcessor.processAdd(FieldMutatingUpdateProcessor.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldMutatingUpdateProcessor.processAdd(FieldMutatingUpdateProcessor.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldNameMutatingUpdateProcessorFactory$1.processAdd(FieldNameMutatingUpdateProcessorFactory.java:71)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.FieldMutatingUpdateProcessor.processAdd(FieldMutatingUpdateProcessor.java:111)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.UpdateRequestProcessor.processAdd(UpdateRequestProcessor.java:55)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.processor.AbstractDefaultValueUpdateProcessorFactory$DefaultValueUpdateProcessor.processAdd(AbstractDefaultValueUpdateProcessorFactory.java:82)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.handler.loader.JavabinLoader$1.update(JavabinLoader.java:123)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.client.solrj.request.JavaBinUpdateRequestCodec$StreamingCodec.readOuterMostDocIterator(JavaBinUpdateRequestCodec.java:342)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.client.solrj.request.JavaBinUpdateRequestCodec$StreamingCodec.readIterator(JavaBinUpdateRequestCodec.java:286)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.common.util.JavaBinCodec.readObject(JavaBinCodec.java:338)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.common.util.JavaBinCodec.readVal(JavaBinCodec.java:283)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.client.solrj.request.JavaBinUpdateRequestCodec$StreamingCodec.readNamedList(JavaBinUpdateRequestCodec.java:236)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.common.util.JavaBinCodec.readObject(JavaBinCodec.java:303)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.common.util.JavaBinCodec.readVal(JavaBinCodec.java:283)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.common.util.JavaBinCodec.unmarshal(JavaBinCodec.java:193)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.client.solrj.request.JavaBinUpdateRequestCodec.unmarshal(JavaBinUpdateRequestCodec.java:126)
~[solr-solrj-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944</li>
<li>magibney - 2023-01-17 19:58:00]     at org.apache.solr.handler.loader.JavabinLoader.parseAndLoadDocs(JavabinLoader.java:135)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.handler.loader.JavabinLoader.load(JavabinLoader.java:74)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.handler.UpdateRequestHandler$1.load(UpdateRequestHandler.java:101)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.handler.ContentStreamHandlerBase.handleRequestBody(ContentStreamHandlerBase.java:84)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.handler.RequestHandlerBase.handleRequest(RequestHandlerBase.java:224)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.core.SolrCore.execute(SolrCore.java:2865)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.HttpSolrCall.execute(HttpSolrCall.java:887)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.HttpSolrCall.call(HttpSolrCall.java:606)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.SolrDispatchFilter.dispatch(SolrDispatchFilter.java:250)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.SolrDispatchFilter.lambda$doFilter$0(SolrDispatchFilter.java:218)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.ServletUtils.traceHttpRequestExecution2(ServletUtils.java:257)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.ServletUtils.rateLimitRequest(ServletUtils.java:227)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.SolrDispatchFilter.doFilter(SolrDispatchFilter.java:213)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.servlet.SolrDispatchFilter.doFilter(SolrDispatchFilter.java:195)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.eclipse.jetty.servlet.FilterHolder.doFilter(FilterHolder.java:201)
~[jetty-servlet-9.4.48.v20220622.jar:9.4.48.v20220622]    at
org.eclipse.jetty.servlet.ServletHandler$Chain.doFilter(ServletHandler.java:1626)
~[jetty-servlet-9.4.48.v20220622.jar:9.4.48.v20220622]    at
org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:552)
~[jetty-servlet-9.4.48.v20220622.jar:9.4.48.v20220622]    at
org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:143)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:600)
~[jetty-security-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:127)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ScopedHandler.nextHandle(ScopedHandler.java:235)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:1624)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ScopedHandler.nextHandle(ScopedHandler.java:233)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1440)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:188)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:505)
~[jetty-servlet-9.4.48.v20220622.jar:9.4.48.v20220622]    at
org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:1594)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:186)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1355)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:141)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:191)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.InetAccessHandler.handle(InetAccessHandler.java:177)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:146)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:127)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.rewrite.handler.RewriteHandler.handle(RewriteHandler.java:322)
~[jetty-rewrite-9.4.48.v20220622.jar:9.4.48.v20220622]    at
org.eclipse.jetty.server.handler.gzip.GzipHandler.handle(GzipHandler.java:772)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:127)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.Server.handle(Server.java:516)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.HttpChannel.lambda$handle$1(HttpChannel.java:487)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.HttpChannel.dispatch(HttpChannel.java:732)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.HttpChannel.handle(HttpChannel.java:479)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.server.HttpConnection.onFillable(HttpConnection.java:277)
~[jetty-server-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.AbstractConnection$ReadCallback.succeeded(AbstractConnection.java:311)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:105)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.ssl.SslConnection$DecryptedEndPoint.onFillable(SslConnection.java:555)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.ssl.SslConnection.onFillable(SslConnection.java:410)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.ssl.SslConnection$2.succeeded(SslConnection.java:164)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:105)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.io.ChannelEndPoint$1.run(ChannelEndPoint.java:104)
~[jetty-io-9.4.48.v20220622.jar:9.4.48.v20220622]     at
org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.runTask(EatWhatYouKill.java:338)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.doProduce(EatWhatYouKill.java:315)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.tryProduce(EatWhatYouKill.java:173)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.strategy.EatWhatYouKill.run(EatWhatYouKill.java:131)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.ReservedThreadExecutor$ReservedThread.run(ReservedThreadExecutor.java:409)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:883)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
org.eclipse.jetty.util.thread.QueuedThreadPool$Runner.run(QueuedThreadPool.java:1034)
~[jetty-util-9.4.48.v20220622.jar:9.4.48.v20220622]   at
java.lang.Thread.run(Unknown Source) ~[?:?] Caused by:
java.lang.NumberFormatException: For input string:
&quot;'77777383;+4377777383'&quot;  at
java.lang.NumberFormatException.forInputString(Unknown Source) ~[?:?]
at java.lang.Long.parseLong(Unknown Source) ~[?:?]  at
java.lang.Long.parseLong(Unknown Source) ~[?:?]   at
org.apache.solr.schema.LongPointField.createField(LongPointField.java:161)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.schema.PointField.createFields(PointField.java:270)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DocumentBuilder.addField(DocumentBuilder.java:67)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DocumentBuilder.addOriginalField(DocumentBuilder.java:302)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   at
org.apache.solr.update.DocumentBuilder.toDocument(DocumentBuilder.java:218)
~[solr-core-9.1.1.jar:9.1.1 d998e63978abfedde3b75bab4ba6e1e78ddb5944 -
magibney - 2023-01-17 19:58:00]   ... 111 more 2023-09-08 05:52:53.653
INFO  (searcherExecutor-12-thread-1-processing-vdb) [ x:vdb]
o.a.s.c.QuerySenderListener QuerySenderListener done. 2023-09-08
05:52:53.684 INFO  (searcherExecutor-12-thread-1-processing-vdb) [
x:vdb] o.a.s.c.SolrCore Registered new searcher autowarm time: 22 ms</li>
</ul>
</blockquote>
<p>Does anyone have an idea how I can index this field into solar with NIfi without changing its contents and still have it searchable in Query. I have tried WhiteSpaceTokenizerFactory and  PatternTokenizer without any success.</p>


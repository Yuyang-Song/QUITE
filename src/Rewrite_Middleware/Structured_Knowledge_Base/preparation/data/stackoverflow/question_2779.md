# Apply a function on a partitioned Parquet dataset without a shuffle
[Link to question](https://stackoverflow.com/questions/52063132/apply-a-function-on-a-partitioned-parquet-dataset-without-a-shuffle)
**Creation Date:** 1535476134
**Score:** 0
**Tags:** python, pyspark
## Question Body
<p>I have a reasonably large (~1TB) Parquet dataset partitioned by a column <code>database_id</code>. I want to copy this dataset to a new dataset keeping only those rows where the <code>index</code> column is contained in a separate "special_indexes" table.</p>

<p>My current approach is:</p>

<pre><code>import pyspark.sql.functions as F

big_table = spark.read.parquet("path/to/partitioned/big_table.parquet")
unique_indexes_table = spark.read.parquet("path/to/unique_indexes.parquet")

out = (
    big_table
    .join(F.broadcast(unique_indexes_table), on="index")
    .write
    .save(
        path="{path/to/partitioned/big_table_2.parquet}",
        format='parquet',
        mode='overwrite',
        partitionBy="database_id")
)
</code></pre>

<p>However, this leads to a shuffle and fails with an <code>java.io.IOException: No space left on device</code> error on my 10-node cluster with each node having ~ 900MB of disk space in <code>SPARK_LOCAL_DIRS</code>.</p>

<p>I've been trying to get this to work for days, but have not been successful. I'm contemplating rewriting this in <code>pyarrow</code> where I read the partition and perform a join one at a time, but I can't figure out why <code>pyspark</code> can't do the same thing?</p>

<p>I posted the SQL diagram and the query execution plan below. I'm thinking that the <code>Exchange</code> step is what is causing the problem, and I am not sure why is it necessary?!</p>

<hr>

<p><a href="https://i.sstatic.net/rJYbd.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/rJYbd.png" alt="enter image description here"></a></p>

<pre>
== Parsed Logical Plan ==
'InsertIntoHadoopFsRelationCommand file:/scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet, false, ['database_id], Parquet, Map(path -> /scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet), Overwrite, [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
+- AnalysisBarrier
      +- RepartitionByExpression [database_id#104], 200
         +- Project [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
            +- Join Inner, (__index_level_0__#77L = __index_level_0__#222L)
               :- Relation[uniparc_id#70,sequence#71,database#72,interpro_name#73,interpro_id#74,domain_start#75L,domain_end#76L,__index_level_0__#77L,domain_length#78L,structure_id#79,model_id#80,chain_id#81,pc_identity#82,alignment_length#83,mismatches#84,gap_opens#85,q_start#86,q_end#87,s_start#88,s_end#89,evalue_log10#90,bitscore#91,qseq#92,sseq#93,... 11 more fields] parquet
               +- ResolvedHint (broadcast)
                  +- Relation[__index_level_0__#222L] parquet

== Analyzed Logical Plan ==
InsertIntoHadoopFsRelationCommand file:/scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet, false, [database_id#104], Parquet, Map(path -> /scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet), Overwrite, [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
+- RepartitionByExpression [database_id#104], 200
   +- Project [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
      +- Join Inner, (__index_level_0__#77L = __index_level_0__#222L)
         :- Relation[uniparc_id#70,sequence#71,database#72,interpro_name#73,interpro_id#74,domain_start#75L,domain_end#76L,__index_level_0__#77L,domain_length#78L,structure_id#79,model_id#80,chain_id#81,pc_identity#82,alignment_length#83,mismatches#84,gap_opens#85,q_start#86,q_end#87,s_start#88,s_end#89,evalue_log10#90,bitscore#91,qseq#92,sseq#93,... 11 more fields] parquet
         +- ResolvedHint (broadcast)
            +- Relation[__index_level_0__#222L] parquet

== Optimized Logical Plan ==
InsertIntoHadoopFsRelationCommand file:/scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet, false, [database_id#104], Parquet, Map(path -> /scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet), Overwrite, [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
+- RepartitionByExpression [database_id#104], 200
   +- Project [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
      +- Join Inner, (__index_level_0__#77L = __index_level_0__#222L)
         :- Filter isnotnull(__index_level_0__#77L)
         :  +- Relation[uniparc_id#70,sequence#71,database#72,interpro_name#73,interpro_id#74,domain_start#75L,domain_end#76L,__index_level_0__#77L,domain_length#78L,structure_id#79,model_id#80,chain_id#81,pc_identity#82,alignment_length#83,mismatches#84,gap_opens#85,q_start#86,q_end#87,s_start#88,s_end#89,evalue_log10#90,bitscore#91,qseq#92,sseq#93,... 11 more fields] parquet
         +- ResolvedHint (broadcast)
            +- Filter isnotnull(__index_level_0__#222L)
               +- Relation[__index_level_0__#222L] parquet

== Physical Plan ==
Execute InsertIntoHadoopFsRelationCommand InsertIntoHadoopFsRelationCommand file:/scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet, false, [database_id#104], Parquet, Map(path -> /scratch/username/datapkg_output_dir/uniparc-domain-wstructure/master/remove_duplicate_matches/adjacency_matrix.parquet), Overwrite, [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
+- Exchange hashpartitioning(database_id#104, 200)
   +- *(2) Project [__index_level_0__#77L, uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
      +- *(2) BroadcastHashJoin [__index_level_0__#77L], [__index_level_0__#222L], Inner, BuildRight
         :- *(2) Project [uniparc_id#70, sequence#71, database#72, interpro_name#73, interpro_id#74, domain_start#75L, domain_end#76L, __index_level_0__#77L, domain_length#78L, structure_id#79, model_id#80, chain_id#81, pc_identity#82, alignment_length#83, mismatches#84, gap_opens#85, q_start#86, q_end#87, s_start#88, s_end#89, evalue_log10#90, bitscore#91, qseq#92, sseq#93, ... 11 more fields]
         :  +- *(2) Filter isnotnull(__index_level_0__#77L)
         :     +- *(2) FileScan parquet [uniparc_id#70,sequence#71,database#72,interpro_name#73,interpro_id#74,domain_start#75L,domain_end#76L,__index_level_0__#77L,domain_length#78L,structure_id#79,model_id#80,chain_id#81,pc_identity#82,alignment_length#83,mismatches#84,gap_opens#85,q_start#86,q_end#87,s_start#88,s_end#89,evalue_log10#90,bitscore#91,qseq#92,sseq#93,... 11 more fields] Batched: false, Format: Parquet, Location: InMemoryFileIndex[file:/scratch/username/datapkg_output_dir/uniparc-domain-wstructure/v0.1/contru..., PartitionCount: 1373, PartitionFilters: [], PushedFilters: [IsNotNull(__index_level_0__)], ReadSchema: struct
</pre>


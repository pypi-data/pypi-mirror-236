Copy_options = {
    "kafka": {
        "source_options": {
            "topic": {"type": "text", "editable": False, "optional": False,
                "syntax":"'topic': `'<topic>'`",
                "description":"""The topic to read from"""
            }
        },
        "job_options": {
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            },
            "deduplicate_with": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'deduplicate_with': {'COLUMNS' : ['col1', 'col2'],'WINDOW': 'N HOURS'}",
                "description":"""You can use DEDUPLICATE_WITH to prevent duplicate rows arriving in your target. One or more columns can be supplied in the column list to act as a key so that all events within the timeframe specified in the WINDOW value are deduplicated.
                For example, if you have a third-party application that sends the same event multiple times a day, you can define one or more columns as the key and set the timeframe to be 1 DAY. Upsolver will exclude all duplicate events that arrive within the day, ensuring your target only receives unique events.
                Note that if you have multiple jobs writing to a table in your lake, duplicate rows can be generated, even when you include this option"""
            },
            "consumer_properties": {"type": "text", "editable": True, "optional": True,
                "syntax":"'consumer_properties': `'<consumer_properties>'`",
                "description":"""Additional properties to use when configuring the consumer. This overrides any settings in the Apache Kafka connection"""
            },
            "reader_shards": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'reader_shards': `<integer>`",
                "description":"""Determines how many readers are used in parallel to read the stream.
                This number does not need to equal your number of partitions in Apache Kafka.
                A recommended value would be to increase it by 1 for every 70 MB/s sent to your topic.
                Default: 1"""
            },
            "store_raw_data": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'store_raw_data': True/False",
                "description":"""When true, an additional copy of the data is stored in its original format.
                Default: false"""
            },
            "start_from": {"type": "value", "editable": False, "optional": True,
                "syntax":"'start_from': 'BEGINNING/NOW'",
                "description":"""Configures the time from which to start ingesting data. Files before the specified time are ignored.
                Default: BEGINNING
                Values: { NOW | BEGINNING }"""
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored. Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Values: { NOW | <timestamp> }
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job.
                This option can only be omitted when there is only one cluster in your environment.
                If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "run_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'run_parallelism': `<integer>`",
                "description":"""The number of parser jobs to run in parallel per minute.
                Default: 1"""
            },
            "content_type": {"type": "value", "editable": True, "optional": True,
                "syntax":"'content_type': 'AUTO/CSV/...'",
                "description":"""The file format of the content being read. Note that AUTO only works when reading Avro, JSON, or Parquet. To configure additional options for particular content types, see Content type options.
                Values: { AUTO | CSV | JSON | PARQUET | TSV | AVRO | AVRO_SCHEMA_REGISTRY | FIXED_WIDTH | REGEX | SPLIT_LINES | ORC | XML }
                Default: AUTO"""
            },
            "compression": {"type": "value", "editable": False, "optional": True,
                "syntax":"'compression': 'AUTO/GZIP/...'",
                "description":"""The compression format of the source.
                Values: { AUTO | GZIP | SNAPPY | LZO | NONE | SNAPPY_UNFRAMED | KCL }
                Default: AUTO"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "commit_interval": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'commit_interval': `'<N MINUTE[S]/HOUR[S]/DAY[S]>'`",
                "description":"""Defines how often the job will load and commit data to the target in a direct ingestion job. This interval must be divisible by the number of hours in a day."""
            },
            "skip_validations": {"type": "list", "editable": False, "optional": True,
                "syntax":"'skip_validations': ('MISSING_TOPIC')",
                "description":"""Use this option if data is expected to arrive in the source at a later point in time.
                This option tells Upsolver to ignore specific validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "skip_all_validations": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'skip_all_validations': True/False",
                "description":"""If data is expected to arrive in the source at a later point in time, set this value to true.
                This option instructs Upsolver to ignore all validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            }
        }
    },
    "mysql": {
        "source_options": {
            "table_include_list": {"type": "list", "editable": True, "optional": True,
                "syntax":"'table_include_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match fully-qualified table identifiers of tables whose changes you want to capture. This maps to the Debezium table.include.list property.
                By default, the connector captures changes in every non-system table in all databases. To match the name of a table, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the table.  It does not match substrings that might be present in a table name.
                Default: ''"""
            },
            "column_exclude_list": {"type": "list", "editable": True, "optional": True,
                "syntax":"'column_exclude_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match the fully-qualified names of columns to exclude from change event record values. This maps to Debezium column.exclude.list property.
                By default, the connector matches all columns of the tables listed in TABLE_INCLUDE_LIST. To match the name of a column, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the column; it does not match substrings that might be present in a column name.
                Default: ''"""
            }
        },
        "job_options": {
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "skip_snapshots": {"type": "boolean", "editable": True, "optional": True,
                "syntax":"'skip_snapshots': True/False",
                "description":"""By default, snapshots are enabled for new tables. This means that SQLake will take a full snapshot of the table(s) and ingest it into the staging table before it continues to listen for change events. When set to True, SQLake will not take an initial snapshot and only process change events starting from the time the ingestion job is created.
                In the majority of cases, when you connect to your source tables, you want to take a full snapshot and ingest it as the baseline of your table. This creates a full copy of the source table in your data lake before you begin to stream the most recent change events. If you skip taking a snapshot, you will not have the historical data in the target table, only the newly added or changed rows.
                Skipping a snapshot is useful in scenarios where your primary database instance crashed or became unreachable, failing over to the secondary. In this case, you will need to re-establish the CDC connection but would not want to take a full snapshot because you already have all of the history in your table. In this case, you would want to restart processing from the moment you left off when the connection to the primary database went down"""
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored.
                Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job. This option can only be omitted when there is only one cluster in your environment. If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "snapshot_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'snapshot_parallelism': `<integer>`",
                "description":"""Configures how many snapshots are performed concurrently. The more snapshots performed concurrently, the quicker it is to have all tables streaming. However, doing more snapshots in parallel increases the load on the source database.
                Default: 1"""
            },
            "ddl_filters": {"type": "list", "editable": False, "optional": True,
                "syntax":"'ddl_filters': (`'<filter>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            }
        }
    },
    "postgres": {
        "source_options": {
            "table_include_list": {"type": "list", "editable": False, "optional": False,
                "syntax":"'table_include_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match fully-qualified table identifiers of tables whose changes you want to capture. Tables not included in this list will not be loaded. If the list is left empty all tables will be loaded. This maps to Debezium table.include.list property.
                By default, the connector captures changes in every non-system table in all databases. To match the name of a table, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the table.  It does not match substrings that might be present in a table name.
                Default: ''"""
            },
            "column_exclude_list": {"type": "list", "editable": False, "optional": True,
                "syntax":"'column_exclude_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match the fully-qualified names of columns to exclude from change event record values. This maps to the Debezium column.exclude.list property.
                By default, the connector matches all columns of the tables listed in TABLE_INCLUDE_LIST. To match the name of a column, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the column; it does not match substrings that might be present in a column name.
                Default: ''"""
            }
        },
        "job_options": {
            "heartbeat_table": {"type": "text", "editable": False, "optional": True,
                "syntax":"'heartbeat_table': `'<heartbeat_table>'`",
                "description":"""If it is not set, no heartbeat table is used. Using a heartbeat table is recommended to avoid the replication slot growing indefinitely when no CDC events are captured for the subscribed tables"""
            },
            "skip_snapshots": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'skip_snapshots': True/False",
                "description":"""The snapshot-taking process will be skipped.
                This is a way to skip the original snapshot-taking process for this specific job. The remainder of the job actions will be the same.
                Default: false"""
            },
            "publication_name": {"type": "text", "editable": False, "optional": False,
                "syntax":"'publication_name': `'<publication_name>'`",
                "description":"""Adds a new publication to the current database. The publication name must be distinct from the name of any existing publication in the current database. DDL will be filtered"""
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored. Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Values: { NOW | <timestamp> }
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job. This option can only be omitted when there is only one cluster in your environment. If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            },
            "parse_json_columns": {"type": "boolean", "editable": False, "optional": False,
                "syntax":"'parse_json_columns': True/False",
                "description":"""If enabled, Upsolver will parse JSON columns into a struct matching the JSON value.
                Default: false"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "snapshot_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'snapshot_parallelism': `<integer>`",
                "description":"""Configures how many snapshots are performed concurrently. The more snapshots performed concurrently, the quicker it is to have all tables streaming. However, doing more snapshots in parallel increases the load on the source database.
                Default: 1"""
            },
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            }
        }
    },
    "s3": {
        "source_options": {
            "location": {"type": "text", "editable": False, "optional": False,
                "syntax":"'location': `'<location>'`",
                "description":"""The location to read files from, as a full Amazon S3 URI"""
            }
        },
        "job_options": {
            "date_pattern": {"type": "text", "editable": False, "optional": True,
                "syntax":"'date_pattern': `'<date_pattern>'`",
                "description":"""The date pattern of the partitions on the Amazon S3 bucket to read from. SQLake supports reading from buckets partitioned up to the minute.
                Example: 'yyyy/MM/dd/HH/mm'.
                When you set a DATE_PATTERN, SQLake uses the date in the folder path to understand when new files are added. The date in the path is used to process data in order of arrival, as well as set the $source_time and $event_time system columns used to keep jobs synchronized. If files are added to a folder named with a future date, these files will not be ingested until that date becomes the present.
                If you don’t set a DATE_PATTERN, SQLake will list and ingest files in the ingest job’s BUCKET and PREFIX location as soon as they are discovered. Historical data will also be processed as soon as it is added and discovered by SQLake.
                To discover new files, when a DATE_PATTERN is not set, SQLake lists the top-level prefix and performs a diff to detect newly added files. Subsequently, it lists the paths adjacent to these new files with the assumption that if a file was added here, others will be as well. This process is performed at regular intervals to ensure files are not missed.
                For buckets with few files and predictable changes, this works well. However, for buckets with many changes across millions of files and hundreds of prefixes, the scanning and diffing process may result in ingestion and processing delay. To optimize this process, consider setting the job’s DELETE_FILES_AFTER_LOAD property to TRUE. This moves ingested files to another staging location, leaving the source folder empty, and making it easier and faster for SQLake to discover new files. Be aware that configuring SQLake to move ingested files could impact other systems if they depend on the same raw files.
                To troubleshoot jobs that ingest data, you can query the task execution system table and inspect whether 0 bytes of data have been read in the “ingest data” stage, or SQLake is throwing parse errors in the “parse data” stage. In the case that 0 bytes have been read, it means that your job is configured correctly, but there is no new data. In the case where you see parse errors, you can narrow it down to either a misconfiguration of the job or bad data"""
            },
            "file_pattern": {"type": "text", "editable": False, "optional": True,
                "syntax":"'file_pattern': `'<file_pattern>'`",
                "description":"""Only files that match the provided regex pattern are loaded.
                Use this option to filter out irrelevant data. For example, you could filter by a suffix to only keep .parquet files in a folder that may have some additional files that should not be ingested.
                Default: ''"""
            },
            "initial_load_pattern": {"type": "text", "editable": False, "optional": True,
                "syntax":"'initial_load_pattern': `'<initial_load_pattern>'`",
                "description":"""Any file matching this regex pattern is immediately loaded when the job is run.
                This loads data separately from the date pattern and is primarily used in CDC use cases, where you load some initial files named LOAD00001, LOAD00002, etc. After that, all the data has a date pattern in the file name"""
            },
            "initial_load_prefix": {"type": "text", "editable": False, "optional": True,
                "syntax":"'initial_load_prefix': `'<initial_load_prefix>'`",
                "description":"""Any file matching this prefix is immediately loaded when the job is run"""
            },
            "delete_files_after_load": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'delete_files_after_load': True/False",
                "description":"""When true, files are deleted from the storage source once they have been ingested into the target location within your metastore.
                This allows Upsolver to discover new files immediately, regardless of how many files are in the source, or what file names and patterns are used.
                Default: false"""
            },
            "deduplicate_with": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'deduplicate_with': {'COLUMNS' : ['col1', 'col2'],'WINDOW': 'N HOURS'}",
                "description":"""You can use DEDUPLICATE_WITH to prevent duplicate rows arriving in your target. One or more columns can be supplied in the column list to act as a key so that all events within the timeframe specified in the WINDOW value are deduplicated.
                For example, if you have a third-party application that sends the same event multiple times a day, you can define one or more columns as the key and set the timeframe to be 1 DAY. Upsolver will exclude all duplicate events that arrive within the day, ensuring your target only receives unique events.
                Note that if you have multiple jobs writing to a table in your lake, duplicate rows can be generated, even when you include this option.
                Values: ( {COLUMNS = (, ...) | COLUMN = }, WINDOW = { MINUTE[S] | HOUR[S] | DAY[S] } ) """
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored. Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Values: { NOW | <timestamp> }
                Default: Never"""
            },
            "start_from": {"type": "value", "editable": False, "optional": True,
                "syntax":"'start_from': `'<timestamp>/NOW/BEGINNING'`",
                "description":"""Configures the time to start ingesting data. Files before the specified time are ignored. Timestamps should be in the UTC time format.
                When a DATE_PATTERN is not specified, configuring this option is not allowed. By default, all available data is ingested.
                If the DATE_PATTERN is not lexicographically ordered, then this option cannot be set to BEGINNING.
                Values: { NOW | BEGINNING | <timestamp> }
                Default: BEGINNING"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job. This option can only be omitted when there is only one cluster in your environment. If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "run_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'run_parallelism': `<integer>`",
                "description":"""The number of parser jobs to run in parallel per minute.
                Default: 1"""
            },
            "content_type": {"type": "value", "editable": True, "optional": True,
                "syntax":"'content_type': 'AUTO/CSV...'",
                "description":"""Values: { AUTO | CSV | JSON | PARQUET | TSV | AVRO | AVRO_SCHEMA_REGISTRY | FIXED_WIDTH | REGEX | SPLIT_LINES | ORC | XML }
                Default: AUTO
                The file format of the content being read.
                Note that AUTO only works when reading Avro, JSON, or Parquet"""
            },
            "compression": {"type": "value", "editable": False, "optional": True,
                "syntax":"'compression': 'AUTO/GZIP...'",
                "description":"""The compression of the source.
                Default: AUTO"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "commit_interval": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'commit_interval': `'<N MINUTE[S]/HOUR[S]/DAY[S]>'`",
                "description":"""Defines how often the job will load and commit data to the target in a direct ingestion job. This interval must be divisible by the number of hours in a day."""
            },
            "skip_validations": {"type": "list", "editable": False, "optional": True,
                "syntax":"'skip_validations': ('EMPTY_PATH')",
                "description":"""Use this option if data is expected to arrive in the source at a later point in time.
                This option tells Upsolver to ignore specific validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "skip_all_validations": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'skip_all_validations': True/False",
                "description":"""If data is expected to arrive in the source at a later point in time, set this value to true.
                This option instructs Upsolver to ignore all validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            }
        }
    },
    "kinesis": {
        "source_options": {
            "stream": {"type": "text", "editable": False, "optional": False,
                "syntax":"'stream': `'<stream>'`",
                "description":"""The stream to read from"""
            }
        },
        "job_options": {
            "reader_shards": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'reader_shards': `<integer>`",
                "description":"""Determines how many readers are used in parallel to read the stream.
                This number does not need to equal your number of shards in Kinesis.
                A recommended value would be to increase it by 1 for every 70 MB/s sent to your stream.
                Default: 1"""
            },
            "store_raw_data": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'store_raw_data': True/False",
                "description":"""When true, an additional copy of the data is stored in its original format.
                Default: false"""
            },
            "start_from": {"type": "value", "editable": False, "optional": True,
                "syntax":"'start_from': `'<timestamp>/NOW/BEGINNING'`",
                "description":"""Configures the time to start ingesting data. Files dated before the specified time are ignored.
                Values: { NOW | BEGINNING }
                Default: BEGINNING"""
            },
            "end_at": {"type": "value", "editable": False, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored. Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Values: { NOW | <timestamp> }
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job.
                This option can only be omitted when there is only one cluster in your environment.
                If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "run_parallelism": {"type": "integer", "editable": False, "optional": True,
                "syntax":"'run_parallelism': `<integer>`",
                "description":"""The number of parser jobs to run in parallel per minute.
                Default: 1"""
            },
            "content_type": {"type": "value", "editable": True, "optional": True,
                "syntax":"'content_type': 'AUTO/CSV...'",
                "description":"""The file format of the content being read.
                Note that AUTO only works when reading Avro, JSON, or Parquet.
                To configure additional options for certain content types, see Content type options.
                Values: { AUTO | CSV | JSON | PARQUET | TSV | AVRO | AVRO_SCHEMA_REGISTRY | FIXED_WIDTH | REGEX | SPLIT_LINES | ORC | XML }
                Default: AUTO"""
            },
            "compression": {"type": "value", "editable": False, "optional": True,
                "syntax":"'compression': 'AUTO/GZIP...'",
                "description":"""The compression of the source.
                Values: { AUTO | GZIP | SNAPPY | LZO | NONE | SNAPPY_UNFRAMED | KCL }
                Default: AUTO"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            },
            "column_transformations": {"type": "dict", "editable": True, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "deduplicate_with": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'deduplicate_with': {'COLUMNS' : ['col1', 'col2'],'WINDOW': 'N HOURS'}",
                "description":"""You can use DEDUPLICATE_WITH to prevent duplicate rows arriving in your target. One or more columns can be supplied in the column list to act as a key so that all events within the timeframe specified in the WINDOW value are deduplicated.
                For example, if you have a third-party application that sends the same event multiple times a day, you can define one or more columns as the key and set the timeframe to be 1 DAY. Upsolver will exclude all duplicate events that arrive within the day, ensuring your target only receives unique events.
                Note that if you have multiple jobs writing to a table in your lake, duplicate rows can be generated, even when you include this option.
                Values: ( {COLUMNS = (, ...) | COLUMN = }, WINDOW = { MINUTE[S] | HOUR[S] | DAY[S] } ) """
            },
            "commit_interval": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'commit_interval': `'<N MINUTE[S]/HOUR[S]/DAY[S]>'`",
                "description":"""Defines how often the job will load and commit data to the target in a direct ingestion job. This interval must be divisible by the number of hours in a day."""
            },
            "skip_validations": {"type": "list", "editable": False, "optional": True,
                "syntax":"'skip_validations': ('MISSING_STREAM')",
                "description":"""Use this option if data is expected to arrive in the source at a later point in time.
                This option tells Upsolver to ignore specific validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "skip_all_validations": {"type": "boolean", "editable": False, "optional": True,
                "syntax":"'skip_all_validations': True/False",
                "description":"""If data is expected to arrive in the source at a later point in time, set this value to true.
                This option instructs Upsolver to ignore all validations to allow you to create a job that reads from a source that currently has no data."""
            },
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            }
        }
    },
    "mssql": {
        "source_options": {
            "table_include_list": {"type": "list", "editable": True, "optional": True,
                "syntax":"'table_include_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match fully-qualified table identifiers of tables whose changes you want to capture. This maps to the Debezium table.include.list property.
                By default, the connector captures changes in every non-system table in all databases. To match the name of a table, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the table.  It does not match substrings that might be present in a table name.
                Default: ''"""
            },
            "column_exclude_list": {"type": "list", "editable": True, "optional": True,
                "syntax":"'column_exclude_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match the fully-qualified names of columns to exclude from change event record values. This maps to Debezium column.exclude.list property.
                By default, the connector matches all columns of the tables listed in TABLE_INCLUDE_LIST. To match the name of a column, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the column; it does not match substrings that might be present in a column name.
                Default: ''"""
            }
        },
        "job_options": {
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "skip_snapshots": {"type": "boolean", "editable": True, "optional": True,
                "syntax":"'skip_snapshots': True/False",
                "description":"""By default, snapshots are enabled for new tables. This means that SQLake will take a full snapshot of the table(s) and ingest it into the staging table before it continues to listen for change events. When set to True, SQLake will not take an initial snapshot and only process change events starting from the time the ingestion job is created.
                In the majority of cases, when you connect to your source tables, you want to take a full snapshot and ingest it as the baseline of your table. This creates a full copy of the source table in your data lake before you begin to stream the most recent change events. If you skip taking a snapshot, you will not have the historical data in the target table, only the newly added or changed rows.
                Skipping a snapshot is useful in scenarios where your primary database instance crashed or became unreachable, failing over to the secondary. In this case, you will need to re-establish the CDC connection but would not want to take a full snapshot because you already have all of the history in your table. In this case, you would want to restart processing from the moment you left off when the connection to the primary database went down"""
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored.
                Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job. This option can only be omitted when there is only one cluster in your environment. If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "snapshot_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'snapshot_parallelism': `<integer>`",
                "description":"""Configures how many snapshots are performed concurrently. The more snapshots performed concurrently, the quicker it is to have all tables streaming. However, doing more snapshots in parallel increases the load on the source database.
                Default: 1"""
            },
            "parse_json_columns": {"type": "boolean", "editable": False, "optional": False,
                "syntax":"'parse_json_columns': True/False",
                "description":"""If enabled, Upsolver will parse JSON columns into a struct matching the JSON value.
                Default: false"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            }
        }
    },
    "mongodb": {
        "source_options": {
            "collection_include_list": {"type": "list", "editable": True, "optional": True,
                "syntax":"'collection_include_list': (`'<regexFilter>'`, ...)",
                "description":"""Comma-separated list of regular expressions that match fully-qualified table identifiers of tables whose changes you want to capture. This maps to the Debezium table.include.list property.
                By default, the connector captures changes in every non-system table in all databases. To match the name of a table, SQLake applies the regular expression that you specify as an anchored regular expression. That is, the specified expression is matched against the entire name string of the table.  It does not match substrings that might be present in a table name.
                Default: ''"""
            }
        },
        "job_options": {
            "exclude_columns": {"type": "list", "editable": False, "optional": True,
                "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
                "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
                When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
                Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target"""
            },
            "column_transformations": {"type": "dict", "editable": False, "optional": True,
                "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
                "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
                However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
                If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection"""
            },
            "skip_snapshots": {"type": "boolean", "editable": True, "optional": True,
                "syntax":"'skip_snapshots': True/False",
                "description":"""By default, snapshots are enabled for new tables. This means that SQLake will take a full snapshot of the table(s) and ingest it into the staging table before it continues to listen for change events. When set to True, SQLake will not take an initial snapshot and only process change events starting from the time the ingestion job is created.
                In the majority of cases, when you connect to your source tables, you want to take a full snapshot and ingest it as the baseline of your table. This creates a full copy of the source table in your data lake before you begin to stream the most recent change events. If you skip taking a snapshot, you will not have the historical data in the target table, only the newly added or changed rows.
                Skipping a snapshot is useful in scenarios where your primary database instance crashed or became unreachable, failing over to the secondary. In this case, you will need to re-establish the CDC connection but would not want to take a full snapshot because you already have all of the history in your table. In this case, you would want to restart processing from the moment you left off when the connection to the primary database went down"""
            },
            "end_at": {"type": "value", "editable": True, "optional": True,
                "syntax":"'end_at': `'<timestamp>/NOW'`",
                "description":"""Configures the time to stop ingesting data. Files after the specified time are ignored.
                Timestamps should be based on UTC and in the following format: TIMESTAMP 'YYYY-MM-DD HH:MM:SS'
                Default: Never"""
            },
            "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
                "syntax":"'compute_cluster': `'<compute_cluster>'`",
                "description":"""The compute cluster to run this job. This option can only be omitted when there is only one cluster in your environment. If you have more than one compute cluster, you need to determine which one to use through this option.
                Default: The sole cluster in your environment"""
            },
            "snapshot_parallelism": {"type": "integer", "editable": True, "optional": True,
                "syntax":"'snapshot_parallelism': `<integer>`",
                "description":"""Configures how many snapshots are performed concurrently. The more snapshots performed concurrently, the quicker it is to have all tables streaming. However, doing more snapshots in parallel increases the load on the source database.
                Default: 1"""
            },
            "comment": {"type": "text", "editable": True, "optional": True,
                "syntax":"'comment': `'<comment>'`",
                "description":"""A description or comment regarding this job"""
            }
        }
    }
}

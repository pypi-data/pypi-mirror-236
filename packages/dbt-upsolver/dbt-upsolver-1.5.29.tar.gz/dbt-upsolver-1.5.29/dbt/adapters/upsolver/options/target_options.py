# use for ingression job to incert into target
Target_options = {
    "datalake": {
        "globally_unique_keys": {"type": "boolean", "editable": False, "optional": True,
            "syntax":"'globally_unique_keys': True/False",
            "description":""" By default, partition keys are implicitly part of the primary key. This means that when upserting, only rows with the same primary key and partition are replaced. This is the more performant and therefore recommended option.
            However, some use cases may require that the primary keys be globally unique (in other words, unique across partitions). This means that when upserting, rows with the same primary key should be replaced, even if they belong to different partitions. Note that this also means that rows can "switch" partitions.
            If such is the case, you should set this option as true.
            Default: false"""},
        "storage_connection": {"type": "value", "editable": False, "optional": True,
            "syntax":"'storage_connection': `'<storage_connection>'`",
            "description":"""The storage connection associated with the STORAGE_LOCATION for the table's underlying files.
            Only a storage type connection can be used here (e.g. S3, Blob storage, GCS, Oracle object storage), and it should match the catalog's metastore. For example, if Glue is used as the metastore, only S3 is allowed as a storage connection.
            When set, STORAGE_LOCATION must be configured as well to provide a path to store the data.
            Default: Default storage connection configured for the metastore connection this table is created under"""},
        "storage_location": {"type": "text", "editable": False, "optional": True,
            "syntax":"'storage_location': `'<storage_location>'`",
            "description":"""The storage location for the table's underlying files.
            For S3, it should be provided in the format s3://bucket_name/path_to_data.
            This option is required when STORAGE_CONNECTION is set.
            When set, STORAGE_CONNECTION must be configured as well to provide a connection with access to write to the specified storage location.
            Default: Default storage location configured for the metastore connection this table is created under"""},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
            "syntax":"'compute_cluster': `'<compute_cluster>'`",
            "description":"""The compute cluster that processes the table.
            This option can only be omitted when there is just one cluster in your environment.
            Once you have more than one compute cluster, you are required to provide which one to use through this option.
            Default: The sole cluster in your environment"""},
        "compression": {"type": "value", "editable": True, "optional": True,
            "syntax":"'compression': 'SNAPPY/GZIP'",
            "description":"""Type of compression for the table data.
            Values: { SNAPPY | GZIP }
            Default: SNAPPY"""},
        "compaction_processes": {"type": "integer", "editable": True, "optional": True,
            "syntax":"'compaction_processes': `<integer>`",
            "description":""" This determines the number of compaction processes your table can do in parallel when it periodically compacts your data.
            Default: 1"""},
        "disable_compaction": {"type": "boolean", "editable": True, "optional": True,
            "syntax":"'disable_compaction': True/False",
            "description":"""When true, disables the compaction process.
            Default: false"""},
        "retention_date_partition": {"type": "value", "editable": False, "optional": True,
            "syntax":"'retention_date_partition': `'<column>'`",
            "description":"""This configures the partition column to use to determine whether the retention period has passed for a given record.
            This option is required if you have more than one date partition column.
            Default: The only partition column of type date"""},
        "table_data_retention": {"type": "integer", "editable": True, "optional": True,
            "syntax":"'table_data_retention': `'<N DAYS>'`",
            "description":"""When set, data in partitions that have passed the retention period are deleted from the table. Number of days can range between 1 and 9999.
            This option is not a deterministic mechanism that deletes data when it immediately surpasses the defined threshold. This mechanism is closer to the lifecycle policies on common blob storage services, such as Amazon S3, and is designed to save storage costs, not to delete data based on a specific time. Therefore when data passes the retention period, it will be deleted at some point in the future, and can no longer be relied to exist, though Upsolver aims to delete it within a reasonable timeframe.
            You should be aware that transformation job that reads from a table with a defined data retention may or may not read data that has surpassed the retention threshold.
            For example, if the current time is 2023-02-23 12:30:00 UTC, and you have defined TABLE_DATA_RETENTION = 2 days, you can expect data written during 2023-02-23, 2023-02-22, and 2023-02-21 to exist in the table. The retention threshold truncates data to the nearest day, so when the time changes to 2023-02-24 00:00:00 UTC, you can no longer expect data from 2023-02-21 to be present in the table, although it might be there for a while.
            Note that you need at least one date partition column for this option to work.
            Value: <integer> DAYS"""},
        "column_data_retention": {"type": "list_dict", "editable": True, "optional": True,
            "syntax":"'column_data_retention': ({'COLUMN' : `'<column>'`,'DURATION': `'<N DAYS>'`})",
            "description":"""When set, after the duration of a column elapses in a partition, the data is rewritten without the contents of that column. Number of days can range between 1 and 9999.
            Note that you need at least one date partition column for this to work.
            Type: list of (<column_name>, <integer> DAYS) pairs"""},
        "comment": {"type": "text", "editable": True, "optional": True,
            "syntax":"'comment': `'<comment>'`",
            "description":"""A description or comment regarding this table"""}
  },
    "materialized_view": {
        "storage_connection": {"type": "value", "editable": False, "optional": True,
            "syntax":"'storage_connection': `'<storage_connection>'`",
            "description":"""The storage connection associated with the STORAGE_LOCATION for the table's underlying files.
            Only a storage type connection can be used here (e.g. S3, Blob storage, GCS, Oracle object storage), and it should match the catalog's metastore. For example, if Glue is used as the metastore, only S3 is allowed as a storage connection.
            When set, STORAGE_LOCATION must be configured as well to provide a path to store the data.
            Default: The storage  connection of the first table in the FROM statement"""},
        "storage_location": {"type": "text", "editable": False, "optional": True,
            "syntax":"'storage_location': `'<storage_location>'`",
            "description":"""The storage location for the materialized view's underlying files. It should be provided in the format s3://bucket_name/path_to_data. This option is required when STORAGE_CONNECTION is set.
            When set, STORAGE_CONNECTION must be configured as well to provide a connection with access to write to the specified storage location.
            Default: The storage location of the first table in the FROM statement"""},
        "max_time_travel_duration": {"type": "integer", "editable": True, "optional": True,
            "syntax":"'max_time_travel_duration': `'<N DAYS>'`",
            "description":"""How long, in days, the state information maintained by the materialized view should be retained. By default, the state is maintained indefinitely, allowing you to time travel to any point in time from the creation of the MV.
            Default: infinite"""},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True,
            "syntax":"'compute_cluster': `'<compute_cluster>'`",
            "description":"""The compute cluster that processes the materialized view.
            Default: The compute cluster of the first source table within the SELECT statement"""}
    },
    "snowflake": {
        "column_transformations": {"type": "dict", "editable": False, "optional": True,
            "syntax":"'column_transformations': {`'<column>'` : `'<expression>'` , ...}",
            "description":"""If transformations must be applied prior to data landing in your target, you can use this option to perform data transformations during ingestion. When ingesting into the data lake, it is recommended that you only apply essential transformations, such as protecting PII, as it is easier to make amendments or corrections at a later date if the data remains in its raw state and instead use a transformation job to apply modifications. Therefore, as a general rule, you should only transform data that must be modified before it reaches the target.
            However, transformations provide the flexibility to shape your data before it lands in the target. You can use all the functions and operators supported by Upsolver to create calculated fields within your ingestion job. New columns can be added to your target, and existing column data can be transformed. You can perform actions such as converting data types, formatting string values, and concatenating columns to create a new column.
            If you need to mask sensitive or personally identifiable information (PII) prior to loading into your staging tables or when performing direct ingestion into your target destination, you can use hashing functions to prevent data from being exposed downstream. Combining hash functions with the EXCLUDE_COLUMNS option enables you to control your data protection.
            Values: ( <column> = <expression>, ...)"""},
        "deduplicate_with": {"type": "dict", "editable": False, "optional": True,
            "syntax":"'deduplicate_with': {'COLUMNS' : ['col1', 'col2'],'WINDOW': 'N HOURS'}",
            "description":""" You can use DEDUPLICATE_WITH to prevent duplicate rows arriving in your target. One or more columns can be supplied in the column list to act as a key so that all events within the timeframe specified in the WINDOW value are deduplicated.
            For example, if you have a third-party application that sends the same event multiple times a day, you can define one or more columns as the key and set the timeframe to be 1 DAY. Upsolver will exclude all duplicate events that arrive within the day, ensuring your target only receives unique events.
            Note that if you have multiple jobs writing to a table in your lake, duplicate rows can be generated, even when you include this option.
            Values: ( {COLUMNS = (, ...) | COLUMN = }, WINDOW = { MINUTE[S] | HOUR[S] | DAY[S] } )"""},
        "exclude_columns": {"type": "list", "editable": False, "optional": True,
            "syntax":"'exclude_columns': (`'<exclude_column>'`, ...)",
            "description":"""The EXCLUDE_COLUMNS option tells Upsolver to ignore data in the columns specified in this list, and the column is not created on the target. To exclude columns, provide a single column or a list of column names, or use a glob pattern.
            When you simply don't need columns, you want to save storage space, or maintain a clean data structure, use EXCLUDE_COLUMNS and the specified columns will be ignored. This option gives you control over the width of the target table by enabling you to manage how many columns are created. If your target system has a limit on the number of columns it supports, continuously adding columns can cause issues.
            Furthermore, columns containing sensitive information can be excluded, ensuring private data is not copied downstream to a staging table in your data lake, or directly into your target.
            Values: ( <column>, ...)"""},
        "create_table_if_missing": {"type": "boolean", "editable": False, "optional": True,
            "syntax":"'create_table_if_missing': True/False}",
            "description":""" """},
        "run_interval": {"type": "integer", "editable": False, "optional": True,
            "syntax":"'run_interval': `'<N MINUTES/HOURS/DAYS>'`",
            "description":"""How often the job runs.
            The runs take place over a set period of time defined by this interval and they must be divisible by the number of hours in a day."""},
        "add_missing_columns": {"type": "boolean", "editable": False, "optional": True,
            "syntax":"'add_missing_columns': True/False",
            "description":"""When true, columns that don't exist in the target table are added automatically when encountered.
            Default: false"""}
    }
}

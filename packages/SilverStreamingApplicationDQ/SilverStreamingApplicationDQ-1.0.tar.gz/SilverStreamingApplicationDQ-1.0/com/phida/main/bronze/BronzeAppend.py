import datetime

from pyspark.sql import Window
from pyspark.sql.functions import lit, to_timestamp, row_number, col

from com.phida.main.Operations import tableExists, createDeltaTable, schemaDiff, \
    schemaDataTypeDiff, hiveDDL, alterDeltaTable, initialMultilineRead, multilineRead
from com.phida.main.sparksession import logger, spark
from com.phida.main.utils import filePathExists, convertStrToList, pathExists


class BronzeAppend:
    """
    A streaming pipeline for cleansing incremental data from Raw file and append into Bronze

    args:
        srcFilePath: String - Source File (Raw Data File)
        tgtDatabaseName: String - Target Database Name (Will be created if not exists)
        tgtTableName: String - Target Table Name (Will be created if not exists)
        tgtTablePath: String - Target Table Path (so that the table is created as external)
        tgtTableKeyColumns: String - Column names separated by comma to help identify the primary key for the target table
        tgtPartitionColumns: String - Target partition columns (optional)
        triggerOnce: String - Whether continuous streaming or just once

    methods:
        bronzeCleansing
        prepareTarget

    example:
        from com.phida.main.bronze.BronzeAppend import BronzeAppend
        bronzeAppendObj = BronzeAppend(srcFilePath, tgtDatabaseName, tgtTableName,
                                        tgtTablePath, tgtTableKeyColumns, tgtPartitionColumns, triggerOnce)

    """

    def __init__(self, srcFilePath, tgtDatabaseName, tgtTableName, tgtTablePath, tgtTableKeyColumns,
                 tgtPartitionColumns, triggerOnce):
        """
        desc:
            Initialize the required class variables

        args:
            srcFilePath: String - Source File Path(Raw Data File. Currently, supports only .csv files)
            tgtDatabaseName: String - Target Database Name (Will be created if not exists)
            tgtTableName: String - Target Table Name (Will be created if not exists)
            tgtTablePath: String - Target Table Path (so that the table is created as external)
            tgtTableKeyColumns: String - Column names separated by comma to help identify the primary key
                                         for the target table
            tgtPartitionColumns: String - Target partition columns (optional)
            triggerOnce: String - Whether continuous streaming or just once

        """

        logger.info("phida_log: Initialising class variables for raw to bronze delta transfer")

        self.srcFilePath = srcFilePath
        self.tgtDatabaseName = tgtDatabaseName
        self.tgtTableName = tgtTableName
        self.tgtTablePath = tgtTablePath
        self.tgtTableKeyColumns = tgtTableKeyColumns
        self.tgtPartitionColumns = tgtPartitionColumns
        self.triggerOnce = triggerOnce

        if filePathExists(self.srcFilePath):
            logger.info(f"phida_log: source file exists")
            logger.info(f"phida_log: initialising derived class variables")

            self.keyColsList = convertStrToList(self.tgtTableKeyColumns, ",")

            utc_now = datetime.datetime.utcnow()
            self.currentDate = utc_now.strftime("%-m/%-d/%Y")

            self.columnsToBeAppendedInBronze = ['source_operation', 'src_key_cols', 'ADLS_LOADED_DATE']

    def writeDataframeToBronzeTable(self, change_df):
        """
        desc:
            A Function to write DF to target table

        args:
            change_df: DataFrame - DataFrame created from source file

        return:
            None - Does not return anything

        example:
            writeDataframeToBronzeTable(inserts_df)

        tip:
            N/A
        """
        change_df.write \
            .format("delta") \
            .option("mergeSchema", True) \
            .mode("append") \
            .saveAsTable(f"{self.tgtDatabaseName}.{self.tgtTableName}")

    def appendInsertsToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify inserts b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendInsertsToBronze(source_df, target_df)

        tip:
            N/A
        """
        inserts_df = source_df.join(target_df, self.keyColsList, "leftanti") \
            .withColumn("source_operation", lit("1")) \
            .withColumn("src_key_cols", lit(self.tgtTableKeyColumns)) \
            .withColumn("ADLS_LOADED_DATE", lit(self.currentDate))

        self.writeDataframeToBronzeTable(inserts_df)

        logger.info(f"phida_log: Inserts data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendUpdatesToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify updates b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendDeletesToBronze(source_df, target_df)

        tip:
            N/A
        """
        updates_df = source_df.alias("source") \
            .join(target_df.alias("target"), self.keyColsList) \
            .select("source.*") \
            .filter(to_timestamp(col("source.UPDATESTAMP"), "M/d/yyyy h:mm:ss a") >
                    to_timestamp(col("target.UPDATESTAMP"), "M/d/yyyy h:mm:ss a")) \
            .withColumn("source_operation", lit("2")) \
            .withColumn("src_key_cols", lit(self.tgtTableKeyColumns)) \
            .withColumn("ADLS_LOADED_DATE", lit(self.currentDate))

        self.writeDataframeToBronzeTable(updates_df)

        logger.info(f"phida_log: Appends data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendDeletesToBronze(self, source_df, target_df):
        """
        desc:
            A Function to identify deletes b/w source DF and target DF and append it to target table

        args:
            source_df: DataFrame - DataFrame created from source file
            target_df: DatFrame - DataFrame created from target table

        return:
            None - Does not return anything

        example:
            appendDeletesToBronze(source_df, target_df)

        tip:
            N/A
        """
        deletes_df = target_df.join(source_df, self.keyColsList, "leftanti") \
            .withColumn("source_operation", lit("0")) \
            .withColumn("src_key_cols", lit(self.tgtTableKeyColumns)) \
            .withColumn("ADLS_LOADED_DATE", lit(self.currentDate))

        self.writeDataframeToBronzeTable(deletes_df)

        logger.info(f"phida_log: Deletes data added into bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

    def appendChangesToBronze(self, source_df):
        """
        desc:
            A Function to help in appending change data into the bronze target

        args:
            None

        return:
            None - Does not return anything

        example:
            appendChangesToBronze()

        tip:
            N/A
        """
        target_df = spark.read.table(f"{self.tgtDatabaseName}.{self.tgtTableName}")

        window_spec = Window.partitionBy(*self.keyColsList).orderBy(
            to_timestamp(target_df.UPDATESTAMP, "M/d/yyyy h:mm:ss a").desc())

        target_filtered_df = target_df.withColumn("row_num", row_number().over(window_spec)) \
            .filter("row_num == 1") \
            .filter(target_df.source_operation != "0") \
            .drop("row_num")

        self.appendInsertsToBronze(source_df, target_filtered_df)
        self.appendUpdatesToBronze(source_df, target_filtered_df)
        self.appendDeletesToBronze(source_df, target_filtered_df)

    def checkForSchemaChanges(self, source_df, existing_df):
        """
        desc:
            A Function for checking schema changes between the source file DF and the target bronze table DF

        args:
            None

        return:
            None - Does not return anything

        example:
            see method ingestToBronzeTarget() for usage()

        tip:
            N/A
        """
        diff2_df = schemaDiff(existing_df, source_df)
        missing_cols = list(set(diff2_df.columns) - set(self.columnsToBeAppendedInBronze))
        if missing_cols:
            raise Exception(f"Column(s) {missing_cols} is(are) missing")

        mismatched_columns = schemaDataTypeDiff(existing_df, source_df)
        missing_cols = list(set(mismatched_columns) - set(self.columnsToBeAppendedInBronze))
        if missing_cols:
            raise Exception(f"There is data type mismatch in column(s): {missing_cols}")

        diff_df = schemaDiff(source_df, existing_df)
        add_columns = hiveDDL(diff_df)
        if add_columns:
            logger.info(f"phida_log: There seems to be a schema change in bronze")
            logger.info(f"phida_log: Altering the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            alterDeltaTable(self.tgtDatabaseName, self.tgtTableName, add_columns)

            logger.info(f"phida_log: newly added columns {add_columns}")
        else:
            logger.info(f"phida_log: There is no change in schema in bronze")

    def ingestToBronzeTarget(self):
        """
        desc:
            A Function for appending the records from the source into delta Target table

        args:
            None

        return:
            None - Does not return anything

        example:
            ingestToBronzeTarget()

        tip:
            Make sure the values provided in the notebook are correct
        """

        logger.info(f"phida_log: preparing the target delta table ")

        target_path_exists = pathExists(self.tgtTablePath)

        target_table_exists = tableExists(self.tgtDatabaseName, self.tgtTableName)

        if target_path_exists and not target_table_exists:
            raise Exception(f"phida_log: {self.tgtDatabaseName}.{self.tgtTableName} cannot be created"
                            f" because {self.tgtTablePath} already exists. Clean the path and run again.")

        first_run = False if target_table_exists else True

        if first_run:
            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            source_df = initialMultilineRead(self.srcFilePath, "|", True)

            createDeltaTable(source_df,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

            raw_refined_df = source_df.withColumn("source_operation", lit("1").cast("string")) \
                .withColumn("src_key_cols", lit(self.tgtTableKeyColumns).cast("string")) \
                .withColumn("ADLS_LOADED_DATE", lit(self.currentDate).cast("string"))

            raw_refined_df.write \
                .format("delta") \
                .option("overwriteSchema", "true") \
                .mode("overwrite") \
                .saveAsTable(f"{self.tgtDatabaseName}.{self.tgtTableName}")

            logger.info(
                f"phida_log: first write into bronze table {self.tgtDatabaseName}.{self.tgtTableName} completed")
        else:
            existing_df = spark.read.table(self.tgtDatabaseName + "." + self.tgtTableName)
            ddl_schema = hiveDDL(existing_df, self.columnsToBeAppendedInBronze)
            source_df = multilineRead(self.srcFilePath, ddl_schema, "|", True)

            self.checkForSchemaChanges(source_df, existing_df)

            logger.info(f"phida_log: Appending data change to bronze table {self.tgtDatabaseName}.{self.tgtTableName}")

            self.appendChangesToBronze(source_df)


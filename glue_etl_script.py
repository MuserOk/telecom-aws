import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import to_date, year

    # Inicializar Glue context
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

    # Leer datos del Glue Data Catalog
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="telecom_db", table_name="example_data_csv")

    # Convertir DynamicFrame a DataFrame
dataframe = datasource0.toDF()

    # Transformaciones
dataframe = dataframe.withColumn("fecha_inicio", to_date("fecha_inicio", "yyyy-MM-dd"))\
    .withColumn("fecha_fin", to_date("fecha_fin", "yyyy-MM-dd"))\
    .withColumn("anio_inicio", year("fecha_inicio"))

    # Escribir los datos transformados a S3
glueContext.write_dynamic_frame.from_options(frame = DynamicFrame.fromDF(dataframe, glueContext, "transformed_data"), connection_type = "s3", connection_options = {"path": "s3://telecom-datalake-s3/transformed_data/"}, format = "parquet")

job = Job(glueContext)
job.init("etl_job", {})
job.commit()
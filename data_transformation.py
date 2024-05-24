from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    lag,
    lead,
    unix_timestamp,
    when,
    min,
    max,
    sum,
    lit,
    date_format,
)
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder.appName("AttendanceFilter").getOrCreate()

# Read the data
df = spark.read.option("header", "true").csv("data/ingestion/historic_attendance.csv")

# Convert Time column to timestamp
df = df.withColumn("Time", col("Time").cast("timestamp"))

# Extract date from timestamp to handle day changes
df = df.withColumn("Date", date_format(col("Time"), "yyyy-MM-dd"))

# Define window specification
window_spec = Window.partitionBy("Name").orderBy("Time")

# Identify session changes
df = df.withColumn("prev_status", lag("Status", 1).over(window_spec))
df = df.withColumn("prev_date", lag("Date", 1).over(window_spec))
df = df.withColumn(
    "session_change",
    when(
        (col("Status") == "IN")
        & ((col("prev_status") == "OUT") | (col("Date") != col("prev_date"))),
        1,
    ).otherwise(0),
)

# Generate session_id using a cumulative sum over session_change
df = df.withColumn(
    "session_id",
    sum("session_change").over(
        window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow)
    ),
)

# Pair IN and OUT records by matching session_id
paired_df = df.withColumn(
    "paired_time",
    when(col("Status") == "IN", col("Time")).otherwise(
        lead("Time", 1).over(window_spec)
    ),
)

# Filter out incomplete pairs
paired_df = paired_df.filter(
    (col("Status") == "IN")
    | ((col("Status") == "OUT") & col("paired_time").isNotNull())
)

# Aggregate to get first IN and last OUT for each session
final_df = paired_df.groupBy("Name", "session_id").agg(
    min(when(col("Status") == "IN", col("Time"))).alias("first_in"),
    max(when(col("Status") == "OUT", col("Time"))).alias("last_out"),
)

# Filter out rows where first_in or last_out is NULL
final_df = final_df.filter(col("first_in").isNotNull() & col("last_out").isNotNull())

# Show the filtered data (for debugging purposes)
final_df.show()

# Save the transformed data back to a CSV file
final_df.write.option("header", "true").csv(
    "data/transformation/transformed_attendance"
)

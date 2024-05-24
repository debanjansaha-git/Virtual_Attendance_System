from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, lead, unix_timestamp, when, min, max, sum
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder.appName("AttendanceFilter").getOrCreate()

# Read the data
df = spark.read.option("header", "true").csv("attendance.csv")

# Convert Time column to timestamp
df = df.withColumn("Time", col("Time").cast("timestamp"))

# Define window specification
window_spec = Window.partitionBy("Name").orderBy("Time")

# Calculate the time difference in seconds between consecutive rows for each person
df = df.withColumn("prev_status", lag("Status").over(window_spec))
df = df.withColumn("prev_time", lag("Time").over(window_spec))
df = df.withColumn("time_diff", unix_timestamp("Time") - unix_timestamp("prev_time"))

# Define lead columns to get next status and time difference
df = df.withColumn("next_status", lead("Status").over(window_spec))
df = df.withColumn("next_time_diff", lead("time_diff").over(window_spec))

# Mark valid rows with a new column
df = df.withColumn(
    "valid",
    when(
        (col("Status") == "IN")
        & (col("prev_status") == "OUT")
        & (col("time_diff") <= 2),
        False,
    )
    .when(
        (col("Status") == "OUT")
        & (col("next_status") == "IN")
        & (col("next_time_diff") <= 2),
        False,
    )
    .otherwise(True),
)

# Add a column to identify session changes
df = df.withColumn(
    "session_change",
    when(
        (col("Status") == "IN")
        & (col("prev_status") == "OUT")
        & (col("time_diff") > 2),
        1,
    )
    .when(
        (col("Status") == "OUT")
        & (col("prev_status") == "IN")
        & (col("time_diff") > 2),
        1,
    )
    .otherwise(0),
)

# Calculate session_id using a cumulative sum over session_change
df = df.withColumn(
    "session_id",
    sum("session_change").over(
        window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow)
    ),
)

# Filter only valid rows
filtered_df = df.filter(col("valid"))

# Get the first IN and last OUT for each session
session_window = Window.partitionBy("Name", "session_id").orderBy("Time")

final_df = (
    filtered_df.groupBy("Name", "session_id")
    .agg(
        min(when(col("Status") == "IN", col("Time"))).alias("first_in"),
        max(when(col("Status") == "OUT", col("Time"))).alias("last_out"),
    )
    .select("Name", "first_in", "last_out")
)

# Show the filtered data (for debugging purposes)
final_df.show()

# Save the transformed data back to a CSV file
final_df.write.option("header", "true").csv("transformed_attendance.csv")

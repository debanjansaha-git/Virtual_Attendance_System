import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

// Initialize Spark session
val spark = SparkSession.builder.appName("AttendanceFilter").getOrCreate()

// Read the data
val df = spark.read.option("header", "true").csv("attendance.csv")

// Convert Time column to timestamp
val dfWithTime = df.withColumn("Time", col("Time").cast("timestamp"))

// Define window specification
val windowSpec = Window.partitionBy("Name").orderBy("Time")

// Calculate the time difference in seconds between consecutive rows for each person
val dfWithDiffs = dfWithTime
  .withColumn("prev_status", lag("Status", 1).over(windowSpec))
  .withColumn("prev_time", lag("Time", 1).over(windowSpec))
  .withColumn("time_diff", unix_timestamp(col("Time")) - unix_timestamp(col("prev_time")))

// Define lead columns to get next status and time difference
val dfWithLeads = dfWithDiffs
  .withColumn("next_status", lead("Status", 1).over(windowSpec))
  .withColumn("next_time_diff", lead("time_diff", 1).over(windowSpec))

// Mark valid rows with a new column
val dfWithValid = dfWithLeads.withColumn(
  "valid",
  when(
    col("Status") === "IN" && col("prev_status") === "OUT" && col("time_diff") <= 2,
    false
  ).when(
    col("Status") === "OUT" && col("next_status") === "IN" && col("next_time_diff") <= 2,
    false
  ).otherwise(true)
)

// Add a column to identify session changes
val dfWithSessionChange = dfWithValid.withColumn(
  "session_change",
  when(
    col("Status") === "IN" && col("prev_status") === "OUT" && col("time_diff") > 2,
    1
  ).when(
    col("Status") === "OUT" && col("prev_status") === "IN" && col("time_diff") > 2,
    1
  ).otherwise(0)
)

// Calculate session_id using a cumulative sum over session_change
val windowSpecWithUnbounded = windowSpec.rowsBetween(Window.unboundedPreceding, Window.currentRow)
val dfWithSessionId = dfWithSessionChange.withColumn(
  "session_id",
  sum("session_change").over(windowSpecWithUnbounded)
)

// Filter only valid rows
val filteredDf = dfWithSessionId.filter(col("valid"))

// Get the first IN and last OUT for each session
val sessionWindow = Window.partitionBy("Name", "session_id").orderBy("Time")

val finalDf = filteredDf.groupBy("Name", "session_id")
  .agg(
    min(when(col("Status") === "IN", col("Time"))).alias("first_in"),
    max(when(col("Status") === "OUT", col("Time"))).alias("last_out")
  )
  .select("Name", "first_in", "last_out")

// Show the filtered data (for debugging purposes)
finalDf.show()

// Save the transformed data back to a CSV file
finalDf.write.option("header", "true").csv("transformed_attendance.csv")

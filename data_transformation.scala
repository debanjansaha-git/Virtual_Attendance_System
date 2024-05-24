import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

object AttendanceFilter {
  def main(args: Array[String]): Unit = {
    // Initialize Spark session
    val spark = SparkSession.builder.appName("AttendanceFilter").getOrCreate()

    // Read the data
    val df = spark.read.option("header", "true").csv("data/ingestion/historic_attendance.csv")

    // Convert Time column to timestamp
    val dfWithTimestamp = df.withColumn("Time", col("Time").cast("timestamp"))

    // Extract date from timestamp to handle day changes
    val dfWithDate = dfWithTimestamp.withColumn("Date", date_format(col("Time"), "yyyy-MM-dd"))

    // Define window specification
    val windowSpec = Window.partitionBy("Name").orderBy("Time")

    // Identify session changes
    val dfWithSessionChange = dfWithDate
      .withColumn("prev_status", lag("Status", 1).over(windowSpec))
      .withColumn("prev_date", lag("Date", 1).over(windowSpec))
      .withColumn("session_change", when(
        (col("Status") === "IN") && ((col("prev_status") === "OUT") || (col("Date") =!= col("prev_date"))),
        1
      ).otherwise(0))

    // Generate session_id using a cumulative sum over session_change
    val dfWithSessionId = dfWithSessionChange.withColumn("session_id",
      sum("session_change").over(windowSpec.rowsBetween(Window.unboundedPreceding, Window.currentRow))
    )

    // Pair IN and OUT records by matching session_id
    val pairedDf = dfWithSessionId.withColumn("paired_time",
      when(col("Status") === "IN", col("Time")).otherwise(lead("Time", 1).over(windowSpec))
    )

    // Filter out incomplete pairs
    val filteredPairedDf = pairedDf.filter(
      (col("Status") === "IN") ||
        ((col("Status") === "OUT") && col("paired_time").isNotNull)
    )

    // Aggregate to get first IN and last OUT for each session
    val finalDf = filteredPairedDf.groupBy("Name", "session_id").agg(
      min(when(col("Status") === "IN", col("Time"))).alias("first_in"),
      max(when(col("Status") === "OUT", col("Time"))).alias("last_out")
    )

    // Filter out rows where first_in or last_out is NULL
    val resultDf = finalDf.filter(col("first_in").isNotNull && col("last_out").isNotNull)

    // Show the filtered data (for debugging purposes)
    resultDf.show()

    // Save the transformed data back to a CSV file
    resultDf.write.option("header", "true").csv("data/transformation/transformed_attendance")
  }
}

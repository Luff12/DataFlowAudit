import pandas as pd
import time

from datetime import datetime

from database import save_pipeline_log
from alerting import send_email


# Run data pipeline
def run_pipeline():

    print("\nDATA PIPELINE STARTED")

    start_time = datetime.now()

    start_clock = time.time()

    status = "SUCCESS"

    records_processed = 0

    error_message = ""

    try:

        # Load CSV dataset
        data = pd.read_csv("data/sample_data.csv")

        # Count records
        records_processed = len(data)

        print("Dataset loaded successfully!")

        print("Records:", records_processed)

    except Exception as error:

        status = "FAILED"

        error_message = str(error)

        print("Pipeline failed!")

        print(error_message)

    # Calculate execution time
    execution_time = round(time.time() - start_clock, 2)

    # Save pipeline log
    save_pipeline_log(
        "CSV Data Pipeline",
        status,
        records_processed,
        execution_time,
        start_time.strftime("%Y-%m-%d %H:%M:%S"),
        error_message,
    )

    # Display report
    print("\nPIPELINE REPORT")

    print("Status:", status)

    print("Records:", records_processed)

    print("Execution Time:", execution_time)

    # Send failure notification
    if status == "FAILED":

        send_email(
            "DataFlow Audit - Pipeline Failure",
            "Your data pipeline failed.\n\n" + error_message,
        )


# Run program
if __name__ == "__main__":

    run_pipeline()

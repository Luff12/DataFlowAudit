import pandas as pd

from database import save_audit_result
from alerting import send_email


# Load dataset
def run_audit():

    print("\nSTARTING DATA QUALITY AUDIT")

    data = pd.read_csv("data/sample_data.csv")

    issues = []

    # Check missing values
    for column in data.columns:

        count = int(data[column].isnull().sum())

        if count > 0:

            issues.append({"Issue": "Missing Values", "Column": column, "Count": count})

    # Check duplicate rows
    duplicate_count = int(data.duplicated().sum())

    if duplicate_count > 0:

        issues.append(
            {
                "Issue": "Duplicate Rows",
                "Column": "All Columns",
                "Count": duplicate_count,
            }
        )

    # Check negative amounts
    negative_count = int((data["amount"] < 0).sum())

    if negative_count > 0:

        issues.append(
            {"Issue": "Negative Amount", "Column": "amount", "Count": negative_count}
        )

    # Check invalid order IDs
    invalid_ids = int((data["order_id"] <= 0).sum())

    if invalid_ids > 0:

        issues.append(
            {"Issue": "Invalid Order ID", "Column": "order_id", "Count": invalid_ids}
        )

    # Save results in database
    print("\nAUDIT RESULTS")

    for issue in issues:

        print(issue)

        save_audit_result(issue["Issue"], issue["Column"], issue["Count"])

    # Send email alert
    if issues:

        message = "Data quality problems detected!\n\n"

        for issue in issues:

            message += (
                issue["Issue"]
                + " | "
                + issue["Column"]
                + " | "
                + str(issue["Count"])
                + "\n"
            )

        send_email("DataFlow Audit - Quality Alert", message)

    else:

        print("No data quality problems found.")

    return data, issues


# Run program directly
if __name__ == "__main__":

    run_audit()

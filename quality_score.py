import pandas as pd


# Calculate data quality score
def calculate_quality_score(data):

    total_records = len(data)

    total_columns = len(data.columns)

    if total_records == 0:

        return {
            "overall_score": 0,
            "completeness": 0,
            "uniqueness": 0,
            "validity": 0,
            "consistency": 0,
            "accuracy": 0,
        }

    # 1. Completeness
    total_cells = total_records * total_columns

    missing_cells = data.isnull().sum().sum()

    completeness = ((total_cells - missing_cells) / total_cells) * 100

    # 2. Uniqueness
    duplicate_count = data.duplicated().sum()

    uniqueness = ((total_records - duplicate_count) / total_records) * 100

    # 3. Validity
    invalid_amounts = (data["amount"] < 0).sum()

    invalid_ids = (data["order_id"] <= 0).sum()

    invalid_records = (data["amount"].lt(0) | data["order_id"].le(0)).sum()

    validity = ((total_records - invalid_records) / total_records) * 100

    # 4. Consistency
    valid_dates = pd.to_datetime(data["order_date"], errors="coerce").notnull().sum()

    consistency = (valid_dates / total_records) * 100

    # 5. Accuracy
    # For this beginner project, use unusual
    # transaction values as a simple proxy.

    valid_amounts = data["amount"].dropna()

    if len(valid_amounts) > 0:

        mean_amount = valid_amounts.mean()

        std_amount = valid_amounts.std()

        if pd.notna(std_amount) and std_amount > 0:

            unusual_values = (
                (valid_amounts - mean_amount).abs() > 3 * std_amount
            ).sum()

        else:

            unusual_values = 0

        accuracy = ((len(valid_amounts) - unusual_values) / len(valid_amounts)) * 100

    else:

        accuracy = 0

    # Calculate overall score
    overall_score = (completeness + uniqueness + validity + consistency + accuracy) / 5

    # Return results
    return {
        "overall_score": round(overall_score, 2),
        "completeness": round(completeness, 2),
        "uniqueness": round(uniqueness, 2),
        "validity": round(validity, 2),
        "consistency": round(consistency, 2),
        "accuracy": round(accuracy, 2),
    }


# Test the program
if __name__ == "__main__":

    data = pd.read_csv("data/sample_data.csv")

    results = calculate_quality_score(data)

    print("\nDATA QUALITY SCORE REPORT")

    for name, score in results.items():

        print(name, ":", score, "%")

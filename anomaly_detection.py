import pandas as pd

from datetime import datetime
from sklearn.ensemble import IsolationForest

from database import save_anomalies
from alerting import send_email


# Detect unusual transactions
def detect_anomalies():

    print("\nSTARTING AI ANOMALY DETECTION")

    # Load dataset
    data = pd.read_csv("data/sample_data.csv")

    # Select valid amount records
    amount_data = data[["order_id", "amount"]].dropna().copy()

    # Remove negative amounts from model training
    amount_data = amount_data[amount_data["amount"] >= 0].copy()

    # Check sufficient data
    if len(amount_data) < 5:

        print("Not enough valid records.")

        return pd.DataFrame()

    # Create AI model
    model = IsolationForest(contamination=0.15, random_state=42)

    # Train model
    model.fit(amount_data[["amount"]])

    # Predict anomalies
    predictions = model.predict(amount_data[["amount"]])

    # Store predictions
    amount_data["prediction"] = predictions

    # Convert predictions into labels
    amount_data["status"] = amount_data["prediction"].map({1: "Normal", -1: "Anomaly"})

    # Add detection time
    amount_data["detected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save results
    save_anomalies(amount_data)

    # Find unusual transactions
    unusual_data = amount_data[amount_data["status"] == "Anomaly"]

    print("\nANOMALY RESULTS")

    print(amount_data)

    print("\nUNUSUAL TRANSACTIONS")

    print(unusual_data)

    # Send alert if anomalies exist
    if not unusual_data.empty:

        message = "Unusual transactions detected!\n\n"

        for index, row in unusual_data.iterrows():

            message += "Order ID: " + str(row["order_id"]) + "\n"

            message += "Amount: " + str(row["amount"]) + "\n\n"

        send_email("DataFlow Audit - AI Anomaly Alert", message)

    return amount_data


# Run directly
if __name__ == "__main__":

    detect_anomalies()

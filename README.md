
# DataFlow Audit
## AI-Powered Data Quality and Pipeline Monitoring

### 1. Project Overview
DataFlow Audit is a Python-based data quality monitoring system. It checks datasets for errors, detects unusual transactions using Machine Learning, monitors pipeline execution, and displays results through an interactive Streamlit dashboard.

### 2. Project Objectives
- Identify missing values in datasets.
- Detect duplicate records.
- Find invalid and negative values.
- Detect unusual transactions using Isolation Forest.
- Store audit results in an SQLite database.
- Monitor pipeline execution.
- Generate email alerts when configured.
- Calculate data quality scores.
- Display results through a dashboard.

### 3. Technologies Used
- Python
- Pandas
- Scikit-learn
- SQLite
- Streamlit
- Plotly
- Machine Learning

### 4. Project Structure

```text
DataFlowAudit/
│
├── data/
│   └── sample_data.csv
│
├── audit.py
├── anomaly_detection.py
├── database.py
├── pipeline_monitor.py
├── alerting.py
├── dashboard.py
├── quality_score.py
│
├── audit_database.db
├── requirements.txt
└── README.md
```

### 5. Main Features

**Data Quality Audit**

Checks missing values, duplicate records, negative amounts, and invalid order IDs.

**AI Anomaly Detection**

Uses the Isolation Forest machine learning algorithm to identify unusual transaction amounts.

**Database Integration**

Uses SQLite to store audit results, pipeline logs, and anomaly detection results.

**Pipeline Monitoring**

Records pipeline status, execution time, and number of processed records.

**Email Alerts**

Sends email notifications when issues or anomalies are detected, if email settings are configured.

**Data Quality Score**

Calculates completeness, uniqueness, validity, consistency, and an estimated accuracy score.

**Interactive Dashboard**

Uses Streamlit and Plotly to display audit results, quality scores, pipeline information, and anomalies.

### 6. Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 7. How to Run the Project

Run the data quality audit:

```bash
python audit.py
```

Run AI anomaly detection:

```bash
python anomaly_detection.py
```

Run pipeline monitoring:

```bash
python pipeline_monitor.py
```

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

### 8. Database

The project uses SQLite.

The database stores:
- Audit results
- Pipeline execution logs
- Anomaly detection results

Database file: `audit_database.db`

### 9. Expected Results

The system can identify:
- Missing transaction amounts
- Duplicate records
- Negative transaction amounts
- Invalid order IDs
- Unusual transaction amounts

The dashboard displays the results and calculated data quality scores.

### 10. Future Enhancements

- Connect to real-time databases.
- Add automatic scheduled pipeline monitoring.
- Support larger datasets.
- Add more machine learning algorithms.
- Improve anomaly detection accuracy.
- Add user authentication.
- Support multiple datasets.

### 11. Conclusion

DataFlow Audit demonstrates how Python, machine learning, databases, and data visualization can be combined to build a basic data quality monitoring system.

It helps users identify data problems, detect unusual transactions, monitor pipeline execution, and understand dataset quality through an interactive dashboard.

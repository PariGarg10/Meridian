from google.cloud import bigquery
from datetime import datetime, timezone
import os


class BigQueryResultStore:
    """
    Stores forecast results in Google BigQuery.
    Results are queryable via SQL for analytics and reporting.
    """

    def __init__(self):
        self.client     = bigquery.Client()
        self.project    = self.client.project
        self.dataset    = "meridian_data"
        self.table      = "forecast_results"
        self.table_ref  = f"{self.project}.{self.dataset}.{self.table}"

        print(f"✅ Connected to BigQuery: {self.table_ref}")

    def save_forecast(self, job_id: str, tenant_id: str,
                      result: dict):
        """
        Save forecast predictions to BigQuery.
        One row per date in the forecast horizon.
        """

        rows = []
        now  = datetime.now(timezone.utc).isoformat()

        for i, date in enumerate(result["dates"]):
            rows.append({
                "job_id":     job_id,
                "tenant_id":  tenant_id,
                "ds":         date,
                "yhat":       result["predictions"][i],
                "yhat_lower": result["lower_bound"][i],
                "yhat_upper": result["upper_bound"][i],
                "model_used": result["model"],
                "created_at": now,
            })

        errors = self.client.insert_rows_json(self.table_ref, rows)

        if errors:
            print(f"❌ BigQuery insert errors: {errors}")
        else:
            print(f"✅ Saved {len(rows)} rows to BigQuery for job {job_id}")

    def get_forecast(self, job_id: str) -> list:
        """Fetch forecast results for a job from BigQuery"""

        query = f"""
            SELECT ds, yhat, yhat_lower, yhat_upper, model_used
            FROM `{self.table_ref}`
            WHERE job_id = @job_id
            ORDER BY ds ASC
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("job_id", "STRING", job_id)
            ]
        )

        results = self.client.query(query, job_config=job_config).result()

        rows = []
        for row in results:
            rows.append({
                "date":        str(row.ds),
                "prediction":  row.yhat,
                "lower_bound": row.yhat_lower,
                "upper_bound": row.yhat_upper,
                "model_used":  row.model_used,
            })

        return rows
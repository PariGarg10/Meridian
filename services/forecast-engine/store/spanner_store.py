from google.cloud import spanner
from google.cloud.spanner_v1 import param_types
from datetime import datetime, timezone
import os


class SpannerJobStore:
    """
    Stores and retrieves job metadata from Google Cloud Spanner.
    Replaces the in-memory dict we used in Weeks 2-4.
    """

    def __init__(self):
        self.instance_id = "meridian-instance"
        self.database_id = "meridian-db"

        self.client   = spanner.Client()
        self.instance = self.client.instance(self.instance_id)
        self.database = self.instance.database(self.database_id)

        print(f"✅ Connected to Spanner: {self.instance_id}/{self.database_id}")

    def create_job(self, job_id: str, tenant_id: str,
                   dataset_ref: str, horizon_days: int):
        """Insert a new job record with PENDING status"""

        def insert_job(transaction):
            transaction.insert(
                table="jobs",
                columns=["job_id", "tenant_id", "status",
                         "dataset_ref", "horizon_days",
                         "created_at", "updated_at"],
                values=[(
                    job_id,
                    tenant_id,
                    "PENDING",
                    dataset_ref,
                    horizon_days,
                    spanner.COMMIT_TIMESTAMP,
                    spanner.COMMIT_TIMESTAMP,
                )]
            )

        self.database.run_in_transaction(insert_job)
        print(f"📝 Job {job_id} created in Spanner")

    def update_job_status(self, job_id: str, status: str,
                          model_used: str = None, error_msg: str = None):
        """Update job status in Spanner"""

        def update(transaction):
            cols   = ["job_id", "status", "updated_at"]
            values = [job_id, status, spanner.COMMIT_TIMESTAMP]

            if model_used:
                cols.append("model_used")
                values.append(model_used)
            if error_msg:
                cols.append("error_msg")
                values.append(error_msg)

            transaction.update(
                table="jobs",
                columns=cols,
                values=[values]
            )

        self.database.run_in_transaction(update)
        print(f"📝 Job {job_id} status updated to {status}")

    def get_job(self, job_id: str) -> dict:
        """Fetch a job by ID"""

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                "SELECT job_id, tenant_id, status, model_used, error_msg "
                "FROM jobs WHERE job_id = @job_id",
                params={"job_id": job_id},
                param_types={"job_id": param_types.STRING}
            )

            for row in results:
                return {
                    "job_id":     row[0],
                    "tenant_id":  row[1],
                    "status":     row[2],
                    "model_used": row[3] or "",
                    "error_msg":  row[4] or "",
                }

        return None
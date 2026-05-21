import grpc
import uuid
import pandas as pd
from concurrent import futures
import time
import os

import forecast_pb2
import forecast_pb2_grpc
from models.auto_forecaster import AutoForecaster

# Try to connect to GCP — fall back to in-memory if not configured
try:
    from store.spanner_store   import SpannerJobStore
    from store.bigquery_store  import BigQueryResultStore
    spanner_store = SpannerJobStore()
    bq_store      = BigQueryResultStore()
    USE_GCP       = True
    print("✅ GCP mode: using Spanner + BigQuery")
except Exception as e:
    print(f"⚠️  GCP not configured, using in-memory store: {e}")
    spanner_store = None
    bq_store      = None
    USE_GCP       = False


class ForecastServicer(forecast_pb2_grpc.ForecastServiceServicer):

    def __init__(self):
        self.forecaster = AutoForecaster()
        self.jobs       = {}  # fallback in-memory store

    def SubmitForecastJob(self, request, context):

        print(f"\n📥 New forecast request")
        print(f"   Tenant  : {request.tenant_id}")
        print(f"   Dataset : {request.dataset_ref}")
        print(f"   Horizon : {request.horizon_days} months")

        job_id = str(uuid.uuid4())[:8]

        # Save to Spanner or memory
        if USE_GCP:
            spanner_store.create_job(
                job_id, request.tenant_id,
                request.dataset_ref, request.horizon_days
            )
        else:
            self.jobs[job_id] = {
                "status": "RUNNING", "result": None, "error": None,
                "tenant_id": request.tenant_id
            }

        try:
            df     = self._load_dataset(request.dataset_ref)
            result = self.forecaster.forecast(df, horizon=request.horizon_days)

            # Save result
            if USE_GCP:
                bq_store.save_forecast(job_id, request.tenant_id, result)
                spanner_store.update_job_status(job_id, "DONE", model_used=result["model"])
            else:
                self.jobs[job_id]["status"] = "DONE"
                self.jobs[job_id]["result"] = result

            print(f"✅ Job {job_id} complete — best model: {result['model'].upper()}")

        except Exception as e:
            if USE_GCP:
                spanner_store.update_job_status(job_id, "FAILED", error_msg=str(e))
            else:
                self.jobs[job_id]["status"] = "FAILED"
                self.jobs[job_id]["error"]  = str(e)
            print(f"❌ Job {job_id} failed: {e}")

        return forecast_pb2.JobResponse(job_id=job_id, status="DONE")

    def GetJobStatus(self, request, context):
        job_id = request.job_id

        if USE_GCP:
            job = spanner_store.get_job(job_id)
            if not job:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return forecast_pb2.JobStatusResponse()
            return forecast_pb2.JobStatusResponse(
                job_id     = job_id,
                status     = job["status"],
                model_used = job["model_used"],
                error_msg  = job["error_msg"]
            )
        else:
            if job_id not in self.jobs:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return forecast_pb2.JobStatusResponse()
            job = self.jobs[job_id]
            return forecast_pb2.JobStatusResponse(
                job_id     = job_id,
                status     = job["status"],
                model_used = job["result"]["model"] if job["result"] else "",
                error_msg  = job["error"] or ""
            )

    def GetForecastResult(self, request, context):
        job_id = request.job_id

        if USE_GCP:
            rows = bq_store.get_forecast(job_id)
            if not rows:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return forecast_pb2.ForecastResult()

            job = spanner_store.get_job(job_id)

            return forecast_pb2.ForecastResult(
                job_id      = job_id,
                model_used  = rows[0]["model_used"],
                dates       = [r["date"]        for r in rows],
                predictions = [r["prediction"]  for r in rows],
                upper_bound = [r["upper_bound"] for r in rows],
                lower_bound = [r["lower_bound"] for r in rows],
                scores      = forecast_pb2.ModelScores(
                    prophet_mae = 0.0,
                    arima_mae   = 0.0,
                    lstm_mae    = 0.0,
                )
            )
        else:
            if job_id not in self.jobs:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return forecast_pb2.ForecastResult()

            job = self.jobs[job_id]
            if job["status"] != "DONE":
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                return forecast_pb2.ForecastResult()

            result = job["result"]
            return forecast_pb2.ForecastResult(
                job_id      = job_id,
                model_used  = result["model"],
                dates       = result["dates"],
                predictions = result["predictions"],
                upper_bound = result["upper_bound"],
                lower_bound = result["lower_bound"],
                scores      = forecast_pb2.ModelScores(
                    prophet_mae = result["all_scores"].get("prophet", 0.0),
                    arima_mae   = result["all_scores"].get("arima",   0.0),
                    lstm_mae    = result["all_scores"].get("lstm",    0.0),
                )
            )

    def _load_dataset(self, dataset_ref: str) -> pd.DataFrame:
        df = pd.read_csv(dataset_ref)
        df["ds"] = pd.to_datetime(df["ds"])
        return df


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    forecast_pb2_grpc.add_ForecastServiceServicer_to_server(ForecastServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print(f"🚀 Meridian gRPC server running on port 50051")
    print(f"   Waiting for forecast requests...\n")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
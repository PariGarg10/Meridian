import grpc
import uuid
import pandas as pd
from concurrent import futures
import time

import forecast_pb2
import forecast_pb2_grpc
from models.auto_forecaster import AutoForecaster


class ForecastServicer(forecast_pb2_grpc.ForecastServiceServicer):
    """
    gRPC server that exposes the AutoForecaster as a real API.
    Any service (Java scheduler, Angular via proxy) can call this.
    """

    def __init__(self):
        self.forecaster = AutoForecaster()
        # In-memory job store (Week 5 we move this to Spanner)
        self.jobs = {}

    def SubmitForecastJob(self, request, context):
        """
        Receives a ForecastRequest, runs the forecast, stores result.
        Returns a job_id the client can use to fetch results.
        """

        print(f"\n📥 New forecast request received")
        print(f"   Tenant  : {request.tenant_id}")
        print(f"   Dataset : {request.dataset_ref}")
        print(f"   Horizon : {request.horizon_days} months")

        # Generate unique job ID
        job_id = str(uuid.uuid4())[:8]

        # Store job as RUNNING
        self.jobs[job_id] = {
            "status":     "RUNNING",
            "tenant_id":  request.tenant_id,
            "dataset_ref": request.dataset_ref,
            "result":     None,
            "error":      None
        }

        try:
            # Load dataset
            # For now we load from local CSV
            # Week 5: this will load from BigQuery
            df = self._load_dataset(request.dataset_ref)

            # Run AutoForecaster
            result = self.forecaster.forecast(df, horizon=request.horizon_days)

            # Store result
            self.jobs[job_id]["status"] = "DONE"
            self.jobs[job_id]["result"] = result

            print(f"✅ Job {job_id} complete — best model: {result['model'].upper()}")

        except Exception as e:
            self.jobs[job_id]["status"] = "FAILED"
            self.jobs[job_id]["error"]  = str(e)
            print(f"❌ Job {job_id} failed: {e}")

        return forecast_pb2.JobResponse(
            job_id=job_id,
            status=self.jobs[job_id]["status"]
        )

    def GetJobStatus(self, request, context):
        """Check the status of a submitted job"""

        job_id = request.job_id

        if job_id not in self.jobs:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Job {job_id} not found")
            return forecast_pb2.JobStatusResponse()

        job = self.jobs[job_id]

        return forecast_pb2.JobStatusResponse(
            job_id    = job_id,
            status    = job["status"],
            model_used= job["result"]["model"] if job["result"] else "",
            error_msg = job["error"] or ""
        )

    def GetForecastResult(self, request, context):
        """Fetch the completed forecast result for a job"""

        job_id = request.job_id

        if job_id not in self.jobs:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Job {job_id} not found")
            return forecast_pb2.ForecastResult()

        job = self.jobs[job_id]

        if job["status"] != "DONE":
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(f"Job {job_id} is {job['status']}, not DONE yet")
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
        """
        Load dataset from local CSV for now.
        Week 5: replace with BigQuery loader.
        """
        df = pd.read_csv(dataset_ref)
        df["ds"] = pd.to_datetime(df["ds"])
        return df


def serve():
    """Start the gRPC server"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    forecast_pb2_grpc.add_ForecastServiceServicer_to_server(
        ForecastServicer(), server
    )

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"🚀 Meridian gRPC server running on port {port}")
    print(f"   Waiting for forecast requests...\n")

    try:
        while True:
            time.sleep(86400)  # keep alive
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down...")
        server.stop(0)


if __name__ == "__main__":
    serve()
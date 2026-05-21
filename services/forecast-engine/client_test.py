import grpc
import forecast_pb2
import forecast_pb2_grpc
import time


def run():
    """
    Test client that calls our gRPC server.
    Simulates what the Java scheduler will do in Week 3.
    """

    # Connect to server
    channel = grpc.insecure_channel("localhost:50051")
    stub    = forecast_pb2_grpc.ForecastServiceStub(channel)

    print("🔌 Connected to Meridian gRPC server")
    print("=" * 50)

    # ── Test 1: Submit a forecast job ──────────────────
    print("\n📤 Submitting forecast job...")

    request = forecast_pb2.ForecastRequest(
        tenant_id   = "team-analytics",
        dataset_ref = "data/passengers.csv",
        horizon_days= 12
    )

    response = stub.SubmitForecastJob(request)
    job_id   = response.job_id

    print(f"   Job ID : {job_id}")
    print(f"   Status : {response.status}")

    # ── Test 2: Check job status ───────────────────────
    print(f"\n📋 Checking job status for {job_id}...")

    status_response = stub.GetJobStatus(
        forecast_pb2.JobID(job_id=job_id)
    )

    print(f"   Status     : {status_response.status}")
    print(f"   Model used : {status_response.model_used}")

    # ── Test 3: Get forecast result ────────────────────
    if status_response.status == "DONE":
        print(f"\n📊 Fetching forecast result...")

        result = stub.GetForecastResult(
            forecast_pb2.JobID(job_id=job_id)
        )

        print(f"\n   Model used : {result.model_used.upper()}")
        print(f"\n   Model scores:")
        print(f"     Prophet MAE : {result.scores.prophet_mae}")
        print(f"     ARIMA MAE   : {result.scores.arima_mae}")
        print(f"     LSTM MAE    : {result.scores.lstm_mae}")

        print(f"\n   Forecast (first 6 months):")
        print(f"   {'Date':<15} {'Predicted':>10} {'Lower':>10} {'Upper':>10}")
        print(f"   {'-' * 48}")

        for i in range(min(6, len(result.dates))):
            print(f"   {result.dates[i]:<15} "
                  f"{result.predictions[i]:>10.1f} "
                  f"{result.lower_bound[i]:>10.1f} "
                  f"{result.upper_bound[i]:>10.1f}")

        print(f"\n✅ gRPC round-trip complete!")

    else:
        print(f"❌ Job not done yet: {status_response.status}")


if __name__ == "__main__":
    run()
    
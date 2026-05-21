from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import grpc
import uuid

import forecast_pb2
import forecast_pb2_grpc

app = FastAPI(title="Meridian REST Bridge")

# Allow Angular to call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to gRPC server
channel = grpc.insecure_channel("localhost:50051")
stub    = forecast_pb2_grpc.ForecastServiceStub(channel)


class ForecastRequest(BaseModel):
    tenantId:    str
    datasetRef:  str
    horizonDays: int


@app.post("/forecast")
def submit_forecast(req: ForecastRequest):
    """Angular calls this → we call gRPC Python server"""
    try:
        grpc_request = forecast_pb2.ForecastRequest(
            tenant_id   = req.tenantId,
            dataset_ref = req.datasetRef,
            horizon_days= req.horizonDays
        )
        response = stub.SubmitForecastJob(grpc_request)
        return { "jobId": response.job_id, "status": response.status }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Check job status"""
    try:
        response = stub.GetJobStatus(forecast_pb2.JobID(job_id=job_id))
        return {
            "jobId":     response.job_id,
            "status":    response.status,
            "modelUsed": response.model_used,
            "errorMsg":  response.error_msg
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/result/{job_id}")
def get_result(job_id: str):
    """Get completed forecast result"""
    try:
        result = stub.GetForecastResult(forecast_pb2.JobID(job_id=job_id))
        return {
            "jobId":       result.job_id,
            "modelUsed":   result.model_used,
            "dates":       list(result.dates),
            "predictions": list(result.predictions),
            "upperBound":  list(result.upper_bound),
            "lowerBound":  list(result.lower_bound),
            "allScores": {
                "prophet": result.scores.prophet_mae,
                "arima":   result.scores.arima_mae,
                "lstm":    result.scores.lstm_mae,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return { "status": "ok", "service": "Meridian REST Bridge" }
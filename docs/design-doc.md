# Meridian — Design Document
**Author:** PARI GARG
**Date:** May 2025
**Status:** In Progress

---

1. Problem Statement

Every team at a data-driven company needs forecasting like sales, traffic, infrastructure load, user growth. Today, each team solves this from scratch: they hire data scientists, write one-off scripts, and build throwaway dashboards.

Meridian fixes this. It is a self-serve, multi-tenant ML forecasting platform. Any team uploads time-series data and gets back production-grade forecasts with confidence intervals zero ML knowledge required.

---

2. Goals

- Any tenant can submit a forecasting job via UI or API
- System auto-selects the best model (Prophet, ARIMA, LSTM)
- Results are stored and queryable via BigQuery
- Forecasts are served in under 1 second via gRPC
- Platform supports multiple isolated tenants simultaneously

3. Non-Goals (v1)

- We will NOT support image or text data just time-series only
- We will NOT build a billing system
- We will NOT support real-time streaming data (batch only in v1)

---

4. System Architecture

[ Angular UI ]
|
[ gRPC API Gateway ] (Python/Go)
|
[ Java Job Scheduler ] ←→ [ Spanner: job metadata ]
|
[ Python Forecast Engine ]
|
┌───┴───┐
Prophet  ARIMA  TensorFlow LSTM
|
[ BigQuery: results warehouse ]

---------------------

5. Data Flow

1. Tenant uploads CSV or connects BigQuery table via Angular UI
2. UI sends ForecastRequest to API Gateway over gRPC
3. API Gateway validates request, writes job to Spanner, queues it
4. Java Scheduler picks up job, calls Python Forecast Engine
5. Forecast Engine runs all 3 models, picks best by lowest MAE
6. Results (predictions + confidence intervals) written to BigQuery
7. Tenant polls for result, UI renders forecast chart

-------------

6. Tech Stack Decisions

Component: Frontend
Tech Stack: Angular + TypeScript
Why: Google’s own framework, strongly typed, and highly scalable for large applications.

Component: API Layer
Tech Stack: gRPC
Why: Provides fast communication, typed contracts, and follows Google-standard architecture practices.

Component: Job Scheduler
Tech Stack: Java
Why: Offers strong typing, reliability, and excellent support for queue-based systems.

Component: ML Engine
Tech Stack: Python
Why: Best suited for machine learning because of its rich ecosystem including TensorFlow, Prophet, and scikit-learn.

Component: Metadata Store
Tech Stack: Cloud Spanner
Why: Ensures global consistency and seamless integration with Google Cloud services.

Component: Data Warehouse
Tech Stack: BigQuery
Why: Scalable, serverless, and supports powerful SQL-based analytics.

Component: Deployment
Tech Stack: Kubernetes
Why: Enables scalable, production-grade container orchestration and deployment.

Component: Build System
Tech Stack: Bazel
Why: Optimized for monorepo builds and widely used in Google-standard workflows.
------------------

7. Data Schema

#Spanner: jobs table
job_id        STRING (PK)
tenant_id     STRING
status        STRING  (PENDING | RUNNING | DONE | FAILED)
dataset_ref   STRING
horizon_days  INT64
model_used    STRING
created_at    TIMESTAMP
updated_at    TIMESTAMP

#Spanner: tenants table
tenant_id     STRING (PK)
name          STRING
tier          STRING  (FREE | PRO)
created_at    TIMESTAMP

### BigQuery: forecast_results table
job_id        STRING
tenant_id     STRING
ds            DATE
yhat          FLOAT64   -- predicted value
yhat_lower    FLOAT64   -- lower confidence bound
yhat_upper    FLOAT64   -- upper confidence bound
model_used    STRING
created_at    TIMESTAMP

--------------------

8. API Contract (gRPC)

```protobuf
service ForecastService {
  rpc SubmitForecastJob (ForecastRequest) returns (JobResponse);
  rpc GetJobStatus      (JobID)           returns (JobStatusResponse);
  rpc GetForecastResult (JobID)           returns (ForecastResult);
}

message ForecastRequest {
  string tenant_id    = 1;
  string dataset_ref  = 2;
  int32  horizon_days = 3;
}

message JobResponse {
  string job_id  = 1;
  string status  = 2;
}

message ForecastResult {
  string          job_id       = 1;
  string          model_used   = 2;
  repeated double predictions  = 3;
  repeated double upper_bound  = 4;
  repeated double lower_bound  = 5;
  repeated string dates        = 6;
}
```

-------------

9. Model Selection Logic
Run Prophet   → compute MAE on holdout set
Run ARIMA     → compute MAE on holdout set
Run LSTM      → compute MAE on holdout set
Pick model with lowest MAE
Log all 3 scores to BigQuery for observability
Return best model's forecast

-----------------

10. What Could Go Wrong

Risk: LSTM takes too long
Mitigation: Set a 30-second timeout and fall back to Prophet if exceeded.

Risk: Bad CSV format from tenant
Mitigation: Validate the schema during upload and return an error for invalid files.

Risk: Spanner consistency lag
Mitigation: Use strong reads for job status polling to ensure consistency.

Risk: One tenant hogs compute
Mitigation: The Java scheduler enforces per-tenant compute quotas.

Risk: Model accuracy is bad
Mitigation: Always display confidence intervals along with predictions.
---------------

11. Success Metrics

- Forecast job completes in under 60 seconds (p95)
- gRPC result query returns in under 1 second
- Auto-selected model beats naive baseline by >10% MAE
- System handles 50 concurrent tenant jobs without degradation
# 🔮 Meridian

> A self-serve, multi-tenant ML forecasting platform.
> Upload time-series data. Get production-grade forecasts. Zero ML knowledge required.

---

## What It Does

Meridian is an internal ML-as-a-service platform. Any team (tenant) can:
1. Upload a CSV or point to a BigQuery table
2. Set a forecast horizon (30 / 60 / 90 days)
3. Get back predictions with confidence intervals, powered by auto-selected ML models

The system automatically benchmarks Prophet, ARIMA, and TensorFlow LSTM —
and returns the best one for your data.

---

## Architecture
[ Angular UI ] → [ gRPC API Gateway ] → [ Java Scheduler ] → [ Python ML Engine ]
↕                       ↕
[ Spanner ]             [ BigQuery ]

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | Angular + TypeScript              |
| API         | gRPC (Protocol Buffers)           |
| Scheduler   | Java 17 + Spring Boot             |
| ML Engine   | Python + TensorFlow + Prophet     |
| Metadata    | Google Cloud Spanner              |
| Warehouse   | Google BigQuery                   |
| Deployment  | Kubernetes on GCP                 |
| Build       | Bazel (monorepo)                  |

## Status

- [x] Week 0 — Design doc + repo setup
- [ ] Week 1 — Python ML engine
- [ ] Week 2 — Auto model selection
- [ ] Week 3 — Java job scheduler
- [ ] Week 4 — gRPC API layer
- [ ] Week 5 — GCP integration
- [ ] Week 6 — Angular UI
- [ ] Week 7 — Kubernetes deploy
- [ ] Week 8 — Demo + polish
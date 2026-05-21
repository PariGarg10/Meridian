CREATE TABLE tenants (
  tenant_id   STRING(100) NOT NULL,
  name        STRING(200),
  tier        STRING(20),
  created_at  TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (tenant_id);

CREATE TABLE jobs (
  job_id       STRING(100) NOT NULL,
  tenant_id    STRING(100) NOT NULL,
  status       STRING(20)  NOT NULL,
  dataset_ref  STRING(500),
  horizon_days INT64,
  model_used   STRING(50),
  error_msg    STRING(1000),
  created_at   TIMESTAMP   NOT NULL OPTIONS (allow_commit_timestamp=true),
  updated_at   TIMESTAMP   NOT NULL OPTIONS (allow_commit_timestamp=true),
) PRIMARY KEY (job_id);
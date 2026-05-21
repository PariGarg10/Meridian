package com.meridian;

import java.time.Instant;
import java.util.UUID;

/**
 * Represents a single forecast job in the scheduler.
 * Tracks status, tenant, and timing.
 */
public class Job {

    public enum Status {
        PENDING, RUNNING, DONE, FAILED
    }

    private final String  jobId;
    private final String  tenantId;
    private final String  datasetRef;
    private final int     horizonDays;
    private       Status  status;
    private       String  modelUsed;
    private       String  errorMsg;
    private final Instant createdAt;
    private       Instant updatedAt;

    public Job(String tenantId, String datasetRef, int horizonDays) {
        this.jobId       = UUID.randomUUID().toString().substring(0, 8);
        this.tenantId    = tenantId;
        this.datasetRef  = datasetRef;
        this.horizonDays = horizonDays;
        this.status      = Status.PENDING;
        this.createdAt   = Instant.now();
        this.updatedAt   = Instant.now();
    }

    // ── Getters ──────────────────────────────────────

    public String  getJobId()       { return jobId;       }
    public String  getTenantId()    { return tenantId;    }
    public String  getDatasetRef()  { return datasetRef;  }
    public int     getHorizonDays() { return horizonDays; }
    public Status  getStatus()      { return status;      }
    public String  getModelUsed()   { return modelUsed;   }
    public String  getErrorMsg()    { return errorMsg;    }
    public Instant getCreatedAt()   { return createdAt;   }
    public Instant getUpdatedAt()   { return updatedAt;   }

    // ── Setters ──────────────────────────────────────

    public void setStatus(Status status) {
        this.status    = status;
        this.updatedAt = Instant.now();
    }

    public void setModelUsed(String modelUsed) {
        this.modelUsed = modelUsed;
    }

    public void setErrorMsg(String errorMsg) {
        this.errorMsg = errorMsg;
    }

    @Override
    public String toString() {
        return String.format(
            "Job{id=%s, tenant=%s, status=%s, model=%s}",
            jobId, tenantId, status, modelUsed
        );
    }
}
package com.meridian;

import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Thread-safe job queue with per-tenant limits.
 * Prevents one tenant from hogging all compute resources.
 */
public class JobQueue {

    // Max concurrent jobs per tenant
    private static final int MAX_JOBS_PER_TENANT = 3;

    // The actual queue — LinkedBlockingQueue is thread-safe
    private final BlockingQueue<Job> queue = new LinkedBlockingQueue<>();

    // All jobs ever submitted — for status lookups
    private final Map<String, Job> allJobs = new ConcurrentHashMap<>();

    // Per-tenant active job count
    private final Map<String, AtomicInteger> tenantJobCounts
        = new ConcurrentHashMap<>();

    /**
     * Submit a job to the queue.
     * Returns false if tenant has hit their limit.
     */
    public boolean submit(Job job) {
        String tenantId = job.getTenantId();

        // Check tenant limit
        tenantJobCounts.putIfAbsent(tenantId, new AtomicInteger(0));
        int currentCount = tenantJobCounts.get(tenantId).get();

        if (currentCount >= MAX_JOBS_PER_TENANT) {
            System.out.printf("⚠️  Tenant %s has hit job limit (%d)%n",
                tenantId, MAX_JOBS_PER_TENANT);
            return false;
        }

        // Add to queue and tracking map
        allJobs.put(job.getJobId(), job);
        queue.offer(job);
        tenantJobCounts.get(tenantId).incrementAndGet();

        System.out.printf("📥 Job %s queued for tenant %s (queue size: %d)%n",
            job.getJobId(), tenantId, queue.size());

        return true;
    }

    /**
     * Take the next job from the queue (blocks until one is available)
     */
    public Job take() throws InterruptedException {
        return queue.take();
    }

    /**
     * Look up any job by ID
     */
    public Job getJob(String jobId) {
        return allJobs.get(jobId);
    }

    /**
     * Mark a job as done and decrement tenant count
     */
    public void markDone(Job job) {
        String tenantId = job.getTenantId();
        AtomicInteger count = tenantJobCounts.get(tenantId);
        if (count != null) {
            count.decrementAndGet();
        }
    }

    public int size() {
        return queue.size();
    }
}
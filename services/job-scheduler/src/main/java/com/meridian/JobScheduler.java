package com.meridian;

import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Main entry point for Meridian Job Scheduler.
 * Starts worker threads and accepts jobs via console for testing.
 */
public class JobScheduler {

    private static final int    NUM_WORKERS  = 3;
    private static final String PYTHON_HOST  = "localhost";
    private static final int    PYTHON_PORT  = 50051;

    public static void main(String[] args) throws InterruptedException {

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║     Meridian Job Scheduler v1.0      ║");
        System.out.println("╚══════════════════════════════════════╝");
        System.out.printf("%nStarting %d workers...%n%n", NUM_WORKERS);

        // Create shared job queue
        JobQueue queue = new JobQueue();

        // Start worker threads
        ExecutorService executor = Executors.newFixedThreadPool(NUM_WORKERS);
        for (int i = 0; i < NUM_WORKERS; i++) {
            executor.submit(new ForecastWorker(queue, PYTHON_HOST, PYTHON_PORT));
        }

        System.out.println("✅ Scheduler ready!\n");
        System.out.println("Commands:");
        System.out.println("  submit <tenantId> <horizonDays>  — submit a job");
        System.out.println("  status <jobId>                   — check job status");
        System.out.println("  quit                             — exit\n");

        // Simple console interface for testing
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();

            if (line.startsWith("submit")) {
                // submit team-analytics 12
                String[] parts = line.split(" ");
                if (parts.length >= 3) {
                    String tenantId    = parts[1];
                    int    horizon     = Integer.parseInt(parts[2]);
                    String datasetRef  = "data/passengers.csv";

                    Job job = new Job(tenantId, datasetRef, horizon);
                    boolean queued = queue.submit(job);

                    if (queued) {
                        System.out.printf("✅ Submitted job %s%n", job.getJobId());
                    } else {
                        System.out.println("❌ Tenant job limit reached");
                    }
                }

            } else if (line.startsWith("status")) {
                String[] parts = line.split(" ");
                if (parts.length >= 2) {
                    String jobId = parts[1];
                    Job job = queue.getJob(jobId);
                    if (job != null) {
                        System.out.println(job);
                    } else {
                        System.out.println("Job not found: " + jobId);
                    }
                }

            } else if (line.equals("quit")) {
                System.out.println("Shutting down...");
                executor.shutdownNow();
                break;
            }
        }

        System.out.println("Goodbye!");
    }
}

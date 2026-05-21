package com.meridian;

import com.meridian.proto.ForecastServiceGrpc;
import com.meridian.proto.ForecastProto;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

/**
 * Worker thread that pulls jobs from the queue
 * and calls the Python gRPC forecast engine.
 */
public class ForecastWorker implements Runnable {

    private final JobQueue queue;
    private final String   pythonHost;
    private final int      pythonPort;

    public ForecastWorker(JobQueue queue, String pythonHost, int pythonPort) {
        this.queue      = queue;
        this.pythonHost = pythonHost;
        this.pythonPort = pythonPort;
    }

    @Override
    public void run() {
        System.out.printf("👷 Worker started — connecting to Python at %s:%d%n",
            pythonHost, pythonPort);

        // Create gRPC channel to Python forecast engine
        ManagedChannel channel = ManagedChannelBuilder
            .forAddress(pythonHost, pythonPort)
            .usePlaintext()
            .build();

        ForecastServiceGrpc.ForecastServiceBlockingStub stub
            = ForecastServiceGrpc.newBlockingStub(channel);

        // Keep processing jobs forever
        while (!Thread.currentThread().isInterrupted()) {
            try {
                // Block until a job is available
                Job job = queue.take();

                System.out.printf("%n⚙️  Processing job %s for tenant %s%n",
                    job.getJobId(), job.getTenantId());

                job.setStatus(Job.Status.RUNNING);

                // Call Python gRPC server
                ForecastProto.ForecastRequest request
                    = ForecastProto.ForecastRequest.newBuilder()
                        .setTenantId(job.getTenantId())
                        .setDatasetRef(job.getDatasetRef())
                        .setHorizonDays(job.getHorizonDays())
                        .build();

                ForecastProto.JobResponse response
                    = stub.submitForecastJob(request);

                // Mark complete
                job.setStatus(Job.Status.DONE);
                job.setModelUsed(response.getStatus());
                queue.markDone(job);

                System.out.printf("✅ Job %s complete%n", job.getJobId());

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("👷 Worker interrupted, shutting down");
                break;
            } catch (Exception e) {
                System.out.printf("❌ Worker error: %s%n", e.getMessage());
            }
        }

        channel.shutdown();
    }
}
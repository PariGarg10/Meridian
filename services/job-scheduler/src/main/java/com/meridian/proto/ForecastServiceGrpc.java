package com.meridian.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.62.2)",
    comments = "Source: forecast.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ForecastServiceGrpc {

  private ForecastServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "meridian.ForecastService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.ForecastRequest,
      com.meridian.proto.ForecastProto.JobResponse> getSubmitForecastJobMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "SubmitForecastJob",
      requestType = com.meridian.proto.ForecastProto.ForecastRequest.class,
      responseType = com.meridian.proto.ForecastProto.JobResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.ForecastRequest,
      com.meridian.proto.ForecastProto.JobResponse> getSubmitForecastJobMethod() {
    io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.ForecastRequest, com.meridian.proto.ForecastProto.JobResponse> getSubmitForecastJobMethod;
    if ((getSubmitForecastJobMethod = ForecastServiceGrpc.getSubmitForecastJobMethod) == null) {
      synchronized (ForecastServiceGrpc.class) {
        if ((getSubmitForecastJobMethod = ForecastServiceGrpc.getSubmitForecastJobMethod) == null) {
          ForecastServiceGrpc.getSubmitForecastJobMethod = getSubmitForecastJobMethod =
              io.grpc.MethodDescriptor.<com.meridian.proto.ForecastProto.ForecastRequest, com.meridian.proto.ForecastProto.JobResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "SubmitForecastJob"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.ForecastRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.JobResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ForecastServiceMethodDescriptorSupplier("SubmitForecastJob"))
              .build();
        }
      }
    }
    return getSubmitForecastJobMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID,
      com.meridian.proto.ForecastProto.JobStatusResponse> getGetJobStatusMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetJobStatus",
      requestType = com.meridian.proto.ForecastProto.JobID.class,
      responseType = com.meridian.proto.ForecastProto.JobStatusResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID,
      com.meridian.proto.ForecastProto.JobStatusResponse> getGetJobStatusMethod() {
    io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID, com.meridian.proto.ForecastProto.JobStatusResponse> getGetJobStatusMethod;
    if ((getGetJobStatusMethod = ForecastServiceGrpc.getGetJobStatusMethod) == null) {
      synchronized (ForecastServiceGrpc.class) {
        if ((getGetJobStatusMethod = ForecastServiceGrpc.getGetJobStatusMethod) == null) {
          ForecastServiceGrpc.getGetJobStatusMethod = getGetJobStatusMethod =
              io.grpc.MethodDescriptor.<com.meridian.proto.ForecastProto.JobID, com.meridian.proto.ForecastProto.JobStatusResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetJobStatus"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.JobID.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.JobStatusResponse.getDefaultInstance()))
              .setSchemaDescriptor(new ForecastServiceMethodDescriptorSupplier("GetJobStatus"))
              .build();
        }
      }
    }
    return getGetJobStatusMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID,
      com.meridian.proto.ForecastProto.ForecastResult> getGetForecastResultMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetForecastResult",
      requestType = com.meridian.proto.ForecastProto.JobID.class,
      responseType = com.meridian.proto.ForecastProto.ForecastResult.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID,
      com.meridian.proto.ForecastProto.ForecastResult> getGetForecastResultMethod() {
    io.grpc.MethodDescriptor<com.meridian.proto.ForecastProto.JobID, com.meridian.proto.ForecastProto.ForecastResult> getGetForecastResultMethod;
    if ((getGetForecastResultMethod = ForecastServiceGrpc.getGetForecastResultMethod) == null) {
      synchronized (ForecastServiceGrpc.class) {
        if ((getGetForecastResultMethod = ForecastServiceGrpc.getGetForecastResultMethod) == null) {
          ForecastServiceGrpc.getGetForecastResultMethod = getGetForecastResultMethod =
              io.grpc.MethodDescriptor.<com.meridian.proto.ForecastProto.JobID, com.meridian.proto.ForecastProto.ForecastResult>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetForecastResult"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.JobID.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.meridian.proto.ForecastProto.ForecastResult.getDefaultInstance()))
              .setSchemaDescriptor(new ForecastServiceMethodDescriptorSupplier("GetForecastResult"))
              .build();
        }
      }
    }
    return getGetForecastResultMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ForecastServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ForecastServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ForecastServiceStub>() {
        @java.lang.Override
        public ForecastServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ForecastServiceStub(channel, callOptions);
        }
      };
    return ForecastServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ForecastServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ForecastServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ForecastServiceBlockingStub>() {
        @java.lang.Override
        public ForecastServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ForecastServiceBlockingStub(channel, callOptions);
        }
      };
    return ForecastServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ForecastServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ForecastServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ForecastServiceFutureStub>() {
        @java.lang.Override
        public ForecastServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ForecastServiceFutureStub(channel, callOptions);
        }
      };
    return ForecastServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     * <pre>
     * Submit a new forecast job
     * </pre>
     */
    default void submitForecastJob(com.meridian.proto.ForecastProto.ForecastRequest request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSubmitForecastJobMethod(), responseObserver);
    }

    /**
     * <pre>
     * Check job status
     * </pre>
     */
    default void getJobStatus(com.meridian.proto.ForecastProto.JobID request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobStatusResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetJobStatusMethod(), responseObserver);
    }

    /**
     * <pre>
     * Get completed forecast result
     * </pre>
     */
    default void getForecastResult(com.meridian.proto.ForecastProto.JobID request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.ForecastResult> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetForecastResultMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service ForecastService.
   */
  public static abstract class ForecastServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return ForecastServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service ForecastService.
   */
  public static final class ForecastServiceStub
      extends io.grpc.stub.AbstractAsyncStub<ForecastServiceStub> {
    private ForecastServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ForecastServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ForecastServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * Submit a new forecast job
     * </pre>
     */
    public void submitForecastJob(com.meridian.proto.ForecastProto.ForecastRequest request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getSubmitForecastJobMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * Check job status
     * </pre>
     */
    public void getJobStatus(com.meridian.proto.ForecastProto.JobID request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobStatusResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetJobStatusMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * Get completed forecast result
     * </pre>
     */
    public void getForecastResult(com.meridian.proto.ForecastProto.JobID request,
        io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.ForecastResult> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetForecastResultMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service ForecastService.
   */
  public static final class ForecastServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<ForecastServiceBlockingStub> {
    private ForecastServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ForecastServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ForecastServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * Submit a new forecast job
     * </pre>
     */
    public com.meridian.proto.ForecastProto.JobResponse submitForecastJob(com.meridian.proto.ForecastProto.ForecastRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getSubmitForecastJobMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * Check job status
     * </pre>
     */
    public com.meridian.proto.ForecastProto.JobStatusResponse getJobStatus(com.meridian.proto.ForecastProto.JobID request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetJobStatusMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * Get completed forecast result
     * </pre>
     */
    public com.meridian.proto.ForecastProto.ForecastResult getForecastResult(com.meridian.proto.ForecastProto.JobID request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetForecastResultMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service ForecastService.
   */
  public static final class ForecastServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<ForecastServiceFutureStub> {
    private ForecastServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ForecastServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ForecastServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * Submit a new forecast job
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.meridian.proto.ForecastProto.JobResponse> submitForecastJob(
        com.meridian.proto.ForecastProto.ForecastRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getSubmitForecastJobMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * Check job status
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.meridian.proto.ForecastProto.JobStatusResponse> getJobStatus(
        com.meridian.proto.ForecastProto.JobID request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetJobStatusMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * Get completed forecast result
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.meridian.proto.ForecastProto.ForecastResult> getForecastResult(
        com.meridian.proto.ForecastProto.JobID request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetForecastResultMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_SUBMIT_FORECAST_JOB = 0;
  private static final int METHODID_GET_JOB_STATUS = 1;
  private static final int METHODID_GET_FORECAST_RESULT = 2;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_SUBMIT_FORECAST_JOB:
          serviceImpl.submitForecastJob((com.meridian.proto.ForecastProto.ForecastRequest) request,
              (io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobResponse>) responseObserver);
          break;
        case METHODID_GET_JOB_STATUS:
          serviceImpl.getJobStatus((com.meridian.proto.ForecastProto.JobID) request,
              (io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.JobStatusResponse>) responseObserver);
          break;
        case METHODID_GET_FORECAST_RESULT:
          serviceImpl.getForecastResult((com.meridian.proto.ForecastProto.JobID) request,
              (io.grpc.stub.StreamObserver<com.meridian.proto.ForecastProto.ForecastResult>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getSubmitForecastJobMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.meridian.proto.ForecastProto.ForecastRequest,
              com.meridian.proto.ForecastProto.JobResponse>(
                service, METHODID_SUBMIT_FORECAST_JOB)))
        .addMethod(
          getGetJobStatusMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.meridian.proto.ForecastProto.JobID,
              com.meridian.proto.ForecastProto.JobStatusResponse>(
                service, METHODID_GET_JOB_STATUS)))
        .addMethod(
          getGetForecastResultMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.meridian.proto.ForecastProto.JobID,
              com.meridian.proto.ForecastProto.ForecastResult>(
                service, METHODID_GET_FORECAST_RESULT)))
        .build();
  }

  private static abstract class ForecastServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ForecastServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.meridian.proto.ForecastProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("ForecastService");
    }
  }

  private static final class ForecastServiceFileDescriptorSupplier
      extends ForecastServiceBaseDescriptorSupplier {
    ForecastServiceFileDescriptorSupplier() {}
  }

  private static final class ForecastServiceMethodDescriptorSupplier
      extends ForecastServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    ForecastServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ForecastServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ForecastServiceFileDescriptorSupplier())
              .addMethod(getSubmitForecastJobMethod())
              .addMethod(getGetJobStatusMethod())
              .addMethod(getGetForecastResultMethod())
              .build();
        }
      }
    }
    return result;
  }
}

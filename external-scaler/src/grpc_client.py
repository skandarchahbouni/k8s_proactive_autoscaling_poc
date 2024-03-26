import grpc
import externalscaler_pb2
import externalscaler_pb2_grpc


with grpc.insecure_channel("localhost:50051") as channel:
    print("------------------IsActive------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    is_active_request = externalscaler_pb2.ScaledObjectRef(
        name="test", namespace="default", scalerMetadata={"test": "test"}
    )
    response = stub.IsActive(is_active_request)
    print(response.result)

    print("------------------GetMetricsSpec------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    request = externalscaler_pb2.ScaledObjectRef(
        name="test", namespace="default", scalerMetadata={"test": "test"}
    )
    response = stub.GetMetricSpec(request)
    print(response.metricSpecs)

    print("------------------GetMetrics------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    scaledObjectRef = externalscaler_pb2.ScaledObjectRef(
        name="test", namespace="default", scalerMetadata={"test": "test"}
    )
    request = externalscaler_pb2.GetMetricsRequest(
        scaledObjectRef=scaledObjectRef, metricName="test"
    )
    response = stub.GetMetrics(request)
    print(response.metricValues)

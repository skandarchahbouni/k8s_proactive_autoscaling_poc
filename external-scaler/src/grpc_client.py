import grpc
import externalscaler_pb2
import externalscaler_pb2_grpc


with grpc.insecure_channel("localhost:50051") as channel:
    scaledObjectRef = externalscaler_pb2.ScaledObjectRef(
        name="test",
        namespace="default",
        scalerMetadata={
            "serverAddress": "test",
            "metric": "rps",
            "query": "",
            "threshold": "12",
        },
    )
    print("------------------IsActive------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    try:
        response = stub.IsActive(scaledObjectRef)
        print(response.result)
    except Exception as e:
        print("Exception: IsActive")

    print("------------------GetMetricsSpec------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    try:
        response = stub.GetMetricSpec(scaledObjectRef)
        print(response.metricSpecs)
    except Exception as e:
        print("Exception: GetMetricsSpec")

    print("------------------GetMetrics------------------")
    stub = externalscaler_pb2_grpc.ExternalScalerStub(channel)
    request = externalscaler_pb2.GetMetricsRequest(
        scaledObjectRef=scaledObjectRef, metricName="rps"
    )
    try:
        response = stub.GetMetrics(request)
        print(response.metricValues)
    except Exception as e:
        print("Exception: GetMetrics")

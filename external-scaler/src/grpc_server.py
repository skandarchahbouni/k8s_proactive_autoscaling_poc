from concurrent import futures
import grpc
import externalscaler_pb2
import externalscaler_pb2_grpc
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ExternalScalerServicer(externalscaler_pb2_grpc.ExternalScalerServicer):
    def IsActive(self, request, context):
        logging.info("IsActive function is called.")
        # request
        print(request.name)
        print(request.namespace)
        print(request.scalerMetadata)
        # returning response
        response = externalscaler_pb2.IsActiveResponse()
        response.result = True
        return response

    def StreamIsActive(self, request, context):
        return super().StreamIsActive(request, context)

    def GetMetricSpec(self, request, context):
        logging.info("GetMetricSpec function is called.")
        # request
        print(request.name)
        print(request.namespace)
        print(request.scalerMetadata)
        # returning response
        response = externalscaler_pb2.GetMetricSpecResponse()
        metric_spec = externalscaler_pb2.MetricSpec()
        metric_spec.metricName = "key1"
        metric_spec.targetSize = 5
        response.metricSpecs.append(metric_spec)
        return response

    def GetMetrics(self, request, context):
        logging.info("GetMetrics is called.")
        # scaledObjectRef
        scaledObjectRef = request.scaledObjectRef
        print(scaledObjectRef.name)
        print(scaledObjectRef.namespace)
        print(scaledObjectRef.scalerMetadata)
        # metricName
        print(request.metricName)
        # returning response
        response = externalscaler_pb2.GetMetricsResponse()
        metric_value = externalscaler_pb2.MetricValue()
        metric_value.metricName = "key1"
        metric_value.metricValue = 20
        response.metricValues.append(metric_value)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    externalscaler_pb2_grpc.add_ExternalScalerServicer_to_server(
        ExternalScalerServicer(), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    # server.add_insecure_port("localhost:50051")
    server.start()
    logging.info("Server listening on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

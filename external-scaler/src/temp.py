from concurrent import futures
import grpc
import externalscaler_pb2
import externalscaler_pb2_grpc
import logging
from utils import simulate_prediction

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_request(metadata, context) -> bool:
    if (
        not "serverAddress" in metadata
        or not "query" in metadata
        or not "metric" in metadata
        or not "threshold" in metadata
    ):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details("Missing required field(s).")
        logging.error("Missing required field(s).")
        return False
    return True


def get_predicted_value(prometheus_url, a):
    pass


class ExternalScalerServicer(externalscaler_pb2_grpc.ExternalScalerServicer):
    def IsActive(self, request, context):
        logging.info("IsActive function is called.")
        # validation
        is_valid = validate_request(metadata=request.scalerMetadata, context=context)
        if not is_valid:
            return externalscaler_pb2.IsActiveResponse()
        # ----
        response = externalscaler_pb2.IsActiveResponse()
        # TODO: add logic here (either using simulate_predict or fetch_data...)
        response.result = True
        return response

    def StreamIsActive(self, request, context):
        return super().StreamIsActive(request, context)

    def GetMetricSpec(self, request, context):
        logging.info("GetMetricSpec function is called.")
        # validation
        is_valid = validate_request(metadata=request.scalerMetadata, context=context)
        if not is_valid:
            return externalscaler_pb2.GetMetricSpecResponse()
        # ----
        response = externalscaler_pb2.GetMetricSpecResponse()
        metric_spec = externalscaler_pb2.MetricSpec()
        metric_spec.metricName = request.scalerMetadata["metric"]
        metric_spec.targetSize = int(request.scalerMetadata["threshold"])
        response.metricSpecs.append(metric_spec)
        return response

    def GetMetrics(self, request, context):
        logging.info("GetMetrics is called.")
        # validation
        metadata = request.scaledObjectRef.scalerMetadata
        is_valid = validate_request(metadata=metadata, context=context)
        if not is_valid:
            return externalscaler_pb2.GetMetricsResponse()
        # -----
        response = externalscaler_pb2.GetMetricsResponse()
        metric_value = externalscaler_pb2.MetricValue()
        metric_value.metricName = request.metricName
        try:
            predicted_value = get_predicted_value(
                prometheus_url=metadata["serverAddress"],
                query=metadata["query"],
                period=metadata["period"],
            )
        except Exception as e:
            logging.error(f"Exception: => GetMetrics \n{e}")
        logging.info(f"Predicted ===> {predicted_value}")
        metric_value.metricValue = predicted_value
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
    logging.info(f"Server listening on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

from abc import abstractmethod, ABC

from opentelemetry import trace, metrics, propagate
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagators.aws import AwsXRayPropagator
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import _set_tracer_provider
from opentelemetry.metrics._internal import _set_meter_provider


class KLYMInstrumentor(ABC):

    def __init__(self, service_name: str, endpoint: str) -> None:
        propagate.set_global_textmap(AwsXRayPropagator())
        self._service_name = service_name
        self._endpoint = endpoint

    @property
    def _resource(self):
        return Resource.create(attributes={"service.name": self._service_name})

    @property
    def _span_exporter(self):
        return OTLPSpanExporter(endpoint=self._endpoint)

    @property
    def _processor(self):
        return BatchSpanProcessor(span_exporter=self._span_exporter)

    @property
    def _metrics_exporter(self):
        return OTLPMetricExporter(endpoint=self._endpoint)

    @property
    def _reader(self):
        return PeriodicExportingMetricReader(exporter=self._metrics_exporter)

    @property
    def tracer_provider(self):
        tracer_provider = TracerProvider(resource=self._resource, id_generator=AwsXRayIdGenerator())
        tracer_provider.add_span_processor(span_processor=self._processor)
        _set_tracer_provider(tracer_provider=tracer_provider, log=False)
        return tracer_provider

    @property
    def meter_provider(self):
        meter_provider = MeterProvider(resource=self._resource, metric_readers=[self._reader])
        _set_meter_provider(meter_provider, log=False)
        return meter_provider

    @abstractmethod
    def instrument(self, **kwargs):
        pass

from opentelemetry.instrumentation.requests import RequestsInstrumentor

from klym_telemetry.instrumenters.base import KLYMInstrumentor


class _RequestsInstrumentor(KLYMInstrumentor):

    def __init__(self, service_name: str, endpoint: str) -> None:
        super().__init__(service_name=service_name, endpoint=endpoint)

    def instrument(self):
        RequestsInstrumentor().instrument(
            tracer_provider=self.tracer_provider,
            meter_provider=self.meter_provider
        )

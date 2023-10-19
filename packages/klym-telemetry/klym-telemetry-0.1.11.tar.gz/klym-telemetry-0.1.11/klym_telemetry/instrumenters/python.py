from typing import Collection

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor

from klym_telemetry.instrumenters.base import KLYMInstrumentor


class PythonInstrumentor(BaseInstrumentor):

    def instrumentation_dependencies(self) -> Collection[str]:
        return ()

    def _instrument(self, **kwargs):
        kwargs.get("tracer_provider")
        kwargs.get("meter_provider")

    def _uninstrument(self, **kwargs):
        pass


class _PythonInstrumentor(KLYMInstrumentor):

    def __init__(self, service_name: str, endpoint: str) -> None:
        super().__init__(service_name=service_name, endpoint=endpoint)

    def instrument(self):
        PythonInstrumentor().instrument(
            tracer_provider=self.tracer_provider,
            meter_provider=self.meter_provider
        )

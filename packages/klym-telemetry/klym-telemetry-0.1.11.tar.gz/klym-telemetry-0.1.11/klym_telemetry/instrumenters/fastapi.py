from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from klym_telemetry.instrumenters.base import KLYMInstrumentor


class _FastAPIInstrumentor(KLYMInstrumentor):

    def __init__(self, service_name: str, endpoint: str, **kwargs) -> None:
        super().__init__(service_name=service_name, endpoint=endpoint)
        if "app" not in kwargs:
            raise ValueError("Missing required argument: app")
        self._app = kwargs.pop("app")
        self._excluded_urls = None
        if "excluded_urls" in kwargs:
            self._excluded_urls = kwargs.pop("excluded_urls")

    def instrument(self):
        FastAPIInstrumentor.instrument_app(
            app=self._app,
            tracer_provider=self.tracer_provider,
            meter_provider=self.meter_provider,
            excluded_urls=self._excluded_urls,
        )

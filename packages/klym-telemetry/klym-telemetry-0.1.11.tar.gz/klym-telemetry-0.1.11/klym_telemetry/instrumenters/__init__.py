import traceback
from enum import Enum
import klym_telemetry.instrumenters.module_import as importer

class SupportedInstrumenters(Enum):

    INSTRUMENTERS = {
        "python": ("klym_telemetry.instrumenters.python", "_PythonInstrumentor"),
        "fastapi": ("klym_telemetry.instrumenters.fastapi", "_FastAPIInstrumentor"),
        "airflow": ("klym_telemetry.instrumenters.airflow", "_AirflowInstrumentor"),
        "django": ("klym_telemetry.instrumenters.django", "_DjangoInstrumentor"),
        "celery": ("klym_telemetry.instrumenters.celery", "_CeleryInstrumentor"),
        "psycopg2": ("klym_telemetry.instrumenters.psycopg2", "_Psycopg2Instrumentor"),
        "requests": ("klym_telemetry.instrumenters.requests", "_RequestsInstrumentor"),
        "aiohttp": ("klym_telemetry.instrumenters.aiohttp", "_AioHttpClientInstrumentor"),
    }

def instrument_app(app_type: str, **kwargs):
    try:
        package = SupportedInstrumenters.INSTRUMENTERS.value.get(app_type)[0]
        classname = SupportedInstrumenters.INSTRUMENTERS.value.get(app_type)[1]
        return importer.import_module(package, classname)(**kwargs).instrument()
    except Exception as e:
        traceback.print_exc()
        print(f"Dependency error. You need to import the instrumenter for {app_type} if you want to use it")
        raise

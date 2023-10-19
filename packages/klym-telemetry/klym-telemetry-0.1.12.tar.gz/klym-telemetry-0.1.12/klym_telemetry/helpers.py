from abc import ABC
from typing import Dict, ContextManager

from opentelemetry import trace, metrics
from opentelemetry.metrics import UpDownCounter
from opentelemetry.trace.span import Span


class KlymTelemetry(ABC):
    """
    Class wrapping the OpenTelemetry functionality, like metrics and spans. This class serves
    2 functionalities:

    1. It keeps singleton instances of the different metrics created using this class to guarantee
    consistent reporting across the app
    2. It makes sure the same tracer and meter instances are used consistently across the app to
    avoid having instances all over the app

    This is a static class, i.e. all methods are meant to use directly on the class. No instance
    of this class should be created at any point
    """

    __tracer = trace.get_tracer(__name__)
    __meter = metrics.get_meter(__name__)
    __up_down_counters: Dict[str, UpDownCounter] = {}

    @staticmethod
    def __get_or_create_up_down_counter(name: str, description: str) -> UpDownCounter:
        metric = KlymTelemetry.__up_down_counters.get(name, None)
        if not metric:
            metric = KlymTelemetry.__meter.create_up_down_counter(name, description=description)
            KlymTelemetry.__up_down_counters[name] = metric

        return metric

    @staticmethod
    def add_event_curr_span(value: str) -> None:
        """Adds an event to the current span"""
        trace.get_current_span().add_event(value)

    @staticmethod
    def new_curr_span(name: str, **kwargs) -> ContextManager[Span]:   # type: ignore
        """Starts a new span and sets it as the current span"""

        return KlymTelemetry.__tracer.start_as_current_span(name, **kwargs)

    @staticmethod
    def set_attr_curr_span(key: str, value: str) -> None:
        """Sets an attribute to the current span"""
        trace.get_current_span().set_attribute(key, value)

    @staticmethod
    def up(name: str, by: int = 1, description: str = "") -> None:
        """
        Increases the counter with the given name by `by`
        By default, increases the counter by 1
        """

        metric = KlymTelemetry.__get_or_create_up_down_counter(name, description)
        metric.add(by)

    @staticmethod
    def down(name: str, by: int = 1, description: str = "") -> None:
        """
        Reduces the counter with the given name by `-by`
        By default, decreases the counter by 1
        """

        metric = KlymTelemetry.__get_or_create_up_down_counter(name, description)
        metric.add(-1 * by)

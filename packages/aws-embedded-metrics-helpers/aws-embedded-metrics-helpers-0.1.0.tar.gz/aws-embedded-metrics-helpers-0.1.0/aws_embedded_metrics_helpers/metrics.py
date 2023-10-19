import asyncio
import inspect
import logging
from copy import deepcopy
from functools import wraps
from time import time
from typing import Any, Callable, Dict, Optional, Tuple, Union

from aws_embedded_metrics.logger.metrics_logger_factory import create_metrics_logger


_UNKNOWN_DIMENSION_VALUE = "unknown"
_DEFAULT_DIMENSIONS_MAP = {
    "namespace": "__class.name",
    "operation": "__function.name",
}

_DIMENSION_VALUES_HELPERS = {
    "__class.name": lambda fn, cls_self_arg: (
        cls_self_arg.__name__
        if inspect.isclass(cls_self_arg)
        else cls_self_arg.__class__.__name__
    ),
    "__function.name": lambda fn, cls_self_arg: fn.__name__,
}


Primitive = Union[str, int, float, bool]


class MetricDimensionsMap:
    dimensions_map: Dict[str, Optional[Primitive]] = _DEFAULT_DIMENSIONS_MAP


class MetricNames:
    TIME = "Time"
    SUCCESS = "Success"
    SUCCESs_TIME = "SuccessTime"
    FAILURE = "Failure"
    FAILURE_TIME = "FailureTime"
    VALIDATION_FAILURE = "ValidationError"
    CLIENT_ERROR = "ClientError"
    DEPENDENCY_ERROR = "DependencyError"
    INTERNAL_ERROR = "InternalError"
    UNKNOWN_ERROR = "UnknownError"


logger = logging.getLogger(__name__)


def _get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as exc:
        if str(exc).startswith("There is no current event loop in thread"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        else:
            logger.error(f"Error getting current thread event loop: {str(exc)}")
            raise exc


def _get_current_time_ms():
    return int(time() * 1000)


def _metrics_log_provider_function_wrapper(
    dimensions_map: Dict[str, str],
    fn: Callable,
    args: Tuple[Any],
    kwargs: Dict[str, Any],
):
    logger = create_metrics_logger()
    logger.put_dimensions(dimensions_map)
    if "metrics_logger" in inspect.getfullargspec(fn).args:
        kwargs["metrics_logger"] = logger

    start_time = _get_current_time_ms()
    try:
        result = fn(*args, **kwargs)
        time_taken = _get_current_time_ms() - start_time
        if not logger.context.metrics:  # If no metrics are created, publish some default metrics
            logger.put_metric(MetricNames.SUCCESS, 1)
            logger.put_metric(MetricNames.FAILURE, 0)
            logger.put_metric(MetricNames.TIME, time_taken, "Milliseconds")
            logger.put_metric(MetricNames.SUCCESs_TIME, time_taken, "Milliseconds")
        return result
    except Exception as exc:
        time_taken = _get_current_time_ms() - start_time
        if not logger.context.metrics:  # If no metrics are created, publish some default metrics
            logger.put_metric(MetricNames.SUCCESS, 0)
            logger.put_metric(MetricNames.FAILURE, 1)
            logger.put_metric(type(exc).__name__, 1)
            logger.put_metric(MetricNames.TIME, time_taken, "Milliseconds")
            logger.put_metric(MetricNames.FAILURE_TIME, time_taken, "Milliseconds")
        raise exc
    finally:
        loop = _get_event_loop()
        loop.run_until_complete(logger.flush())


def get_updated_dimensions_map(dimension_values: Dict[str, Optional[Primitive]], fn, cls_self_arg):
    dimensions_map = deepcopy(
        MetricDimensionsMap.dimensions_map if MetricDimensionsMap.dimensions_map else _DEFAULT_DIMENSIONS_MAP
    )

    for dimension_name, dimension_value in dimensions_map.items():
        if dimension_name in dimension_values:
            dimensions_map[dimension_name] = dimension_values[dimension_name]
        elif dimension_value:
            if dimension_value in _DIMENSION_VALUES_HELPERS:
                dimensions_map[dimension_name] = _DIMENSION_VALUES_HELPERS[dimension_value](fn, cls_self_arg)
        else:
            logger.warn(f"No value provided for dimension {dimension_name}. Setting it to 'unknown'")
            dimensions_map[dimension_name] = _UNKNOWN_DIMENSION_VALUE

    return dimensions_map


def metric_scope_func(**dimension_values: Optional[Primitive]):
    def custom_metric_scope_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            dimensions_map = get_updated_dimensions_map(dimension_values, fn, None)
            return _metrics_log_provider_function_wrapper(dimensions_map, fn, args, kwargs)

        return wrapper

    return custom_metric_scope_decorator


def metric_scope_method(**dimension_values: Optional[Primitive]):
    def custom_metric_scope_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            dimensions_map = get_updated_dimensions_map(dimension_values, fn, args[0])
            return _metrics_log_provider_function_wrapper(dimensions_map, fn, args, kwargs)

        return wrapper

    return custom_metric_scope_decorator

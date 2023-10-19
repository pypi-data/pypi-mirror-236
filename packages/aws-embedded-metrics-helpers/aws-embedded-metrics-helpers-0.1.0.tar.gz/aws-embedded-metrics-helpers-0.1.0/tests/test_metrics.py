import unittest.mock as mock
import pytest
from aws_embedded_metrics.logger.metrics_logger_factory import create_metrics_logger

from aws_embedded_metrics_helpers.metrics import (
    _metrics_log_provider_function_wrapper,
    metric_scope_func,
    metric_scope_method,
)


@pytest.fixture
def mock_create_metrics_logger():
    with mock.patch(
        "aws_embedded_metrics_helpers.metrics.create_metrics_logger"
    ) as mock_create_metrics_logger:
        mock_logger = mock.create_autospec(create_metrics_logger())
        mock_create_metrics_logger.return_value = mock_logger
        yield mock_create_metrics_logger, mock_logger


@pytest.fixture
def mock_create_metrics_logger_wrapper():
    with mock.patch(
        "aws_embedded_metrics_helpers.metrics._metrics_log_provider_function_wrapper"
    ) as mock_create_metrics_logger_wrapper:
        mock_create_metrics_logger_wrapper.return_value = "function-result"
        yield mock_create_metrics_logger_wrapper


@pytest.fixture
def mock_asyncio():
    with mock.patch("aws_embedded_metrics_helpers.metrics._get_event_loop") as mock_get_event_loop:
        mock_event_loop = mock.MagicMock()
        mock_event_loop.run_until_complete.return_value = None
        mock_get_event_loop.side_effect = mock_event_loop
        yield mock_get_event_loop


@pytest.fixture
def get_event_loop_result(request):
    return request.getfixturevalue(request.param) if request.param else None


@pytest.fixture
def new_event_loop_result(request):
    return request.getfixturevalue(request.param) if request.param else None


def test_metric_scope_func(mock_create_metrics_logger_wrapper):
    @metric_scope_func(namespace="namespace", operation="operation")
    def test_func():
        return True

    assert test_func() == "function-result"

    mock_create_metrics_logger_wrapper.assert_called_once()


def test_metric_scope_func_no_operation(mock_create_metrics_logger_wrapper):
    @metric_scope_func(namespace="namespace")
    def test_func():
        return True

    assert test_func() == "function-result"

    mock_create_metrics_logger_wrapper.assert_called_once()


def test_metric_scope_method(mock_create_metrics_logger_wrapper):
    class TestClass:
        @metric_scope_method(operation="operation")
        def test_method(self):
            return True

    assert TestClass().test_method() == "function-result"

    mock_create_metrics_logger_wrapper.assert_called_once()


def test_metric_scope_method_no_operation(mock_create_metrics_logger_wrapper):
    class TestClass:
        @metric_scope_method()
        def test_method(self):
            return True

    assert TestClass().test_method() == "function-result"

    mock_create_metrics_logger_wrapper.assert_called_once()


def test_create_metrics_logger_wrapper_metrics_added(mock_create_metrics_logger, mock_asyncio):
    mock_create_metrics_logger[1].context.metrics = {"test": "test"}
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    def test_func(metrics_logger):
        metrics_logger.put_metric(key="key", value=1)
        return True

    assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    mock_create_metrics_logger[1].put_metric.assert_called_once()
    mock_create_metrics_logger[1].put_metric.assert_called_with(key="key", value=1)
    mock_asyncio.assert_called_once()


def test_create_metrics_logger_wrapper_metrics_added_raise_exception(mock_create_metrics_logger, mock_asyncio):
    mock_create_metrics_logger[1].context.metrics = {"test": "test"}
    expected_exc = Exception("test-error")
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    def test_func(metrics_logger):
        metrics_logger.put_metric(key="key", value=1)
        raise expected_exc

    with pytest.raises(Exception, match="test-error"):
        assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    mock_create_metrics_logger[1].put_metric.assert_called_once()
    mock_create_metrics_logger[1].put_metric.assert_called_with(key="key", value=1)
    mock_asyncio.assert_called_once()


def test_create_metrics_logger_wrapper_no_metrics_added(mock_create_metrics_logger, mock_asyncio):
    def test_func(metrics_logger):
        return True
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    assert mock_create_metrics_logger[1].put_metric.call_count == 4
    mock_create_metrics_logger[1].put_metric.assert_any_call("Success", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Failure", 0)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Time", mock.ANY, "Milliseconds")
    mock_create_metrics_logger[1].put_metric.assert_any_call("SuccessTime", mock.ANY, "Milliseconds")
    mock_asyncio.assert_called_once()


def test_create_metrics_logger_wrapper_no_metrics_added_raise_exception(mock_create_metrics_logger, mock_asyncio):
    expected_exc = Exception("test-error")
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    def test_func(metrics_logger):
        raise expected_exc

    with pytest.raises(Exception, match="test-error"):
        assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    assert mock_create_metrics_logger[1].put_metric.call_count == 5
    mock_create_metrics_logger[1].put_metric.assert_any_call("Success", 0)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Failure", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Exception", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Time", mock.ANY, "Milliseconds")
    mock_create_metrics_logger[1].put_metric.assert_any_call("FailureTime", mock.ANY, "Milliseconds")
    mock_asyncio.assert_called_once()


def test_create_metrics_logger_wrapper_no_logger_param(mock_create_metrics_logger, mock_asyncio):
    def test_func():
        return True
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    assert mock_create_metrics_logger[1].put_metric.call_count == 4
    mock_create_metrics_logger[1].put_metric.assert_any_call("Success", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Failure", 0)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Time", mock.ANY, "Milliseconds")
    mock_create_metrics_logger[1].put_metric.assert_any_call("SuccessTime", mock.ANY, "Milliseconds")
    mock_asyncio.assert_called_once()


def test_create_metrics_logger_wrapper_no_logger_param_raise_exception(mock_create_metrics_logger, mock_asyncio):
    expected_exc = Exception("test-error")
    dimensions_map = {
        "Namespace": "test-namespace",
        "Operation": "test-operation",
    }

    def test_func():
        raise expected_exc

    with pytest.raises(Exception, match="test-error"):
        assert _metrics_log_provider_function_wrapper(dimensions_map, test_func, (), {})

    mock_create_metrics_logger[0].assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_once()
    mock_create_metrics_logger[1].put_dimensions.assert_called_with(dimensions_map)
    assert mock_create_metrics_logger[1].put_metric.call_count == 5
    mock_create_metrics_logger[1].put_metric.assert_any_call("Success", 0)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Failure", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Exception", 1)
    mock_create_metrics_logger[1].put_metric.assert_any_call("Time", mock.ANY, "Milliseconds")
    mock_create_metrics_logger[1].put_metric.assert_any_call("FailureTime", mock.ANY, "Milliseconds")
    mock_asyncio.assert_called_once()

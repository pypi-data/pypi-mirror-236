# aws-embedded-metrics-python-helper

Some helper decorators that use the [`aws-embedded-metrics`](https://github.com/awslabs/aws-embedded-metrics-python) Python library to make publishing metrics from code a little bit easier

## How to use

For configuring the AWS embedded metrics library, follow the [configuration section](https://github.com/awslabs/aws-embedded-metrics-python#configuration) in the aws-embedded-metrics-python GitHub repo. This section provides a comprehensive explanation on how to configure the library to be able to publish your metrics correctly.

Once done, this library provides you with the ability to decorate your functions and class methods with two decorators.

- `metric_scope_func` - Use to decorate functions to publish metrics for them.
- `metric_scope_method` - Use to decorate class methods to publish metrics for them.

By default, these two functions can take two metric dimension values: `namespace` and `operation`. Depending on which decorator is used, some or all of these are optional.

### Using `metric_scope_func`

Example:

```python
from aws_embedded_metrics_helpers.metrics import metric_scope_func


# Providing all possible parameters
@metric_scope_func(namespace="metric_namespace", operation="metric_operation")
def foo():
    return True

# Providing only required parameters
@metric_scope_func(namespace="metric_namespace")
def foo():
    return True

# Using on a static method
class FooBar:
    @metric_scope_func(namespace="metric_namespace", operation="metric_operation")
    @staticmethod
    def foo():
        return True
```

By default, the `metric_scope_func` decorator requires providing a value for the `namespace` dimension. The `operation` dimension is an optional parameter for `metric_scope_func`. If not provided, the default value used for the `operation` dimension is the name of the function.

It is recommended to use this decorator for functions and static methods.

### Using `metric_scope_method`

Example:

```python
from aws_embedded_metrics_helpers.metrics import metric_scope_method


# Using on a method with all possible parameters
class FooBar:
    @metric_scope_method(namespace="metric_namespace", operation="metric_operation")
    def foo(self):
        return True


# Using on a method with only required parameters
class FooBar:
    @metric_scope_method()
    def foo(self):
        return True


# Using on a class method
class FooBar:
    @metric_scope_method(namespace="metric_namespace", operation="metric_operation")
    @classmethod
    def foo(cls):
        return True
```

By default, the `metric_scope_method` decorator doesn't require any dimensions to be provided as parameters. Both, the `namespace` dimension and `operation` dimension are optional parameters for `metric_scope_method`. If not provided, the default value used for the `namesapce` dimension is the name of the class, and the default value used for the `operation` dimension is the name of the method.

It is recommended to use this decorator for methods and class methods.

### Metrics being published

By default the decorators will publish the following metrics for the annotated functions and methods:

- **Success** - If the function has successfully executed, this metric will be published with a value of `1`. If the function raises an error, then it will be published with a value of `0`.
- **Failure** - If the function has successfully executed, this metric will be published with a value of `0`. If the function raises an error, then it will be published with a value of `1`.
- **Time** - This metric is published with the amount of time it took the function to execute (in milliseconds).
- **SuccessTime** - This metric is published with the amount of time it took the function to execute if the function has succeeded (in milliseconds).
- **FailureTime** - This metric is published with the amount of time it took the function to execute if the function has raised an error (in milliseconds).
- When a function raises an error, a metric with the name of the error is also published with a value of `1`.

### Overriding default published metrics

To publish your own metrics instead of relying on the default generated metrics, you can take the parameter `metrics_logger` as an argument in your function/method, which is an instance of `MetricsLogger` from [`aws-embedded-metrics`](https://github.com/awslabs/aws-embedded-metrics-python#metricslogger).

```python
from aws_embedded_metrics.logger.metrics_logger import MetricsLogger
from aws_embedded_metrics_helpers.metrics import metric_scope_func, metric_scope_method


@metric_scope_func(namespace="metric_namespace")
def foo(metrics_logger: MetricsLogger):
    metrics_logger.put_metric("CustomTime", 200, "Milliseconds", StorageResolution.STANDARD)
    return True

# Using on a static method
class FooBar:
    @metric_scope_method()
    def foo(self, metrics_logger: MetricsLogger):
        metrics_logger.put_metric("CustomTime", 200, "Milliseconds", StorageResolution.STANDARD)
        return True
```

Check out the [`MetricsLogger` API docs in `aws-embedded-metrics`](https://github.com/awslabs/aws-embedded-metrics-python#metricslogger) for more details on how to use it.

### Overriding default metric dimensions

If you wish to override the metric dimensions we take as inputs through the decorators, you can do so by overriding the `MetricDimensionsMap.dimensions_map`, where the key is the name of the dimension, and the value denotes whether it has a default value or not.

```python
from aws_embedded_metrics_helpers.metrics import MetricDimensionsMap
from aws_embedded_metrics_helpers.metrics import metric_scope_func


MetricDimensionsMap.dimensions_map = {
    "custom_dimension": None,
    "custom_dimension_default_str": "default_value",
    "custom_dimension_default_int": 1,
    "custom_dimension_default_float": 1.5,
    "custom_dimension_default_bool": True,
    "class_dimension": "__class.name",
    "function_dimension": "__function.name",
}


@metric_scope_func(namespace="metric_namespace")
def foo():
    return True
```

If a key is provided with the value set to `None`, then the dimension becomes a required parameter to be passed to the decorators. If the parameter is not provided, then the default value will be set to `"unknown"`.

If a key is provided with any primitive value, then the dimension becomes an optional parameter to be passed to the decorators. If the parameter is not provided, then the default value will be set to the primitive value provided for the dimension in the `MetricDimensionsMap.dimensions_map` map.

Alongside this, we have "magic" default values that can be used to use details about the class or function as the default value for a dimension if they are not overriden through the decorator parameters. The currently supported list of "magic" default values are:

- `"__class.name"` - The name of the class of methods decorated with `metric_scope_method`. This works based on the assumption that the first argument in a method is the class or object (`cls` or `self`), and determines the class name based on that. Note that for functions decorated with `metric_scope_func`, this will be treated the same as `None`, meaning that it will become a required parameter, otherwise `"unknown"` will be used as the default value.
- `"__function.name"` - The name of the method decorated with `metric_scope_method` and function decorated with `metric_scope_func`.

### Contributing

Currently there are no contribution guidelines. If you have any issues or feature requests, create one under the issues tab and we can discuss the process to follow to contribute to this repository.

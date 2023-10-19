from setuptools import find_packages, setup

setup(
    name="aws-embedded-metrics-helpers",
    packages=find_packages(include=["aws_embedded_metrics_helpers"]),
    install_requires=["aws-embedded-metrics"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
    version="0.1.0",
    description=(
        "Some helper decorators that use the aws-embedded-metrics to make "
        "publishing metrics from code a little bit easier"
    ),
    author="Sabarna Chakravarty",
    author_email="sabarnac@gmail.com"
)

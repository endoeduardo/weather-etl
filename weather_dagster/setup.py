from setuptools import find_packages, setup

setup(
    name="weather_dagster",
    packages=find_packages(exclude=["weather_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "requests"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)

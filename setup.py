from setuptools import setup, find_packages

setup(
    name="tps_balancer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
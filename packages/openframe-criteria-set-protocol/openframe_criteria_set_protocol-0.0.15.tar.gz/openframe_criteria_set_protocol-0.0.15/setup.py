from setuptools import find_packages, setup

setup(
    name='openframe_criteria_set_protocol',
    packages=find_packages(),
    version='0.0.15',
    description='A protocol and tools for defining and working with criteria sets',
    author='Andrés Angulo <aa@openframe.org>',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)

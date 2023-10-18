from setuptools import setup, find_packages

setup(
    name='weather_program',
    version='0.1',
    description='weatherProgram',
    long_description="weatherProgram",
    long_description_content_type='text/x-rst',
    url="https://gitlab.com/stebasta/2023_assignment1_weather.git",
    author='Gruppo SteSte',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
        'requests',
    ],
)

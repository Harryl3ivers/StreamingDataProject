from setuptools import setup, find_packages

setup(
    name="guardian_streamer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "boto3",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "guardian-streamer=cli:main",
        ],
    },
)
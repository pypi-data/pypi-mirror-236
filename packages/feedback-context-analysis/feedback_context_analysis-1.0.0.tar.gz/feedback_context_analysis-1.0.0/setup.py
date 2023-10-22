from setuptools import setup, find_packages
# List of requirements
requirements = []  # This could be retrieved from requirements.txt
# Package (minimal) configuration
setup(
    name="feedback_context_analysis",
    version="1.0.0",
    description="identify whether a piece of text is contextual enough as a feedback or not",
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements
)
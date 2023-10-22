from setuptools import setup, find_packages
# List of requirements
requirements = []  # This could be retrieved from requirements.txt
# Package (minimal) configuration
setup(
    name="feedback-analysis",
    version="1.0.0",
    description="classify feedback into 'product aspect', 'customer experience', 'issues'",
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements
)
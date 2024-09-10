# __init__.py

print("Initializing my ITD-EPA Package")

version = "1.0.0"

def print_version():
    print(f"Package version: {version}")

from .lambda_function import lambda_handler
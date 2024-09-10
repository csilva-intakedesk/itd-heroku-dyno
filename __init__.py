"""
This module initializes the ITD-EPA package and provides access to the lambda_handler.
"""

from .lambda_function import handler

print("Initializing my ITD-EPA Package")

VERSION = "1.0.0"

def print_version():
    """
    Prints the current version of the package.
    """
    print(f"Package version: {VERSION}")

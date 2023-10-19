"""The Watz Python SDK."""

from importlib.metadata import version

__version__ = version("watz")

from . import models
from .client import Client

__all__ = ["models", "Client"]

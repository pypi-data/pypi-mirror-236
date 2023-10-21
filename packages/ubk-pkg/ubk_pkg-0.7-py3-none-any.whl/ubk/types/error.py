"""
error response dataclass.
"""
from dataclasses import dataclass


@dataclass
class ErrorMessage:
    """
    ErrorMessage represents.
    """
    uz: str
    ru: str
    en: str


@dataclass
class Error:
    """
    Error represents.
    """
    code: int
    message: ErrorMessage


@dataclass
class Host:
    """
    Host represents.
    """
    host: str
    timestamp: str


@dataclass
class ErrorResponse:
    """
    ErrorResponse represents.
    """
    jsonrpc: str
    id: str
    status: bool
    origin: str
    host: Host
    result: str = None
    error: Error = None

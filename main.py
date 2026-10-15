"""Punto de entrada compatible con `uvicorn main:app`."""
from app.main import app

__all__ = ["app"]

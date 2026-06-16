"""Automation sessions for aruba-ssid-manager."""

from __future__ import annotations

import nox

nox.options.sessions = ["tests"]


@nox.session
def tests(session: nox.Session) -> None:
    """Run the test suite under the active interpreter."""
    session.install("-e", ".")
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=aruba_ssid_manager", "--cov-report=term-missing")

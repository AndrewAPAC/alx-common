# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# pytest routines for alx.itrs.environment

import os
import pytest
from alx.itrs.environment import Environment
import sys

@pytest.fixture
def sample_env(monkeypatch):
    monkeypatch.setenv("location", "Hong Kong")
    monkeypatch.setenv("application", "OMS")
    monkeypatch.setenv("_SEVERITY", "WARNING")
    monkeypatch.setenv("_GATEWAY", "Demo Gateway")
    monkeypatch.setenv("_MANAGED_ENTITY", "OMS 1")
    monkeypatch.setenv("_SAMPLER", "Order Monitor")
    monkeypatch.setenv("_DATAVIEW", "Orders")
    monkeypatch.setenv("_ROWNAME", "orderCount")
    monkeypatch.setenv("_COLUMN", "Value")
    monkeypatch.setenv("_VALUE", "999")
    if sys.platform != "win32":
        # Retarded capitalisation of environment variables.
        monkeypatch.setenv("_units", "orders")
        monkeypatch.setenv("_threshold", "1000")
    monkeypatch.setenv("_NETPROBE_HOST", "host01")
    monkeypatch.setenv("_HEADLINE", "")  # Simulate no fallback needed
    yield


def test_environment_parses_values(sample_env):
    env = Environment()

    assert env.location == "Hong Kong"
    assert env.application == "OMS"
    assert env.severity == "warning"
    assert env.gateway == "Demo Gateway"
    assert env.managed_entity == "OMS 1"
    assert env.sampler == "Order Monitor"
    assert env.dataview == "Orders"
    assert env.rowname == "orderCount"
    assert env.column == "Value"
    assert env.value == "999"
    assert env.host == "host01"

    if sys.platform != "win32":
        # Not set above
        assert env.dataview_columns["units"] == "orders"
        assert env.dataview_columns["threshold"] == "1000"


def test_environment_defaults_to_critical(monkeypatch):
    monkeypatch.delenv("_SEVERITY", raising=False)
    env = Environment()
    assert env.severity == "critical"


def test_environment_falls_back_to_headline(monkeypatch):
    monkeypatch.delenv("_ROWNAME", raising=False)
    monkeypatch.setenv("_HEADLINE", "CPU Headline")
    env = Environment()
    assert env.rowname == "CPU Headline"

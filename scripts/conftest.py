"""Tests marked core read files of sentinel-engine. They are skipped when the checkout is missing."""

import pytest

from paths import CORE


def pytest_collection_modifyitems(config, items):
    if CORE.is_dir():
        return
    skip = pytest.mark.skip(reason=f"no sentinel-engine checkout at {CORE}")
    for item in items:
        if "core" in item.keywords:
            item.add_marker(skip)

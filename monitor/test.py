import pytest
import hypothesis

import monitor


def test_log_entry_timestamp_to_posix_timestamp():
    assert monitor.log_entry_timestamp_to_posix_timestamp("May 17 18:00:38") == 1621376485


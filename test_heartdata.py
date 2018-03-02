import pytest


def test_read_file():
    from heartdata import HeartData
    # Check if data splits into time, voltage
    test1 = HeartData('test_data/test_data1.csv')
    assert test1.time is not None
    assert test1.voltage is not None
    assert test1.time[9] == 0.025
    assert test1.voltage[9] == -0.135

    assert test1.duration == 27.775

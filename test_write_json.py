import pytest


def test_write(capsys):
    from heartdata import HeartData
    ex_file = 'test_data/test_data10.csv'
    test1 = HeartData(ex_file)
    out, err = capsys.readouterr()
    assert out == 'test_data/test_data10.csv converted\n'

import pytest

from dml.exceptions import MetadataCommandException


def test_create(dml):
    key = 'test_create'
    dml.create(key)
    assert dml.get(key) is None


def test_set_get(dml):
    key = 'test_set_get'
    value = bytes(32)
    dml.create(key)
    dml.set(key, value)
    assert dml.get(key) == value
    dml.set(key, None)
    assert dml.get(key) is None


def test_lock_unlock(dml):
    key = 'test_lock_unlock'
    value = bytes(8)
    dml.create(key)
    dml.set(key, value)
    lock_token = dml.lock(key)
    dml.unlock(key, lock_token)
    assert dml.get(key) == value


def test_delete(dml):
    key = 'test_delete'
    dml.create(key)
    dml.delete(key)
    with pytest.raises(MetadataCommandException):
        assert dml.get(key)

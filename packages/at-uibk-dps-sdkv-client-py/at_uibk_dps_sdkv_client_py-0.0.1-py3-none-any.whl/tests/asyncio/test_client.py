import pytest

from dml.exceptions import MetadataCommandException


@pytest.mark.asyncio
async def test_create(dml):
    key = 'test_create'
    await dml.create(key)
    assert await dml.get(key) is None


@pytest.mark.asyncio
async def test_set_get(dml):
    key = 'test_set_get'
    value = bytes(64)
    await dml.create(key)
    await dml.set(key, value)
    assert await dml.get(key) == value


@pytest.mark.asyncio
async def test_lock_unlock(dml):
    key = 'test_lock_unlock'
    value = bytes(10)
    await dml.create(key)
    await dml.set(key, value)
    lock_token = await dml.lock(key)
    await dml.unlock(key, lock_token)
    assert await dml.get(key) == value


@pytest.mark.asyncio
async def test_delete(dml):
    key = 'test_delete'
    await dml.create(key)
    await dml.delete(key)
    with pytest.raises(MetadataCommandException):
        assert await dml.get(key)

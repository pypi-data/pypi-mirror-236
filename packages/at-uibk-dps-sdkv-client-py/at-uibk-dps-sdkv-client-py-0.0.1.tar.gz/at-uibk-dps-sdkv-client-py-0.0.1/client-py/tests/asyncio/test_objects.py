import pytest

from dml.asyncio.objects import SharedJson
from dml.exceptions import StorageCommandException


@pytest.mark.asyncio
async def test_json_create(dml):
    json = await SharedJson.create(dml, 'test_json_create1')
    assert await json.get() == {}
    initial_value = {'test': 321}
    json = await SharedJson.create(dml, 'test_json_create2', json=initial_value)
    assert await json.get() == initial_value


@pytest.mark.asyncio
async def test_json_set_get(dml):
    json = await SharedJson.create(dml, 'test_json_set_get')
    value = {'test': 1}
    await json.set(value)
    assert await json.get() == value
    await json.set(2, path='$.test')
    assert await json.get(path='$.test') == 2
    await json.set(test_data)
    assert await json.get() == test_data


@pytest.mark.asyncio
async def test_json_get_path(dml):
    json = await SharedJson.create(dml, 'test_json_get_path')
    await json.set(test_data)
    assert await json.get(path='$.store') == test_data['store']
    assert await json.get(path='$.store.book[0].author') == 'Nigel Rees'
    assert await json.get(path='$..book[1].category') == ['fiction']
    assert await json.get(path='$.store.bicycle.price') == 19.95
    assert len(await json.get(path='$..book[?(@.isbn)]')) == 2
    with pytest.raises(StorageCommandException):
        assert await json.get(path='$.non.existing.path')


@pytest.mark.asyncio
async def test_json_put_get(dml):
    json = await SharedJson.create(dml, 'test_json_put_get')
    await json.set(test_data)
    await json.put('test', 10, path='$.store')
    assert await json.get(path='$.store.test') == 10


@pytest.mark.asyncio
async def test_json_delete(dml):
    json = await SharedJson.create(dml, 'test_json_delete')
    await json.set(test_data)
    await json.delete('$.store.book[1:]')
    assert len(await json.get(path='$.store.book')) == 1
    await json.delete()
    assert await json.get() == {}


test_data = {
    'store': {
        'book': [
            {
                'category': 'reference',
                'author': 'Nigel Rees',
                'title': 'Sayings of the Century',
                'price': 8.95
            },
            {
                'category': 'fiction',
                'author': 'Evelyn Waugh',
                'title': 'Sword of Honour',
                'price': 12.99
            },
            {
                'category': 'fiction',
                'author': 'Herman Melville',
                'title': 'Moby Dick',
                'isbn': '0-553-21311-3',
                'price': 8.99
            },
            {
                'category': 'fiction',
                'author': 'J. R. R. Tolkien',
                'title': 'The Lord of the Rings',
                'isbn': '0-395-19395-8',
                'price': 22.99
            }
        ],
        'bicycle': {
            'color': 'red',
            'price': 19.95
        }
    },
    'expensive': 10
}
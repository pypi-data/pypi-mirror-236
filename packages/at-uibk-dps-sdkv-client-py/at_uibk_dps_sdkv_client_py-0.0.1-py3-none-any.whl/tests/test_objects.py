import pytest

from dml.exceptions import StorageCommandException
from dml.storage.objects import SharedJson, SharedBuffer, SharedCounter


def test_buffer(dml):
    buf = SharedBuffer(dml, 'test_buffer')
    assert buf.get() is None
    value = bytes(8)
    buf.set(value)
    assert buf.get() == value
    buf.set(None)
    assert buf.get() is None


def test_counter(dml):
    counter = SharedCounter(dml, 'test_counter')
    assert counter.get() == 0
    assert counter.increment() == 1
    assert counter.get() == 1
    assert counter.increment() == 2
    assert counter.increment(delta=5) == 7


def test_json_create(dml):
    json = SharedJson(dml, 'test_json_create')
    assert json.get() == {}


def test_json_set_get(dml):
    json = SharedJson(dml, 'test_json_set_get')
    value = {'test': 123}
    json.set(value)
    assert json.get() == value
    json.set(124, path='$.test')
    assert json.get(path='$.test') == 124
    json.set(test_data)
    assert json.get() == test_data


def test_json_get_path(dml):
    json = SharedJson(dml, 'test_json_get_path')
    json.set(test_data)
    assert json.get(path='$.store') == test_data['store']
    assert json.get(path='$.store.book[0].author') == 'Nigel Rees'
    assert json.get(path='$..book[1].category') == ['fiction']
    assert json.get(path='$.store.bicycle.price') == 19.95
    assert len(json.get(path='$..book[?(@.isbn)]')) == 2
    with pytest.raises(StorageCommandException):
        assert json.get(path='$.non.existing.path')


def test_json_put_get(dml):
    json = SharedJson(dml, 'test_json_put_get')
    json.set(test_data)
    json.put('test', 10, path='$.store')
    assert json.get(path='$.store.test') == 10


def test_json_delete(dml):
    json = SharedJson(dml, 'test_json_delete')
    json.set(test_data)
    json.delete('$.store.book[1:]')
    assert len(json.get(path='$.store.book')) == 1
    json.delete()
    assert json.get() == {}


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

import os
import sys
import tempfile

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage


def test_append_only_array_storage_append():
    with tempfile.NamedTemporaryFile() as tmp_file:
        storage = AppendOnlyArrayStorage(tmp_file.name)
        for i in range(10):
            storage.append(i)
        storage.append("hehe")
        storage.append({"a": "b"})
        storage.append({"a", "b", "c"})
        assert len(storage) == 13

def test_append_only_array_storage_get():
    with tempfile.NamedTemporaryFile() as tmp_file:
        storage = AppendOnlyArrayStorage(tmp_file.name)
        for i in range(10):
            storage.append(i)
        storage.append("hehe")
        storage.append({"a": "b"})
        storage.append({"a", "b", "c"})
        for i in range(10):
            assert storage[i] == i
        assert storage[10] == "hehe"
        assert storage[11] == {"a": "b"}
        assert storage[12] == {"a", "b", "c"}

def test_append_only_array_storage_iter():
    with tempfile.NamedTemporaryFile() as tmp_file:
        storage = AppendOnlyArrayStorage(tmp_file.name)
        for i in range(100):
            storage.append(i + 10)
        for index, value in enumerate(storage):
            assert value == index + 10
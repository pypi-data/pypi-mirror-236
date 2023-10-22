import pytest
from tests.mocking import mock_file_handle

def test_mock_file_handle_write(mock_file_handle):
    mock_file_handle.write("Hello, World!")
    assert mock_file_handle.data == "Hello, World!"

def test_mock_file_handle_writelines(mock_file_handle):
    lines = ["Line 1", "Line 2", "Line 3"]
    mock_file_handle.writelines(lines)
    assert mock_file_handle.data == "Line 1\nLine 2\nLine 3"

def test_mock_file_handle_read(mock_file_handle):
    mock_file_handle.data = "Testing Read Functionality"
    assert mock_file_handle.read() == "Testing Read Functionality"

def test_mock_file_handle_readline(mock_file_handle):
    mock_file_handle.data = "Line 1\nLine 2\nLine 3"
    assert mock_file_handle.readline() == "Line 1\n"
    assert mock_file_handle.readline() == "Line 2\n"
    assert mock_file_handle.readline() == "Line 3\n"
    assert mock_file_handle.readline() is None

def test_mock_file_handle_readlines(mock_file_handle):
    mock_file_handle.data = "Line 1\nLine 2\nLine 3"
    assert mock_file_handle.readlines() == ["Line 1\n", "Line 2\n", "Line 3\n"]

def test_moked_file_handle_write_and_read(mock_file_handle):
    # Use the mock_file_handle as a fixture in your test
    mock_file_handle.write("Line 1\nLine 2\nLine 3")
    assert mock_file_handle.read() == "Line 1\nLine 2\nLine 3"
    assert mock_file_handle.readline() == "Line 1\n"
    assert mock_file_handle.readline() == "Line 2\n"
    assert mock_file_handle.readlines() == ["Line 1\n","Line 2\n","Line 3\n"]
    assert mock_file_handle.readline() == "Line 3\n"

# test code for `with .. as ..` block

def test_mock_file_handle_write_withblock(mock_file_handle):
    with mock_file_handle as file_handle:
        file_handle.write("Hello, World!")
    assert mock_file_handle.data == "Hello, World!"

def test_mock_file_handle_writelines_withblock(mock_file_handle):
    lines = ["Line 1", "Line 2", "Line 3"]
    with mock_file_handle as file_handle:
        file_handle.writelines(lines)
    assert mock_file_handle.data == "Line 1\nLine 2\nLine 3"

def test_mock_file_handle_read_withblock(mock_file_handle):
    mock_file_handle.data = "Testing Read Functionality"
    with mock_file_handle as file_handle:
        assert file_handle.read() == "Testing Read Functionality"

def test_mock_file_handle_readline_withblock(mock_file_handle):
    mock_file_handle.data = "Line 1\nLine 2\nLine 3"
    with mock_file_handle as file_handle:
        assert file_handle.readline() == "Line 1\n"
        assert file_handle.readline() == "Line 2\n"
        assert file_handle.readline() == "Line 3\n"
        assert file_handle.readline() is None

def test_mock_file_handle_readlines_withblock(mock_file_handle):
    mock_file_handle.data = "Line 1\nLine 2\nLine 3"
    with mock_file_handle as file_handle:
        assert file_handle.readlines() == ["Line 1\n", "Line 2\n", "Line 3\n"]

# tested mocking

def test_open_with_mock_file_handle(monkeypatch, mock_file_handle):
    # Replace the built-in open function with the mock_file_handle
    monkeypatch.setattr('builtins.open', lambda file, mode='r': mock_file_handle)

    # Now any code that calls open will get your mock_file_handle instead
    with open('test_file.txt', 'w') as file:
        file.write("Testing open with mock_file_handle")

    # Verify that the data was written to the mock_file_handle
    assert mock_file_handle.data == "Testing open with mock_file_handle"

    # You can also use other file operations with the mock_file_handle
    with open('test_file.txt', 'r') as file:
        content = file.read()

    # Verify that the content matches what was written
    assert content == "Testing open with mock_file_handle"

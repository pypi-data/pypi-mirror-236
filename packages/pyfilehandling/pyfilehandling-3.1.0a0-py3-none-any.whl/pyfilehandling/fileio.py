import os


def create_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except FileNotFoundError as e:
        raise ValueError(f"Invalid path '{path}': {e}")


def remove_dir(path):
    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass  # Directory doesn't exist, nothing to remove
    except OSError as e:
        raise ValueError(f"Invalid path '{path}': {e}")


def create_file(path):
    try:
        with open(path, 'x'):
            pass
    except FileExistsError:
        pass  # File already exists, nothing to create
    except FileNotFoundError as e:
        raise ValueError(f"Invalid path '{path}': {e}")


def remove_file(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass  # File doesn't exist, nothing to remove
    except OSError as e:
        raise ValueError(f"Invalid path '{path}': {e}")


def write(path, data, mode="a"):
    if mode not in ["w", "a"]:
        raise ValueError(f"Invalid mode '{mode}'. it should be 'w' or 'a'.")
    with open(path, mode) as f:
        f.write(data)


def writeline(path, data, mode="a"):
    if mode not in ["w", "a"]:
        raise ValueError(f"Invalid mode '{mode}'. it should be 'w' or 'a'.")
    with open(path, mode) as f:
        f.write(data + '\n')


def writelines(path, data_list, mode="a"):
    if mode not in ["w", "a"]:
        raise ValueError(f"Invalid mode '{mode}'. it should be 'w' or 'a'.")
    with open(path, mode) as f:
        for item in data_list:
            f.write(item + '\n')


def read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except OSError as e:
        raise ValueError(f"Error reading from '{path}': {e}")


def readline(path, lineno):
    try:
        with open(path, "r") as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
            return lines[lineno]
    except FileNotFoundError:
        return ""
    except OSError as e:
        raise ValueError(f"Error reading from '{path}': {e}")


def readlines(path):
    try:
        with open(path, "r") as f:
            return [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        return []
    except OSError as e:
        raise ValueError(f"Error reading from '{path}': {e}")


def get_reader(path):
    try:
        with open(path, "r") as f:
            for line in f:
                yield line.rstrip('\n')
    except FileNotFoundError:
        return
    except OSError as e:
        raise ValueError(f"Error reading from '{path}': {e}")

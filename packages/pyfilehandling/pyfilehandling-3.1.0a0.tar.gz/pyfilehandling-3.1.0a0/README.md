# PyFileHandling - Streamlining Pythonic File Operations
[![Run-Tests](https://github.com/JeelDobariya38/PyFileHandling/actions/workflows/Run-Tests.yaml/badge.svg)](https://github.com/JeelDobariya38/PyFileHandling/actions/workflows/Run-Tests.yaml)

## Overview
PyFileHandling is a Python package designed to simplify file handling operations. Whether you need to create, modify, or read files, this package offers an array of convenient functions to streamline your file manipulation tasks.

## Features
- **File Creation**: Easily create files at specified paths.
- **Directory Manipulation**: Create, remove directories, and manage file structures.
- **File Writing**: Write data to files with options for overwriting or appending.
- **File Reading**: Read file contents, individual lines, or use generators to efficiently handle large files.
- **Tested and Reliable**: Thoroughly tested with a focus on robustness and reliability.

## Installation
You can install PyFileHandling using pip:

```shell
pip install pyfilehandling
```

## Getting Started
For detailed usage instructions, consult the [PyFileHandling Documentation](https://jeeldobariya38.github.io/PyFileHandling/).

Here's a quick start with some common use cases:

```python
import pyfilehandling

# Create a directory
pyfilehandling.create_dir("my_directory")

# Write data to a file
pyfilehandling.write("my_file.txt", "Hello, PyFileHandling!")

# Read file content
content = pyfilehandling.read("my_file.txt")
print(content)
```

## Contributing
Contributions are welcome! To contribute to PyFileHandling, please read the [Contribution Guidelines](CONTRIBUTING.md). We appreciate your help in making this package even better.

## Code of Conduct
We strive to maintain a positive and inclusive community. We encourage everyone participating in PyFileHandling to read and adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). It's essential for creating a welcoming and collaborative environment.

## License
By contributing to `PyFileHandling`, you agree that your contributions will be licensed under the [MIT License](LICENSE.txt). Make sure you understand and agree with this before submitting your contributions.

from setuptools import setup

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

long_description = read_file('README.md')

setup(
    name='pyfilehandling',
    version='3.1.0-alpha',
    description='A Python package for file manipulation operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeel Dobariya',
    author_email='dobariyaj34@gmail.com',
    url='https://github.com/JeelDobariya38/PyFileHandling',
    packages=['pyfilehandling'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['file handling', 'file manipulation', 'file operation', 'utility'],
    project_urls={
        'Bug Tracker': 'https://github.com/JeelDobariya38/PyFileHandling/issues',
        'Documentation': 'https://jeeldobariya38.github.io/PyFileHandling/',
        'Source Code': 'https://github.com/JeelDobariya38/PyFileHandling',
    },
    package_data={
        'pyfilehandling': ['py.typed', '*.pyi'],
    },
    license='MIT',
    license_file='LICENSE.txt',
    python_requires='>=3.9',
    install_requires=[
        # Add any required dependencies here
    ],
    extras_require={
        'testing': [
            'pytest',
            'coverage',
        ],
    },
)

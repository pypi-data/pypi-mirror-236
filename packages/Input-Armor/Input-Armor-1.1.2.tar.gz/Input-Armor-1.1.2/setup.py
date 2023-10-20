from setuptools import setup

setup(
    name='Input-Armor',  # Your package name
    packages=['input_armor'],  # Package directory
    version='1.1.2',  # Your library version, increment as needed
    license='MIT',  # License type

    description='A Python library for input validation and security.',
    # Short description of your library

    author='Armen-Jean Andreasian',  # Your name
    author_email='armen.andreasian77@gmail.com',  # Your email

    url='https://github.com/Armen-Jean-Andreasian',  # Homepage of your library (e.g. GitHub or your website)
    keywords=['sql-injection', 'bad input', 'input validation', 'security', 'python'],  # Keywords users can search on PyPI

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    install_requires=[
        # List any dependencies your library may have
    ],

    python_requires='>=3.8',  # Specify the Python versions your library supports

    long_description='''\
A Python library for input validation and security.

InputArmor is designed to help you protect your Python applications from malicious input. It checks for encoding issues, SQL queries, and potential security vulnerabilities, raising custom errors when invalid input is detected.

For more details and documentation, please visit the [GitHub repository](https://github.com/Armen-Jean-Andreasian/Input-Armor).

Features:
- Validate user input for potential security issues.
- Easily integrate input validation into your Python projects.
- Protect your applications from common security threats.

Installation:
```commandline 
pip install Input-Armor
```
''',
    long_description_content_type='text/markdown',
)

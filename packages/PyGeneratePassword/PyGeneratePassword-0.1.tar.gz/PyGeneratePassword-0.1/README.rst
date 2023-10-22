PyGeneratePassword
===================

PyGeneratePassword is a Python package that provides a simple tool to generate random passwords with customizable parameters. You can easily create secure passwords for various applications and scenarios.

Installation
------------

You can install PyGeneratePassword using pip, the Python package manager. Open your terminal or command prompt and run the following command:

.. code-block:: bash

    pip install PyGeneratePassword

Usage
-----

.. code-block:: python

    from PyGeneratePassword import PasswordGenerate

    # Generate a random password with default settings
    password = PasswordGenerate()
    print("Generated Password:", password)

    # Generate a password with custom settings (e.g., length and character set)
    custom_password = PasswordGenerate(length=16, use_digits=True, use_special_chars=True)
    print("Custom Password:", custom_password)

Output
------

The above usage example will produce output similar to the following:

.. code-block:: plaintext

    Generated Password: W!lA0$qVnS7C
    Custom Password: ZS4jB9$+xQvH6D!2

Options
-------

The `PasswordGenerate` class supports the following options:

- `length` (default is 12): Specify the length of the generated password.
- `use_digits` (default is `True`): Include digits (0-9) in the password.
- `use_special_chars` (default is `True`): Include special characters in the password.

You can customize these options to create passwords that meet your specific requirements.

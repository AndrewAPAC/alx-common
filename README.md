# alx-common

**A comprehensive Python framework for infrastructure automation, monitoring, and reporting. Designed to standardize common development tasks and eliminate code duplication in production environments.**

---
## Preamble

On first invocation, if the directory `$HOME/.config/alx` 
(or `%APPDATA%\alx` on Windows) is not found, then it is created 
along with the following files:
* `alx.ini`: The module configuration file which should be used to 
override settings in the defaults found in `alx.ini` in the installed 
module directory
* `env`: This file contains the path to the virtual environment in use
and is set to the current python used to execute a script using 
`alx-common`
* `key`: An encryption key used to encrypt and decrypt strings. If
there are multiple developers, then it is wise to share the key so
the configuration file can remain consistent. *This file must be stored
readable only by the user and not shared*. The command to create a key is:

```
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

These files can (and should) be modified to suit your needs. For example,
changing `alx.ini` and adding 

```
[mail]
from:   Application User <valid@email.address>
```

would be a good idea.

---
## Summary

**alx-common** provides a consistent foundation for building reliable internal applications that deal with:

- ✅ Configuration management
- ✅ Argument parsing
- ✅ Different environment handling: dev, test, prod
- ✅ Secure password, etc. handling with encryption
- ✅ Logging (including file rotation, maximum size and console output)
- ✅ Database utilities (MySQL, MariaDB, SQLite, PostgreSQL)
- ✅ HTML report generation
- ✅ Email notifications (plain, HTML, attachments, inline images)
- ✅ Monitoring integrations (ITRS Geneos support)
- ✅ Lightweight internal automation tools

Originally designed to simplify and standardize automation scripts, 
reporting jobs, monitoring pipelines, and operational tooling across 
real-world production environments.  The aim of `alx-common` is to 
reduce hard coding and duplication of snippets. 

Too many times, I have seen developers share code to 'send an email'.
Then the `mailhost` changes and there are 200 scripts to fix. Or
a shell script is copied and something edited to create a wrapper
to start a python script. Or the same code is used over and over to 
set up logging or read a configuration file coupled with a lot of hard
coding an inconsistencies.

Bad practice is endemic in the developer community as there are too
many coders adopting a cut-and-paste mentality.

The name comes from my company, ALX Solutions which is no longer in 
operation but now lives on in PyPI and GitHub!

---

## Features

- ### Application Framework (`alx.app.ALXapp`)
  - Simplified argparse-based CLI definition
  - Config-driven parameter management (`alx.ini`)
  - Environment separation (dev/test/prod)
  - Secure password storage (Fernet encryption)
  - Dynamic path management (logs, data, config)
  - Application configuration automatically parsed 
    and stored in `alx.app.ALXapp` object
  - Centralized logger management handled providing
    automatic house-keeping based on configuration

- ### Database Utilities (`alx.db_util.ALXdatabase`)
  - Simplifies open source database access
  - Auto-formatted SQL logging
  - Centralized connection lifecycle
  - Transaction management
  - Simplified execution mechanism

- ### Reporting (`alx.html.ALXhtml`)
  - Easy HTML generation
  - Promotes tidy and consistent code

- ### Email creation (`alx.mail.ALXmail`)
  - Supports plaintext and html formats
  - Easy email formatting and sending
  - Flexible
  - Integrated with SMTP servers, attachments, and inline images

- ### String manipulation (`strings.py`)
  - Commonly used string manipulation routines

- ### ITRS Geneos Alerts (`alx.itrs.alert.HtmlAlert`)
  - Provides a consistent way to parse the environment on an event
  - A standard alert in html / table format
  - A class to create a toolkit sampler without the
    need to know internal details (`alx.itrs.toolkit.Toolkit`)
  - Standardised environment parsing (`alx.itrs.environment.Environment`)

## Quick Start

```python
from alx.app import ALXapp
import sys

args = [
    ['string'],
    ['-d', '--decrypt', {'action': 'store_true', 'default': False}]
]

app = ALXapp("Password encryption tool", args=args)

string = app.arguments.string

if not app.arguments.decrypt:
    string = app.encrypt(string)
    print("Encrypted: " + string)

print("Decrypted: " + app.decrypt(string))

sys.exit(0)
```

## Examples

Please refer to the files [in the examples directory](https://github.com/AndrewAPAC/alx-common/tree/main/examples)

## Stats for nerds

* ![Downloads](https://static.pepy.tech/badge/alx-common)
* ![Downloads per week](https://static.pepy.tech/badge/alx-common/week)
* ![Downloads per month](https://static.pepy.tech/badge/alx-common/month)

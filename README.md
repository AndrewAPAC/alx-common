# alx-common

**A comprehensive Python framework for infrastructure automation, monitoring, and reporting. Designed to standardize common development tasks and eliminate code duplication in production environments.**

---
## Prerequisites

Before use, create 2 files in `$HOME/.config/alx`:
* `$HOME/.config/alx/env` with contents
  * `venv=<path/to/venv>` (do not include the /bin path)
  * Other environment settings can also go in here if required 
* `$HOME/.config/alx/key`
  * Add the output from 
  ```
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```
  * This is your key to encrypt and decrypt strings - do not share

---
## Summary

**alx-common** provides a consistent foundation for building reliable internal applications that deal with:

- ✅ Configuration management
- ✅ Argument parsing
- ✅ Different environment handling: dev, test, prod
- ✅ Secure password, etc handling with encryption
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
operation.

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

## Examples

Please refer to the files [in the examples directory](https://github.com/AndrewAPAC/alx-common/tree/main/examples)


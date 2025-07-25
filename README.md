# alx-common

**Reusable Python framework for infrastructure automation, monitoring, reporting, and internal tooling.**

> Before use, you need to create 2 files in `$HOME/.config/alx`:
>   * `$HOME/.config/alx/env` with contents
>     * `venv=<path/to/venv>`
>     (do not include the /bin)
> * `$HOME/.config/alx/key`
>   * Add the output from `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

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

Originally designed to simplify and standardize automation scripts, reporting jobs, monitoring pipelines, and operational tooling across real-world production environments.

---

## Features

* ### Application Framework (`ALXapp`)
  - Simplified argparse-based CLI definition
  - Config-driven parameter management (`alx.ini`)
  - Environment layering (dev/test/prod)
  - Secure password storage (Fernet encryption)
  - Dynamic path management (logs, data, config)
  - Application configuration parsed and stored in `ALXapp` object

- ### Database Utilities (`ALXdatabase`)
  - Simplifies open source database access
  - Auto-formatted SQL logging
  - Centralized connection lifecycle
  - Transaction management

- ### Reporting & Email
  - Easy HTML generation (`ALXhtml`)
  - Easy email formatting and sending(`ALXmail`)
  - Integrated with SMTP servers, attachments, and inline images

- ### Logging
  - Centralized logger management
  - Config-driven log levels, rotation, and retention

- ### String manipulation (`strings.py`)
  - Commonly used string manipulation routines

- ### ITRS Geneos routines
  - Provides a consistent way to parse the environment on an event
  - A standard alert in html / table format
  - A class to create a toolkit sampler without the need to know internal details

## Examples

Please refer to the files in the examples directory


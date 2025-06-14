# ALX-Common

**Reusable Python framework for infrastructure automation, monitoring, reporting, and internal tooling.**

ALX-Common provides a consistent foundation for building reliable internal applications that deal with:

- ✅ Configuration management
- ✅ Argument parsing
- ✅ Secure secrets handling
- ✅ Logging (including file rotation, console output, and environments)
- ✅ Database utilities (currently MySQL/MariaDB)
- ✅ HTML report generation
- ✅ Email notifications (plain, HTML, attachments, inline images)
- ✅ Monitoring integrations (ITRS Geneos support)
- ✅ Lightweight internal automation tools

Originally designed to simplify and standardize automation scripts, reporting jobs, monitoring pipelines, and operational tooling across real-world production environments.

---

## Features

- **Application Framework (`ALXapp`)**
  - Simplified argparse-based CLI definition
  - Config-driven parameter management (`alx.ini`)
  - Environment layering (dev/test/prod)
  - Secure password storage (Fernet encryption)
  - Dynamic path management (logs, data, config)

- **Database Utilities (`ALXdatabase`)**
  - Simplifies MariaDB/MySQL access
  - Auto-formatted SQL logging
  - Centralized connection lifecycle
  - Transaction management
  - Config-driven SQL templates

- **Reporting & Email**
  - Easy HTML generation (`ALXhtml`)
  - Templated alert formatting (`ALXmail`)
  - Integrated with SMTP servers, attachments, and inline images
  - Monitoring alert support via ITRS Geneos environment parsing

- **Logging**
  - Centralized logger management
  - Config-driven log levels, rotation, and retention

- **Broadlink Controller (Example Project)**
  - Home automation integration
  - Interactive scanning, learning, and sending of IR codes

---

## Quick Example

```python
from alx.app import ALXapp

args = [
    ["-c", "--customer", {"help": "Customer name"}]
]

app = ALXapp("ExampleApp", args=args)

print(f"Running job for customer: {app.arguments.customer}")


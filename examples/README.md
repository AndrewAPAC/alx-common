# Examples Area

The examples in here are intended to guide you on how to
use alx-common effectively. They should be run by using the 
script `run_examples`. The structure can be deployed
anywhere as the location is determined dynamically.

Points to note:
* You will need to create some configuration files:
  * `$HOME/.config/alx/env` with contents
    * venv=<path/to/venv>
  * `$HOME/.config/alx/key`
    * Add the output from `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
* On the first run, the `alx.ini` file will be copied to the 
configuration area so it can be modified to your liking
* The directory structure is intended to be Unix like and
is created in the ALXapp initialisation. Some directories
may not be used.
* Comprehensive documentation is included. Once the module
is installed it can be accessed with `pdoc alx`

```
.
├── bin
│   ├── encrypt -> start    # calculate script to run from name
│   └── start               # start script for all apps
├── data
│   └── encrypt             # created at run time
├── etc                     # holds the config (ini) files
├── log                     # created at run time
│   └── encrypt
│       └── encrypt.log     # logs rotated according to `alx.ini`
├── README.md               # this file
├── run_examples            # run examples using this script
└── scripts                 # script area
    └── encrypt             # directory same name as symlink
        └── encrypt.py      # script same name as symlink + .py
```
The `start` script uses the name of the symbolic link to determine
the directory and script name to run. The `ALXapp` class then 
calculates the `ini` file, log file location and name and the data 
area. The data area can be added to the ini file as `$data` for 
convenience.



# Examples Area

These examples are intended to guide you on how to
use alx-common effectively. They should be run by using the 
script `run_examples`. The structure can be deployed
anywhere as the location is determined dynamically.

* On the first run, a skeleton `alx.ini` file will be created
in `$HOME/config/alx/alx.ini` as described in the Preamble in 
[README.md](https://github.com/AndrewAPAC/alx-common/blob/main/README.md).
Any modified key will override the global values. You can even 
store your own if required.
* The directory structure is intended to be Unix like and
is created in the ALXapp initialisation. If a data directory is 
required, it should be created manually.
* Comprehensive documentation is included. Once the module
is installed it can be accessed with `pdoc alx`

```
.
├── bin
│   ├── encrypt -> start    # each script is a symlink to start
│   └── start               # start script for all apps
├── data
│   └── encrypt             # create if required
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
area. 

The data area can be added to the ini file as `$data` for 
convenience.  So you might have:
```
[DEFAULT]
output_file:        $data/output.txt
```
and it will be replaced dynamically in `alx.app.py:parse_config` with the
application's data directory


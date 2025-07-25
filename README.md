## Description

`creds_manager.py` - a wrapper over the linux `keyring` that manages the credential in a secure way.

### Usage

```bash
└─$ python creds_manager.py -h         
usage: creds_manager.py [-h] {set,get,del,view_all} ...

A helper script that stores credentials in linux keyring

optional arguments:
  -h, --help            show this help message and exit

commands:
  {set,get,del,view_all}
                        See '[command] --help' for details
    set                 set up a keyring
    get                 get credentials from a keyring
    del                 delete a keyring
    view_all            view all keyrings
```

Create an alias in `zshrc` file to run the script from anywhere.
```bash
creds_manager() {python3 path/creds_manager.py "$@"}
```

Example

```bash
╰─$ creds_manager set -n mysql_service -u mysql_user -p mysql_password
[+] credential is set
(venv_3.12.5) ╭─asinha@ubuntu-dev ~ 
╰─$ creds_manager view_all                             
[+] listing all service_names for keyring user: ubuntu
mysql_service
(venv_3.12.5) ╭─asinha@ubuntu-dev ~ 
╰─$ creds_manager get -n mysql_service
username: mysql_user
password has been copied to your clipboard

```
The password is securely retrieved without being exposed in the terminal


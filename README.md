## Description

`creds_manager.py` - a wrapper over the linux `keyring` that securely create and retrieve the password without being exposed in the terminal.

### Usage

```bash
(creds_manager_3.12.5) ╭─asinha@ubuntu-dev /mnt/pentest/code_dev/python/utils/creds_manager  ‹main*› 
╰─➤  creds_manager -h               
usage: creds_manager.py [-h] {set,get,del,view} ...

A utility script for securely storing credentials in the Linux keyring

options:
  -h, --help          show this help message and exit

commands:
  {set,get,del,view}  See '[command] --help' for details
    set               create a keyring service
    get               get credentials from a keyring service
    del               delete a keyring service
    view              Retrieving all keyring service names associated with the keyring user: ubuntu-dev
```

### Example

```bash
(creds_manager_3.12.5) ╭─asinha@ubuntu-dev /mnt/pentest/code_dev/python/utils/creds_manager  ‹main*› 
╰─➤  creds_manager set -n test_creds -u "test_user"
Enter your password: *************

[+] a new credential has been set

(creds_manager_3.12.5) ╭─asinha@ubuntu-dev /mnt/pentest/code_dev/python/utils/creds_manager  ‹main*› 
╰─➤  creds_manager view                            
[+] Retrieving all service names associated with the keyring user: ubuntu-dev
1. test_creds

(creds_manager_3.12.5) ╭─asinha@ubuntu-dev /mnt/pentest/code_dev/python/utils/creds_manager  ‹main*› 
╰─➤  creds_manager get -n test_creds               
username: test_user
password has been copied to your clipboard

(creds_manager_3.12.5) ╭─asinha@ubuntu-dev /mnt/pentest/code_dev/python/utils/creds_manager  ‹main*› 
╰─➤  creds_manager del -n test_creds               
[+] deleted keyring service: test_creds
```

#### Configure

Create an alias in `zshrc` file to run the script from anywhere.
```bash
creds_manager() {python3 FULL_PATH_for_creds_manager.py "$@"}
```

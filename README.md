## Description

`creds_manager.py` - a wrapper over the linux `keyring` that manages the credential in a secure way.

### Usage

```
u└─$ python creds_manager.py -h         
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

 



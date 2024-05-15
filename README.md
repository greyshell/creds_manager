## Description

`creds_manager.py` - a wrapper over the linux `keyring` that manages the credential in a secure way.

### Usage

```
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
### Silently copy the credentials into clipboard

Update the following lines in zshrc.

```
alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'
mute_creds_manager() { creds_manager get -n "$1" | cut -d " " -f 4 | pbcopy; }
```
 



#!/usr/bin/env python3

# author: greyshell
# description: a helper script / wrapper to perform all keyring operations


import argparse
import sys
import json
import keyring
import secretstorage

KEYRING_USERNAME = "kali_creds"


def get_keyring(keyring_name):
    try:
        cred = json.loads(keyring.get_password(keyring_name, KEYRING_USERNAME))
    except TypeError as e:
        print(f"error: {e}")
        sys.exit(0)
    username = list(cred.keys())[0]
    password = list(cred.values())[0]
    return username, password


def set_keyring(keyring_name, username, password):
    # existing username will overwrite the existing entry
    cred = dict()
    cred[username] = password
    try:
        keyring.set_password(keyring_name, KEYRING_USERNAME, json.dumps(cred).encode('utf-8'))
    except TypeError as e:
        print(f"error: {e}")
        sys.exit(0)


def del_keyring(keyring_name):
    try:
        keyring.delete_password(keyring_name, KEYRING_USERNAME)
    except (keyring.errors.PasswordDeleteError, TypeError) as e:
        print(f"error: {e}")
        sys.exit(0)


def view_all_keyrings():
    conn = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(conn)
    for item in collection.get_all_items():
        print(f"{item.get_label()}")
        print(f"{item.get_attributes()}")
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A helper script that stores credentials in linux keyring")
    subparsers = parser.add_subparsers(title="commands",
                                       help="See '[command] --help' for details")

    # set a keyring
    set_keyring_parser = subparsers.add_parser("set", description="set up a keyring",
                                               help="set up a keyring")
    set_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring name", required=True)
    set_keyring_parser.add_argument("-u", "--username", metavar="",
                                    help="provide the username", required=True)
    set_keyring_parser.add_argument("-p", "--password", metavar="",
                                    help="provide the password", required=True)
    set_keyring_parser.set_defaults(cmd="set")

    # get a keyring
    get_keyring_parser = subparsers.add_parser("get", description="get credentials from a keyring",
                                               help="get credentials from a keyring")
    get_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring name", required=True)
    get_keyring_parser.set_defaults(cmd="get")

    # delete a keyring
    del_keyring_parser = subparsers.add_parser("del", description="delete a keyring",
                                               help="delete a keyring")
    del_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring name", required=True)
    del_keyring_parser.set_defaults(cmd="del")

    # view all keyrings
    get_keyring_parser = subparsers.add_parser("view_all", description="view all keyrings",
                                               help="view all keyrings")
    # get_keyring_parser.add_argument("-a", "--name", metavar="",
    #                                 help="", required=True)
    get_keyring_parser.set_defaults(cmd="view_all")

    # get the arguments
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    if args.cmd == "set":
        set_keyring(args.name, args.username, args.password)
        print(f"credential is set !!")
    elif args.cmd == "get":
        usr, passwd = get_keyring(args.name)
        print(f"username: {usr}, password: {passwd}")
    elif args.cmd == "del":
        del_keyring(args.name)
        print(f"deleted keyring: {args.name}")

    elif args.cmd == "view_all":
        view_all_keyrings()

    else:
        parser.print_help(sys.stderr)

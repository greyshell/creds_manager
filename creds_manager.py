#!/usr/bin/env python3

# author: greyshell
# description: a helper script / wrapper to perform all keyring operations


import argparse
import sys
import json
import keyring
import secretstorage

KEYRING_USERNAME = "kali_nuc12_vault"


def get_keyring(service_name):
    try:
        cred = json.loads(keyring.get_password(service_name, KEYRING_USERNAME))
    except TypeError:
        print(f"[x] error: service_name not found")
        sys.exit(0)
    username = list(cred.keys())[0]
    password = list(cred.values())[0]
    return username, password


def set_keyring(service_name, username, password):
    cred = dict()
    cred[username] = password
    found_flag = False
    choice = None
    try:
        # if any entry is found
        if f"'{service_name}'" in view_all_keyrings():
            found_flag = True
            choice = input(f"[+] found existing entry, would you like to overwrite [y/n]: ")
        else:
            found_flag = False

        if choice == "y" or found_flag is False:
            # example: mysql service, KEYRING_USERNAME, {root:toor} as binary object
            keyring.set_password(service_name, KEYRING_USERNAME, json.dumps(cred).encode('utf-8'))
            print(f"[+] credential is set")

    except TypeError as e:
        print(f"[x] error: {e}")
        sys.exit(0)


def del_keyring(service_name):
    try:
        if get_keyring(service_name):
            keyring.delete_password(service_name, KEYRING_USERNAME)
    except (keyring.errors.PasswordDeleteError, TypeError) as e:
        print(f"[x] error: {e}")
        sys.exit(0)


def view_all_keyrings():
    conn = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(conn)
    services = []
    for item in collection.get_all_items():
        label = item.get_label()
        if KEYRING_USERNAME in label:
            services.append(label.split()[-1])

    return services


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
    get_keyring_parser.set_defaults(cmd="view_all")

    # get the arguments
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    if args.cmd == "set":
        set_keyring(args.name, args.username, args.password)
    elif args.cmd == "get":
        usr, passwd = get_keyring(args.name)
        print(f"username: {usr}, password: {passwd}")
    elif args.cmd == "del":
        del_keyring(args.name)
        print(f"[+] deleted keyring: {args.name}")

    elif args.cmd == "view_all":
        print(f"[+] listing all service_names for {KEYRING_USERNAME}:")
        for service in view_all_keyrings():
            print(service.strip("'"))

    else:
        parser.print_help(sys.stderr)

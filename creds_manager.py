#!/usr/bin/env python3

# author: greyshell
# description: a helper script / wrapper to perform all keyring operations


import argparse
import sys
import json
import keyring
import secretstorage
import pyperclip
import tty
import termios

KEYRING_USERNAME = "ubuntu-dev"


def get_hidden_input(prompt=''):
    print(prompt, end='', flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    password = ''
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == '\n' or ch == '\r':
                print()
                break
            elif ch == '\x7f':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password += ch
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print("")
    return password


def get_keyring_service(service_name):
    try:
        cred = json.loads(keyring.get_password(service_name, KEYRING_USERNAME))
    except TypeError:
        print(f"[x] error: service_name not found")
        sys.exit(0)
    username = list(cred.keys())[0]
    password = list(cred.values())[0]
    pyperclip.copy(password)  # copies text to clipboard

    return username


def set_keyring_service(service_name, username, password):
    cred = dict()
    cred[username] = password
    found_flag = False
    choice = None
    try:
        # if any entry is found
        if f"'{service_name}'" in view_keyring_services():
            found_flag = True
            choice = input(f"[+] found existing entry, would you like to overwrite [y/n]: ")
        else:
            found_flag = False

        if choice == "y" or found_flag is False:
            # example: mysql service, KEYRING_USERNAME, {root:toor} as a binary object
            keyring.set_password(service_name, KEYRING_USERNAME, json.dumps(cred).encode('utf-8'))
            print(f"[+] a new credential has been set")

    except TypeError as e:
        print(f"[x] error: {e}")
        sys.exit(0)


def del_keyring_service(service_name):
    try:
        if get_keyring_service(service_name):
            keyring.delete_password(service_name, KEYRING_USERNAME)
    except (keyring.errors.PasswordDeleteError, TypeError) as e:
        print(f"[x] error: {e}")
        sys.exit(0)


def view_keyring_services():
    conn = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(conn)
    services = []
    for item in collection.get_all_items():
        label = item.get_label()
        if KEYRING_USERNAME in label:
            services.append(label.split()[-1])

    return services


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A utility script for securely storing credentials in the Linux "
                                                 "keyring")

    subparsers = parser.add_subparsers(title="commands",
                                       help="See '[command] --help' for details")

    # set a keyring
    set_keyring_parser = subparsers.add_parser("set", description="create a keyring service",
                                               help="create a keyring service")
    set_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring service name", required=True)
    set_keyring_parser.add_argument("-u", "--username", metavar="",
                                    help="provide the username", required=True)

    set_keyring_parser.set_defaults(cmd="set")

    # get a keyring
    get_keyring_parser = subparsers.add_parser("get", description="get credentials from a keyring service",
                                               help="get credentials from a keyring service")
    get_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring service name", required=True)
    get_keyring_parser.set_defaults(cmd="get")

    # delete a keyring
    del_keyring_parser = subparsers.add_parser("del", description="delete a keyring service",
                                               help="delete a keyring service")
    del_keyring_parser.add_argument("-n", "--name", metavar="",
                                    help="provide the keyring service name", required=True)
    del_keyring_parser.set_defaults(cmd="del")

    # view all keyrings
    get_keyring_parser = subparsers.add_parser("view", description=f"Retrieving all service_names associated with the "
                                                                   f"keyring user: {KEYRING_USERNAME}",
                                               help=f"Retrieving all keyring service names associated with the "
                                                    f"keyring user: {KEYRING_USERNAME}")
    get_keyring_parser.set_defaults(cmd="view")

    # get the arguments
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    if args.cmd == "set":
        secret = get_hidden_input("Enter your password: ")
        set_keyring_service(args.name, args.username, secret)
    elif args.cmd == "get":
        usr = get_keyring_service(args.name)
        print(f"username: {usr}")
        print(f"password has been copied to your clipboard")
    elif args.cmd == "del":
        del_keyring_service(args.name)
        print(f"[+] deleted keyring service: {args.name}")

    elif args.cmd == "view":
        print(f"[+] Retrieving all service names associated with the keyring user: {KEYRING_USERNAME}")
        count = 1
        for service in view_keyring_services():
            print(f"{count}. {service.strip("'")}")
            count += 1

    else:
        parser.print_help(sys.stderr)

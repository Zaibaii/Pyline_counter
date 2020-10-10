#! /usr/bin/env python3
# coding: utf-8

"""

sample 3

"""


def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice


@do_twice
def main():
    """Fonction principale du programme"""

    print("Whee!")


if __name__ == '__main__':
    main()

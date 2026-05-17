#! /usr/bin/env python3

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
    """Main function of the program"""

    print("Yay!")


if __name__ == '__main__':
    main()

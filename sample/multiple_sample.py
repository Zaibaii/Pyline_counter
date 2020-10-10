#! /usr/bin/env python3
# coding: utf-8

"""Pyline counter command line sample"""

# Import - standard
import os
import subprocess


def main():
    """Main function of the program"""

    path_project = os.path.abspath(__file__ + '/../../')
    os.chdir(path_project)

    s = 'python pyline_counter.py'
    l_cmd = [
        rf'{s} sample\sample_script\sample_1.py',
        rf'{s} sample\sample_script',
        rf'{s} -d sample\sample_script',
        rf'{s} -db sample\sample_script',
        rf'{s} -dbr sample',
        rf'{s} -dbre sample',
        rf'{s} -dbre sample -s nb',
        rf'{s} -dbre -o sample_script_recursion -i multiple_sample.py sample',
        rf'{s} -dbrev -o sample_script_recursion -i multiple_sample.py sample',
        rf'{s} -dbre -o .idea;env;sample;test -i __init__ .',
        rf'{s} -h'
    ]

    for command in l_cmd:
        print("", command, sep='\n')
        subprocess.call(command)
        print("\n")
    input("Press the enter key to exit...\n")


# Main
if __name__ == '__main__':
    main()

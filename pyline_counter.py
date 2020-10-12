#! /usr/bin/env python3
# coding: utf-8

"""
Pyline counter gives the line count of your script / project Python.
Pyline counter has several options so that the result is as detailed and
precise as you wish.
usage: pyline_counter.py [-h] [-v] [-g] [-d] [-b] [-r] [-e]
[-o [EXCLUDE_FOLDER]] [-i [EXCLUDE_FILE]]
[-s [{file,nb,class,deco,func,doc,com,blank,_file,_nb,...}]] [path_or_file]

positional arguments:
 path_or_file          path (relative path authorized) or file (extension
                       file authorized: *.py; *.pyw; *.py3; *.pyi; *.pyde)
                       this argument is required if gui mode is not enabled

optional arguments:
 -h, --help            show this help message and exit
 -v, --verbose         increases the level of verbosity for debugging
 -g, --gui             enable gui mode (if no argument is given, gui mode is
                       enabled)
 -d, --detail          display detail information (number of
                       Class/Decorator/Function/Docstring/Comment/Blank line)
 -b, --byfile          display information by file (one more line for the
                       total)
 -r, --recursive       search files in subfolders (path only)
 -e, --exclude_empty   exclude empty files from result
 -o, --exclude_folder [EXCLUDE_FOLDER]
                       exclude folders from analysis (recursive option must
                       be enabled; regex default pattern:'.*\\your_input\\.*';
                       delimiter:';')
 -i, --exclude_file [EXCLUDE_FILE]
                       exclude files from analysis (path only;
                       regex default pattern:'^your_input$'; delimiter:';')
 -s, --sort [{file,nb,class,deco,func,doc,com,blank,_file,_nb,...}]
                       sort the result by (byfile option must be enabled) :
                        file: filename (default)
                        nb: number of line
                        class: number of class
                        deco: number of decorator
                        func: number of function
                        doc: number of docstring
                        com: number of comment
                        blank: number of blank line
                        _: Use the '_' prefix to reverse the sort order
"""

# Import - standard
import sys
import argparse

# Import - local
import lib_local.gui.gui as gui
import lib_local.pyline as pl


# Function
def parse_arguments():
    """Settings arguments"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("path_or_file", type=str, nargs="?", default="",
                        help="path (relative path "
                             "authorized) or file (extension file "
                             "authorized: *.py; *.pyw; *.py3; *.pyi; *.pyde)"
                             "\nthis argument is required if gui mode is not "
                             "enabled")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="increases the level of verbosity for "
                             "debugging")
    parser.add_argument("-g", "--gui", action="store_true",
                        help="enable gui mode (if no argument is given, "
                             "gui mode is enabled)")
    parser.add_argument("-d", "--detail", action="store_true",
                        help="display detail information (number of "
                             "Class/Decorator/Function/Docstring/Comment/"
                             "Blank line)")
    parser.add_argument("-b", "--byfile", action="store_true",
                        help="display information by file (one more line "
                             "for the total)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="search files in subfolders (path only)")
    parser.add_argument("-e", "--exclude_empty", action="store_true",
                        help="exclude empty files from result")
    parser.add_argument("-o", "--exclude_folder", type=str, nargs="?",
                        default="",
                        help="exclude folders from analysis (recursive "
                             "option must be enabled; regex default pattern:"
                             "'.*\\your_input\\.*'; delimiter:';')")
    parser.add_argument("-i", "--exclude_file", type=str, nargs="?",
                        default="",
                        help="exclude files from analysis (path "
                             "only; regex default pattern:'^your_input$'; "
                             "delimiter:';')")
    parser.add_argument("-s", "--sort", nargs="?", default="", const="file",
                        choices=["file", "nb", "class", "deco", "func",
                                 "doc", "com", "blank", "_file", "_nb",
                                 "_class", "_deco", "_func",
                                 "_doc", "_com", "_blank"],
                        help="sort the result by (byfile option must be "
                             "enabled) :\n"
                             " file: filename (default)\n"
                             " nb: number of line\n"
                             " class: number of class\n"
                             " deco: number of decorator\n"
                             " func: number of function\n"
                             " doc: number of docstring\n"
                             " com: number of comment\n"
                             " blank: number of blank line\n"
                             " _: Use the '_' prefix to reverse the sort order"
                        )

    return parser.parse_args()


def main():
    """Main function of the program"""

    args = parse_arguments()

    # Enable gui mode if no argument is given
    if len(sys.argv) - 1 == 0:
        args.gui = True

    if args.gui:
        guip = gui.Guip(args.path_or_file, args.verbose, args.detail,
                        args.byfile, args.recursive, args.exclude_empty,
                        args.exclude_folder, args.exclude_file, args.sort)
        guip.mainloop()
    else:
        print()  # Blank line before progress info and result
        result = pl.launch_analysis(args.path_or_file, None, args.verbose,
                                    args.detail, args.byfile, args.recursive,
                                    args.exclude_empty, args.exclude_folder,
                                    args.exclude_file, args.sort)
        print(result)


# Main
if __name__ == '__main__':
    main()

# Amélioration possible
# mettre le projet sur github

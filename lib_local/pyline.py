#! /usr/bin/env python3
# coding: utf-8

"""Pyline gives the line count of your script / project"""

# Import - standard
import os.path as os_path
from pathlib import Path
from datetime import datetime
import logging as lg
import sys
import glob
import re

# Constant
I_SPACE_COL = 3
T_EXT = (".py", ".pyw", ".py3", ".pyi", ".pyde")  # Script allowed / searched
T2D_COLUMN = (("File", 4 + I_SPACE_COL), ("Nb line", 7 + I_SPACE_COL),
              ("Class", 5 + I_SPACE_COL), ("Decorator", 9 + I_SPACE_COL),
              ("Function", 8 + I_SPACE_COL), ("Doctring", 8 + I_SPACE_COL),
              ("Comment", 7 + I_SPACE_COL), ("Blank line", 0))

T_SORT = ("file", "nb", "class", "deco", "func", "doc", "com", "blank")
T_REGEX = (
    re.compile(r'^\s*class .+'),  # Class
    re.compile(r'^\s*@.+'),  # Decorator
    re.compile(r'^\s*def .+'),  # Function / Method
    re.compile(r'^\s*"""'),  # Docstring
    re.compile(r'^\s*#'),  # Comment
    re.compile(r'^\s*$')  # Blank line
)
DOCSTR_PATTERN_ONELINE = re.compile(r'^\s*""".*"""')
DOCSTR_PATTERN_MULTILINE = re.compile(r'.*""".*')
EXCLUDE_DELIMITER = ";"
I_MAX_PROGRESS_PHRASE = 65
SORT_PREFIX = "_"
CANCEL_ANALYSIS = "CANCEL_ANALYSIS"
RESULT_EMPTY = "No python script was found."
RESULT_EMPTY_EXEM = "Only empty python scripts were found."
RESULT_TOTAL_BYFILE = "TOTAL"


# Function
def dtnt():
    """Return current date and time"""

    return datetime.now().time()


def debug_verbose(msg, o_gui, b_verbose):
    """Verbose cmd or gui if b_verbose is ON"""

    if not b_verbose:
        return False

    if o_gui:
        o_gui.display_debug(msg)
    else:
        lg.debug(msg)
    return True


def launch_analysis(pof, o_gui, b_verbose, b_detail, b_byfile, b_recur, b_exem,
                    ex_fo, ex_fi, sort):
    """Check if pof (path or file) is a good argument and start analysis"""

    lg.basicConfig(level=lg.DEBUG)
    pof_error = f"Invalid argument 'path_or_file': '{pof}'"
    pof_is = ""
    result = ""
    l_result = []
    i_align_max = 0
    b_cancel = False

    if os_path.isdir(pof):
        pof_is = "project"
        debug_verbose(f"{dtnt()}:pof detected {pof_is}", o_gui, b_verbose)
        l_result, i_align_max, b_cancel = analysis_folder(pof, o_gui,
                                                          b_verbose, b_detail,
                                                          b_byfile, b_recur,
                                                          ex_fo, ex_fi)
    elif os_path.isfile(pof) and Path(pof).suffix in T_EXT:
        pof_is = "script"
        debug_verbose(f"{dtnt()}:pof detected {pof_is}", o_gui, b_verbose)
        debug_verbose(f"{dtnt()}:File analysis", o_gui, b_verbose)
        l_result, i_align_max, b_cancel = analysis_file(pof, 1, 1, o_gui,
                                                        b_verbose, b_detail,
                                                        b_byfile)
        l_result = [l_result]

    if b_cancel:
        progress_info(-1, -1, o_gui)  # Erases analysis progress line
        debug_verbose(f"{dtnt()}:gui:Analysis canceled", o_gui, b_verbose)
        o_gui.la_th_canceled()
        return result

    if pof_is:
        progress_info(-1, -1, o_gui)  # Erases analysis progress line
        debug_verbose(f"{dtnt()}:Formatting the result", o_gui, b_verbose)
        result = format_result(l_result, pof_is, i_align_max, sort, o_gui,
                               b_verbose, b_detail, b_byfile, b_exem)
    elif o_gui:
        debug_verbose(f"{dtnt()}:gui:pof error", o_gui, b_verbose)
        result = pof_error
    else:
        debug_verbose(f"{dtnt()}:cmd:pof error\n", o_gui, b_verbose)
        raise Exception(pof_error)

    if o_gui:
        debug_verbose(f"{dtnt()}:gui:Displays the result of the analysis\n",
                      o_gui, b_verbose)
        o_gui.la_th_result(result)
    else:
        debug_verbose(f"{dtnt()}:cmd:Return the result of the analysis\n",
                      o_gui, b_verbose)
        return result


def analysis_folder(path, o_gui, b_verbose, b_detail, b_byfile, b_recur,
                    ex_fo, ex_fi):
    """
    Search all files with T_EXT extension and start analysis
    Exclude folders (ex_fo) - regex default pattern: '.*\\your_input\\.*'
    Exclude files (ex_fi) - regex default pattern: '^your_input$'
    """

    l_file = []
    l2d_result = []
    i_file_current = 0
    i_align_max = 0
    l_ex_fo = []
    l_ex_fi = []
    b_cancel = False

    if b_recur:
        path = os_path.join(path, "**")
        if ex_fo:
            debug_verbose(f"{dtnt()}:Exclude folder pattern list:", o_gui,
                          b_verbose)
            l_ex_fo = ex_fo.split(EXCLUDE_DELIMITER)
            for i, el in enumerate(l_ex_fo):
                if o_gui and o_gui.la_th_cancel():
                    b_cancel = True
                    return l2d_result, i_align_max, b_cancel
                l_ex_fo[i] = re.compile(rf'.*\\{el}\\.*')
            debug_verbose(f"{dtnt()}:{l_ex_fo}", o_gui, b_verbose)

    if ex_fi:
        debug_verbose(f"{dtnt()}:Exclude file pattern list:", o_gui, b_verbose)

        l_ex_fi = ex_fi.split(EXCLUDE_DELIMITER)
        for i, el in enumerate(l_ex_fi):
            if o_gui and o_gui.la_th_cancel():
                b_cancel = True
                return l2d_result, i_align_max, b_cancel
            l_ex_fi[i] = re.compile(rf'^{el}$')
        debug_verbose(f"{dtnt()}:{l_ex_fi}", o_gui, b_verbose)

    debug_verbose(f"{dtnt()}:Search files by extension", o_gui, b_verbose)
    for ext in T_EXT:
        ext = "*" + ext
        for file in glob.glob(os_path.join(path, ext), recursive=b_recur):
            if o_gui and o_gui.la_th_cancel():
                b_cancel = True
                return l2d_result, i_align_max, b_cancel
            l_file.append(file)

    if l_ex_fo:
        debug_verbose(f"{dtnt()}:Exclude folder:", o_gui, b_verbose)
        l_file_temp = []
        for file in l_file:
            b_exclude = False
            fon = os_path.dirname(file) + "\\"
            for pattern in l_ex_fo:
                if o_gui and o_gui.la_th_cancel():
                    b_cancel = True
                    return l2d_result, i_align_max, b_cancel
                if pattern.match(fon):
                    debug_verbose(f"{dtnt()}:{file}", o_gui, b_verbose)
                    b_exclude = True
                    break
            if not b_exclude:
                l_file_temp.append(file)
        l_file = l_file_temp.copy()

    if l_ex_fi:
        debug_verbose(f"{dtnt()}:Exclude file:", o_gui, b_verbose)
        l_file_temp = []
        for file in l_file:
            b_exclude = False
            fin = os_path.basename(file)
            fin_less_ext = fin[:fin.index('.')]
            for pattern in l_ex_fi:
                if o_gui and o_gui.la_th_cancel():
                    b_cancel = True
                    return l2d_result, i_align_max, b_cancel
                if pattern.match(fin) or pattern.match(fin_less_ext):
                    debug_verbose(f"{dtnt()}:{file}", o_gui, b_verbose)
                    b_exclude = True
                    break
            if not b_exclude:
                l_file_temp.append(file)
        l_file = l_file_temp.copy()

    i_file_total = len(l_file)
    debug_verbose(f"{dtnt()}:Files analysis", o_gui, b_verbose)
    for file in l_file:
        i_file_current += 1
        l_result, i_align, b_cancel = analysis_file(file, i_file_current,
                                                    i_file_total, o_gui,
                                                    b_verbose, b_detail,
                                                    b_byfile)
        if b_cancel:
            return l2d_result, i_align_max, b_cancel

        l2d_result.append(l_result)
        if i_align > i_align_max:
            i_align_max = i_align

    if o_gui and o_gui.la_th_cancel():
        b_cancel = True

    return l2d_result, i_align_max, b_cancel


def analysis_file(file, i_file_current, i_file_total, o_gui, b_verbose,
                  b_detail, b_byfile):
    """Analysis a python file"""

    i_align = 0
    l_result = [0]
    b_cancel = False
    b_docstring_multiline = False
    if b_detail:
        l_result = [0] * (len(T_REGEX) + 1)

    progress_info(i_file_current, i_file_total, o_gui)
    try:
        f = open(file, 'rt', errors='ignore')
    except Exception as err:
        progress_info(-1, -1, o_gui)  # Erases analysis progress line
        if not debug_verbose(f"{dtnt()}:Exception:{file}\n\t{err}", o_gui,
                             b_verbose):
            print(f"Warning:{file}\n\t{err}\n")
    else:
        for line in f:
            l_result[0] += 1
            if o_gui and o_gui.la_th_cancel():
                b_cancel = True
                break

            if not b_detail:
                continue

            if b_docstring_multiline:
                if DOCSTR_PATTERN_MULTILINE.match(line):
                    b_docstring_multiline = False
                continue

            for i, pattern in enumerate(T_REGEX):
                if pattern.match(line):
                    l_result[i + 1] += 1
                    if i == 3 and not DOCSTR_PATTERN_ONELINE.match(
                            line):
                        b_docstring_multiline = True
                    break
        f.close()

    if b_byfile:
        fn = os_path.basename(file)
        i_align = len(fn)
        l_result.insert(0, fn)

    return l_result, i_align, b_cancel


def progress_info(i_file_current, i_file_total, o_gui):
    """Displays/Update/Clear analysis progress"""

    result = f"Analysis in progress: {i_file_current}/{i_file_total} file(s)"
    result += " " * (I_MAX_PROGRESS_PHRASE - len(result))

    if i_file_current == -1 and i_file_total == -1:
        if not o_gui:
            print(" " * I_MAX_PROGRESS_PHRASE, end='\r')
        else:
            o_gui.progress_end()
    elif not o_gui:
        sys.stdout.write(result + '\r')
    else:
        o_gui.progress_update(i_file_current, i_file_total, result)


def format_result(l_result, pof_is, i_align_max, sort, o_gui, b_verbose,
                  b_detail, b_byfile, b_exem):
    """Format a result of analysis in string"""

    if b_exem:
        i_col = 0
        if b_byfile:
            i_col = 1

        l_temp = [l_line for l_line in l_result if l_line[i_col]]
        if l_result and not l_temp:
            return RESULT_EMPTY_EXEM
        l_result = l_temp.copy()

    if not l_result:
        result = RESULT_EMPTY
    elif not b_detail and not b_byfile:
        result = f"Your {pof_is} contains {sum(sum(l_result, []))} lines."
    else:

        display_columns = ""
        display_dash = ""
        len_result = len(l_result)
        total_name = f"{RESULT_TOTAL_BYFILE} ({len_result} files)"
        i_align_max = max(len(total_name) + I_SPACE_COL,
                          i_align_max + I_SPACE_COL)

        for i, (column_name, i_align) in enumerate(T2D_COLUMN):

            if not b_detail and i >= 2:
                break

            if not b_byfile and i == 0:
                continue

            if i == 0 and i_align_max > i_align:
                i_align = i_align_max

            len_column = len(column_name)
            display_columns += f"{column_name:<{i_align}}"
            display_dash += "-" * len_column + " " * (i_align - len_column)

        len_line_columns = len(display_columns.rstrip())
        result = display_columns + '\n'
        result += display_dash + '\n'

        if not b_byfile:
            l_result = [[sum(x) for x in zip(*l_result)]]
        elif len_result > 1:

            if not sort:
                sort = T_SORT[0]
            debug_verbose(f"{dtnt()}:sorting order:{sort}", o_gui, b_verbose)

            b_sreverse = False
            if sort[0] == SORT_PREFIX:
                b_sreverse = True
                sort = sort[1:]

            for i, select in enumerate(T_SORT):
                if sort == select:
                    l_result.sort(
                        key=lambda x: x[i].casefold() if i == 0 else x[i],
                        reverse=b_sreverse)

            l_total = [row[1:] for row in l_result]
            l_total = [sum(x) for x in zip(*l_total)]
            l_total.insert(0, total_name)
            l_result.append(l_total)

        for l_line in l_result:
            for i, el in enumerate(l_line):
                if not b_byfile:
                    i += 1
                elif el == total_name:
                    result += "-" * len_line_columns + '\n'

                i_align = T2D_COLUMN[i][1]
                if i == 0 and i_align_max > i_align:
                    i_align = i_align_max
                result += f"{el:<{i_align}}"

            result += '\n'
        result = result.rstrip('\n')

    return result

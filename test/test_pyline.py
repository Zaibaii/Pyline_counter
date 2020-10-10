#! /usr/bin/env python3
# coding: utf-8

"""Test the pyline local labrary"""

# Import - standard
import os.path as os_path
import sys
import unittest

# Constant
PATH_FILE = os_path.dirname(os_path.abspath(__file__))
PATH_PROJECT = os_path.abspath(PATH_FILE + '/../')
PATH_TESTSCRIPT = os_path.join(PATH_FILE, "test_script")

# Import - local
sys.path.append(os_path.normpath(PATH_PROJECT))
import lib_local.pyline as pl


class PylineTest(unittest.TestCase):

    def test_debug_verbose_true(self):
        result = pl.debug_verbose("debug msg", None, True)
        self.assertTrue(result)

    def test_debug_verbose_false(self):
        result = pl.debug_verbose("debug msg", None, False)
        self.assertFalse(result)

    def test_launch_analysis_error(self):
        filename = "test_bad_ext.pyd"
        file = os_path.join(PATH_TESTSCRIPT, filename)
        a_result = f"Invalid argument 'path_or_file': '.+{filename}'$"

        with self.assertRaisesRegex(Exception, a_result):
            pl.launch_analysis(file, None, False, False, False, False,
                               False, "", "", "")

    def test_analysis_file(self):
        a_result = [13]
        file = os_path.join(PATH_TESTSCRIPT, "test_1.py")
        l_result, i_align_max, b_cancel = pl.analysis_file(file, -1, -1, None,
                                                           False, False, False)
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 0)

    def test_analysis_file_detail(self):
        a_result = [13, 0, 0, 1, 2, 2, 6]
        file = os_path.join(PATH_TESTSCRIPT, "test_1.py")
        l_result, i_align_max, b_cancel = pl.analysis_file(file, -1, -1, None,
                                                           False, True, False)
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 0)

    def test_analysis_file_byfile(self):
        a_result = ['test_1.py', 13]
        file = os_path.join(PATH_TESTSCRIPT, "test_1.py")
        l_result, i_align_max, b_cancel = pl.analysis_file(file, -1, -1, None,
                                                           False, False, True)
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 9)

    def test_analysis_file_detail_byfile(self):
        a_result = ['test_1.py', 13, 0, 0, 1, 2, 2, 6]
        file = os_path.join(PATH_TESTSCRIPT, "test_1.py")
        l_result, i_align_max, b_cancel = pl.analysis_file(file, -1, -1, None,
                                                           False, True, True)
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 9)

    def test_analysis_folder(self):
        a_result = [[13], [26], [14]]
        l_result, i_align_max, b_cancel = pl.analysis_folder(PATH_TESTSCRIPT,
                                                             None, False,
                                                             False, False,
                                                             False, "", "")
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 0)

    def test_analysis_folder_detail(self):
        a_result = [[13, 0, 0, 1, 2, 2, 6], [26, 0, 1, 3, 2, 2, 8],
                    [14, 0, 0, 1, 2, 2, 6]]
        l_result, i_align_max, b_cancel = pl.analysis_folder(PATH_TESTSCRIPT,
                                                             None, False,
                                                             True, False,
                                                             False, "", "")
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 0)

    def test_analysis_folder_byfile(self):
        a_result = [['test_1.py', 13], ['test_3.py', 26],
                    ['test_2.pyw', 14]]
        l_result, i_align_max, b_cancel = pl.analysis_folder(PATH_TESTSCRIPT,
                                                             None, False,
                                                             False, True,
                                                             False, "", "")
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 10)

    def test_analysis_folder_detail_byfile(self):
        a_result = [['test_1.py', 13, 0, 0, 1, 2, 2, 6],
                    ['test_3.py', 26, 0, 1, 3, 2, 2, 8],
                    ['test_2.pyw', 14, 0, 0, 1, 2, 2, 6]]
        l_result, i_align_max, b_cancel = pl.analysis_folder(PATH_TESTSCRIPT,
                                                             None, False,
                                                             True, True,
                                                             False, "", "")
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 10)

    def test_analysis_folder_recur(self):
        a_result = [[13], [26], [15], [14]]
        l_result, i_align_max, b_cancel = pl.analysis_folder(PATH_TESTSCRIPT,
                                                             None, False,
                                                             False, False,
                                                             True,
                                                             "foldername",
                                                             "__init__")
        self.assertEqual(l_result, a_result)
        self.assertEqual(i_align_max, 0)

    def test_format_result_script(self):
        a_result = "Your script contains 13 lines."
        l_result = [[13]]
        pos_is = "script"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, False, False)
        self.assertEqual(result, a_result)

    def test_format_result_script_detail(self):
        a_result = "Nb line   Class   Decorator   Function   Doctring   "\
                   "Comment   Blank line\n-------   -----   ---------   "\
                   "--------   --------   -------   ----------\n13        0  "\
                   "     0           1          2          2         6"
        l_result = [[13, 0, 0, 1, 2, 2, 6]]
        pos_is = "script"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, True, False, False)
        self.assertEqual(result, a_result)

    def test_format_result_script_byfile(self):
        a_result = "File              Nb line   \n----              -------  "\
                   " \ntest_1.py         13        "
        l_result = [['test_1.py', 13]]
        pos_is = "script"
        i_align_max = 9
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, True, False)
        self.assertEqual(result, a_result)

    def test_format_result_script_detail_byfile(self):
        a_result = "File              Nb line   Class   Decorator   Function "\
                   "  Doctring   Comment   Blank line\n----              "\
                   "-------   -----   ---------   --------   --------   "\
                   "-------   ----------\ntest_1.py         13        0      "\
                   " 0           1          2          2         6"
        l_result = [['test_1.py', 13, 0, 0, 1, 2, 2, 6]]
        pos_is = "script"
        i_align_max = 9
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, True, True, False)
        self.assertEqual(result, a_result)

    def test_format_result_project(self):
        a_result = "Your project contains 53 lines."
        l_result = [[13], [26], [14]]
        pos_is = "project"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, False, False)
        self.assertEqual(result, a_result)

    def test_format_result_project_noscript(self):
        a_result = "No python script was found."
        l_result = []
        pos_is = "project"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, False, True)
        self.assertEqual(result, a_result)

    def test_format_result_project_exem(self):
        a_result = "Only empty python scripts were found."
        l_result = [[0]]
        pos_is = "project"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, False, True)
        self.assertEqual(result, a_result)

    def test_format_result_project_detail(self):
        a_result = "Nb line   Class   Decorator   Function   Doctring   "\
                   "Comment   Blank line\n-------   -----   ---------   "\
                   "--------   --------   -------   ----------\n53        0  "\
                   "     1           5          6          6         20"
        l_result = [[13, 0, 0, 1, 2, 2, 6], [26, 0, 1, 3, 2, 2, 8],
                    [14, 0, 0, 1, 2, 2, 6]]
        pos_is = "project"
        i_align_max = 0
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, True, False, False)
        self.assertEqual(result, a_result)

    def test_format_result_project_byfile(self):
        a_result = "File              Nb line   \n----              -------  "\
                   " \ntest_1.py         13        \ntest_2.pyw        14    "\
                   "    \ntest_3.py         26        "\
                   "\n-------------------------\nTOTAL (3 files)   53        "
        l_result = [['test_1.py', 13], ['test_3.py', 26], ['test_2.pyw', 14]]
        pos_is = "project"
        i_align_max = 10
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, False, True, False)
        self.assertEqual(result, a_result)

    def test_format_result_project_detail_byfile(self):
        a_result = "File              Nb line   Class   Decorator   Function "\
                   "  Doctring   Comment   Blank line\n----              "\
                   "-------   -----   ---------   --------   --------   "\
                   "-------   ----------\ntest_1.py         13        0      "\
                   " 0           1          2          2         "\
                   "6\ntest_2.pyw        14        0       0           1     "\
                   "     2          2         6\ntest_3.py         26        "\
                   "0       1           3          2          2         "\
                   "8\n------------------------------------------------------"\
                   "------------------------------------\nTOTAL (3 files)   "\
                   "53        0       1           5          6          6    "\
                   "     20"
        l_result = [['test_1.py', 13, 0, 0, 1, 2, 2, 6],
                    ['test_3.py', 26, 0, 1, 3, 2, 2, 8],
                    ['test_2.pyw', 14, 0, 0, 1, 2, 2, 6]]
        pos_is = "project"
        i_align_max = 10
        result = pl.format_result(l_result, pos_is, i_align_max, "", None,
                                  False, True, True, False)
        self.assertEqual(result, a_result)

    def test_format_result_project_detail_byfile_sort(self):
        a_result = "File                  Nb line   Class   Decorator   "\
                   "Function   Doctring   Comment   Blank line\n----         "\
                   "         -------   -----   ---------   --------   "\
                   "--------   -------   ----------\ntest_3.py             "\
                   "26        0       1           3          2          2    "\
                   "     8\ntest_recursion_1.py   15        0       0        "\
                   "   1          2          2         6\ntest_2.pyw         "\
                   "   14        0       0           1          2          2 "\
                   "        6\ntest_1.py             13        0       0     "\
                   "      1          2          2         "\
                   "6\n------------------------------------------------------"\
                   "----------------------------------------\nTOTAL (4 files)"\
                   "       68        0       1           6          8        "\
                   "  8         26"
        l_result = [['test_1.py', 13, 0, 0, 1, 2, 2, 6],
                    ['test_3.py', 26, 0, 1, 3, 2, 2, 8],
                    ['test_recursion_1.py', 15, 0, 0, 1, 2, 2, 6],
                    ['test_2.pyw', 14, 0, 0, 1, 2, 2, 6]]
        pos_is = "project"
        i_align_max = 19
        result = pl.format_result(l_result, pos_is, i_align_max, "_nb", None,
                                  False, True, True, False)
        self.assertEqual(result, a_result)


if __name__ == '__main__':
    unittest.main()

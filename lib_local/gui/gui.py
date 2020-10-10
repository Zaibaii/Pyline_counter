#! /usr/bin/env python3
# coding: utf-8

"""GUI library"""

# Import - standard
import os.path as os_path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import wx
import wx.lib.agw.multidirdialog as mdd

# Import - local
import lib_local.pyline as pl

# Constant
PATH_FILE = os_path.dirname(os_path.abspath(__file__))
PATH_PROJECT = os_path.abspath(PATH_FILE + '/../../')
PATH_PICTURE = os_path.join(PATH_FILE, "picture")
EXCLUDE_DELIMITER = ";"
T_FILEEXT = ("Python files", "*.py;*.pyw;*.py3;*.pyi;*.pyde")
PROGRESS_DEFAULT = "Progress of analysis"
APP_WX = wx.App(0)


# Class
class GuiTextScrollCombo(tk.Frame):
    """GUI - Text + scrollbar widget"""

    def __init__(self, *args, **kwargs):
        """Builder Text + scrollbar widget"""

        super().__init__(*args, **kwargs)

        # Ensure a consistent GUI size and implement stretchability
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a Text widget
        self.wtxt = tk.Text(self, padx=20, pady=10, bd=2,
                            bg='SystemButtonFace', font=("consolas", 12),
                            undo=True, wrap='word', state=tk.DISABLED)
        self.wtxt.grid(row=0, column=0, sticky="nsew")

        # Create a scrollbar and associate it with wtxt
        scrollb = tk.Scrollbar(self, command=self.wtxt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.wtxt['yscrollcommand'] = scrollb.set


class Guip(tk.Tk):
    """GUI - main"""

    def __init__(self, pof, b_verbose, b_detail, b_byfile, b_recur, b_exem,
                 ex_fo, ex_fi, sort, *args, **kwargs):
        """Builder gui"""

        # Master gui
        super().__init__(*args, **kwargs)
        self.withdraw()  # Hide GUI
        self.iconbitmap(fr'{PATH_PICTURE}/icon.ico')
        self.title('Pyline counter')

        # Size and coordinate
        w = 1200
        h = 800
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Defaults attributes
        self.la_th = Thread()
        self.b_cancel = False

        # Custom multi directory dialog
        self.dlg = mdd.MultiDirDialog(None, message="Select one or more "
                                                    "folders",
                                      defaultPath=PATH_PROJECT,
                                      agwStyle=mdd.DD_MULTIPLE |
                                      mdd.DD_DIR_MUST_EXIST)

        # Label / Buttons select pof
        frame_pof = tk.Frame(self)
        frame_pof.pack(anchor=tk.W, padx=2, pady=3)
        tk.Label(frame_pof, text="Select").pack(side=tk.LEFT)
        tk.Button(frame_pof, text="path",
                  command=self.button_browse_path).pack(side=tk.LEFT)
        tk.Label(frame_pof, text="or").pack(side=tk.LEFT)
        tk.Button(frame_pof, text="file",
                  command=self.button_browse_file).pack(side=tk.LEFT)
        tk.Label(frame_pof, text=":").pack(side=tk.LEFT)
        self.label_pof = tk.StringVar()
        self.label_pof.trace('w', self.prerequisite_analysis)
        tk.Entry(frame_pof, width=90,
                 textvariable=self.label_pof).pack(side=tk.LEFT)

        # Checkbutton option
        self.option = [["verbose (-v) : Increases the level of verbosity for "
                        "debugging.",
                        tk.BooleanVar(value=b_verbose)],
                       ["detail (-d) : Display detail information (number of "
                        "Class/Decorator/Function/Docstring/Comment/Blank "
                        "line).",
                        tk.BooleanVar(value=b_detail)],
                       ["byfile (-b) : Display information by file (one "
                        "more line for the total).",
                        tk.BooleanVar(value=b_byfile)],
                       ["recursive (-r) : Search files in subfolders (path "
                        "only).",
                        tk.BooleanVar(value=b_recur)],
                       ["exclude_empty (-e) : Exclude empty files "
                        "from result.", tk.BooleanVar(value=b_exem)]]
        frame_option = tk.Frame(self)
        frame_option.pack(anchor=tk.W)
        for name, b_etat in self.option:
            check = tk.Checkbutton(frame_option, text=name, variable=b_etat)
            check.pack(anchor=tk.W)

        # Option -o (exclude folder) and -i (exclude file)
        self.option_ex_fo = tk.BooleanVar()
        self.label_ex_fo = tk.StringVar()
        self.option_ex_fi = tk.BooleanVar()
        self.label_ex_fi = tk.StringVar()
        l_ex = [[self.option_ex_fo, self.label_ex_fo, self.lab_ex_fo,
                 self.button_ex_fo, self.checkbox_option_ex_fo, ex_fo,
                 "exclude_folder (-o) :", "Exclude folders",
                 "from analysis (recursive option must be enabled; regex "
                 "default pattern:'.*\\your_input\\.*'; delimiter:';') :", 65],
                [self.option_ex_fi, self.label_ex_fi, self.lab_ex_fi,
                 self.button_ex_fi, self.checkbox_option_ex_fi, ex_fi,
                 "exclude_file (-i) :", "Exclude files",
                 "from analysis (path only; regex default pattern:"
                 "'^your_input$'; delimiter:';') :", 70]]
        for el in l_ex:
            frame = tk.Frame(self)
            frame.pack(anchor=tk.W)
            el[1].trace('w', el[2])
            tk.Checkbutton(frame, text=el[6], variable=el[0]).pack(
                anchor=tk.W, side=tk.LEFT)
            tk.Button(frame, text=el[7], command=el[3]).pack(side=tk.LEFT)
            lab = tk.Label(frame, text=el[8])
            lab.pack(side=tk.LEFT, expand=True)
            lab.bind("<Button-1>", el[4])
            tk.Entry(frame, width=el[9], textvariable=el[1]).pack(side=tk.LEFT)
            el[1].set(el[5])

        # Option -s (sort)
        frame_sort = tk.Frame(self)
        frame_sort.pack(anchor=tk.W)
        self.option_sort = tk.BooleanVar()
        self.select_sort = tk.StringVar()
        self.select_sort.trace('w', self.str_sort)
        tk.Checkbutton(frame_sort, text="sort (-s) : Sort the "
                                        "result by (byfile option must be "
                                        "enabled) :",
                       variable=self.option_sort).pack(anchor=tk.W,
                                                       side=tk.LEFT)
        combo_sort = ttk.Combobox(frame_sort, width=8,
                                  textvariable=self.select_sort,
                                  state="readonly")
        combo_sort.bind("<<ComboboxSelected>>", lambda e: frame_sort.focus())
        combo_sort.config(values=("file", "nb", "class", "deco", "func", "doc",
                                  "com", "blank", "_file", "_nb", "_class",
                                  "_deco", "_func", "_doc", "_com", "_blank"))
        combo_sort.pack(side=tk.LEFT)
        self.select_sort.set(sort)
        if not sort:
            combo_sort.current(0)
            self.option_sort.set(False)

        # Button analysis and clear text result
        frame_analysis = tk.Frame(self)
        frame_analysis.pack(pady=(30, 0))
        self.button_analysis = tk.Button(frame_analysis, text="Start analysis",
                                         command=self.button_sc_analysis)
        self.button_clear = tk.Button(frame_analysis, text="Clear result",
                                      command=self.button_clear_result)
        self.label_pof.set(pof)  # Disable button analysis if empty
        self.button_analysis.pack(side=tk.LEFT, padx=30)
        self.button_clear.pack(side=tk.LEFT)

        # Progressbar
        frame_progress = tk.Frame(self)
        frame_progress.pack(fill=tk.BOTH, pady=(15, 0))
        self.progress_var = tk.DoubleVar()
        self.progress_style = ttk.Style(self)
        self.progress_style.layout(  # add label in the layout
            'text.Horizontal.TProgressbar',
            [('Horizontal.Progressbar.trough',
              {'children': [('Horizontal.Progressbar.pbar',
                             {'side': 'left', 'sticky': 'ns'})],
               'sticky': 'nswe'}),
             ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.progress_style.configure(  # set initial text
            'text.Horizontal.TProgressbar', text=PROGRESS_DEFAULT)
        self.progress = ttk.Progressbar(frame_progress, style='text.Horizontal'
                                                              '.TProgressbar',
                                        variable=self.progress_var)
        self.progress.pack(fill=tk.BOTH)

        # Text result
        self.text_scroll = GuiTextScrollCombo()
        self.text_scroll.pack(fill=tk.BOTH, expand=True)
        self.textvar_result = tk.StringVar()
        self.textvar_result.trace('w', self.display_result)
        self.textvar_result.set('')  # Disable button clear

        # Display GUI
        self.update()
        self.deiconify()

    def button_browse_path(self):
        """button event - select path"""

        path = filedialog.askdirectory(mustexist=True)
        self.label_pof.set(path)

    def button_browse_file(self):
        """button event - select file"""

        file = filedialog.askopenfilename(filetypes=[T_FILEEXT])
        self.label_pof.set(file)

    def button_ex_fo(self):
        """button event - exclude folders"""

        lab_ex_fo = ""
        if self.dlg.ShowModal() != wx.ID_OK:
            paths = ""
        else:
            paths = self.dlg.GetPaths()

        for path in enumerate(paths):
            lab_ex_fo += os_path.basename(path[1]) + EXCLUDE_DELIMITER

        lab_ex_fo = lab_ex_fo[:-1]
        self.label_ex_fo.set(lab_ex_fo)

    def button_ex_fi(self):
        """button event - exclude files"""

        lab_ex_fi = ""
        files = filedialog.askopenfilenames(filetypes=[T_FILEEXT],
                                            multiple=True)
        for file in files:
            lab_ex_fi += os_path.basename(file) + EXCLUDE_DELIMITER

        lab_ex_fi = lab_ex_fi[:-1]
        self.label_ex_fi.set(lab_ex_fi)

    def button_sc_analysis(self):
        """button event - start or cancel analysis"""

        if not self.la_th.is_alive():
            self.progress_start()
            b_verbose = self.option[0][1].get()
            b_detail = self.option[1][1].get()
            b_byfile = self.option[2][1].get()
            b_recur = self.option[3][1].get()
            b_exem = self.option[4][1].get()
            pof = self.label_pof.get()
            ex_fo = ""
            ex_fi = ""
            if self.option_ex_fo.get():
                ex_fo = self.label_ex_fo.get()
            if self.option_ex_fi.get():
                ex_fi = self.label_ex_fi.get()
            sort = ""
            if self.option_sort.get():
                sort = self.select_sort.get()

            self.la_th = Thread(target=pl.launch_analysis,
                                args=(pof, self, b_verbose, b_detail,
                                      b_byfile, b_recur, b_exem, ex_fo,
                                      ex_fi, sort))
            self.la_th.daemon = True
            self.la_th.start()
            self.button_analysis.configure(text="Cancel analysis")
        else:
            self.b_cancel = True

    def button_clear_result(self):
        """button event - clear the result of text_scroll"""

        wtxt = self.text_scroll.wtxt
        wtxt.config(state=tk.NORMAL)
        self.text_scroll.wtxt.delete("1.0", "end")
        wtxt.config(state=tk.DISABLED)
        self.textvar_result.set('')  # Disable button clear

    def checkbox_option_ex_fo(self, *args):
        """Checkbox ex_fo event - update checkbox option"""

        if self.option_ex_fo.get():
            self.option_ex_fo.set(False)
        else:
            self.option_ex_fo.set(True)

    def checkbox_option_ex_fi(self, *args):
        """Checkbox ex_fi event - update checkbox option"""

        if self.option_ex_fi.get():
            self.option_ex_fi.set(False)
        else:
            self.option_ex_fi.set(True)

    def lab_ex_fo(self, *args):
        """StringVar label_ex_fo - update checkbox option"""

        if self.label_ex_fo.get() != "":
            self.option_ex_fo.set(True)
        else:
            self.option_ex_fo.set(False)

    def lab_ex_fi(self, *args):
        """StringVar label_ex_fi - update checkbox option"""

        if self.label_ex_fi.get() != "":
            self.option_ex_fi.set(True)
        else:
            self.option_ex_fi.set(False)

    def str_sort(self, *args):
        """StringVar select_sort - update checkbox option"""

        if self.select_sort.get() != "":
            self.option_sort.set(True)
        else:
            self.option_sort.set(False)

    def prerequisite_analysis(self, *args):
        """StringVar label_pof - disable button if no prerequisite"""

        if self.label_pof.get() != "":
            self.button_analysis.configure(state=tk.NORMAL)
        else:
            self.button_analysis.configure(state=tk.DISABLED)

    def display_result(self, *args):
        """StringVar textvar_result - display result in text widget"""

        result = self.textvar_result.get()
        if result:
            wtxt = self.text_scroll.wtxt
            wtxt.config(state=tk.NORMAL)
            wtxt.insert("end", result + "\n\n\n")
            wtxt.see("end")
            wtxt.config(state=tk.DISABLED)
            self.button_clear.configure(state=tk.NORMAL)
        else:
            self.button_clear.configure(state=tk.DISABLED)

    def display_debug(self, msg):
        """Display debug message in Text widget"""

        wtxt = self.text_scroll.wtxt
        wtxt.config(state=tk.NORMAL)
        wtxt.insert("end", msg + '\n')
        wtxt.see("end")
        wtxt.config(state=tk.DISABLED)
        self.button_clear.configure(state=tk.NORMAL)

    def progress_start(self):
        """Progressbar start analysis"""

        self.progress_var.set(0)
        self.progress_style.configure('text.Horizontal.TProgressbar',
                                      text="Starting analysis")

    def progress_update(self, i_file_current, i_file_total, result):
        """Progressbar update and label"""

        i_percent = (i_file_current / i_file_total) * 100
        if i_percent != self.progress_var.get():
            self.progress_var.set(i_percent)
        self.progress_style.configure('text.Horizontal.TProgressbar',
                                      text=result)

    def progress_end(self):
        """Progressbar finish analysis"""

        if self.b_cancel:
            self.progress_var.set(0)
            self.progress_style.configure('text.Horizontal.TProgressbar',
                                          text="Cancelled analysis")
        else:
            self.progress_style.configure('text.Horizontal.TProgressbar',
                                          text="Completed analysis")

    def la_th_result(self, result):
        """Update textvar_result with result of thread of analysis"""

        self.textvar_result.set(result)
        self.button_analysis.configure(text="Start analysis")

    def la_th_cancel(self):
        """Cancel status for thread of analysis"""

        return self.b_cancel

    def la_th_canceled(self):
        """Cancel the thread of analysis"""

        self.b_cancel = False
        self.button_analysis.configure(text="Start analysis")

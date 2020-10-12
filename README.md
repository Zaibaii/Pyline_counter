# Pyline_counter
Pyline counter gives the line count of your script / project Python.

Pyline counter has several options so that the result is as detailed and precise as you wish.

usage: pyline_counter.py [-h] [-v] [-g] [-d] [-b] [-r] [-e] [-o [EXCLUDE_FOLDER]] [-i [EXCLUDE_FILE]]
<br>[-s [{file,nb,class,deco,func,doc,com,blank,_file,_nb,...}]] [path_or_file]

| Positional arguments  | Description |
| :------------- | :----------------- |
| path_or_file   | path (relative path authorized) or file (extension file authorized: *.py; *.pyw; *.py3; *.pyi; *.pyde)<br>this argument is required if gui mode is not enabled|

| Optional arguments  | Description |
| :------------- | :------------- |
| -h, --help	 |	show this help message and exit|
| -v, --verbose	 |	increases the level of verbosity for debugging|
| -g, --gui	 |	enable gui mode (if no argument is given, gui mode is enabled)|
| -d, --detail	 |	display detail information (number of Class/Decorator/Function/Docstring/Comment/Blank line)|
| -b, --byfile	 |	display information by file (one more line for the total)|
| -r, --recursive|	search files in subfolders (path only)|
| -e, --exclude_empty|	exclude empty files from result|
| -o, --exclude_folder [EXCLUDE_FOLDER]| exclude folders from analysis (recursive option must be enabled; regex default pattern:'.*\\your_input\\.*'; delimiter:';')|
| -i, --exclude_file [EXCLUDE_FILE]| exclude files from analysis (path only; regex default pattern:'^your_input$'; delimiter:';')|
| -s, --sort [{file,nb,class,deco,func,doc,com,blank,_file,_nb,...}]|sort the result by (byfile option must be enabled) :<br>-  file: filename (default)<br>-  nb: number of line<br>-  class: number of class<br>-  deco: number of decorator<br>-  func: number of function<br>-  doc: number of docstring<br>-  com: number of comment<br>-  blank: number of blank line<br>-  \_: Use the '\_' prefix to reverse the sort order|

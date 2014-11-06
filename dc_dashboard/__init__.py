import os
DASHBOARD_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "static")
from IPython.display import display, Javascript, HTML

def load_libraries():
    with open(DASHBOARD_STATIC_FILES_PATH + "/dashboard_widget.css", 'r') as f:
        display(HTML("<style>" + f.read() + "</style>" +
        """<link rel="stylesheet" type="text/css" href="http://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.css">"""))

def link_js():
    lib_code = []
    with open(DASHBOARD_STATIC_FILES_PATH + "/base_plot.js", 'r') as f:
        lib_code.append(f.read())

    for file in os.listdir(DASHBOARD_STATIC_FILES_PATH + "/plots/"):
        with open(DASHBOARD_STATIC_FILES_PATH + "/plots/" + file) as f:
            lib_code.append(f.read())

    with open(DASHBOARD_STATIC_FILES_PATH + "/dashboard_widget.js", 'r') as f:
        code = f.read()
        code = code.replace("$$INSERT$$", "\n".join(lib_code))
        display(Javascript(code))


load_libraries()
link_js()
del os

#Import public components of the module
import Backend
from Dashboard import Dashboard
from Dimension import Dimension,Group
from Plot import Plot,Layer

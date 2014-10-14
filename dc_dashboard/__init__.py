import os
DASHBOARD_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "static")
from IPython.display import display, Javascript, HTML
del os


def load_libraries():
    with open(DASHBOARD_STATIC_FILES_PATH + "/dashboard_widget.css", 'r') as f:
        display(HTML("<style>" + f.read() + "</style>" +
        """<link rel="stylesheet" type="text/css" href="http://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.css">"""))
    with open(DASHBOARD_STATIC_FILES_PATH + "/dashboard_widget.js", 'r') as f:
        display(Javascript(data=f.read()))

load_libraries()

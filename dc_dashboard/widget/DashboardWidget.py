from IPython.html import widgets
from IPython.utils.traitlets import Unicode

class DashboardWidget(widgets.DOMWidget):
    _view_name = Unicode('DashboardView', sync=True)
    layout     = Unicode("[]", sync=True)
    data       = Unicode("[]", sync=True)
    filters    = Unicode("[]", sync=True)
    preproc    = Unicode("(function(data) {return data;})", sync=True)

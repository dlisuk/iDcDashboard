from IPython.display import display
from widget.DashboardWidget import DashboardWidget

class Dashboard(object):
    def __init__(self, df, layout, backend=None):
        self._widget         = DashboardWidget()
        self._widget.data    = df.to_json(orient="records")
        self._widget.layout  = layout
        if backend != None:
            self._widget.on_trait_change(lambda (n,filters):backend.update_fitlers(filters),"filters")

    def show(self):
        display(self._widget)

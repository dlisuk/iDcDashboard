from IPython.display import display
from widget.DashboardWidget import DashboardWidget

class Dashboard(object):
    def __init__(self, df=None, layout=None, filter_callback=None):
        self._widget = DashboardWidget()

        if filter_callback is not None:
            self._widget.on_trait_change(lambda (n,filters):filter_callback(filters),"filters")

        if df is not None:
            self.set_data(df)

        if layout is not None:
            self.set_layout(layout)

    def set_data(self, df):
        self._widget.data = df.to_json(orient="records")

    def set_layout(self, layout):
        self._widget.layout = layout

    def show(self):
        display(self._widget)




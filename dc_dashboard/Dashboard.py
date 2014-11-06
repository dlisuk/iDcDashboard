from IPython.display import display
from IPython.html import widgets
from widget.DashboardWidget import DashboardWidget
import json
import pandas as pd

class Dashboard(object):
    def __init__(self, backend, dimensions, plots):
        """
        The primary constructor for Dashboard Widgets.

        :param backend:    A dc_dashboard.Backend.Backend object which provides the backing data for
                           the dashboard
        :param dimensions: A list of dc_dashboard.Dimension.Dimension objects describing cross filter
                           dimensions and groups used in the Dashboard
        :param plots:      A list of dc_dashboard.Plot.Plot/Layer objects describing the plots you
                           wish to use
        """
        self._backend = backend
        self._widget = DashboardWidget()

        self._widget.on_trait_change(lambda tmp:backend.filter_changed(),"filters")
        self._dimensions = {dim.name: dim for dim in dimensions}
        self._widget.dim_code = json.dumps({dim.name: dim.get_json_object() for dim in dimensions})
        self._widget.layout = json.dumps([plot.get_json_object() for plot in plots])
        backend.register_dashboard(self)

    def set_data(self, data):
        """
        Passes data from Python -> JavaScript

        :param data: a pd.core.frame.Dataframe or JSon string representing the data to be passed
                     to java script
        :raise ("Unknown data type"):  if an illegal type of data is passed
        """
        t = type(data)
        if t == pd.core.frame.DataFrame:
            self._widget.data = data.to_json(orient="records")
        elif t == str:
            self._widget.data = data
        else:
            raise("Unknown data type")

    def get_filters(self):
        """
        Parses the dimensional filters returned by JavaScript into column level filters usable by a backend.

        :return: A list of tuples (column_name, filters) describing filters which have been applied by the client.
                 The filters object is a list of individual filters which should be ORed together.
                 Multiple tuples for the same column may coexist and should be ORed together.
                 Individual filters are one of two forms, a single value which is an equivalence filter or
                 a list of the form [min max] which describes a range filter.
        """
        filter_json = json.loads(self._widget.filters)
        filter_map = {name.encode("utf8"): filters for name, filters in filter_json.iteritems() if len(filters) > 0}
        filters = []
        for dim, dim_filts in filter_map.iteritems():
            filters = filters + self._dimensions[dim].proc_filters(dim_filts).items()
        return filters

    def show(self):
        """ Method to cause rendering of the widget. """
        display(self._widget)

        buttons = self._backend.get_toolbar()
        if buttons is not None:
            toolbar = widgets.ContainerWidget()
            toolbar.children = buttons
            display(toolbar)
            toolbar.remove_class('vbox')
            toolbar.add_class('hbox')




from IPython.display import display
from widget.DashboardWidget import DashboardWidget
import json

class Dashboard(object):
    def __init__(self, df=None, layout=None, filter_callback=None, preproc=None):
        self._widget = DashboardWidget()

        if filter_callback is not None:
            filter_callback(self)
            self._widget.on_trait_change(lambda any:filter_callback(self),"filters")

        if preproc is not None:
            self._widget.preproc = preproc

        if df is not None:
            self.set_data(df)

        if layout is not None:
            self.set_layout(layout)

    def set_data(self, df, preproc=None):
        if preproc is not None:
            self._widget.preproc = preproc
        self.data = df

        self._widget.data = df.to_json(orient="records")

    def set_layout(self, layout):
        self._widget.layout = layout

    def get_filters(self):
        filter_json = json.loads(self._widget.filters)
        filter_funs = [lambda df: [True for x in df.index]]
        for j in filter_json:
            var_name      = j[0]
            filter_type   = j[1]
            filter_params = j[2]
            if filter_type == "in":
                if type(filter_params) != "list":
                    s = set([filter_params])
                else:
                    s = set(filter_params)
                filter_funs.append((lambda v,s:lambda df:[x in s for x in df[v]])(var_name,s) )
            elif filter_type == "between":
                filter_funs.append((lambda v,s:lambda df:[s[0] <= x and x <= s[1] for x in df[v]])(var_name,filter_params))

        def filter(df):
            fs = [f(df) for f in filter_funs]
            f_out = fs[0]
            for f in fs[1:]:
                f_out = [ x & y for x,y in zip(f_out, f)]
            return f_out

        return filter

    def get_filtered_df(self):
        filter = self.get_filters()
        return self.data[filter(self.data)]


    def show(self):
        display(self._widget)




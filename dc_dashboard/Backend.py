import Dashboard
import pandas as pd

class Backend(object):
    def register_dashboard(self, dashboard):
        None

    def filter_changed(self):
        None

class DF_Backend(Backend):
    def __init__(self,df):
        if type(df) != pd.core.frame.DataFrame:
            raise("DF_Backend requires a data frame")
        self.df = df

    def register_dashboard(self, dashboard):
        dashboard.set_data(self.df)


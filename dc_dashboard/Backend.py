import Dashboard
import pandas as pd
import numpy as np

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

class Sampling_DF_Backend(Backend):
    def __init__(self,df,max=1000):
        if type(df) != pd.core.frame.DataFrame:
            raise("DF_Backend requires a data frame")
        self.max = max
        self.df = df
        self.filters = []

        self.df_samp = None
        self._sample_df()

    def _sample_df(self):
        df_filt = self.df
        for col,filts in self.filters:
            if len(filts) == 0:
                continue
            eq_set = set()
            screen = [False] * df_filt.shape[0]
            for filt in filts:
                if type(filt) == list:
                    screen = [s or (filt[0] <= x and x <= filt[1]) for s,x in zip(screen, df_filt[col])]
                else:
                    eq_set.add(filt)
            if len(eq_set) > 0:
                screen = [s or (x in eq_set) for s,x in zip(screen, df_filt[col])]
            df_filt = df_filt[screen]

        self.df_samp = df_filt.loc[np.random.permutation(df_filt.index)[:min(self.max,df_filt.shape[0])]]

    def register_dashboard(self, dashboard):
        self.dashboard = dashboard
        dashboard.set_data(self.df_samp)

    def filter_changed(self):
        self.filters = self.dashboard.get_filters()
        self._sample_df()
        self.dashboard.set_data(self.df_samp)


from IPython.html import widgets

import pandas as pd
import numpy as np
import itertools


class Backend(object):
    def register_dashboard(self, dashboard):
        None

    def filter_changed(self):
        None

    def get_toolbar(self):
        return None

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
        self.dashboard = None
        self.max = max
        self.filters = []

        df = df.reindex(np.random.permutation(df.index))
        self.global_df = df.head(self.max)
        self.df = df.drop(self.max)


        self._sample_size_widget = widgets.IntProgressWidget(
            value=0,
            min=0,
            max=2*max,
            step=1,
            description='Sample Load:',
        )

        self._b_resamp = widgets.ButtonWidget(description='Resample')
        self._b_resamp.on_click(lambda w:self._resample_data())

        self._toolbar = [self._b_resamp, self._sample_size_widget]
        self._resample_data()


    def get_toolbar(self):
        return self._toolbar

    def register_dashboard(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.set_data(self.df_samp)

    def filter_changed(self):
        self.old_filters = self.filters
        self.filters = self.dashboard.get_filters()


    def _resample_data(self):
        self._lock_buttons()
        self._sample_df()
        if self.dashboard is not None:
            self.dashboard.set_data(self.df_samp)
        else:
            print "no dashboard"
        self._unlock_buttons()


    def _lock_buttons(self):
        for elem in self._toolbar:
            elem.disabled = True

    def _unlock_buttons(self):
        for elem in self._toolbar:
            elem.disabled = False

    def _make_screen(self):
        g_screen = [True] * self.df.shape[0]
        for col,filts in self.filters:
            dat = self.df[col]
            screen = [False] * self.df.shape[0]
            if len(filts) == 0:
                continue
            eq_set = set()
            for filt in filts:
                if type(filt) == list:
                    screen = screen | ((filt[0] <= dat) & (dat <= filt[1]))
                else:
                    eq_set.add(filt)
            if len(eq_set) > 0:
                screen = screen | dat.isin(eq_set)
            g_screen = g_screen & screen
        return g_screen

    def _sample_df(self):
        screen = self._make_screen()

        self.df_samp= pd.concat([self.df[screen].head(self.max), self.global_df])
        self._sample_size_widget.value = self.df_samp.shape[0]

class Callback_Backend(Backend):
    def __init__(self, onRegister=None, onFilter=None):
        """
        This is a 'glue backend' used when a layer of indirection between the true backend
        and the widget is required.

        :param onRegister: A callback function called when register_dashboard is called
        :param onFilter:   A callback function called when filter_changed is called
        """
        self.dashboard = None
        self.onRegister = onRegister
        self.onFilter = onFilter

    def register_dashboard(self, dashboard):
        self.dashboard = dashboard
        if self.onRegister is not None:
            self.onRegister(dashboard)

    def filter_changed(self):
        if self.onFilter is not None:
            self.onFilter()



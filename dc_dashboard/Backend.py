from IPython.html import widgets

import pandas as pd
import numpy as np
import requests


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
        self.df = df
        self.filters = []

        self._visible = [True] * self.df.shape[0]

        self._sample_size_widget = widgets.IntProgressWidget(
            value=0,
            min=0,
            max=max,
            step=1,
            description='Sample Load:',
        )

        self._b_resamp = widgets.ButtonWidget(description='Resample')
        self._b_resamp.on_click(lambda w:self._resample_data())

        self._b_hide = widgets.ButtonWidget(description='Mark as Hidden')
        self._b_hide.on_click(lambda w:self._mark_hidden())

        self._b_reset = widgets.ButtonWidget(description='Reset Hidden')
        self._b_reset.on_click(lambda w:self._mark_hidden())

        self._b_mark = widgets.ButtonWidget(description='Mark')
        self._b_mark.on_click(lambda w:self._mark())

        self._toolbar=[self._b_resamp, self._b_hide, self._b_reset, self._b_mark, self._sample_size_widget]

        self.df_samp = None
        self._sample_df()

    def get_toolbar(self):
        return self._toolbar

    def register_dashboard(self, dashboard):
        self.dashboard = dashboard
        dashboard.set_data(self.df_samp)

    def filter_changed(self):
        self._lock_buttons()
        self.filters = self.dashboard.get_filters()
        self._unlock_buttons()

    def _resample_data(self):
        self._lock_buttons()
        self.filters = self.dashboard.get_filters()
        self._sample_df()
        self.dashboard.set_data(self.df_samp)
        self._unlock_buttons()

    def _mark(self):
        self._lock_buttons()
        screen = self._make_screen()
        self._visible = [(x and (not y)) for (x, y) in zip(self._visible, screen)]
        self._unlock_buttons()

    def _mark_hidden(self):
        self._lock_buttons()
        screen = self._make_screen()
        self._visible = [(x and (not y)) for (x, y) in zip(self._visible, screen)]
        self._unlock_buttons()

    def _reset_visible(self):
        self._lock_buttons()
        self._visible = [True] * self.df.shape[0]
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
            screen = [False] * self.df.shape[0]
            if len(filts) == 0:
                continue
            eq_set = set()
            for filt in filts:
                if type(filt) == list:
                    screen = [s or (filt[0] <= x and x <= filt[1]) for s,x in zip(screen, self.df[col])]
                else:
                    eq_set.add(filt)
            if len(eq_set) > 0:
                screen = [s or (x in eq_set) for s,x in zip(screen, self.df[col])]
            g_screen = [g and s for g,s in zip(g_screen,screen)]
        return g_screen

    def _sample_df(self):
        screen = self._make_screen()
        screen = [(x and y) for (x, y) in zip(self._visible, screen)]

        df_filt = self.df[screen]
        self.df_samp = df_filt.loc[np.random.permutation(df_filt.index)[:min(self.max, df_filt.shape[0])]]
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

class HTTP_Backend(Backend):
    def __init__(self, url):
        r = requests.get(url)
        self.data = r.text

    def register_dashboard(self, dashboard):
        dashboard.set_data(self.data)
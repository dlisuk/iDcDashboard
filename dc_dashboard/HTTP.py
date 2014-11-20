from Backend import Backend
import requests
import json
from IPython.html import widgets

class HTTP_Backend(Backend):
    def __init__(self, url, dataset, n = 1000):
        self.root_url  = url
        self.url       = url + dataset
        self.db        = None
        self.n         = n
        self.filters   = "{}"
        self.data      = self._get_data()

        self._b_resamp = widgets.ButtonWidget(description='Resample')
        self._b_resamp.on_click(lambda w:self._resample_data())

        self._toolbar=[self._b_resamp]

    def get_toolbar(self):
        return self._toolbar

    def filter_changed(self):
        self._lock_buttons()
        f = {}
        for k,v in self.db.get_filters():
            if k not in f:
                f[k] = []
            f[k] = f[k] + v
        self.filters = json.dumps(f)
        self._unlock_buttons()

    def _resample_data(self):
        self._lock_buttons()
        self.data = self._get_data()
        self.db.set_data(self.data)
        self._unlock_buttons()

    def _get_data(self):
        parms = {"method":"sample", "n":str(self.n),"filter":self.filters}
        response = requests.post(self.url, parms)

        data = "[]"
        if response.status_code == 200:
            target = self.root_url + "data/" + response.content
            status = 202
            while status == 202:
                response = requests.get(target)
                status = response.status_code

            if status == 200:
                data = response.text
            requests.delete(target)
        return data

    def _lock_buttons(self):
        for elem in self._toolbar:
            elem.disabled = True

    def _unlock_buttons(self):
        for elem in self._toolbar:
            elem.disabled = False

    def register_dashboard(self, dashboard):
        self.db = dashboard
        self.db.set_data(self.data)

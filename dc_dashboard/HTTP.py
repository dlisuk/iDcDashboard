from Backend import Backend
import requests
import json
from IPython.html import widgets
import time

class HTTP_Backend(Backend):
    def __init__(self, url, dataset, n=1000, post_proc=None):
        self.gen_url   = url + "/make/" + dataset
        self.get_url   = url + "/result/"
        self.db        = None
        self.n         = n
        self.post_proc = post_proc
        self.filters   = "{}"
        self.data      = self._get_data()

        self._b_resamp = widgets.ButtonWidget(description='Resample')
        self._b_resamp.on_click(lambda w:self._resample_data())

        self._toolbar = [self._b_resamp]

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
        response = requests.post(self.gen_url, parms)

        data = "[]"
        if response.status_code == 200:
            target = self.get_url + response.content
            status = 202
            while status == 202:
                response = requests.get(target)
                status = response.status_code
                time.sleep(0.5)

            if status == 200:
                data = response.text
            else:
                print response.status_code
                print response.text
            requests.delete(target)

        if self.post_proc is not None:
            data = self.post_proc(data)

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

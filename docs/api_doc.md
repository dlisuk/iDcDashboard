# IDcDashboard API

  * [About](#about)
  * [Setup](#setup)
  * [Dashboards](#dashboards)
  * [Backends](#backends)
  * [Dimensions](#dimensions)
  * [Groups](#groups)
  * [Plots](#plots)
  * [Extending](#extending)
  
## About

IDcDashboard is an IPython notebook widget which eases integration of [dc.js](http://dc-js.github.io/dc.js/) with IPyton notebook.  It allows interactive visualization of arbitrarily sized data sets via interactive filtering.

The dashboards are meant for exploratory use by data scientists and are thus weaker in the looks department vs the hand tunable d3/dc code you can get in a static page.  Nicer plots can be done via   

## Setup
Once IDcDashboard is installed on your python library path, the followign 2 lines of code will load the library for use in your notebook.

```python
import dc_dashboard
from dc_dashboard import *
```

These import statements load all frontend code and libraries into the browser.  If a notebook is left running after it is closed, the front end code will be erased from the output and thus no longer working.  This can be remedied by calling:

```python
dc_dashboard.load_libraries()
dc_dashboard.link_js()
```

Or by restarting the python kernel and starting over.

## Dashboards

The Dashboard class configures and creates the widget object.  It is constructed as so:

```python
db = Dashboard(Backend, Dimensions, Plots)
```

The three constructor arguements will be discussed further in this document, but the basic idea follows:

  * **Backend**: The interface between the Dashboard and Data Source.  A basic backend may simply push all data from a Pandas DataFrame to the widget for display.  A more complicated backend reacts the applied filters to augment which data is displayed or processed on a remote server.
  * **Dimensions**: Analogs to Crossfilter [dimensions](https://github.com/square/crossfilter/wiki/API-Reference#dimension) and [groups](https://github.com/square/crossfilter/wiki/API-Reference#group-map-reduce), defines which fields can be plotted and how data can be binned/grouped.
  * **Plots**: Collection of python objects which describe the layout and plots which the widget displays.
  
The dashboard object exports 4 methods: set_data, get_filters, and show.

###set_data
```python
db.set_data(data)
```
Erases the currently displayed data and replaces it with the new data.  Data can either be a string containing JSON records or a Pandas Data Frame.

###get_filters
```python
db.get_filters()
```
Returns a list of all filters currently applied on the front end.  Format follows:

```[
  (field_name, [filter_1, filter_2])
  (field2, [])
]
```

Pretty much a list of tuples `(fieldname, filters)`.  A filter is either a single value `x` which implies a filter of the form `field_name == x` or a pair of values `[x, y]` which implies a range filter of the form `x <= field_name <= y`.  Multiple filters on a single field are expected to be ORed together (ie `(state, [CA, NV]` means state is either CA or NV), filters for different fields should be ANDed (```[(state, [CA]),(city, [Bejing])]``` should be empty).


###show
```pythnon
db.show()
```
Renders the widget in a IPython notebook shell.  Should usualy be run immediatly after creation of the object.

## Backends

A backend is the glue between a Dashboard and some data provider.      The Backend class is an abstract class which is extended by the user for specific applications.  Several general backends have been developed for quick use:
  * [DF_Backend](#df_backend)
  * [Sampling_DF_Backend](#sampling_df_backend)

The backend interface has two methods: register_dashboard and filter_changed.

###register_dashboard
```python
backend.register_dashboard(dashboard)
```

Informs the backend that *dashboard* has been created and intends on working with the backend.  Typially only one dashboard should register with a given backend.

###filter_changed
```python
backend.filter_changed()
```

Alerts the backend that the filters on the dashboard have changed.  Dashboard that care about filters will typically call get_filters on their target dashboard and take appropriote action.

### Specific Backends

In addition to the abstract backend, several basic implimentations have been completed.

#### DF_Backend
```python
backend = DF_Backend(data_frame)
```

Simply publishes a pandas data frame to the widget.  Does nothing on filtering and only sets data at dashboard registration.

#### Sampling_DF_Backend
```python
backend = Sampling_DF_Backend(data_frame, max=1000)
```

Randomly samples exactly *max* elements from the data_frame which match the applied filters and sends them to the dashboard.  Resends data every time the filters are augmented by the client.

##Dimensions


##Groups

##Plots

##Extending

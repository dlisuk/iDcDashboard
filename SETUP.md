#How to set up

Currently there are sveral external JavaScript libraries that must be put on your path prior to running the DC dashboard widget.  This assumes a unix like system (Mac OSX or Linux for example).  All libraries will be installed relative to the $LIBPATH defined below, no need to set it as an environment variable though.

**$LIBPATH** = ~/.ipython/profile_default/static/

Download these libraries to **$LIBPATH** and **$LIBPATH/custom**:

* **d3.js** http://cdnjs.cloudflare.com/ajax/libs/d3/3.4.11/d3.js
* **crossfilter.js** http://cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.9/         crossfilter.js
* **dc.js** http://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.js
* **dc.js css** http://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.css

Now edit the file **$LIBPATH/custom/custom.css** and add: 
> @import "/static/custom/dc.css"

Now edit the file **$LIBPATH/custom/custom.js** and add: 
> require([ '/static/custom/jquery.handsontable.full.js', '/static/custom/crossfilter.js', '/static/custom/d3.js', '/static/custom/dc.js' ]);

The code should now work.  Note that the JS files have to be put in both the static and custom directories in the libpath, it doesn't seem like ipython can fully see them unless they are in both locations.







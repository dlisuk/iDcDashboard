class Plot(object):
    def __init__(self, type):
        """
        A object to describe the configuration for a plot object.

        :param type: The type (scatter, pie, etc) of the chart you want.
                     Should correspond to a type in the static/plots directory
        """

        self.json_object = {"type": type}
        self.config_object = {}

    def title(self, title):
        """ Define the title of the plot
        """

        self.json_object["title"] = title
        return self

    def data_source(self, dim, group=""):
        """ Define the dimension and group to use.
        """

        self.json_object["data_source"] = "cf/" + dim + "/" + group
        return self

    def width(self, width):
        """ Define the width of hte plot
        """

        self.json_object["width"] = width
        return self

    def config(self, directive, args):
        """
        Call custom, plot specific configuration functions.
        See induvidual plot js files to find options

        :param directive: Config function to call
        :param args: Python list to be passed to the config function
        """

        self.config_object[directive] = args
        return self

    def get_json_object(self):
        """ Helper method to convert from a dimension to a json string to send to JavaScript  """
        if len(self.config_object) > 0:
            self.json_object["config"] = self.config_object
        return self.json_object

class Layer(object):
    def __init__(self, height):
        """
        Indicator that following plots should be in a new layer from previous plots.

        :param height: The height of plots on this layer
        """
        self.height = height

    def get_json_object(self):
        """ Helper method to convert from a dimension to a json string to send to JavaScript  """
        return {"type": "layer", "height": self.height}


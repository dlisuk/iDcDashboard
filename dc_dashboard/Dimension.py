
class Dimension():
    def __init__(self, x_field, y_field = None, name_override = None):
        """
        A crossfilter dimension for data you wish to plot

        :param x_field: The column name you wish to use along the main axis of a plot
        :param y_field: An optional column name for the y location of a bubble/scatter plot
        :param name_override: Override default name format of "$x[_$y]"
        """

        self.name    = x_field
        if y_field is not None:
            self.name = self.name + "_" + y_field

        if name_override is not None:
            self.name = name_override

        self.x_field = x_field
        self.y_field = y_field
        self.groups = {}

    def get_json_object(self):
        """ Helper method to convert from a dimension to a json string to send to JavaScript  """
        out = {"dimension": self._dim_function()}
        if len(self.groups) > 0:
            out["groups"] = {name: group._group_function()
                             for name, group in self.groups.iteritems()}
        return out

    def add_group(self, group_name, group):
        """
        Register a group object to this dimension

        :param group_name: The name you wish to refer to this group by
        :param group:      The dc_dashboard.Dimension.Group object you wish to pass
        """
        self.groups[group_name] = group
        return self

    def proc_filters(self, filter):
        """
        Converts a filter on this dimension to filters on the dimension's fields.
        Primarily used by system rather than user.
        """
        if self.y_field is not None:
            x_filter = []
            y_filter = []
            for a in filter:
                if type(a) == dict:
                    x_filter.append([a["_southWest"]["lat"],a["_northEast"]["lat"]])
                    y_filter.append([a["_southWest"]["lng"],a["_northEast"]["lng"]])
                elif type(a[0]) == list:
                    x_filter.append([a[0][0], a[1][0]])
                    y_filter.append([a[0][1], a[1][1]])
                else:
                    x_filter.append(a[0])
                    y_filter.append(a[1])

            return {self.x_field: x_filter, self.y_field: y_filter}
        else:
            return {self.x_field:filter}

    def _dim_function(self):
        if self.y_field == None:
            return "(function(d){return d." + self.x_field + ";})"
        else:
            return "(function(d){return [d." + self.x_field + ", d." + self.y_field + "];})"



class Group():
    def __init__(self, group_function = ""):
        """
        A crossfilter group to attach to a dimension.
        Usualy used to compute y value and binning for bar charts and similar.

        See reference for cross filter at
        https://github.com/square/crossfilter/wiki/API-Reference#group-map-reduce
        This is just a project of that interface

        :param group_function: Function defining how to go from dimension -> grouped dimension (binning)
        """
        self.functions = ["group(" + group_function + ")"]

    def reduce(self, add, remove, initial):
        """
        Interface for  crossfilter group reduce.
        All parameters must be Strings representing java script functions.
        """
        self.functions.append("reduce(" + add + "," + remove + "," + initial +")")
        return self

    def reduce_sum(self, field):
        """
        Sum over a field to produce the group value

        :param field: Field to sum over
        """
        self.functions.append("reduceSum(function(d){return d." + field + "})")
        return self

    def reduce_count(self):
        """
        Count over a group, useful for histograms.
        """
        self.functions.append("reduceCount()")
        return self

    def _group_function(self):
        if len(self.functions) == 0:
            raise("A group needs at least one function")

        return "(function(dim){return dim." + ".".join(self.functions) + "})"

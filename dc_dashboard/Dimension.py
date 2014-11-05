
class Dimension():
    def __init__(self, x_field, y_field = None):
        self.name    = x_field
        if y_field is not None:
            self.name = self.name + "_" + y_field

        self.x_field = x_field
        self.y_field = y_field
        self.groups = {}

    def get_json_object(self):
        out = {"dimension": self._dim_function()}
        if len(self.groups) > 0:
            out["groups"] = {name: group._group_function()
                             for name, group in self.groups.iteritems()}
        return out

    def add_group(self, group_name, group):
        self.groups[group_name] = group
        return self

    def proc_filters(self, filter):
        if self.y_field is not None:
            x_filter = []
            y_filter = []
            for a in filter:
                if type(a[0]) == list:
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
        self.functions = ["group(" + group_function + ")"]

    def reduce(self, add, remove, initial):
        self.functions.append("reduce(" + add + "," + remove + "," + initial +")")
        return self

    def reduce_sum(self, field):
        self.functions.append("reduceSum(function(d){return d." + field + "})")
        return self

    def reduce_count(self):
        self.functions.append("reduceCount()")
        return self

    def _group_function(self):
        if len(self.functions) == 0:
            raise("A group needs at least one function")

        return "(function(dim){return dim." + ".".join(self.functions) + "})"

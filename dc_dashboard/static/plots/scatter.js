plots.scatter = {};
plots.scatter.prototype = plots.base_cf;

plots.render = function(master, target_div){
    this.plot = dc.scatterPlot(target, $(target).attr('render_group'));
    this.plot.dimension(this.dimension).group(this.group)
    this.plot.x(d3.scale.linear()).elasticX(true)
    this.plot.y(d3.scale.linear()).elasticY(true)
};

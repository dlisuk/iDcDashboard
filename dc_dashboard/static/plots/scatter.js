plots.scatter = function(){
    this.render = function(master, $target_div){
        var render_group = $target_div.attr('render_group');
        this.plot = dc.scatterPlot($target_div[0], render_group);
        this.plot.dimension(this.dimension).group(this.group);
        this.plot.x(d3.scale.linear()).elasticX(true);
        this.plot.y(d3.scale.linear()).elasticY(true);

        this.master = master;
        this.$target_div = $target_div;
        this.init_filter();
    };
};
plots.scatter.prototype = plots.base_cf;



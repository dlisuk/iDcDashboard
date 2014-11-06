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

    this.config = {};
    this.config.parent = this;
    this.config.prototype = this.prototype.config;
    this.config.domain = function(range){
        var the_plot = this.parent.plot;
        the_plot.elasticX(false).x(d3.scale.linear().domain(range));
    };
    this.config.range = function(range){
        var the_plot = this.parent.plot;
        the_plot.elasticY(false).y(d3.scale.linear().domain(range));
    };
};
plots.scatter.prototype = plots.base_cf;



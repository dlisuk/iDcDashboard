plots.line = function(){
    this.render = function(master, $target_div){
        var min = this.dimension.bottom(1);
        var max = this.dimension.top(1);
        if(min.length >0 ){
            min = min[0].TimeStamp;
            max = max[0].TimeStamp;
        }else{
            min = 0;
            max = 1;
        }

        var render_group = $target_div.attr('render_group');
        this.plot = dc.lineChart($target_div[0], render_group);
        this.plot.dimension(this.dimension).group(this.group);
        this.plot.x(d3.scale.linear().domain([min,max]));

        this.master = master;
        this.$target_div = $target_div;
        this.init_filter();

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
};

plots.line.prototype = plots.base_cf;
plots.line.update_data = function(){
    var min = this.dimension.bottom(1);
    var max = this.dimension.top(1);
    if(min.length >0 ){
        min = min[0].TimeStamp;
        max = max[0].TimeStamp;
    }else{
        min = 0;
        max = 1;
    }
    this.plot.x(d3.scale.linear().domain([min,max]));
};



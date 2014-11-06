plots.pie = function(){
    this.render = function(master, $target_div){
        var render_group = $target_div.attr('render_group');
        this.plot = dc.pieChart($target_div[0], render_group);
        this.plot.dimension(this.dimension).group(this.group);
        this.plot.radius($target_div.width()/2);

        this.master = master;
        this.$target_div = $target_div;
        this.init_filter();
    };
};

plots.pie.prototype = plots.base_cf;



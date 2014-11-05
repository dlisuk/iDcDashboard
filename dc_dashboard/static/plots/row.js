plots.row = function(){
    this.render = function(master, $target_div){
        var render_group = $target_div.attr('render_group');
        this.plot = dc.rowChart($target_div[0], render_group);
        this.plot.dimension(this.dimension).group(this.group);

        this.master = master;
        this.$target_div = $target_div;
        this.init_filter();
    };
};
plots.row.prototype = plots.base_cf;



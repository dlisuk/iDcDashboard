plot_funs.scatter =  {
    render:function(target, conf, dim, group){
        //var min = eval("dim.bottom(1)[0]." + conf.x);
        //var max = eval("dim.top(1)[0]." + conf.x);
        var plot = dc.scatterPlot(target, $(target).attr('render_group'));
        plot
            .dimension(dim).group(group)
            .x(d3.scale.linear()).elasticX(true)
            .y(d3.scale.linear()).elasticY(true)
            .xAxisLabel(conf.x).yAxisLabel(conf.y);
        return plot;
    },
    make_dim:function(cf, conf){
        var dim_f = function(d) { return  eval("[d." + conf.x +" , d." + conf.y + "]");};
        return cf.dimension(dim_f);
    },
    make_group:function(dim, conf){
        return dim.group();
    },
    proc_filter:function(filter, conf){
        if(filter == null){
            return [];
        }else{
            return [[conf.x, "between", [filter[0][0], filter[1][0]]],[conf.y, "between", [filter[0][1], filter[1][1]]]];
        }
    }
}

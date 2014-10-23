 plot_funs.line_chart =  {
     render:function(target, conf, dim, group){
         console.log(dim.bottom(1));
         var min = dim.bottom(1);
         var max = dim.top(1);
         console.log(min);
         console.log(max);
         var plot = dc.lineChart(target, $(target).attr('render_group'));
         plot
             .dimension(dim).group(group)
             .x(d3.scale.linear().domain([min,max]))
             .xAxisLabel(conf.x).yAxisLabel(conf.y);
         return plot;
     },
     make_dim:function(cf, conf){
         var dim_f = function(d) { return  eval("d." + conf.x );};
         return cf.dimension(dim_f);
     },
     make_group:function(dim, conf){
         return dim.group(function(d){ return eval("d." + conf.y);});
     },
     proc_filter:function(filter, conf){
         if(filter == null){
             return [];
         }else{
             return [[conf.x, "between", filter]];
         }
     }
 };


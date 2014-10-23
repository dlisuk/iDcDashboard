 plot_funs.pie_chart =  {
     render:function(target, conf, dim, group){
         var plot = dc.pieChart(target, $(target).attr('render_group'));
         plot
             .dimension(dim).group(group)
         return plot;
     },
     make_dim:function(cf, conf){
         var dim_f = function(d) { return  eval("d." + conf.x );};
         return cf.dimension(dim_f);
     },
     make_group:function(dim, conf){
         return dim.group();
     },
     proc_filter:function(filter, conf){
         if(filter == null){
             return [];
         }else{
             return [[conf.x, "in", filter]];
         }
     }
 }

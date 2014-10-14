require('//cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.11/crossfilter.min.js');

require(["//cdnjs.cloudflare.com/ajax/libs/d3/3.4.1/d3.min.js",
         "//cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.min.js",
        "widgets/js/manager"],
        function(d3, dc, WidgetManager){
            var dashboard_id = 0;

            var plot_funs = {
                scatter:{
                    render:function(target, conf, dim, group){
                        //var dim_min = eval("dim.bottom(1)[0]." + conf.x) * 0.9;
                        //var dim_max = eval("dim.top(1)[0]." + conf.x) * 1.1;

                        var plot = dc.scatterPlot(target, $(target).attr('render_group'));
                        plot
                            .dimension(dim).group(group).x(d3.scale.linear())
                            .elasticX(true)
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
                            return [[conf.x, filter[0][0], filter[1][0]],[conf.y, filter[0][1], filter[1][1]]];
                        }
                    }
                }
            };

            var DashboardView = IPython.DOMWidgetView.extend({
                render: function(){
                    //Here we construct the data stores
                    this.cf   = crossfilter([]);
                    var cf    = this.cf;
                    this.filters = {};

                    this.model.set("filters",JSON.stringify([]));
                    this.touch();
                    //Now begin rendering code
                    this.render_group = 'dashboard_' + (dashboard_id++);
                    var render_group  = this.render_group;

                    var $root = this.$el;

                    var $layer = null;
                    var layer_h = null;

                    var layout = $.parseJSON(this.model.get('layout'));
                    var this_obj = this;

                    for(var i in layout){
                        var plot_conf = layout[i];
                        if(plot_conf.type=="layer"){
                            $layer = $('<div />').attr('class','layer').appendTo($root);
                            layer_h = plot_conf.height;
                        }else{
                            var $plot_area = $('<div />')
                                .attr('id', render_group + "_plot_" + i)
                                .attr('render_group', render_group)
                                .appendTo($layer);


                            var plotting_obj = plot_funs[plot_conf.type];

                            //Make cf objects
                            var dim          = plotting_obj.make_dim(cf, plot_conf);
                            var group        = plotting_obj.make_group(dim, plot_conf);

                            var plot         = plotting_obj.render($plot_area[0], plot_conf, dim, group);
                            (function(proc_filter, plot_area, conf){
                                plot
                                    .width(plot_conf.width).height(layer_h)
                                    .on('filtered',function(chart,filter){
                                        dc.events.trigger(function() {

                                            this_obj.update_filter($(plot_area).attr("id"),proc_filter(filter, conf));
                                        }, 1000);
                                    });
                            })(plotting_obj.proc_filter, $plot_area[0], plot_conf);
                        }
                    }
                    this.append_data();
                    dc.renderAll(this.render_group);
                },

                replace_data:function(){
                    this.remove_data();
                    this.append_data();
                },
                remove_data:function(){
                    this.data   = [];
                },
                append_data:function(){
                    var data = $.parseJSON(this.model.get('data'));
                    this.cf.add(data);
                    dc.renderAll(this.render_group);
                },
                update_filter:function(plot_id, filter){
                    dc.redrawAll(this.render_group);
                    this.filters[plot_id] = filter;

                    var filters_deduped = [];
                    for( var i in this.filters){
                        filters_deduped = filters_deduped.concat(this.filters[i]);
                    }
                    this.model.set("filters",JSON.stringify(filters_deduped));
                    this.touch();
                }
            });

            // Register the DashboardView with the widget manager.
            WidgetManager.register_widget_view('DashboardView', DashboardView);
});
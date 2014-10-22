require(['//cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.11/crossfilter.min.js']);
    require(["//cdnjs.cloudflare.com/ajax/libs/d3/3.4.1/d3.min.js",
             "//cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-alpha.2/dc.min.js",
            "widgets/js/widget",
            "widgets/js/manager"],
            function(d3, dc, widget, WidgetManager){
                var dashboard_id = 0;

                var plot_funs = {};

                $$INSERT$$

                var DashboardView = IPython.DOMWidgetView.extend({
                    render: function(){
                        //Here we construct the data stores
                        this.cf   = crossfilter([]);
                        this.filters = {};
                        this.dims    = [];
                        this.charts  = [];
                        this.render_group = 'dashboard_' + (dashboard_id++);
                        this.set_layout();
                        this.set_data();

                        this.model.on('change:data', this.set_data, this);
                        this.model.on('change:layout', this.set_layout, this);
                },

                set_data:function(){
                    alert("Set Data" + this.render_group);
                    //First we remove old data from cross filter and add new data
                    this.dims.forEach(function(dim){dim.filter(null);});
                    this.cf.remove();
                    //Now we refresh the filters applied to all dc charts
                    this.charts.forEach(function(chart){
                        var oldFilters = chart.filters();
                        chart.filter(null);
                        oldFilters.forEach(function(filter){
                            chart.filter(filter);
                        });
                    });

                    var df = $.parseJSON(this.model.get('data'));
                    this.cf.add(df);
                    dc.redrawAll();
                },

                set_layout:function(){
                    alert("Set Layout" + this.render_group);
                    //Clean up existing layout
                    this.dims.forEach(function(dim){dim.dispose();});
                    this.charts = [];
                    var $root = this.$el;
                    $root.empty();

                    var layout = $.parseJSON(this.model.get('layout'));
                    var this_obj = this;
                    var $layer = null;
                    var layer_h = null;

                    for(var i in layout){
                        var plot_conf = layout[i];
                        if(plot_conf.type=="layer"){
                            $layer = $('<div />').attr('class','layer').appendTo($root);
                            layer_h = plot_conf.height;
                        }else{
                            var $plot_area = $('<div />')
                                .attr('id', this_obj.render_group + "_plot_" + i)
                                .attr('render_group', this_obj.render_group)
                                .appendTo($layer);


                            var plotting_obj = plot_funs[plot_conf.type];

                            //Make cf objects
                            var dim          = plotting_obj.make_dim(this_obj.cf, plot_conf);
                            this.dims.push(dim);
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
                            this.charts.push(plot);
                        }
                    }
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
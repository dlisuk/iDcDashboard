var plots = {};

plots.base = {

    render:function(master, target_div){},

    set_data_source:function(ds){},

    update_data:function(){},

    height:function(x){},
    width:function(x){},
    post_render:function(){},

    config:{}
};

plots.base_cf = {};
plots.base_cf.prototype = plots.base;
plots.base_cf.update_data = function(){};
plots.base_cf.height = function(x){this.plot.height(x);};
plots.base_cf.width  = function(x){this.plot.width(x);};
plots.base_cf.init_filter = function(){
    var this_obj = this;
    this.plot.on('filtered',function(chart,filter){
        dc.events.trigger(function(){
            this_obj.master.update_filter();
        },1000)
    });
};
plots.base_cf.post_render = function(){},

plots.base_cf.set_data_source = function(ds){
    this.dimension = ds.dimemsion;
    this.group     = ds.group;
};

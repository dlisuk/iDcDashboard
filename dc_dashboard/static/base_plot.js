plots = {}

plots.base = {

    render:function(master, target_div){},

    set_data_source:function(ds){},

    update_data:function(){},

    config:{}
}

plots.base_cf = {}
plots.base_cf.prototype = plots.base;
plots.base_cf.set_data_source = function(ds){
    this.dimension = ds.dimemsion;
    this.group     = ds.group;
}

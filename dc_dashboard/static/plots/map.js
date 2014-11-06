plots.map = function(){
    this.render = function(master, $target_div){

        var render_group = $target_div.attr('render_group');
        this.plot = dc.geoChoroplethChart($target_div[0], render_group);
        this.plot.dimension(this.dimension).group(this.group);

        this.master = master;
        this.$target_div = $target_div;
        this.init_filter();

    };
    this.config = {};
    this.config.parent = this;
    this.config.prototype = this.prototype.config;
    this.config.map_type = function(type){
        var url = type[0];
        var the_plot = this.parent.plot;
        console.log("A");
        console.log(the_plot);
        console.log("A");
        d3.json(url, function (mapjson){
            console.log(mapjson);
            the_plot.overlayGeoJson(mapjson.features, "state", function (d) { return d.properties.name; })
        });
    };
};

plots.map.prototype = plots.base_cf;


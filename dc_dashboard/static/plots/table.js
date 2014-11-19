plots.table = function(){
    this.render = function(master, $target_div){
        this.master = master;
        this.$target_div = $target_div;

        var render_group = $target_div.attr('render_group');

        var $table  = $("<table />").appendTo(this.$target_div[0]);
        this.$table = $table

        this.plot = dc.dataTable($table[0], render_group);
        this.plot.dimension(this.dimension).group(function(d){return null;});


        this.config = {};
        this.config.parent = this;
        this.config.prototype = this.prototype.config;
        this.config.columns = function(cols){
            var the_plot = this.parent.plot;
            var $table = this.parent.$table;

            var $table_header = $('<thead />')
                .attr('class', 'dc-table-head')
                .appendTo($table);

            cols.forEach(function(c){$("<th />").html(c).appendTo($table_header);})

            the_plot.columns(cols.map(function(c){return function(d){return d[c];};}))

        };
    };
};

plots.table.prototype = plots.base_cf;



frappe.pages['dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});

	$("<div class='view' id='chart' style='min-width: 900px; width:1155px;overflow: hidden;'><b> </b>\
			<div class='chart' id='chart1' style='min-width: 900px; overflow: hidden'>\
			</div>\
		</div>\
		<div class='view' id='graph' style='min-width: 900px; width:1155px; overflow: hidden;'><b> </b>\
			<div class='graph' id='graph1' style='min-width: 900px; overflow: hidden;'>\
			</div>\
		</div>").appendTo($(wrapper).find('.layout-main'));
	wrapper.dashboard = new frappe.Dashboard(wrapper);
	frappe.breadcrumbs.add("Hospital Bed Management");
}

frappe.Dashboard = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".layout-main");
		this.add_filter(wrapper);
		this.chart_view(wrapper);
		this.graph_view(wrapper);
		this.change_filters(wrapper);
		this.refresh(wrapper);
	},

	// Add Speciality filter and Refresh page button
	add_filter: function(wrapper){
		var me =this;
		window.setTimeout(function() { me.chart_view(wrapper)}, 1000);
		window.setTimeout(function() { me.graph_view(wrapper)}, 1000);
		this.page = wrapper.page;
		this.specialities = this.page.add_field({fieldtype:"Link", label:"Specialities", fieldname:"apecialities", reqd:0,
			options:"Specialities"});

		this.hospital = this.page.add_field({fieldtype:"Link", label:"Hospital", fieldname:"hospital", reqd:0,
			options:"Hospital Registration"});
		// this.specialities = this.page.add_field({fieldtype:"Link", label:"Specialities", fieldname:"apecialities", reqd:0,
		// 	options:"Specialities", default:"General"});
		$("<div ><input class='btn btn-default refresh' id='refresh' name ='refresh' type='button' value='Refresh' style='float: right; margin-right:15px; color:#707070 ;'>\
			</div>").appendTo($(wrapper).find('.page-form.row'));
	},

	// Add Bar chart view of hospital bed availability details
	chart_view: function(wrapper){
		var me = this;
		this.page = wrapper.page;
		var specialities = me.specialities.$input.val()
		var hospital = me.hospital.$input.val()
		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.dashboard.dashboard.get_dashbord_details",
			args:{  "specialities": specialities, "hospital": hospital },
			callback: function(r) {
				if(r.message.details.length > 1){
					// get data from query
					data=[];
				  	for(var x in r.message.details){
				  		data.push(r.message.details[x]);				  		
		            }
		            // Drow chart
		            var final_data = google.visualization.arrayToDataTable(data);
				    var options = {
				    	title:"Hospital Availability Details - Bar Chart",	
		                hAxis: {
		                        stacked: true,
		                        title: "No. of Beds",
		                        minValue: 0,
		                        titleTextStyle: {color: '#CC0099'}
		                },
		                vAxis: {
		                        stacked: true,
		                        title: "Hospital Name",
		                        titleTextStyle: {color: '#CC0099'}
		                },
						width: 1200,
						height: 800,
						legend: { position: 'top', maxLines: 5 },
						bar: { groupWidth: '60%' },
						isStacked: true
					};
				    var chart = new google.visualization.BarChart(document.getElementById("chart1"));
				    chart.draw(final_data, options);
				}
				else{
					msgprint(__('No Data Found against this criteria...'));
					me.specialities.$input.val('')
					me.hospital.$input.val('')
					me.chart_view(wrapper);
					me.graph_view(wrapper);
				}
			}
		});
	},

	// Add graphical view of hospital bed availability details
	graph_view: function(wrapper){
		var me = this;
		var specialities = me.specialities.$input.val()
		var hospital = me.hospital.$input.val()
		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.dashboard.dashboard.get_dashbord_details",
			args:{ "specialities": specialities, "hospital": hospital },
			callback: function(r) {
				if(r.message.details.length > 1){
					// get data from query
					data=[];
				  	for(var x in r.message.details){
				  		data.push(r.message.details[x]);				  		
		            }
		            // Draw graphical view from data
		            var final_data = google.visualization.arrayToDataTable(data);
				    var options = {
				        title:"Graphical Representation of Hospital Availability Details",	
				        hAxis: {
		                        stacked: true,
		                        title: "Hospital Name",
		                        titleTextStyle: {color: '#CC0099'}
		                },
		                vAxis: {
		                        stacked: true,
		                        title: "No. of Beds",
		                        minValue: 0,
		                        titleTextStyle: {color: '#CC0099'}
		                },
				    	animationEnabled: true,
						width: 1300,
						height: 700,
						legend: { position: 'top', maxLines: 5 },
						isStacked: true,
						bar: { groupWidth: '65%' }					
					};
				    var chart = new google.visualization.AreaChart(document.getElementById("graph1"));
				    chart.draw(final_data, options);
				}
				else{
					// msgprint(__('No Data Found against this criteria...'));
					me.specialities.$input.val('')
					me.hospital.$input.val('')
					me.chart_view(wrapper);
					me.graph_view(wrapper);
				}
			}
		});
	},

	// refresh chart and graph view on selection of speciality
	change_filters:function(wrapper){
		var me = this
		me.specialities.$input.change(function(){
			me.chart_view(wrapper);
			me.graph_view(wrapper);

		});
		me.hospital.$input.change(function(){
			me.chart_view(wrapper);
			me.graph_view(wrapper);

		});
	},

	// refresh page
	refresh: function(wrapper){
		var me = this
		$(me.wrapper).find('.refresh').on("click", function() {
			me.specialities.$input.val('')
			me.hospital.$input.val('')
			me.chart_view(wrapper);
			me.graph_view(wrapper);
		});
	}
})
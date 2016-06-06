frappe.pages['occupancy-report'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Hospital Occupancy Report',
		single_column: true
	});

	$("<div class='occupancy' style='min-height: 200px; padding:25px; height:520px;'>\
		</div>").appendTo(page.main);
	wrapper.occupancy_report = new frappe.OccupancyReport(wrapper);
}

frappe.OccupancyReport = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".occupancy");
		this.occupancy_details();
	},

	// Get occupancy details of hospital and show on page
	occupancy_details: function(){
		var me =this;
		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.occupancy_report.occupancy_report.get_occupancy_details",
			args:{},
			callback: function(r) {
				if(r.message){
					$(me.wrapper).find(".occupancy").html(frappe.render_template("occupancy_report", {"data":r.message}))
				}
			}
		});
	}
})
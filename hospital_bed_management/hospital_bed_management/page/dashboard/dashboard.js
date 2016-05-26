frappe.pages['dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});

	$("<div class='patient-dashboard' style='min-height: 200px; padding:15px;'>\
		</div>").appendTo(page.main);
	wrapper.dashboard = new frappe.Dashboard(wrapper);
}

frappe.Dashboard = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".patient-dashboard");
	}
})
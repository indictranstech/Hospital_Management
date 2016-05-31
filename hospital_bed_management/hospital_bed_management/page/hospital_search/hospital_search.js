frappe.pages['hospital-search'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Hospital Search and Allocation',
		single_column: true
	});

	$("<div class='hospital-search'	style='min-height: 200px; padding:15px; height:420px; overflow:auto;'>\
		<div class='flt'></div>	</div>").appendTo(page.main);
	wrapper.hospital_search = new frappe.HospitalSearch(wrapper);
}

frappe.HospitalSearch = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".hospital-search");
		this.filters = {};
		this.add_filters();
		this.search_hospital();
		this.book_hospital();
	},

	refresh: function(){
		$('.table').remove();
	},

	// Add filters on Hospital Search page
	add_filters: function(){
		var me = this;

		me.filters.specialities = me.wrapper.page.add_field({
			fieldname: "specialities",
			label: __("Specialities"),
			fieldtype: "Link",
			options: ("Specialities")
		});

		me.filters.patient_type = me.wrapper.page.add_field({
			fieldname: "patient_type",
			label: __("Type of Patients"),
			fieldtype: "Select",
			options: (["","Indigent","Weaker"])
		});

		me.filters.hospital = me.wrapper.page.add_field({
			fieldname: "hospital",
			label: __("Hospital"),
			fieldtype: "Link",
			options: ("Hospital Registration")
		});

		me.filters.search = me.wrapper.page.add_field({
			fieldname: "search",
			label: __("Search"),
			fieldtype: "Button"
		});

		me.filters.book_hosp = me.wrapper.page.add_field({
			fieldname: "book_hosp",
			label: __("Book"),
			fieldtype: "Button"
		});
	},

	// Search Hospital Bed availability information
	search_hospital: function(){
		var me = this
		$(this.wrapper).find('button[data-fieldname = search]').on("click", function() {
			$('.table').remove();
			me.hospital_details();
		})
	},

	// Fetch hospital availability details as per filters and render detialed table
	hospital_details: function(){
		var me = this;
		// Get filters values
		specialities = this.filters.specialities.$input.val();
		p_type =  this.filters.patient_type.$input.val();
		hosp =  this.filters.hospital.$input.val();

		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.hospital_search.hospital_search.get_hospital_details",
			args:{
				"specialities": specialities,
				"p_type": p_type,
				"hosp": hosp
			},
			callback: function(r) {
				if(r.message){
					$(me.wrapper).find(".hospital-search").html(frappe.render_template("hospital_search", {"data":r.message}))
				}
			}
		});	
	},

	// Check bed availability and book bed(Recommend)
	book_hospital: function(){
		var me = this;
		$(this.wrapper).find('button[data-fieldname = book_hosp]').on("click", function(){
			if($("input:radio[name='select']").is(":checked")!=true){
				frappe.throw(__("Please select Hospital for Recommendation..."));
			}
			else{ 
				var p_type = me.filters.patient_type.$input.val()
				var hosp_name = $("input[name=select]:checked").closest('tr').attr('hosp-name')
				frappe.route_options = {"hospital_name": hosp_name, "patient_type":p_type}
				frappe.set_route("Form", "Patient Allotment", "New Patient Allotment"); 
			}
		})
	}
})
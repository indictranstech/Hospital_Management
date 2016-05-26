frappe.pages['patient-allotment-an'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Patient Allotment and Updation',
		single_column: true
	});

	$("<div class='allot-patients' style='min-height: 200px; padding:15px; height:400px; overflow:auto;'>\
		</div>").appendTo(page.main);
	wrapper.patient_allotment_an = new frappe.PatientAllotment(wrapper);
}

frappe.PatientAllotment = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".allot-patients");
		this.filters = {};
		this.add_filters();
		// this.search_hospital();
		this.allot_bed_to_patient();
	},

	add_filters: function(){
		var me = this;

		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.patient_allotment_an.patient_allotment_an.get_all_patients",
			callback: function(r) {
				if(r.message){
					me.options = r.message;
					me.filters.patient_name = me.wrapper.page.add_field({
						fieldname: "patient_name",
						label: __("Patient Name"),
						fieldtype: "Data"
					});
					$(me.wrapper).find('[data-fieldname = patient_name]').autocomplete({source: r.message})
				}

				me.filters.patient_type = me.wrapper.page.add_field({
					fieldname: "patient_type",
					label: __("Type of Patients"),
					fieldtype: "Select",
					options: (["","Indigent","Weaker"])
				});

				me.filters.allotment_id = me.wrapper.page.add_field({
					fieldname: "allotment_id",
					label: __("Provisional Allotment Id"),
					fieldtype: "Link",
					options: ("Patient Allotment")
				});

				me.filters.status = me.wrapper.page.add_field({
					fieldname: "status",
					label: __("Status"),
					fieldtype: "Select",
					options: (["Recommended","Rejected","Alloted"])
				});

				me.search = me.wrapper.page.add_field({
					fieldname: "search",
					label: __("Search"),
					fieldtype: "Button"
				});

				$('select option:contains("Recommended")').prop('selected',true);

				me.search_hospital();
			}
		});
	},

	search_hospital: function(){
		var me = this
		me.search.$input.on("click", function() {
			$('.table').remove();
			me.recommended_hospital_details();
		});
	},

	recommended_hospital_details: function(){
		var me = this;
		patient_name = this.filters.patient_name.$input.val();
		p_type =  this.filters.patient_type.$input.val();
		allotment_id =  this.filters.allotment_id.$input.val();
		status =  this.filters.status.$input.val();

		frappe.call({
			method:"hospital_bed_management.hospital_bed_management.page.patient_allotment_an.patient_allotment_an.get_recommendation_detials",
			args:{
				"patient_name": patient_name,
				"p_type": p_type,
				"allotment_id": allotment_id,
				"status": status,
			},
			callback: function(r) {
				if(r.message){
					$(me.wrapper).find(".allot-patients").html(frappe.render_template("patient_allotment_an", {"data":r.message}))
				}

				me.allot_bed_to_patient();
				me.reject_allotment();
			}
		});
	},

	allot_bed_to_patient: function(){
		var me = this
		$(this.wrapper).find('.btn-allot').on("click", function() {
			if($("input:radio[name='select']").is(":checked")!=true){
				frappe.throw(__("Please select Patient first to Bed Allotment..."));
			}
			else{ 
				if(me.filters.status.$input.val()=="Recommended"){
					var patient_allot_id = $("input[name=select]:checked").closest('tr').attr('allot-id')
					frappe.call({
						method:"hospital_bed_management.hospital_bed_management.page.patient_allotment_an.patient_allotment_an.update_hospital_beds_availability",
						args:{
							"allotment_id":patient_allot_id
						},
						callback: function(r) {
							msgprint("Bed Alloted Successfully to this patient...")
							window.location.reload();
						}
					});
				}
				else if(me.filters.status.$input.val()=="Alloted"){
					frappe.throw(__("Already alloted Bed to selected patient."));
				}
				else{
					frappe.throw(__("Selected patient status must be Recommended for Bed Allotment."));
				}
			}
		})
	},

	reject_allotment: function(){
		var me = this
		$(this.wrapper).find('.btn-reject').on("click", function() {
			if($("input:radio[name='select']").is(":checked")!=true){
				frappe.throw(__("Please select Patient first for Allotment rejection..."));
			}
			else{ 
				if(me.filters.status.$input.val()=="Recommended"){
					var patient_allot_id = $("input[name=select]:checked").closest('tr').attr('allot-id')
					frappe.call({
						method:"hospital_bed_management.hospital_bed_management.page.patient_allotment_an.patient_allotment_an.reject_bed_allotment",
						args:{
							"allotment_id":patient_allot_id
						},
						callback: function(r) {
							msgprint("Bed Allocation Rejected to this patient...")
							window.location.reload();
						}
					});
				}
				else if(me.filters.status.$input.val()=="Alloted"){
					frappe.throw(__("Already alloted Bed to selected patient."));
				}
				else{
					frappe.throw(__("Bed Allotment is already rejected for selected patient."));
				}
			}
		})
	}
})
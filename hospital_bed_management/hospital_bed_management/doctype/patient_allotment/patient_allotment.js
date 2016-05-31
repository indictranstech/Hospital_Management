// Copyright (c) 2016, Bed Management System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient Allotment', {
	onload: function(frm) {
		if(in_list(user_roles, "Hospital User")){
			set_field_permlevel('recommend',2);
		}
	},

	// Add Recommend and Discharge buttons
	refresh: function(frm){
		if(!frm.doc.__islocal && frm.doc.status=="Not Verified" ){
			cur_frm.add_custom_button(__('Recommend'), function() { cur_frm.events.recommend(); }, 'icon-retweet', 'btn-default');
		}
		if(!frm.doc.__islocal && frm.doc.status=="Alloted"){
			cur_frm.add_custom_button(__('Discharge'), function() { cur_frm.events.update_info(); }, 'icon-retweet', 'btn-default');
		}
		
	},

	// Calculate patient age from DOB
	patient_dob: function(frm){
		frappe.call({
			method: "hospital_bed_management.hospital_bed_management.doctype.patient_allotment.patient_allotment.calculate_age",
			args: {"dob": frm.doc.patient_dob},
			callback: function(r) {
				if(r.message) {
					if (r.message){
						frm.doc.patient_age = r.message
						refresh_field('patient_age')
					}
				}
			}
		});
	},

	// Update patient status on recommendation
	recommend: function(frm,cdt,cdn){
		var count = 0
		// if(!(cur_frm.doc["income_document"]).length){
		// 	frappe.throw(__("Please upload Income Verification Documents first for Recommendation..."));
		// }
		if((cur_frm.doc["income_document"]).length < 2){
			frappe.throw(__("Please upload at least 2 Income Verification Documents for Recommendation..."));
		}
		$.each(cur_frm.doc["income_document"] || [], function(i, d) {
			if(d.verified_against_income==1){
				count = count + 1
			}
		});
		
	 	if((cur_frm.doc["income_document"]).length==count){
	 		frappe.call({
				method: "hospital_bed_management.hospital_bed_management.doctype.patient_allotment.patient_allotment.recommended_notification",
				args: {
					"hospital": cur_frm.doc.hospital_name,
					"p_type": cur_frm.doc.patient_type,
					"patient_name": cur_frm.doc.patient_name
				},
				callback: function(r) {
					cur_frm.doc.status = "Recommended"
			 		refresh_field('status')
			 		cur_frm.save();
			 		// frappe.set_route("hospital-search", "Hospital Bed Management");
			 		frappe.set_route("List", "Patient Allotment");
			 		msgprint("Recommendation Successfully Done.!!!")
				}
			});
	 	}
	 	else{
	 		frappe.throw(__("Documents are not verified for Recommendation..."));
	 	}
	},

	// Update bed info and patient info on discherged
	update_info: function(frm,cdt,cdn){
		frappe.call({
			method: "hospital_bed_management.hospital_bed_management.doctype.patient_allotment.patient_allotment.update_dischaged_info",
			args: {
				"hospital": cur_frm.doc.hospital_name,
				"p_type": cur_frm.doc.patient_type,
				"allotment_id": cur_frm.doc.name,
				"owner": cur_frm.doc.owner,
				"patient_name": cur_frm.doc.patient_name
			},
			callback: function(r) {
				cur_frm.doc.status = "Discharged"
		 		refresh_field('status')
		 		cur_frm.doc.discharge = 1
		 		refresh_field('discharge')
		 		cur_frm.save();
		 		msgprint("Patient Discharged Successfully.Also updated discharge information.!!!")
			}
		});
	}
});

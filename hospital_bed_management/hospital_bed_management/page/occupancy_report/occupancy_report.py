from __future__ import unicode_literals
import frappe

# Get occupancy details of hospital
@frappe.whitelist()
def get_occupancy_details():
	# get top-5 occupancy detials of hospital
	top_occupancy = frappe.db.sql("""select name,
		ROUND((i_patient_alloted + w_patient_alloted)/(reserved_for_indigent_patients + reserved_for_weaker_patients) *100) as tot 
		from `tabHospital Registration` order by tot desc LIMIT 5""",as_dict=1)

	# get top-5 occupancy ratio of hospital
	top_occupancy_ratio = frappe.db.sql("""select name,
		ROUND(i_patient_alloted/reserved_for_indigent_patients*100) as i_occupancy, 
		ROUND(w_patient_alloted/reserved_for_weaker_patients*100) as w_occupancy,
		ifnull(ROUND(w_available/(ROUND(i_patient_alloted/reserved_for_indigent_patients*100))*100),0) as iw_occupancy_ratio 
		from `tabHospital Registration` order by iw_occupancy_ratio desc LIMIT 5""",as_dict=1)

	# get bottom-5 occupancy details of hospital
	bottom_occupancy = frappe.db.sql("""select name,
		ROUND((i_patient_alloted + w_patient_alloted)/(reserved_for_indigent_patients + reserved_for_weaker_patients) *100) as tot 
		from `tabHospital Registration` order by tot asc LIMIT 5""",as_dict=1)

	# get bottom-5 occupancy ratio of hospital
	bottom_occupancy_ratio = frappe.db.sql("""select name,
		ROUND(i_patient_alloted/reserved_for_indigent_patients*100) as i_occupancy, 
		ROUND(w_patient_alloted/reserved_for_weaker_patients*100) as w_occupancy,
		ifnull(ROUND(w_available/(ROUND(i_patient_alloted/reserved_for_indigent_patients*100))*100),0) as iw_occupancy_ratio 
		from `tabHospital Registration` order by iw_occupancy_ratio asc LIMIT 5""",as_dict=1)

	return top_occupancy, top_occupancy_ratio, bottom_occupancy, bottom_occupancy_ratio
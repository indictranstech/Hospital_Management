from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_hospital_details(specialities,p_type,hosp):
	conditions = ""
	if specialities: conditions += "and specialities = '%s'"%(specialities)
	if hosp: conditions += "and name = '%s'"%(hosp)

	if p_type == "Indigent":
		data = frappe.db.sql("""select * from `tabHospital Registration` where status = "Active" and i_available > 0 
			%s """%(conditions),as_dict=1)
	elif p_type== "Weaker":
		data = frappe.db.sql("""select * from `tabHospital Registration` where status = "Active" and w_available > 0 
			%s """%(conditions),as_dict=1)
	else:
		data = frappe.db.sql("""select * from `tabHospital Registration` where status = "Active" and (i_available > 0 
			or w_available > 0) %s """%(conditions),as_dict=1)
	return data
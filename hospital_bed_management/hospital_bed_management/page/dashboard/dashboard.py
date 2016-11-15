from __future__ import unicode_literals
import frappe

# Get hospital detials for dashboard
@frappe.whitelist()
def get_dashbord_details(specialities, hospital):
	data = []
	conditions = ""
	if specialities: conditions += "and specialities = '%s'"%(specialities)
	if hospital: conditions += "and hospital_name = '%s'"%(hospital)
	
	# get bed availability details with speciality filter
	data = frappe.db.sql("""select name, total_operational_beds, reserved_for_indigent_patients, 
		reserved_for_weaker_patients, i_patient_alloted, w_patient_alloted, i_available, w_available 
		from `tabHospital Registration` where status = 'Active' %s """%(conditions),as_list=1)
	details = [['','Total Beds','I-Total','W-Total','I-Occupied','W-Occupied','I-Available','W-Available']]
	for d in data:
		details.append(d)

	# Set X and Y axis lables
	lable = {'x_axis':'No Of Beds', 'y_axis':'Hospital Name'}
	ret = {'details': details, 'lable':lable}

	return ret
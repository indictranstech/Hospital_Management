from __future__ import unicode_literals
import frappe
from frappe import throw, _

@frappe.whitelist()
def get_recommendation_detials(patient_name,p_type,allotment_id,status):
	conditions = ""
	if patient_name: conditions += "and patient_name = '%s'"%(patient_name)
	if p_type: conditions += "and patient_type = '%s' "%(p_type)
	if allotment_id: conditions += "and name = '%s'"%(allotment_id)
	if status: conditions += "and status = '%s'"%(status)

	val = frappe.db.sql("""select defvalue from `tabDefaultValue` where parent = '%s' and defkey = 'Hospital Registration' """%(frappe.session.user), as_dict=1)
	if val:
		data = frappe.db.sql("""select * from `tabPatient Allotment` where hospital_name = '%s' %s """%(val[0]['defvalue'],conditions),as_dict=1)
	else:
		frappe.throw(_("Please set Hospital in User Permissions first."))
	for d in data:
		files = ""
		documents = frappe.db.sql("""select document_name from `tabIncome Documents` where parent = '%s' """%(d["name"]),as_dict=1)
		for doc in documents:
			files = files + " " + doc['document_name'] + ","

		d['file_name'] = files[:-1]

	return data

@frappe.whitelist()
def get_all_patients():
	patients = frappe.db.sql("""select distinct patient_name from `tabPatient Allotment` """,as_list=1)
	p_list = []
	p_list = [p[0] for p in patients]
	return p_list

@frappe.whitelist()
def update_hospital_beds_availability(allotment_id):
	hospital = frappe.db.get_value("Patient Allotment", allotment_id, ["hospital_name","patient_type"],as_dict=True)
	
	if hospital['patient_type']=="Indigent" :
		i_alloted = frappe.db.get_value("Hospital Registration", hospital['hospital_name'], ["i_patient_alloted","i_available"],as_dict=True)
		if i_alloted['i_available'] != 0:
			allot = i_alloted['i_patient_alloted'] + 1
			total_i_beds = i_alloted['i_available'] - 1

			hosp = frappe.get_doc('Hospital Registration',hospital['hospital_name'])
			hosp.i_patient_alloted = allot
			hosp.i_available = total_i_beds
			hosp.flags.ignore_permissions = 1
			hosp.save()
		else:
			frappe.throw(_("Sorry...Beds are not available for Indigent patients."))
	elif hospital['patient_type']=="Weaker" :
		w_alloted = frappe.db.get_value("Hospital Registration", hospital['hospital_name'], ["w_patient_alloted","w_available"],as_dict=True)
		if w_alloted['w_available'] != 0:
			allot = w_alloted['w_patient_alloted'] + 1
			total_w_beds = w_alloted['w_available'] - 1

			hosp = frappe.get_doc('Hospital Registration',hospital['hospital_name'])
			hosp.w_patient_alloted = allot
			hosp.w_available = total_w_beds
			hosp.flags.ignore_permissions = 1
			hosp.save()
		else:
			frappe.throw(_("Sorry...Beds are not available for Weaker patients."))

	p_allotment_status = frappe.db.get_value("Patient Allotment", allotment_id, "Status")
	allotment = frappe.get_doc('Patient Allotment',allotment_id)
	allotment.status = "Alloted"
	allotment.save()

@frappe.whitelist()
def reject_bed_allotment(allotment_id):
	# hospital = frappe.db.get_value("Patient Allotment", allotment_id, ["hospital_name","patient_type"],as_dict=True)
	p_allotment_status = frappe.db.get_value("Patient Allotment", allotment_id, "Status")
	allotment = frappe.get_doc('Patient Allotment',allotment_id)
	allotment.status = "Rejected"
	allotment.save()
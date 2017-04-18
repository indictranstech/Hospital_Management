from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate, cstr, today
from frappe import _
import math

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_result(filters)

	return columns, data

def get_columns():
	return [_("Hospital Name") + ":Link/Hospital Registration:300",
			_("Recommended Count") + ":Int:150", _("Admitted Count") + ":Int:120", 
			_("Rejected Count") + ":Int:120", _("Discharged Count") + ":Int:120", 
			_("Indigent Patients") + ":Int:120", _("Weaker Patients") + ":Int:120"]

def get_result(filters):
	data = []

	if filters["from_date"] > filters["to_date"]:
		frappe.throw(_("From Date must be less than To Date"))

	if filters["to_date"] > today():
		frappe.throw(_("To Date must be Today's or less than Today's Date"))

	hosp_list = frappe.db.get_all("Hospital Registration")
	for h in hosp_list:
		hosp_data = []
		status = ["recommend_date","alotted_date","rejected_date","discharge_date"]
		hosp_data.extend([h['name']])

		for s in status:
			count = frappe.db.sql("""select count(name) 
					from 
						`tabPatient Allotment` 
					where 
						hospital_name = '%s' 
						and %s >= '%s' 
						and %s <= '%s' 
					"""%(h['name'],s,filters["from_date"],s,filters["to_date"]),as_list=1)
			hosp_data.extend([count[0][0]])
		
		i_count = frappe.db.sql("""select count(name) 
					from 
						`tabPatient Allotment` 
					where 
						patient_type = 'Indigent' 
						and hospital_name = '%s' 
						and register_date >= '%s' 
						and register_date <= '%s' 
					"""%(h['name'],filters["from_date"],filters["to_date"]),as_list=1)

		w_count = frappe.db.sql("""select count(name) 
					from 
						`tabPatient Allotment` 
					where 
						patient_type = 'Weaker' 
						and hospital_name = '%s' 
						and register_date >= '%s' 
						and register_date <= '%s' 
					"""%(h['name'],filters["from_date"],filters["to_date"]),as_list=1)
		
		hosp_data.extend([i_count[0][0]])
		hosp_data.extend([w_count[0][0]])
		data.append(hosp_data)
	
	return data

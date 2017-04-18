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
	return [_("Hospital Name") + ":Link/Hospital Registration:300"]

def get_result(filters):
	data = []

	if filters["date"] > today():
		frappe.throw(_("Filter Date must be Today's or less than Today's Date"))

	hosp_list = frappe.db.get_all("Hospital Registration", filters={"status":"Active"}, fields=["name", "creation"])
	
	for h in hosp_list:
		date = str(h["creation"])[0:10]
		hosp = frappe.db.sql("""select name 
				from 
					`tabPatient Allotment` 
				where 
					alotted_date IS NOT NULL 
					and hospital_name = '%s' 
					and alotted_date = '%s' 
				"""%(h['name'],filters["date"]),as_list=1)
		if not hosp:
			if date <= filters["date"] :
				data.append([h['name']])

	return data

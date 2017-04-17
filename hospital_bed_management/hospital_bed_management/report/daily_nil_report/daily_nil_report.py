from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate, cstr
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
	hosp_list = frappe.db.get_all("Hospital Registration")
	
	for h in hosp_list:
		hosp = frappe.db.sql("""select name 
				from 
					`tabPatient Allotment` 
				where 
					alotted_date IS NOT NULL 
					and hospital_name = '%s' 
					and alotted_date = '%s' 
				"""%(h['name'],filters["date"]),as_list=1)
		if not hosp:
			data.append([h['name']])

	return data

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
	return [_("Hospital Name") + ":Link/Hospital Registration:240",_("Spaciality") + ":Data:130", 
			_("Total Beds") + ":Int:100", _("I-Total") + ":Int:100", _("W-Total") + ":Int:100", 
			_("I-Occupied") + ":Int:100", _("W-Occupied") + ":Int:100", 
			_("I-Available") + ":Int:100", _("W-Available") + ":Int:100"]

def get_result(filters):
	data = []
	
	data = frappe.db.sql("""select name, specialities, total_operational_beds, 
							reserved_for_indigent_patients, reserved_for_weaker_patients, 
							i_patient_alloted, w_patient_alloted, i_available, w_available
						from 
							`tabHospital Registration` 
						where 
							status = 'Active' 
						""",as_list=1)
		
	return data
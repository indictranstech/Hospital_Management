# -*- coding: utf-8 -*-
# Copyright (c) 2015, Bed Management System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, cstr, cint
from frappe import throw, _
import math

class HospitalRegistration(Document):
	pass

# get reserved bed percents from System Settings
@frappe.whitelist()
def get_reserved_percents():
	i_reserved = frappe.db.get_value("System Settings", None, "i_reserved_bed_percents")
	w_reserved = frappe.db.get_value("System Settings", None, "w_reserved_bed_percents")
	return i_reserved, w_reserved
	
# update hospital availability details on change of reserved percentage
@frappe.whitelist()
def update_bed_availability(i_percent, w_percent):
	hosp = frappe.db.get_all("Hospital Registration", ["name"])
	data = []
	if hosp:
		for h in hosp:
			# update indigent patient availabity details
			if i_percent:
				total = frappe.db.get_values("Hospital Registration", {"name":h['name']}, ["total_operational_beds","reserved_for_indigent_patients","i_patient_alloted","i_available"], as_dict=True)
				if total:
					new_i_reserved = round(float(total[0]['total_operational_beds']) * flt(i_percent) / 100)
					if new_i_reserved > total[0]['i_patient_alloted']:
						new_i_available = new_i_reserved - total[0]['i_patient_alloted']

						hosptl = frappe.get_doc('Hospital Registration',h['name'])
						hosptl.reserved_for_indigent_patients = new_i_reserved
						hosptl.i_available = new_i_available
						hosptl.flags.ignore_permissions = 1
						hosptl.save()
					else:
						frappe.throw(_("Sorry.You can not change indigent bed percents because alloted bed are more than reserved beds"))
			
			# update weaker patient availability details
			if w_percent:
				total = frappe.db.get_values("Hospital Registration", {"name":h['name']}, ["total_operational_beds","reserved_for_weaker_patients","w_patient_alloted","w_available"], as_dict=True)
				if total:
					new_w_reserved = round(float(total[0]['total_operational_beds']) * flt(w_percent) / 100)
					if new_w_reserved > total[0]['w_patient_alloted']:
						new_w_available = new_w_reserved - total[0]['w_patient_alloted']

						hosptl = frappe.get_doc('Hospital Registration',h['name'])
						hosptl.reserved_for_weaker_patients = new_w_reserved
						hosptl.w_available = new_w_available
						hosptl.flags.ignore_permissions = 1
						hosptl.save()
					else:
						frappe.throw(_("Sorry.You can not change weaker bed percents because alloted bed are more than reserved beds"))

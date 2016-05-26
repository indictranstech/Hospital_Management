# -*- coding: utf-8 -*-
# Copyright (c) 2015, Bed Management Syastem and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from datetime import date
import datetime
from frappe.utils import flt, cstr, cint
from frappe.model.naming import make_autoname

class PatientAllotment(Document):
	def autoname(self):
		year = datetime.datetime.now().strftime("%Y").upper()
		month = datetime.datetime.now().strftime("%m").upper()
		self.name = make_autoname(self.patient_type[:1] + '-' + self.hospital_code[:4]+ '-' + year + '-' + month  + '-'+ '.####')


@frappe.whitelist()
def calculate_age(dob):
	curr_day = date.today()
	d = datetime.datetime.strptime(dob, '%Y-%m-%d')
	return curr_day.year - d.year - ((curr_day.month, curr_day.day) < (d.month, d.day))

@frappe.whitelist()
def update_dischaged_info(hospital, p_type):
	if p_type == "Indigent":
		i_alloted = frappe.db.get_value("Hospital Registration", hospital, ["i_patient_alloted","i_available"],as_dict=True)
		hosp = frappe.get_doc('Hospital Registration',hospital)
		hosp.i_patient_alloted = i_alloted['i_patient_alloted'] - 1
		hosp.i_available = i_alloted['i_available'] + 1
		hosp.flags.ignore_permissions = 1
		hosp.save()
	elif p_type == "Weaker":
		w_alloted = frappe.db.get_value("Hospital Registration", hospital, ["w_patient_alloted","w_available"],as_dict=True)
		hosp = frappe.get_doc('Hospital Registration',hospital)
		hosp.w_patient_alloted = w_alloted['w_patient_alloted'] - 1
		hosp.w_available = w_alloted['w_available'] + 1
		hosp.flags.ignore_permissions = 1
		hosp.save()



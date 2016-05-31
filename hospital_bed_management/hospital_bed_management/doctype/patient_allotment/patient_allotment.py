# -*- coding: utf-8 -*-
# Copyright (c) 2015, Bed Management System and contributors
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

#Calculate age from birth date
@frappe.whitelist()
def calculate_age(dob):
	curr_day = date.today()
	d = datetime.datetime.strptime(dob, '%Y-%m-%d')
	return curr_day.year - d.year - ((curr_day.month, curr_day.day) < (d.month, d.day))

# Patient recommendation notification
@frappe.whitelist()
def recommended_notification(hospital, p_type, patient_name):
	user = frappe.db.sql("""select parent from `tabDefaultValue` where defvalue = '%s' and defkey = 'Hospital Registration' """%(hospital), as_dict=1)
	message = """Dear Sir/Madam, \n \n One '%s' patient - '%s' is recommended to your hospital - '%s'. \n Please check bed availability and procced. \n \n Thanks. """ %(p_type, patient_name, hospital)
	if user:
		frappe.sendmail(recipients=user[0]['parent'] , content=message, subject='Patient Recommendation Notification')

#Update Hospital and patients information on patient discharge
@frappe.whitelist()
def update_dischaged_info(hospital, p_type, allotment_id,owner,patient_name):
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

	# Send notification to recommended user on patient discharge
	message = """Dear Sir/Madam, \n \n You have recommended a patient - '%s' for hospital - '%s'. \n Now discharged this patient. \n \n Regards, \n %s """ %(patient_name, hospital,hospital)
	if owner:
		frappe.sendmail(recipients=owner, content=message, subject='Patient Discharge Notification')


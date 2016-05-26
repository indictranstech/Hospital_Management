# -*- coding: utf-8 -*-
# Copyright (c) 2015, Bed Management Syastem and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HospitalRegistration(Document):
	pass


@frappe.whitelist()
def get_reserved_percents():
	i_reserved = frappe.db.get_value("System Settings", None, "reserved_percent_beds_for_indigent_and_weaker")
	w_reserved = frappe.db.get_value("System Settings", None, "reserved_bed_percent_for_weaker_patient")
	return i_reserved, w_reserved
	
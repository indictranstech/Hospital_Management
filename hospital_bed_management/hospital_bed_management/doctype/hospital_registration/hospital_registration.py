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

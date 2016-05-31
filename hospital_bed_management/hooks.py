# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "hospital_bed_management"
app_title = "Hospital Bed Management"
app_publisher = "Bed Management System"
app_description = "Charitable Trust : Hospital Bed Management System"
app_icon = "octicon octicon-plus"
app_color = "#FA5858"
app_email = "priya.s@indictranstech.com"
app_version = "0.0.1"
app_license = "Hospital Bed Management system"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hospital_bed_management/css/hospital_bed_management.css"
# app_include_js = "/assets/hospital_bed_management/js/hospital_bed_management.js"

app_include_js = "/assets/hospital_bed_management/charts.js"

# include js, css files in header of web template
# web_include_css = "/assets/hospital_bed_management/css/hospital_bed_management.css"
# web_include_js = "/assets/hospital_bed_management/js/hospital_bed_management.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hospital_bed_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

fixtures = ['Custom Field', 'Property Setter','Role']

# before_install = "hospital_bed_management.install.before_install"
# after_install = "hospital_bed_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hospital_bed_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"hospital_bed_management.tasks.all"
# 	],
# 	"daily": [
# 		"hospital_bed_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"hospital_bed_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hospital_bed_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"hospital_bed_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "hospital_bed_management.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hospital_bed_management.event.get_events"
# }


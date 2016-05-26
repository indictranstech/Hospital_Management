from __future__ import unicode_literals
from frappe import _

def get_icon():
	return [
		{
			"module_name": "Hospital Bed Management",
			"label": _("Hospital Bed Management"),
			"color": "#FA5858",
			"icon": "icon-suitcase",
			"type": "module"
		}
	]
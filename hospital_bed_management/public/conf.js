$(document).bind('toolbar_setup', function() {
	$('.navbar-home').html('<img class="erpnext-icon" height="40" width="40" src="'+
			frappe.urllib.get_base_url()+'/assets/frappe/images/logo.png" />');
});
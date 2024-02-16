frappe.listview_settings['Service Listing'] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		if (doc.status === "Paid") {
			return [__("Paid"), "green", "status,=,Paid"]
        }
    }
}            

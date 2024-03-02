frappe.listview_settings['User Created Investors'] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		if (doc.status === "In Shortlist") {
			return [__("In Shortlist"), "green", "status,=,In Shortlist"]
        }
		else if  (doc.status === "To be Contacted") {
			return [__("To be Contacted"), "blue", "status,=,To be Contacted"]
		}
		else if  (doc.status === "Reached Out") {
			return [__("Reached Out"), "orange", "status,=,Reached Out"]
		}
		else if  (doc.status === "Pitched") {
			return [__("Pitched"), "yellow", "status,=,Pitched"]
		}
		else if  (doc.status === "Diligence") {
			return [__("Diligence"), "purple", "status,=,Diligence"]
		}
		else if  (doc.status === "Funding Secured") {
			return [__("Funding Secured"), "pink", "status,=,Funding Secured"]
		}
		else if  (doc.status === "Investor said no") {
			return [__("Investor said no"), "black", "status,=,Investor said no"]
		}
    }
}            

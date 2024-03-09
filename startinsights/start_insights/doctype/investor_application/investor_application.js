// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Investor Application", {
	refresh:function(frm){
        if (frm.doc.docstatus==0){
            frm.add_custom_button(__('Sent Mail Verify Code'), function (){
            }).css('background-color', '#0EE30E');	
        }
			
	},
});

// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt


frappe.ui.form.on("Investor Application", {
    refresh: function(frm) {
        if (frm.doc.docstatus == 0) {
            frm.add_custom_button(__('Send Verification Code Email'), function() {
                if (!frm.doc.verify_code_email_sent) {
                    frappe.call({
                        method: 'startinsights.start_insights.doctype.investor_application.investor_application.send_verification_email',
                        args: {
                            name: frm.doc.name,
                            email_id :frm.doc.email_id
                        },
                        callback: function(r) {
                            if (r.message) {
                            }
                        }
                    });
                } else {
                    frappe.msgprint('Verification code email has already been sent.');
                }
            }).css('background-color', '#0EE30E');
        }
    }
});

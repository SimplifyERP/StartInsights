// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fundability Quiz Flow", {
        customer_group: function (frm) {
                var customer_group = frm.doc.customer_group;

                // Refresh the child table to fetch the updated list of documents
                frm.fields_dict['quiz_flow_table'].grid.get_field('fundability_quiz_question').get_query = function (doc, cdt, cdn) {
                        return {
                                filters: {
                                        "customer_group": customer_group
                                }
                        };
                };
                frm.refresh_field('fundability_quiz_flow_table');
                frm.fields_dict['quiz_flow_table'].grid.get_field('next_display_question_no ').get_query = function (doc, cdt, cdn) {
                        return {
                                filters: {
                                        "customer_group": customer_group
                                }
                        };
                };
                frm.refresh_field('fundability_quiz_flow_table');
        }
});

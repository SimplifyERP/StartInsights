// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt
frappe.ui.form.on("Services", {
    // validate:function(Frm){
        
    // }
    // refresh(frm) {
    //     if (frm.doc.docstatus == 1) {
    //         frm.add_custom_button(__("Assign to"), function () {
    //             let d = new frappe.ui.Dialog({
    //                 title: __("Services Assign"),
    //                 fields: [
    //                     {
    //                         fieldname: "assign_user", fieldtype: "Table",
    //                         fields: [
    //                             {
    //                                 fieldtype: 'Link',
    //                                 fieldname: 'user',
    //                                 label: __('User'),
    //                                 options: "User",
    //                                 in_list_view: 1
    //                             }
    //                         ]
    //                     }
    //                 ],
    //                 primary_action: function () {
    //                     var data = d.get_values();
    //                     frappe.call({
    //                         method: 'startinsights.start_insights.doctype.pitch_craft.pitch_craft.set_assign_users',
    //                         args: {
    //                             user_list_str: data,
    //                             id: frm.doc.name,
    //                             service_name: frm.doc.service_name
    //                         },
    //                         callback: function (r) {
    //                             frm.refresh();
    //                             d.hide();
    //                         }
    //                     });

    //                 },
    //                 primary_action_label: __('Assign User')
    //             });
    //             d.show();
    //         }).css('background-color', '#0EE30E');
    //     }
    // },
});


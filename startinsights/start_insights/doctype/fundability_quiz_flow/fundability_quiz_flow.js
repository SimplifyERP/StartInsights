// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fundability Quiz Flow", {
	refresh(frm) {
        var table = document.getElementById("myTable");
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.innerHTML = "NEW CELL1";
        cell2.innerHTML = "NEW CELL2";

	},
});
// frappe.ui.form.on("Fundability Quiz Flow Table", {
//     fundability_quiz_question: function(frm, cdt, cdn) {
//         var row = locals[cdt][cdn];
//         frappe.call({
//             method: "startinsights.start_insights.doctype.fundability_quiz_flow.fundability_quiz_flow.get_fundability_quiz_options",
//             args: {
//                 question: row.fundability_quiz_question
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     frm.fields_dict["options_table"].grid.get_field("options").get_query = function(doc, cdt, cdn) {
//                         return {
//                             filters: { "parent": row.name }
//                         };
//                     };
//                     frm.refresh_field("options_table");
//                 }
//             }
//         });
//     }
// });




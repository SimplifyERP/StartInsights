// Copyright (c) 2024, Suriya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Captable Management", {
	// from(frm) {
    //     if (frm.doc.from == "Pre-Seed"){
    //         frm.set_value("to","Seed")
    //     }
    //     else if (frm.doc.from == "Seed"){
    //         frm.set_value("to","Pre-Series A")
    //     }
    //     else if (frm.doc.from == "Pre-Series A"){
    //         frm.set_value("to","Series A")
    //     }
    //     else{
    //         frm.set_value("to","")
    //     }
	// },
    // pre_money_valuation(frm){
    //     if(frm.doc.pre_money_valuation > 0){
    //         var post_money_value = (frm.doc.pre_money_valuation || 0) + (frm.doc.amount_raised || 0)
    //         var dilution_value = ((frm.doc.amount_raised || 0) / (frm.doc.pre_money_valuation || 0)) * 100
    //         frm.set_value("post_money_valuation",post_money_value)
    //         frm.set_value("dilution_for_the_round",dilution_value)
    //     }
    // },  
    // amount_raised(frm){
    //     if(frm.doc.amount_raised){
    //         var post_money = (frm.doc.amount_raised || 0) + (frm.doc.pre_money_valuation || 0)
    //         var dilution_value = ((frm.doc.amount_raised || 0) /(frm.doc.pre_money_valuation || 0)) * 100
    //         frm.set_value("post_money_valuation",post_money)
    //         frm.set_value("dilution_for_the_round",dilution_value)
    //     }
    // },
    
});
